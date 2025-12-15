"""Configuración global del proyecto MVP"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuración centralizada para el MVP"""
    
    # ========================================
    # API Settings (Football API 7)
    # ========================================
    FOOTBALL_API_KEY = os.getenv("FOOTBALL_API_KEY", "")
    FOOTBALL_API_URL = "https://football-api-7.p.rapidapi.com/api/v3"
    
    # ========================================
    # Dashboard Settings
    # ========================================
    REFRESH_INTERVAL = int(os.getenv("REFRESH_INTERVAL", 300))  # 5 min (más frecuente para live)
    PAGE_TITLE = os.getenv("PAGE_TITLE", "Football Live Tracker")
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
    # Timezone Settings
    # ========================================
    DEFAULT_TIMEZONE = os.getenv("DEFAULT_TIMEZONE", "america/santiago")
    DEFAULT_LANG = os.getenv("DEFAULT_LANG", "en")

config = Config()
