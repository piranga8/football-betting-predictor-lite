"""Scraper de predicciones desde PrimaTips"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pytz
from typing import List, Dict, Optional

class PrimaTipsScraper:
    """Scraper de predicciones de primatips.com"""
    
    BASE_URL = "https://primatips.com/tips/"
    CHILE_TZ = pytz.timezone("America/Santiago")
    
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
    
    def get_predictions_by_date(self, date_str: str) -> List[Dict]:
        """
        Obtener predicciones de un día específico
        
        Args:
            date_str: Fecha en formato YYYY-MM-DD
        
        Returns:
            Lista de predicciones
        """
        url = f"{self.BASE_URL}{date_str}"
        
        try:
            print(f"🎯 Scraping PrimaTips: {url}")
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            games = soup.find_all("a", class_="game")
            
            predictions = []
            
            for g in games:
                try:
                    prediction = self._parse_game(g, date_str, url)
                    if prediction:
                        predictions.append(prediction)
                except Exception as e:
                    print(f"⚠️ Error parseando partido: {str(e)}")
                    continue
            
            print(f"✅ {len(predictions)} predicciones obtenidas de PrimaTips")
            return predictions
            
        except Exception as e:
            print(f"❌ Error scraping PrimaTips: {str(e)}")
            return []
    
    def _parse_game(self, game_element, date_str: str, base_url: str) -> Optional[Dict]:
        """
        Parsear un elemento de partido
        
        Returns:
            Dict con la predicción o None si no es válido
        """
        # ID del partido
        game_id = game_element.get("id", "")
        if game_id.startswith("g_"):
            game_id = game_id[2:]
        
        # Estado / minuto
        live_section = game_element.find("span", class_="lvs")
        if not live_section:
            return None
        
        minute_raw = live_section.get_text(strip=True)
        
        # Filtrar solo partidos en vivo o próximos
        # Incluir: minutos (45'), HT, intervalos (+2), o próximos sin minuto
        is_live = ("'" in minute_raw or 
                   minute_raw.isdigit() or 
                   "+" in minute_raw or 
                   minute_raw == "HT")
        
        # Equipos
        teams_elem = game_element.find("span", class_="nms")
        if not teams_elem:
            return None
        
        teams = teams_elem.get_text(" ", strip=True)
        
        # Parsear equipos (formato: "Team1 - Team2")
        teams_split = teams.split(" - ")
        home_team = teams_split[0].strip() if len(teams_split) > 0 else ""
        away_team = teams_split[1].strip() if len(teams_split) > 1 else ""
        
        # Marcador
        local_span = game_element.select_one(".res.lv .l")
        visit_span = game_element.select_one(".res.lv .l.la")
        
        local = local_span.get_text(strip=True) if local_span and local_span.get_text(strip=True) else "0"
        visit = visit_span.get_text(strip=True) if visit_span and visit_span.get_text(strip=True) else "0"
        
        try:
            home_score = int(local)
            away_score = int(visit)
        except:
            home_score = 0
            away_score = 0
        
        # Odds
        odds_raw = game_element.find_all("span", class_="o")
        odds = []
        for o in odds_raw:
            try:
                odds.append(float(o.get_text(strip=True)))
            except:
                odds.append(None)
        
        # Predicción favorita (basada en la menor odd)
        predicted = None
        predicted_name = None
        
        if len(odds) >= 3 and all(odds[:3]):
            idx = odds[:3].index(min(odds[:3]))
            predicted = ["1", "X", "2"][idx]
            predicted_name = ["Local", "Empate", "Visitante"][idx]
        
        # Doble apuesta (tip destacado)
        double_tip = game_element.find("span", class_="tip")
        if double_tip:
            predicted = double_tip.get_text(strip=True)
            # Mapear a nombre legible
            tip_map = {
                "1": "Local",
                "X": "Empate",
                "2": "Visitante",
                "1X": "Local o Empate",
                "12": "Local o Visitante",
                "X2": "Empate o Visitante"
            }
            predicted_name = tip_map.get(predicted, predicted)
        
        # Calcular probabilidades implícitas desde odds
        probabilities = self._calculate_probabilities(odds)
        
        # Link al partido
        href = game_element.get("href", "")
        link = base_url + href if href else base_url
        
        return {
            "id": game_id,
            "home_team": home_team,
            "away_team": away_team,
            "teams": teams,
            "minute": minute_raw,
            "is_live": is_live,
            "home_score": home_score,
            "away_score": away_score,
            "predicted": predicted,
            "predicted_name": predicted_name,
            "odds": {
                "home": odds[0] if len(odds) > 0 else None,
                "draw": odds[1] if len(odds) > 1 else None,
                "away": odds[2] if len(odds) > 2 else None
            },
            "probabilities": probabilities,
            "link": link,
            "date": date_str,
            "source": "PrimaTips"
        }
    
    def _calculate_probabilities(self, odds: List[Optional[float]]) -> Dict:
        """
        Calcular probabilidades implícitas desde las odds
        
        Args:
            odds: Lista de odds [home, draw, away]
        
        Returns:
            Dict con probabilidades normalizadas
        """
        if len(odds) < 3 or not all(odds[:3]):
            return {
                "home": 0.33,
                "draw": 0.33,
                "away": 0.34
            }
        
        # Probabilidad implícita = 1 / odd
        prob_home = 1.0 / odds[0] if odds[0] and odds[0] > 1 else 0.33
        prob_draw = 1.0 / odds[1] if odds[1] and odds[1] > 1 else 0.33
        prob_away = 1.0 / odds[2] if odds[2] and odds[2] > 1 else 0.34
        
        # Normalizar para que sumen 1.0 (eliminar overround)
        total = prob_home + prob_draw + prob_away
        
        if total > 0:
            prob_home /= total
            prob_draw /= total
            prob_away /= total
        
        return {
            "home": round(prob_home, 3),
            "draw": round(prob_draw, 3),
            "away": round(prob_away, 3)
        }
    
    def get_live_predictions(self) -> List[Dict]:
        """
        Obtener predicciones de partidos en vivo (ayer, hoy, mañana)
        
        Returns:
            Lista de predicciones de partidos en vivo
        """
        now = datetime.now(self.CHILE_TZ)
        dates = [(now + timedelta(days=i)).strftime("%Y-%m-%d") for i in (-1, 0, 1)]
        
        all_predictions = []
        
        for date_str in dates:
            predictions = self.get_predictions_by_date(date_str)
            
            # Filtrar solo los que están en vivo
            live_predictions = [
                p for p in predictions 
                if p.get("is_live", False)
            ]
            
            all_predictions.extend(live_predictions)
        
        return all_predictions
    
    def get_predictions_today(self) -> List[Dict]:
        """
        Obtener todas las predicciones del día de hoy
        
        Returns:
            Lista de predicciones de hoy
        """
        now = datetime.now(self.CHILE_TZ)
        today_str = now.strftime("%Y-%m-%d")
        
        return self.get_predictions_by_date(today_str)
