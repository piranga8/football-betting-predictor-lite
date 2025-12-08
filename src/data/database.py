"""Gestión de base de datos SQLite para almacenamiento temporal"""
import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path

class Database:
    """SQLite database manager"""
    
    def __init__(self, db_path: str = "data/predictions.db"):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._create_tables()
    
    def _create_tables(self):
        """Crear tablas si no existen"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabla de partidos en vivo
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS live_matches (
                match_id TEXT PRIMARY KEY,
                home_team TEXT NOT NULL,
                away_team TEXT NOT NULL,
                league TEXT,
                match_time TEXT,
                status TEXT,
                current_minute INTEGER,
                home_score INTEGER DEFAULT 0,
                away_score INTEGER DEFAULT 0,
                last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de predicciones pre-match
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS prematch_predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                match_id TEXT NOT NULL,
                source TEXT NOT NULL,
                prob_home REAL,
                prob_draw REAL,
                prob_away REAL,
                prob_over_2_5 REAL,
                prob_btts REAL,
                confidence REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (match_id) REFERENCES live_matches(match_id)
            )
        ''')
        
        # Tabla de predicciones in-play
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inplay_predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                match_id TEXT NOT NULL,
                minute INTEGER NOT NULL,
                prob_home REAL,
                prob_draw REAL,
                prob_away REAL,
                confidence REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (match_id) REFERENCES live_matches(match_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_live_match(self, match_data: Dict):
        """Guardar o actualizar partido en vivo"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO live_matches 
            (match_id, home_team, away_team, league, match_time, status, 
             current_minute, home_score, away_score, last_update)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            match_data['match_id'],
            match_data['home_team'],
            match_data['away_team'],
            match_data.get('league', ''),
            match_data.get('match_time', ''),
            match_data.get('status', 'LIVE'),
            match_data.get('current_minute', 0),
            match_data.get('home_score', 0),
            match_data.get('away_score', 0),
            datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
    
    def save_prematch_prediction(self, match_id: str, source: str, prediction: Dict):
        """Guardar predicción pre-match"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO prematch_predictions 
            (match_id, source, prob_home, prob_draw, prob_away, 
             prob_over_2_5, prob_btts, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            match_id,
            source,
            prediction.get('prob_home'),
            prediction.get('prob_draw'),
            prediction.get('prob_away'),
            prediction.get('prob_over_2_5'),
            prediction.get('prob_btts'),
            prediction.get('confidence', 0.5)
        ))
        
        conn.commit()
        conn.close()
    
    def save_inplay_prediction(self, match_id: str, minute: int, prediction: Dict):
        """Guardar predicción in-play"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO inplay_predictions 
            (match_id, minute, prob_home, prob_draw, prob_away, confidence)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            match_id,
            minute,
            prediction.get('prob_home'),
            prediction.get('prob_draw'),
            prediction.get('prob_away'),
            prediction.get('confidence', 0.5)
        ))
        
        conn.commit()
        conn.close()
    
    def get_live_matches(self) -> List[Dict]:
        """Obtener todos los partidos en vivo"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM live_matches 
            WHERE status = 'LIVE'
            ORDER BY last_update DESC
        ''')
        
        matches = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return matches
    
    def get_prematch_predictions(self, match_id: str) -> List[Dict]:
        """Obtener predicciones pre-match de un partido"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM prematch_predictions 
            WHERE match_id = ?
            ORDER BY created_at DESC
        ''', (match_id,))
        
        predictions = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return predictions
    
    def get_latest_inplay_prediction(self, match_id: str) -> Optional[Dict]:
        """Obtener última predicción in-play"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM inplay_predictions 
            WHERE match_id = ?
            ORDER BY created_at DESC
            LIMIT 1
        ''', (match_id,))
        
        result = cursor.fetchone()
        conn.close()
        return dict(result) if result else None
    
    def cleanup_old_matches(self, hours: int = 24):
        """Limpiar partidos antiguos"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM live_matches 
            WHERE datetime(last_update) < datetime('now', '-' || ? || ' hours')
        ''', (hours,))
        
        conn.commit()
        conn.close()

db = Database()
