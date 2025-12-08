"""Predictor in-play que combina datos pre-match con estado actual"""
import numpy as np
from scipy.stats import poisson
from typing import Dict, Optional
from datetime import datetime

class InPlayPredictor:
    """
    Predictor que actualiza probabilidades durante el partido
    combinando:
    - Predicción pre-match (desde API)
    - Estado actual (minuto, marcador)
    - Modelo Poisson ajustado
    """
    
    def __init__(self):
        self.max_goals = 10
    
    def predict(self, 
                prematch_pred: Dict, 
                current_minute: int,
                home_score: int = 0,
                away_score: int = 0,
                match_stats: Optional[Dict] = None) -> Dict:
        """
        Genera predicción in-play ajustada
        
        Args:
            prematch_pred: Predicción pre-match con prob_home, prob_draw, prob_away
            current_minute: Minuto actual del partido (0-90+)
            home_score: Goles del equipo local
            away_score: Goles del equipo visitante
            match_stats: Estadísticas opcionales (shots, possession, etc.)
        
        Returns:
            Dict con predicción ajustada:
            {
                'prob_home': 0.72,
                'prob_draw': 0.18,
                'prob_away': 0.10,
                'confidence': 0.85,
                'signal_color': 'green',
                'adjustments': {...}
            }
        """
        # 1. Extraer probabilidades base
        prob_home_base = prematch_pred.get('prob_home', 0.33)
        prob_draw_base = prematch_pred.get('prob_draw', 0.33)
        prob_away_base = prematch_pred.get('prob_away', 0.33)
        
        # 2. Calcular lambda (goles esperados) desde probabilidades base
        lambda_home, lambda_away = self._estimate_lambdas_from_probs(
            prob_home_base, prob_draw_base, prob_away_base
        )
        
        # 3. Ajustar lambda según marcador actual y minuto
        lambda_home_adj, lambda_away_adj = self._adjust_lambdas_inplay(
            lambda_home, lambda_away,
            home_score, away_score,
            current_minute
        )
        
        # 4. Calcular nuevas probabilidades con Poisson
        prob_home, prob_draw, prob_away = self._calculate_match_odds_poisson(
            lambda_home_adj, lambda_away_adj,
            home_score, away_score,
            current_minute
        )
        
        # 5. Calcular confianza
        confidence = self._calculate_confidence(
            current_minute, 
            home_score + away_score,
            prematch_pred.get('confidence', 0.5)
        )
        
        # 6. Determinar color de señal (semáforo)
        signal_color = self._get_signal_color(confidence, prob_home, prob_draw, prob_away)
        
        # 7. Registrar ajustes
        adjustments = {
            'lambda_home_base': round(lambda_home, 3),
            'lambda_away_base': round(lambda_away, 3),
            'lambda_home_adj': round(lambda_home_adj, 3),
            'lambda_away_adj': round(lambda_away_adj, 3),
            'score_diff': home_score - away_score,
            'time_weight': self._get_time_weight(current_minute)
        }
        
        return {
            'prob_home': round(prob_home, 3),
            'prob_draw': round(prob_draw, 3),
            'prob_away': round(prob_away, 3),
            'confidence': round(confidence, 3),
            'signal_color': signal_color,
            'current_minute': current_minute,
            'current_score': f"{home_score}-{away_score}",
            'adjustments': adjustments,
            'timestamp': datetime.now().isoformat()
        }
    
    def _estimate_lambdas_from_probs(self, prob_home, prob_draw, prob_away):
        """
        Estimar lambda (goles esperados) desde probabilidades 1X2
        Usa aproximación inversa simple
        """
        # Aproximación:
        # - Si prob_home alta → lambda_home alto, lambda_away bajo
        # - Si prob_away alta → lambda_away alto, lambda_home bajo
        # - Si prob_draw alta → lambdas similares
        
        # Media de goles por equipo en fútbol: ~1.3-1.5
        base_lambda = 1.4
        
        # Factor de ajuste basado en probabilidades
        home_factor = (prob_home - prob_away) + 1.0  # 0.5 a 1.5
        away_factor = (prob_away - prob_home) + 1.0
        
        lambda_home = base_lambda * home_factor
        lambda_away = base_lambda * away_factor
        
        # Limitar rango razonable
        lambda_home = max(0.5, min(3.5, lambda_home))
        lambda_away = max(0.5, min(3.5, lambda_away))
        
        return lambda_home, lambda_away
    
    def _adjust_lambdas_inplay(self, lambda_home, lambda_away, 
                                home_score, away_score, minute):
        """
        Ajustar lambdas según marcador y tiempo restante
        """
        # Tiempo restante (aprox)
        time_remaining = max(0, 90 - minute)
        time_fraction = time_remaining / 90.0
        
        # Ajuste por marcador
        score_diff = home_score - away_score
        
        # Si un equipo va ganando, tiende a defender más (lambda baja)
        # El que va perdiendo ataca más (lambda sube)
        if score_diff > 0:  # Local ganando
            # Local defiende un poco
            lambda_home_adj = lambda_home * (0.95 + 0.05 * time_fraction)
            # Visitante ataca más
            lambda_away_adj = lambda_away * (1.05 + 0.15 * (1 - time_fraction))
        elif score_diff < 0:  # Visitante ganando
            # Local ataca más
            lambda_home_adj = lambda_home * (1.05 + 0.15 * (1 - time_fraction))
            # Visitante defiende
            lambda_away_adj = lambda_away * (0.95 + 0.05 * time_fraction)
        else:  # Empate
            lambda_home_adj = lambda_home
            lambda_away_adj = lambda_away
        
        return lambda_home_adj, lambda_away_adj
    
    def _calculate_match_odds_poisson(self, lambda_home, lambda_away, 
                                       home_score, away_score, minute):
        """
        Calcular probabilidades 1X2 usando Poisson
        condicionado al marcador actual
        """
        time_remaining = max(0, 90 - minute)
        
        # Escalar lambdas según tiempo restante
        # Lambda es "por partido completo", ajustamos a tiempo restante
        lambda_home_remaining = lambda_home * (time_remaining / 90.0)
        lambda_away_remaining = lambda_away * (time_remaining / 90.0)
        
        # Calcular matriz de probabilidades para goles adicionales
        prob_matrix = np.zeros((self.max_goals, self.max_goals))
        
        for i in range(self.max_goals):
            for j in range(self.max_goals):
                prob_matrix[i, j] = (
                    poisson.pmf(i, lambda_home_remaining) *
                    poisson.pmf(j, lambda_away_remaining)
                )
        
        # Sumar marcador actual a los goles adicionales
        prob_home_win = 0
        prob_draw = 0
        prob_away_win = 0
        
        for i in range(self.max_goals):
            for j in range(self.max_goals):
                final_home = home_score + i
                final_away = away_score + j
                
                if final_home > final_away:
                    prob_home_win += prob_matrix[i, j]
                elif final_home == final_away:
                    prob_draw += prob_matrix[i, j]
                else:
                    prob_away_win += prob_matrix[i, j]
        
        # Normalizar
        total = prob_home_win + prob_draw + prob_away_win
        if total > 0:
            prob_home_win /= total
            prob_draw /= total
            prob_away_win /= total
        
        return prob_home_win, prob_draw, prob_away_win
    
    def _get_time_weight(self, minute):
        """
        Peso del tiempo: más avanzado el partido, más peso al marcador actual
        """
        if minute <= 0:
            return 0.0
        elif minute >= 90:
            return 1.0
        else:
            # Curva exponencial suave
            return (minute / 90.0) ** 1.5
    
    def _calculate_confidence(self, minute, total_goals, base_confidence):
        """
        Calcular confianza de la predicción
        
        - Más avanzado el partido → más confianza
        - Más goles → más información → más confianza
        - Confianza base de predicción pre-match
        """
        # Factor de tiempo (0 a 0.4)
        time_factor = (minute / 90.0) * 0.4
        
        # Factor de goles (0 a 0.3)
        goals_factor = min(total_goals / 5.0, 1.0) * 0.3
        
        # Confianza base (0.3 a 0.95 escalado a 0 a 0.3)
        base_factor = (base_confidence - 0.3) / 0.65 * 0.3
        
        confidence = time_factor + goals_factor + base_factor
        
        return max(0.3, min(0.95, confidence))
    
    def _get_signal_color(self, confidence, prob_home, prob_draw, prob_away):
        """
        Determinar color de señal tipo semáforo
        
        Verde: Alta confianza y resultado claro
        Amarillo: Confianza media o resultado incierto
        Rojo: Baja confianza
        """
        # Resultado claro = una probabilidad domina
        max_prob = max(prob_home, prob_draw, prob_away)
        result_clarity = max_prob - (1.0 / 3.0)  # 0 = empate triple, 0.66 = 100% en uno
        
        if confidence >= 0.75 and result_clarity >= 0.3:
            return 'green'
        elif confidence >= 0.55 and result_clarity >= 0.15:
            return 'yellow'
        else:
            return 'red'


# Instancia global
predictor = InPlayPredictor()
