"""Configuración global del proyecto MVP"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuración centralizada"""
    
    # API Settings
    FOOTBALL_API_KEY = os.getenv("FOOTBALL_API_KEY", "")
    FOOTBALL_API_URL = os.getenv("FOOTBALL_API_URL", "")
    
    # Refresh Settings
    REFRESH_INTERVAL = int(os.getenv("REFRESH_INTERVAL", 900))  # 15 min
    
    # Prediction Settings
    MIN_CONFIDENCE = float(os.getenv("MIN_CONFIDENCE", 0.60))
    
    # Database
    DB_PATH = "data/predictions.db"
    
    # Dashboard
    PAGE_TITLE = "Football Betting Predictor - Live"
    PAGE_ICON = "⚽"

config = Config()
