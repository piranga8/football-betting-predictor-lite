"""Utilidades para emparejar partidos entre diferentes fuentes"""
from typing import List, Dict, Optional
from difflib import SequenceMatcher

def normalize_team_name(name: str) -> str:
    """
    Normalizar nombre de equipo para comparación
    
    Args:
        name: Nombre del equipo
    
    Returns:
        Nombre normalizado (minúsculas, sin espacios extra)
    """
    return name.lower().strip().replace("  ", " ")

def calculate_similarity(str1: str, str2: str) -> float:
    """
    Calcular similitud entre dos strings
    
    Args:
        str1: Primer string
        str2: Segundo string
    
    Returns:
        Score de similitud (0.0 - 1.0)
    """
    return SequenceMatcher(None, 
                          normalize_team_name(str1), 
                          normalize_team_name(str2)).ratio()

def find_matching_prediction(match: Dict, predictions: List[Dict], threshold: float = 0.7) -> Optional[Dict]:
    """
    Encontrar la predicción que corresponde a un partido
    
    Args:
        match: Partido de Football API 7
        predictions: Lista de predicciones de PrimaTips
        threshold: Umbral mínimo de similitud (0.0 - 1.0)
    
    Returns:
        Predicción encontrada o None
    """
    match_home = match['home_team']['name']
    match_away = match['away_team']['name']
    
    best_match = None
    best_score = 0.0
    
    for prediction in predictions:
        pred_home = prediction['home_team']
        pred_away = prediction['away_team']
        
        # Calcular similitud de ambos equipos
        home_similarity = calculate_similarity(match_home, pred_home)
        away_similarity = calculate_similarity(match_away, pred_away)
        
        # Score combinado (promedio)
        combined_score = (home_similarity + away_similarity) / 2.0
        
        if combined_score > best_score and combined_score >= threshold:
            best_score = combined_score
            best_match = prediction
    
    return best_match

def enrich_matches_with_predictions(matches: List[Dict], predictions: List[Dict]) -> List[Dict]:
    """
    Añadir predicciones a los partidos que coincidan
    
    Args:
        matches: Lista de partidos de Football API 7
        predictions: Lista de predicciones de PrimaTips
    
    Returns:
        Lista de partidos enriquecidos con predicciones
    """
    enriched = []
    
    for match in matches:
        enriched_match = match.copy()
        
        # Buscar predicción correspondiente
        prediction = find_matching_prediction(match, predictions)
        
        if prediction:
            enriched_match['prediction'] = {
                'predicted': prediction['predicted'],
                'predicted_name': prediction['predicted_name'],
                'odds': prediction['odds'],
                'probabilities': prediction['probabilities'],
                'source': prediction['source'],
                'link': prediction['link']
            }
        else:
            enriched_match['prediction'] = None
        
        enriched.append(enriched_match)
    
    return enriched
