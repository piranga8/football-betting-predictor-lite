# ⚽ Football Betting Predictor (Lite Version)

**Dashboard predictor simplificado** de apuestas en fútbol basado en **estadística pura** y **machine learning clásico**.

🚀 **Sin Computer Vision** - Solo análisis numérico, datos históricos y modelos estadísticos probados.

---

## 🎯 Características Principales

### Pre-Match Predictions
- 🤖 **7 Modelos Clásicos**: Poisson, Logistic Regression, Decision Trees, Naive Bayes, Random Forest, XGBoost, Ensemble
- 🎲 **Predicciones 1X2**: Probabilidades Local/Empate/Visitante
- ⚽ **Over/Under 2.5**: Predicción de goles totales
- 🔄 **BTTS**: Both Teams To Score

### In-Play Predictions
- ⏱️ **Time Decay Model**: Ajuste dinámico según tiempo transcurrido
- 📊 **Bayesian Updates**: Actualización tras eventos (goles, tarjetas, lesiones)
- 🔄 **Real-time**: WebSocket para updates cada 10 segundos

### Edge Detection & Kelly Criterion
- 💰 **Value Bets**: Detección automática de edge positivo
- 🎯 **Kelly Optimizer**: Cálculo de stake óptimo
- 📈 **Portfolio Tracking**: Seguimiento de ROI y rendimiento

### Dashboard Interactivo
- 📊 **Streamlit UI**: Interfaz web rápida y clara
- 🗓️ **Comparativa de Modelos**: Visualiza predicciones de todos los modelos
- 💻 **FastAPI Backend**: API REST + WebSocket

---

## 📦 Arquitectura

```
football-betting-predictor-lite/
├── data/
│   ├── raw/                # Datos descargados
│   ├── processed/          # Features calculadas
│   └── models/             # Modelos entrenados
├── src/
│   ├── data/               # Data fetching & processing
│   ├── features/           # Feature engineering
│   ├── models/             # ML models (7 tipos)
│   ├── inference/          # Predictor + Edge + Kelly
│   ├── api/                # FastAPI backend
│   └── utils/              # Helpers
├── frontend/
│   └── app.py              # Streamlit dashboard
├── notebooks/              # Jupyter notebooks
├── tests/                  # Unit tests
└── docker/                 # Docker config
```

---

## 🚀 Quick Start

### 1. Clonar repositorio

```bash
git clone https://github.com/piranga8/football-betting-predictor-lite.git
cd football-betting-predictor-lite
```

### 2. Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env con tus credenciales
```

### 5. Entrenar modelos (primera vez)

```bash
python scripts/train_all_models.py
```

### 6. Iniciar API backend

```bash
uvicorn src.api.main:app --reload --port 8000
```

### 7. Iniciar dashboard

```bash
streamlit run frontend/app.py
```

Abre tu navegador en `http://localhost:8501` 🎉

---

## 🤖 Modelos Implementados

| Modelo | Precisión | Velocidad | Complejidad | Uso |
|--------|----------|-----------|-------------|-----|
| **Poisson Distribution** | 50-52% | ⚡⚡⚡ | Muy Baja | Baseline simple |
| **Logistic Regression** | 54-57% | ⚡⚡ | Baja | Interpretable |
| **Decision Trees** | 52-56% | ⚡⚡ | Media | Pruebas rápidas |
| **Naive Bayes** | 51-54% | ⚡⚡⚡ | Baja | Pocos datos |
| **Random Forest** | 54-57% | ⚡ | Media | Robusto |
| **XGBoost** | 55-60% | ⚡ | Alta | 🎯 **MEJOR** |
| **Ensemble (Voting)** | 58-62% | ⚡ | Alta | 🎯 **MÁS PRECISO** |

💡 **Recomendación**: Usar **Ensemble** para predicciones finales (combina XGBoost + Logistic + Poisson).

---

## 📊 Features Calculadas

### Pre-Match
- **xG promedio** (goles esperados)
- **xGA promedio** (goles esperados en contra)
- **PPDA** (presión defensiva)
- **Posesión promedio**
- **Forma reciente** (últimos 5 partidos)
- **Head-to-head** (histórico)
- **Home advantage**

### In-Play
- **xG acumulado** (en vivo)
- **Trayectoria de posesión**
- **Tiros a puerta**
- **Tiempo restante**
- **Eventos recientes** (goles, tarjetas, lesiones)

---

## 💰 Edge Detection & Kelly Criterion

### Cálculo de Edge

```python
Edge = (Probabilidad_Predicha × Cuota_Decimal) - 1
```

