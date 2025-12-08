"""Gestión de base de datos SQLite para almacenamiento temporal"""
import sqlite3
import json
from datetime import datetime, timedelta
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
        
        # Tabla de competiciones (cache)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS competitions (
                competition_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                region TEXT,
                market_count INTEGER,
                last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
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
    
    # ==========================================
    # Métodos de Competiciones (Cache)
    # ==========================================
    
    def save_competitions(self, competitions: List[Dict]):
        """
        Guardar o actualizar competiciones en cache
        
        Args:
            competitions: Lista de competiciones desde la API
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for comp in competitions:
            cursor.execute('''
                INSERT OR REPLACE INTO competitions 
                (competition_id, name, region, market_count, last_update)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                comp['id'],
                comp['name'],
                comp.get('region', ''),
                comp.get('market_count', 0),
                datetime.now().isoformat()
            ))
        
        conn.commit()
        conn.close()
    
    def get_cached_competitions(self, max_age_hours: int = 24) -> Optional[List[Dict]]:
        """
        Obtener competiciones desde cache si son suficientemente recientes
        
        Args:
            max_age_hours: Edad máxima del cache en horas
        
        Returns:
            Lista de competiciones o None si el cache está vencido
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Verificar si hay datos recientes
        cursor.execute('''
            SELECT COUNT(*) as count, MAX(datetime(last_update)) as latest
            FROM competitions
        ''')
        
        result = cursor.fetchone()
        
        if result['count'] == 0:
            conn.close()
            return None
        
        latest_update = datetime.fromisoformat(result['latest'])
        age = datetime.now() - latest_update
        
        # Si el cache es muy viejo, retornar None
        if age > timedelta(hours=max_age_hours):
            conn.close()
            return None
        
        # Obtener competiciones del cache
        cursor.execute('SELECT * FROM competitions ORDER BY market_count DESC')
        competitions = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        # Convertir al formato esperado
        return [{
            'id': comp['competition_id'],
            'name': comp['name'],
            'region': comp['region'],
            'market_count': comp['market_count']
        } for comp in competitions]
    
    def clear_competitions_cache(self):
        """Limpiar cache de competiciones"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM competitions')
        conn.commit()
        conn.close()
    
    # ==========================================
    # Métodos de Partidos (Existentes)
    # ==========================================
    
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
