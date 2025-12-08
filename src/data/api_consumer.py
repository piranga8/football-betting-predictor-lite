"""Consumo de API Betfair para datos de fútbol"""
import requests
from typing import List, Dict, Optional
from datetime import datetime
import time

class BetfairAPIConsumer:
    """Consumidor de Betfair Sports Data API (RapidAPI)"""
    
    SPORT_ID_SOCCER = "1"
    BASE_URL = "https://betfair-sports-data-fast-and-reliable.p.rapidapi.com"
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            'x-rapidapi-key': api_key,
            'x-rapidapi-host': 'betfair-sports-data-fast-and-reliable.p.rapidapi.com'
        }
        self._cache = {}
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """Hacer petición a la API con manejo de errores"""
        try:
            url = f"{self.BASE_URL}/{endpoint}"
            response = requests.get(url, headers=self.headers, params=params, timeout=15)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                print(f"⚠️ Rate limit alcanzado, esperando 60s...")
                time.sleep(60)
                return self._make_request(endpoint, params)
            else:
                print(f"❌ Error {response.status_code}: {response.text}")
                return None
        except Exception as e:
            print(f"❌ Error en petición: {str(e)}")
            return None
    
    def get_competitions(self) -> List[Dict]:
        """
        Obtener todas las competiciones de fútbol
        
        Returns:
            List[Dict]: Lista de competiciones con estructura:
            [
                {
                    'id': '228',
                    'name': 'UEFA Champions League',
                    'region': 'International',
                    'market_count': 1016
                },
                ...
            ]
        """
        data = self._make_request('getCompetitions', {'id': self.SPORT_ID_SOCCER})
        
        if not data:
            return []
        
        competitions = []
        for comp_data in data:
            try:
                comp = {
                    'id': comp_data['competition']['id'],
                    'name': comp_data['competition']['name'],
                    'region': comp_data.get('competitionRegion', ''),
                    'market_count': comp_data.get('marketCount', 0)
                }
                competitions.append(comp)
            except Exception as e:
                print(f"⚠️ Error parseando competición: {str(e)}")
                continue
        
        # Cachear para no pedir constantemente
        self._cache['competitions'] = competitions
        return competitions
    
    def get_events(self, competition_id: str) -> List[Dict]:
        """
        Obtener eventos (partidos) de una competición
        
        Args:
            competition_id: ID de la competición
        
        Returns:
            List[Dict]: Lista de eventos con estructura:
            [
                {
                    'event_id': '35036679',
                    'name': 'Huachipato v Deportes Limache',
                    'home_team': 'Huachipato',
                    'away_team': 'Deportes Limache',
                    'timezone': 'GMT',
                    'start_time': '2025-12-10T23:00:00Z',
                    'competition_id': '961354'
                },
                ...
            ]
        """
        data = self._make_request('getevents', {
            'sid': competition_id,
            'sportid': self.SPORT_ID_SOCCER
        })
        
        if not data:
            return []
        
        events = []
        for event_data in data:
            try:
                event_info = event_data['event']
                name = event_info['name']
                
                # Parsear equipos del nombre (formato: "Team1 v Team2")
                teams = name.split(' v ')
                home_team = teams[0].strip() if len(teams) > 0 else ''
                away_team = teams[1].strip() if len(teams) > 1 else ''
                
                event = {
                    'event_id': str(event_info['id']),
                    'name': name,
                    'home_team': home_team,
                    'away_team': away_team,
                    'timezone': event_info.get('timezone', 'GMT'),
                    'start_time': event_info.get('openDate', ''),
                    'competition_id': competition_id
                }
                events.append(event)
            except Exception as e:
                print(f"⚠️ Error parseando evento: {str(e)}")
                continue
        
        return events
    
    def get_markets_list(self, event_id: str) -> List[Dict]:
        """
        Obtener lista de mercados (tipos de apuesta) de un evento
        
        Args:
            event_id: ID del evento
        
        Returns:
            List[Dict]: Lista de mercados con estructura:
            [
                {
                    'market_id': '1.251405354',
                    'market_name': 'Match Odds',
                    'start_time': '2025-12-10T23:00:00Z',
                    'total_matched': 0,
                    'runners': [...]
                },
                ...
            ]
        """
        data = self._make_request('geMarketsList', {'EventID': event_id})
        
        if not data:
            return []
        
        markets = []
        for market_data in data:
            try:
                market = {
                    'market_id': market_data['marketId'],
                    'market_name': market_data['marketName'],
                    'start_time': market_data.get('marketStartTime', ''),
                    'total_matched': market_data.get('totalMatched', 0),
                    'runners': market_data.get('runners', [])
                }
                markets.append(market)
            except Exception as e:
                print(f"⚠️ Error parseando mercado: {str(e)}")
                continue
        
        return markets
    
    def get_market_odds(self, market_id: str) -> Optional[Dict]:
        """
        Obtener cuotas de un mercado específico
        
        Args:
            market_id: ID del mercado
        
        Returns:
            Dict: Datos del mercado con odds:
            {
                'market_id': '1.251405354',
                'status': 'OPEN',
                'inplay': False,
                'total_matched': 1029.45,
                'runners': [...]
            }
        """
        data = self._make_request('GetMarketOdds', {'market_id': market_id})
        
        if not data or len(data) == 0:
            return None
        
        try:
            market_data = data[0]
            return {
                'market_id': market_data['marketId'],
                'status': market_data.get('status', 'UNKNOWN'),
                'inplay': market_data.get('inplay', False),
                'total_matched': market_data.get('totalMatched', 0),
                'runners': market_data.get('runners', []),
                'last_match_time': market_data.get('lastMatchTime', '')
            }
        except Exception as e:
            print(f"⚠️ Error parseando odds: {str(e)}")
            return None
    
    def get_match_predictions(self, event_id: str) -> Optional[Dict]:
        """
        Obtener predicciones pre-match calculadas desde las odds
        
        Args:
            event_id: ID del evento
        
        Returns:
            Dict: Predicciones con estructura:
            {
                'prob_home': 0.55,
                'prob_draw': 0.28,
                'prob_away': 0.17,
                'prob_over_2_5': 0.52,
                'prob_under_2_5': 0.48,
                'confidence': 0.75,
                'source': 'betfair',
                'odds': {...}
            }
        """
        # 1. Obtener mercados del evento
        markets = self.get_markets_list(event_id)
        if not markets:
            return None
        
        # 2. Encontrar mercados relevantes
        match_odds_market = None
        over_under_market = None
        
        for market in markets:
            if market['market_name'] == 'Match Odds':
                match_odds_market = market
            elif 'Over/Under 2.5' in market['market_name']:
                over_under_market = market
        
        if not match_odds_market:
            return None
        
        # 3. Obtener odds del mercado Match Odds
        match_odds = self.get_market_odds(match_odds_market['market_id'])
        if not match_odds:
            return None
        
        # 4. Calcular probabilidades desde odds
        probs = self._calculate_probabilities_from_odds(match_odds)
        
        # 5. Obtener Over/Under si existe
        if over_under_market:
            ou_odds = self.get_market_odds(over_under_market['market_id'])
            if ou_odds:
                ou_probs = self._calculate_over_under_probs(ou_odds)
                probs.update(ou_probs)
        
        probs['source'] = 'betfair'
        probs['event_id'] = event_id
        return probs
    
    def _calculate_probabilities_from_odds(self, market_odds: Dict) -> Dict:
        """
        Calcular probabilidades desde las odds de Betfair
        
        En Betfair:
        - availableToBack = odds que puedes apostar A FAVOR (back)
        - availableToLay = odds que puedes apostar EN CONTRA (lay)
        
        Usamos el mejor precio disponible (precio más alto en back)
        """
        runners = market_odds['runners']
        
        # Mapear runners por selectionId típicos
        home_runner = None
        draw_runner = None
        away_runner = None
        
        for runner in runners:
            selection_id = runner['selectionId']
            # El draw suele tener selectionId 58805
            if selection_id == 58805:
                draw_runner = runner
            elif home_runner is None:
                home_runner = runner
            else:
                away_runner = runner
        
        # Extraer mejores odds de back
        def get_best_back_price(runner):
            if not runner or 'ex' not in runner:
                return None
            available = runner['ex'].get('availableToBack', [])
            if not available:
                return None
            return available[0]['price']  # Primera es la mejor
        
        home_odds = get_best_back_price(home_runner)
        draw_odds = get_best_back_price(draw_runner)
        away_odds = get_best_back_price(away_runner)
        
        # Convertir odds a probabilidades implícitas
        # Prob = 1 / odds
        def odds_to_prob(odds):
            if not odds or odds <= 1:
                return 0.33  # Fallback
            return 1.0 / odds
        
        prob_home = odds_to_prob(home_odds)
        prob_draw = odds_to_prob(draw_odds)
        prob_away = odds_to_prob(away_odds)
        
        # Normalizar para que sumen 1.0 (eliminar overround)
        total = prob_home + prob_draw + prob_away
        if total > 0:
            prob_home /= total
            prob_draw /= total
            prob_away /= total
        
        # Calcular confianza basada en liquidez
        total_matched = market_odds.get('total_matched', 0)
        confidence = min(0.95, 0.5 + (total_matched / 10000) * 0.45)  # Más liquidez = más confianza
        
        return {
            'prob_home': round(prob_home, 3),
            'prob_draw': round(prob_draw, 3),
            'prob_away': round(prob_away, 3),
            'confidence': round(confidence, 3),
            'odds': {
                'home': home_odds,
                'draw': draw_odds,
                'away': away_odds
            },
            'total_matched': total_matched
        }
    
    def _calculate_over_under_probs(self, ou_odds: Dict) -> Dict:
        """Calcular probabilidades Over/Under 2.5"""
        runners = ou_odds['runners']
        
        over_runner = None
        under_runner = None
        
        for runner in runners:
            name = runner.get('runnerName', '')
            if 'Over' in name:
                over_runner = runner
            elif 'Under' in name:
                under_runner = runner
        
        def get_best_back_price(runner):
            if not runner or 'ex' not in runner:
                return None
            available = runner['ex'].get('availableToBack', [])
            if not available:
                return None
            return available[0]['price']
        
        over_odds = get_best_back_price(over_runner)
        under_odds = get_best_back_price(under_runner)
        
        def odds_to_prob(odds):
            if not odds or odds <= 1:
                return 0.5
            return 1.0 / odds
        
        prob_over = odds_to_prob(over_odds)
        prob_under = odds_to_prob(under_odds)
        
        # Normalizar
        total = prob_over + prob_under
        if total > 0:
            prob_over /= total
            prob_under /= total
        
        return {
            'prob_over_2_5': round(prob_over, 3),
            'prob_under_2_5': round(prob_under, 3)
        }
    
    def get_live_matches(self, competition_ids: Optional[List[str]] = None) -> List[Dict]:
        """
        Obtener partidos en vivo
        
        Args:
            competition_ids: Lista de IDs de competiciones a monitorear
                           Si None, usa las principales de Europa
        
        Returns:
            List[Dict]: Partidos en vivo
        """
        if competition_ids is None:
            # IDs de ligas principales (Champions, Premier, La Liga, etc.)
            competition_ids = ['228', '10932509', '117', '59', '81', '55']
        
        live_matches = []
        
        for comp_id in competition_ids:
            events = self.get_events(comp_id)
            
            for event in events:
                # Verificar si está en vivo
                markets = self.get_markets_list(event['event_id'])
                
                for market in markets:
                    if market['market_name'] == 'Match Odds':
                        odds = self.get_market_odds(market['market_id'])
                        
                        if odds and odds.get('inplay', False):
                            # Partido en vivo
                            match = {
                                'match_id': event['event_id'],
                                'home_team': event['home_team'],
                                'away_team': event['away_team'],
                                'league': comp_id,
                                'status': 'LIVE',
                                'inplay': True,
                                'total_matched': odds.get('total_matched', 0)
                            }
                            live_matches.append(match)
                            break
        
        return live_matches


class MockBetfairAPI(BetfairAPIConsumer):
    """Mock para testing sin consumir API real"""
    
    def __init__(self):
        super().__init__('mock_key')
    
    def get_competitions(self) -> List[Dict]:
        return [
            {'id': '228', 'name': 'UEFA Champions League', 'region': 'International', 'market_count': 1016},
            {'id': '10932509', 'name': 'English Premier League', 'region': 'GBR', 'market_count': 195},
            {'id': '117', 'name': 'Spanish La Liga', 'region': 'ESP', 'market_count': 180}
        ]
    
    def get_match_predictions(self, event_id: str) -> Optional[Dict]:
        return {
            'prob_home': 0.548,
            'prob_draw': 0.287,
            'prob_away': 0.165,
            'prob_over_2_5': 0.520,
            'prob_under_2_5': 0.480,
            'confidence': 0.725,
            'source': 'betfair_mock',
            'event_id': event_id,
            'odds': {'home': 1.82, 'draw': 3.48, 'away': 6.06},
            'total_matched': 5430.25
        }
