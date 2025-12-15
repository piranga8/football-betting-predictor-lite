"""Consumo de Football API 7 para datos de fútbol"""
import requests
from typing import List, Dict, Optional
from datetime import datetime
import pytz

class FootballAPI7Consumer:
    """Consumidor de Football API 7 (RapidAPI)"""
    
    BASE_URL = "https://football-api-7.p.rapidapi.com/api/v3"
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            'x-rapidapi-key': api_key,
            'x-rapidapi-host': 'football-api-7.p.rapidapi.com'
        }
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """Hacer petición a la API con manejo de errores"""
        try:
            url = f"{self.BASE_URL}/{endpoint}"
            
            print(f"🔍 Llamando: {url}")
            print(f"📊 Params: {params}")
            
            response = requests.get(url, headers=self.headers, params=params, timeout=15)
            
            print(f"📡 Status: {response.status_code}")
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 403:
                print(f"❌ Error 403: {response.text}")
                print("⚠️ Verifica tu suscripción a Football API 7 en RapidAPI")
                return None
            elif response.status_code == 429:
                print(f"⚠️ Rate limit alcanzado")
                return None
            else:
                print(f"❌ Error {response.status_code}: {response.text}")
                return None
        except Exception as e:
            print(f"❌ Error en petición: {str(e)}")
            return None
    
    def get_matches_by_date(self, date: str = None, timezone: str = "america/santiago", lang: str = "en") -> List[Dict]:
        """
        Obtener todos los partidos de un día específico
        
        Args:
            date: Fecha en formato DD/MM/YYYY (default: hoy)
            timezone: Zona horaria (default: america/santiago)
            lang: Idioma (default: en)
        
        Returns:
            Lista de partidos parseados
        """
        # Si no se proporciona fecha, usar hoy
        if date is None:
            tz = pytz.timezone('America/Santiago')
            today = datetime.now(tz)
            date = today.strftime('%d/%m/%Y')
        
        params = {
            'date': date,
            'time': timezone,
            'lang': lang
        }
        
        data = self._make_request('matches', params)
        
        if not data:
            return []
        
        # Parsear y aplanar la estructura
        all_matches = []
        
        for competition_data in data:
            try:
                competition = competition_data.get('competition', {})
                games = competition_data.get('games', [])
                
                for game in games:
                    match = self._parse_match(game, competition)
                    all_matches.append(match)
            except Exception as e:
                print(f"⚠️ Error parseando competición: {str(e)}")
                continue
        
        return all_matches
    
    def _parse_match(self, game: Dict, competition: Dict) -> Dict:
        """
        Parsear un partido individual
        
        Returns:
            Dict con estructura unificada
        """
        home = game.get('homeCompetitor', {})
        away = game.get('awayCompetitor', {})
        
        # Determinar status
        status_group = game.get('statusGroup', 2)
        is_live = status_group == 3  # 3 = En vivo, 2 = Programado, 4 = Finalizado
        
        # Parsear score (-1 significa no hay score aún)
        home_score = home.get('score', -1)
        away_score = away.get('score', -1)
        
        if home_score == -1:
            home_score = 0
        if away_score == -1:
            away_score = 0
        
        # Minuto del partido
        game_time = game.get('gameTime', -1)
        if game_time == -1:
            game_time = 0
        
        return {
            'match_id': str(game.get('id')),
            'competition': {
                'id': str(competition.get('id')),
                'name': competition.get('name', ''),
                'logo': competition.get('logo', ''),
                'country': competition.get('countryId', '')
            },
            'home_team': {
                'id': str(home.get('id')),
                'name': home.get('name', ''),
                'logo': home.get('logo', ''),
                'score': home_score,
                'red_cards': home.get('redCards') or 0
            },
            'away_team': {
                'id': str(away.get('id')),
                'name': away.get('name', ''),
                'logo': away.get('logo', ''),
                'score': away_score,
                'red_cards': away.get('redCards') or 0
            },
            'status': {
                'is_live': is_live,
                'status_text': game.get('statusText', ''),
                'short_status': game.get('shortStatusText', ''),
                'game_time': game_time,
                'game_time_display': game.get('gameTimeDisplay', ''),
                'just_ended': game.get('justEnded', False)
            },
            'start_time': game.get('startTime', ''),
            'round_name': game.get('roundName', ''),
            'stage_name': game.get('stageName'),
            'has_lineups': game.get('hasLineups', False),
            'has_video': game.get('hasVideo', False)
        }
    
    def get_live_matches(self, date: str = None) -> List[Dict]:
        """
        Obtener solo los partidos que están en vivo
        
        Args:
            date: Fecha en formato DD/MM/YYYY (default: hoy)
        
        Returns:
            Lista de partidos en vivo
        """
        all_matches = self.get_matches_by_date(date)
        
        # Filtrar solo los que están en vivo
        live_matches = [
            match for match in all_matches 
            if match['status']['is_live']
        ]
        
        print(f"✅ {len(live_matches)} partidos en vivo de {len(all_matches)} totales")
        
        return live_matches
    
    def get_matches_by_competition(self, competition_name: str, date: str = None) -> List[Dict]:
        """
        Filtrar partidos por nombre de competición
        
        Args:
            competition_name: Nombre de la competición (ej: "Premier League")
            date: Fecha en formato DD/MM/YYYY
        
        Returns:
            Lista de partidos de esa competición
        """
        all_matches = self.get_matches_by_date(date)
        
        filtered = [
            match for match in all_matches
            if competition_name.lower() in match['competition']['name'].lower()
        ]
        
        return filtered
