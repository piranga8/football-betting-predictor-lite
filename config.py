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
    
    # IDs de ligas principales (opcionales, se pueden obtener dinámicamente)
    # Estos son backups por si la API falla
    DEFAULT_COMPETITION_IDS = [
        "228",       # UEFA Champions League
        "10932509",  # Premier League
        "117",       # La Liga
        "59",        # Bundesliga
        "81",        # Serie A
        "55"         # Ligue 1
    ]
    
    # ========================================
    # Cache/Update Settings
    # ========================================
    # Cuánto tiempo cachear las ligas en SQLite antes de refrescar
    COMPETITIONS_CACHE_HOURS = int(os.getenv("COMPETITIONS_CACHE_HOURS", 24))

config = Config()
