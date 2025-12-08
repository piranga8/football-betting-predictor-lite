"""Configuración global del proyecto MVP"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuración centralizada para el MVP"""
    
    # ========================================
    # API Settings (Betfair via RapidAPI)
    # ========================================
    FOOTBALL_API_KEY = os.getenv("FOOTBALL_API_KEY", "")
    FOOTBALL_API_URL = os.getenv(
        "FOOTBALL_API_URL", 
        "https://betfair-sports-data-fast-and-reliable.p.rapidapi.com"
    )
    
    # ========================================
    # Dashboard Settings
    # ========================================
    REFRESH_INTERVAL = int(os.getenv("REFRESH_INTERVAL", 900))  # 15 min (segundos)
    PAGE_TITLE = os.getenv("PAGE_TITLE", "Football Betting Predictor - Live")
    PAGE_ICON = os.getenv("PAGE_ICON", "⚽")
    
    # ========================================
    # Prediction Settings
    # ========================================
    MIN_CONFIDENCE = float(os.getenv("MIN_CONFIDENCE", 0.60))
    
    # ========================================
    # Database Settings (SQLite)
    # ========================================
    DB_PATH = os.getenv("DB_PATH", "data/predictions.db")
    
    # ========================================
    # Betfair API Constants
    # ========================================
    SPORT_ID_SOCCER = "1"  # ID de fútbol en Betfair
    
    # ========================================
    # Default Leagues (nombre e ID de las más populares)
    # ========================================
    DEFAULT_LEAGUES = [
        {'id': '228', 'name': 'UEFA Champions League', 'region': 'International'},
        {'id': '10932509', 'name': 'English Premier League', 'region': 'GBR'},
        {'id': '117', 'name': 'Spanish La Liga', 'region': 'ESP'},
        {'id': '59', 'name': 'German Bundesliga', 'region': 'DEU'},
        {'id': '81', 'name': 'Italian Serie A', 'region': 'ITA'},
        {'id': '55', 'name': 'French Ligue 1', 'region': 'FRA'},
        {'id': '2005', 'name': 'UEFA Europa League', 'region': 'International'},
        {'id': '12375833', 'name': 'UEFA Europa Conference League', 'region': 'International'},
        {'id': '7129730', 'name': 'English Sky Bet Championship', 'region': 'GBR'},
        {'id': '12204313', 'name': 'Spanish Segunda Division', 'region': 'ESP'},
        {'id': '61', 'name': 'German Bundesliga 2', 'region': 'DEU'},
        {'id': '67387', 'name': 'Argentinian Primera Division', 'region': 'ARG'},
        {'id': '844197', 'name': 'Colombian Primera A', 'region': 'COL'},
        {'id': '99', 'name': 'Portuguese Primeira Liga', 'region': 'PRT'},
        {'id': '9404054', 'name': 'Dutch Eredivisie', 'region': 'NLD'},
        {'id': '89979', 'name': 'Belgian Pro League', 'region': 'BEL'},
        {'id': '194215', 'name': 'Turkish Super League', 'region': 'TUR'},
        {'id': '105', 'name': 'Scottish Premiership', 'region': 'GBR'},
        {'id': '10479956', 'name': 'Austrian Bundesliga', 'region': 'AUT'},
        {'id': '133', 'name': 'Swiss Super League', 'region': 'CHE'},
    ]
    
    # ========================================
    # Cache/Update Settings
    # ========================================
    COMPETITIONS_CACHE_HOURS = int(os.getenv("COMPETITIONS_CACHE_HOURS", 24))

config = Config()
