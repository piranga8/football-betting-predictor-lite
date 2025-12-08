"""Helper functions"""
import numpy as np
import pandas as pd
from typing import List, Dict, Any
from datetime import datetime, timedelta


def decimal_to_probability(decimal_odds: float) -> float:
    """Convert decimal odds to probability"""
    if decimal_odds <= 1:
        return 0.0
    return 1.0 / decimal_odds


def probability_to_decimal(probability: float) -> float:
    """Convert probability to decimal odds"""
    if probability <= 0 or probability >= 1:
        return 1.0
    return 1.0 / probability


def calculate_edge(predicted_prob: float, decimal_odds: float) -> float:
    """Calculate betting edge"""
    if decimal_odds <= 1:
        return 0.0
    return (predicted_prob * decimal_odds) - 1


def normalize_probabilities(probs: Dict[str, float]) -> Dict[str, float]:
    """Normalize probabilities to sum to 1.0"""
    total = sum(probs.values())
    if total == 0:
        return probs
    return {k: v / total for k, v in probs.items()}


def calculate_variance(predictions: List[Dict[str, float]], key: str) -> float:
    """Calculate variance of predictions across models"""
    values = [p.get(key, 0) for p in predictions if key in p]
    if not values:
        return 0.0
    return float(np.var(values))


def calculate_confidence(predictions: List[Dict[str, float]]) -> float:
    """Calculate confidence based on variance between models
    
    Lower variance = higher confidence
    """
    if not predictions:
        return 0.0
    
    # Calculate variance for 1X2 outcomes
    variances = []
    for outcome in ["1", "X", "2"]:
        var = calculate_variance([p.get("1x2", {}) for p in predictions], outcome)
        variances.append(var)
    
    avg_variance = np.mean(variances)
    
    # Convert variance to confidence (0-1)
    # Lower variance = higher confidence
    confidence = 1.0 - min(avg_variance * 10, 1.0)
    
    return float(confidence)


def get_recent_form(results: List[str], n: int = 5) -> float:
    """Calculate form score from recent results
    
    Args:
        results: List of results ('W', 'D', 'L')
        n: Number of recent matches to consider
    
    Returns:
        Form score between 0 and 1
    """
    if not results:
        return 0.5
    
    recent = results[-n:]
    points = sum([3 if r == 'W' else 1 if r == 'D' else 0 for r in recent])
    max_points = len(recent) * 3
    
    return points / max_points if max_points > 0 else 0.5


def time_weighted_average(values: List[float], weights: List[float] = None) -> float:
    """Calculate time-weighted average (recent matches have more weight)"""
    if not values:
        return 0.0
    
    if weights is None:
        # Exponential decay weights (recent = more weight)
        weights = [0.95 ** i for i in range(len(values))]
        weights.reverse()
    
    weighted_sum = sum(v * w for v, w in zip(values, weights))
    weight_sum = sum(weights)
    
    return weighted_sum / weight_sum if weight_sum > 0 else 0.0


def format_match_name(home_team: str, away_team: str) -> str:
    """Format match name"""
    return f"{home_team} vs {away_team}"


def parse_score(score_str: str) -> tuple:
    """Parse score string '2-1' to (2, 1)"""
    try:
        home, away = score_str.split('-')
        return int(home), int(away)
    except:
        return 0, 0


def calculate_poisson_probability(lambda_value: float, k: int) -> float:
    """Calculate Poisson probability
    
    P(X=k) = (lambda^k * e^-lambda) / k!
    """
    from scipy.stats import poisson
    return float(poisson.pmf(k, lambda_value))


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safe division with default value"""
    if denominator == 0:
        return default
    return numerator / denominator