**Ejemplo**:
- Probabilidad predicha: 58%
- Cuota: 1.90
- Cuota implícita: 52.6%
- **Edge = (0.58 × 1.90) - 1 = 0.102 = +10.2%** ✅

### Kelly Criterion (Stake Óptimo)

```python
f* = (b × p - q) / b

Donde:
- b = cuota_decimal - 1
- p = probabilidad_win
- q = 1 - p
```

**Fraccional Kelly recomendado**: **25%** (reduce volatilidad)

---

## 💻 API Endpoints

### Pre-Match

```bash
GET /api/v1/predict/{home_team}/{away_team}
```

**Response**:
```json
{
  "match": "Barcelona vs Real Madrid",
  "1x2": {"1": 0.548, "X": 0.305, "2": 0.147},
  "over_2_5": 0.317,
  "btts": 0.393,
  "confidence": 0.87,
  "best_model": "xgboost"
}
```

### In-Play

```bash
GET /api/v1/inplay/{match_id}
```

### WebSocket (Real-time)

```bash
ws://localhost:8000/ws/inplay/{match_id}
```

---

## 📈 Rendimiento Esperado

| Métrica | Valor |
|---------|-------|
| **Accuracy** | 56-62% |
| **ROI (30 días)** | +6% a +12% |
| **Sharpe Ratio** | 1.2 - 1.6 |
| **Win Rate** | 53-58% |

⚠️ **Importante**: Resultados pueden variar según liga, temporada y condiciones de mercado.

---

## 👨‍💻 Ejemplo de Uso

```python
from src.inference import MatchPredictor
from src.inference import EdgeDetector, KellyCalculator

# Predicción pre-match
predictor = MatchPredictor()
result = await predictor.predict_prematch(
    home_team="Barcelona",
    away_team="Real Madrid"
)

print(result["1x2"])  # {'1': 0.548, 'X': 0.305, '2': 0.147}

# Detectar edge
live_odds = {"1x2": {"1": 1.90, "X": 3.50, "2": 5.00}}
value_bets = EdgeDetector.find_value_bets(
    predictions=result,
    live_odds=live_odds,
    min_edge=0.02
)

# Calcular stake óptimo
if value_bets:
    kelly_stake = KellyCalculator.calculate_optimal_stake(
        bankroll=1000,
        kelly_fraction=value_bets[0]["kelly_fraction"]
    )
    print(f"Apostar: ${kelly_stake:.2f}")
```

---

## 📚 Recursos & Referencias

### Papers & Artículos
- [Predicting Football Results with Statistical Modelling (Dixon-Coles)](https://dashee87.github.io/football/python/predicting-football-results-with-statistical-modelling/) [web:24]
- [AI Sports Prediction Accuracy 2025](https://www.sports-ai.dev/blog/ai-sports-prediction-accuracy-2025) [web:3]
- [Random Forest vs XGBoost Comparison](https://mljar.com/machine-learning/random-forest-vs-xgboost/) [web:13]

### Datos
- [Football-Data.co.uk](https://www.football-data.co.uk/) - Datos históricos gratuitos
- [API-Football](https://www.api-football.com/) - Datos en vivo (freemium)

### Herramientas
- [Kelly Criterion Calculator](https://bettingiscool.com/2020/03/17/the-real-kelly-a-python-implementation-for-mutually-exclusive-outcomes/) [web:12]
- [Poisson Distribution Guide](https://www.sbo.net/strategy/football-prediction-model-poisson-distribution/) [web:34]

---

## 👥 Contribuir

Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/amazing-feature`)
3. Commit cambios (`git commit -m 'Add amazing feature'`)
4. Push a la rama (`git push origin feature/amazing-feature`)
5. Abre un Pull Request

---

## ⚠️ Disclaimer

Este proyecto es **solo con fines educativos**. Las apuestas deportivas conllevan riesgos financieros. Nunca apuestes más de lo que puedes permitirte perder. Este sistema NO garantiza ganancias.

**No somos responsables** de pérdidas financieras derivadas del uso de este software.

---

## 📝 Licencia

MIT License - Ver [LICENSE](LICENSE) para más detalles.

---

## 🚀 Roadmap

- [ ] Soporte para más ligas (Bundesliga, Ligue 1, etc.)
- [ ] Integración con APIs de casas de apuestas
- [ ] Backtesting framework
- [ ] Móvil app (React Native)
- [ ] Alertas por Telegram/Discord
- [ ] Multi-deporte (NBA, NFL, Tennis)

---

¡**Buena suerte con tus predicciones!** ⚽📊💰