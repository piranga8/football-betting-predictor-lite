"""Constants for the application"""

# Leagues
LEAGUES = {
    "premier_league": "Premier League",
    "la_liga": "La Liga",
    "serie_a": "Serie A",
    "bundesliga": "Bundesliga",
    "ligue_1": "Ligue 1"
}

# Match outcomes
OUTCOMES = {
    "1": "Home Win",
    "X": "Draw",
    "2": "Away Win"
}

# Model names
MODEL_NAMES = [
    "poisson",
    "logistic",
    "tree",
    "naive_bayes",
    "random_forest",
    "xgboost",
    "ensemble"
]

# Feature columns
FEATURE_COLUMNS = [
    "home_xg",
    "home_xga",
    "home_ppda",
    "home_possession",
    "home_form",
    "home_h2h_wins",
    "home_advantage",
    "away_xg",
    "away_xga",
    "away_ppda",
    "away_possession",
    "away_form",
    "away_h2h_wins"
]

# Target columns
TARGET_COLUMN = "result"  # 0=Home, 1=Draw, 2=Away

# Time decay parameters
TIME_DECAY_RATE = 0.95  # 5% decay per minute

# Bayesian update parameters
LIKELIHOOD_HOME_SCORES = 0.65
LIKELIHOOD_AWAY_SCORES = 0.35
LIKELIHOOD_RED_CARD_IMPACT = 0.70
LIKELIHOOD_INJURY_IMPACT = 0.45

# Kelly Criterion risk levels
KELLY_RISK_LEVELS = {
    "aggressive": 1.0,
    "moderate": 0.5,
    "conservative": 0.25,
    "very_conservative": 0.1
}

# Edge thresholds
MIN_EDGE_THRESHOLD = 0.02  # 2%
HIGH_EDGE_THRESHOLD = 0.08  # 8%

# Confidence thresholds
MIN_CONFIDENCE = 0.70
HIGH_CONFIDENCE = 0.85

# Cache TTL (seconds)
CACHE_TTL_LIVE_ODDS = 10  # 10 seconds
CACHE_TTL_PREDICTIONS = 300  # 5 minutes
CACHE_TTL_TEAM_STATS = 3600  # 1 hour

# WebSocket update interval
WEBSOCKET_UPDATE_INTERVAL = 10  # seconds