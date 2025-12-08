# 🏛️ Arquitectura del MVP

## Estructura Simplificada

Este MVP utiliza **únicamente** las tecnologías esenciales:

- **Frontend**: Streamlit (dashboard web interactivo)
- **Backend Logic**: Python puro
- **Base de Datos**: SQLite (local, sin servidor)
- **API Externa**: Betfair via RapidAPI
- **Modelo Estadístico**: Distribución de Poisson

## 📋 NO Incluido en el MVP

Las siguientes tecnologías **NO están** en esta versión:

- ❌ Docker / Docker Compose
- ❌ PostgreSQL
- ❌ Redis
- ❌ FastAPI / API REST
- ❌ Computer Vision
- ❌ Modelos ML avanzados (XGBoost, LightGBM, etc.)
- ❌ WebSockets
- ❌ Celery / Task queues

Estas pueden agregarse en versiones futuras (ver Roadmap en README.md).

---

## 🗂️ Estructura de Archivos

```
football-betting-predictor-lite/
├── 📄 app.py                      # Punto de entrada - Dashboard Streamlit
├── 📄 config.py                   # Configuración global (env vars)
├── 📄 requirements.txt            # Dependencias Python
├── 📄 .env.example                # Template de variables de entorno
├── 📄 .gitignore                  # Git ignore rules
├── 📍c README.md                   # Documentación principal
├── 📍c QUICKSTART.md               # Guía rápida
├── 📍c ARCHITECTURE.md            # Este archivo
├── 📜 run_mvp.sh                  # Script inicio Linux/Mac
├── 📜 run_mvp.bat                 # Script inicio Windows
│
├── 📁 src/
│   ├── 📁 data/
│   │   ├── 🐍 api_consumer.py     # API Betfair (RapidAPI)
│   │   └── 🐍 database.py         # SQLite manager
│   │
│   └── 📁 models/
│       └── 🐍 inplay_predictor.py # Predictor con Poisson
│
└── 📁 data/
    └── 💾 predictions.db          # Base de datos SQLite (auto-creado)
```

---

## 🔄 Flujo de Datos

### 1. Usuario abre Dashboard

```
Usuario ejecuta: streamlit run app.py
         ↓
    app.py carga
         ↓
   Lee config.py
         ↓
Inicializa API consumer
```

### 2. Obtención de Datos

```
api_consumer.py
      ↓
[GET] getCompetitions (ligas disponibles)
      ↓
[GET] getEvents (partidos de cada liga)
      ↓
[GET] geMarketsList (tipos de apuesta)
      ↓
[GET] GetMarketOdds (cuotas actuales)
      ↓
Calcula probabilidades desde odds
      ↓
Retorna predicción pre-match
```

### 3. Predicción In-Play

```
app.py recibe datos del partido:
  - Minuto actual
  - Marcador
  - Predicción pre-match
         ↓
inplay_predictor.py
         ↓
Estima lambdas (λ) desde probs pre-match
         ↓
Ajusta λ según:
  - Diferencia de goles
  - Tiempo transcurrido
         ↓
Calcula nueva matriz de Poisson
         ↓
Genera probabilidades 1X2 actualizadas
         ↓
Calcula confianza y semáforo
         ↓
Retorna predicción in-play
```

### 4. Almacenamiento (Opcional)

```
app.py (opcional)
      ↓
database.py
      ↓
Guarda en SQLite:
  - live_matches
  - prematch_predictions
  - inplay_predictions
      ↓
data/predictions.db
```

### 5. Visualización

```
app.py procesa resultados
         ↓
Genera componentes Streamlit:
  - Métricas generales
  - Tarjetas de partidos
  - Tablas comparativas
  - Gráficos Plotly
         ↓
Muestra en navegador (localhost:8501)
         ↓
Auto-refresh cada 15 min
```

---

## 🧠 Lógica de Negocio

### Cálculo de Probabilidades Pre-Match

**Input**: Odds de Betfair

```python
# Ejemplo:
odds = {
    'home': 1.82,  # Local
    'draw': 3.48,  # Empate
    'away': 6.06   # Visitante
}

# Convertir a probabilidades implícitas
prob_home = 1 / 1.82 = 0.549 (54.9%)
prob_draw = 1 / 3.48 = 0.287 (28.7%)
prob_away = 1 / 6.06 = 0.165 (16.5%)

# Total = 1.001 (ligeramente >1 por el overround)
# Normalizar para que sume 1.0
total = 1.001
prob_home = 0.549 / 1.001 = 0.548
prob_draw = 0.287 / 1.001 = 0.287
prob_away = 0.165 / 1.001 = 0.165
```

### Predicción In-Play con Poisson

**Input**: 
- Probabilidades pre-match
- Minuto actual (ej: 45)
- Marcador (ej: 1-0)

**Proceso**:

1. **Estimar lambdas base** (λ = goles esperados por equipo):

```python
# Heurística simple:
base_lambda = 1.4  # Promedio fútbol

home_factor = (prob_home - prob_away) + 1.0
away_factor = (prob_away - prob_home) + 1.0

lambda_home = 1.4 * home_factor  # ej: 1.82
lambda_away = 1.4 * away_factor  # ej: 0.98
```

2. **Ajustar por marcador y estrategia**:

```python
# Si local va ganando 1-0:
# Local tiende a defender → lambda baja un poco
lambda_home_adj = lambda_home * 0.95

# Visitante necesita atacar → lambda sube
lambda_away_adj = lambda_away * 1.15
```

3. **Calcular matriz de Poisson** para goles restantes:

```python
from scipy.stats import poisson

time_remaining = 90 - minute  # 45 min
lambda_home_remaining = lambda_home_adj * (45/90)  # Escalar
lambda_away_remaining = lambda_away_adj * (45/90)

# Matriz de probabilidades
for i in range(0, 10):  # Goles adicionales local
    for j in range(0, 10):  # Goles adicionales visitante
        prob = poisson.pmf(i, lambda_home_remaining) * \
               poisson.pmf(j, lambda_away_remaining)
        
        final_home = 1 + i  # Ya iban 1-0
        final_away = 0 + j
        
        if final_home > final_away:
            prob_home_win += prob
        elif final_home == final_away:
            prob_draw += prob
        else:
            prob_away_win += prob
```

4. **Normalizar** y devolver predicción actualizada.

### Sistema de Semáforo

```python
def get_signal_color(confidence, probs):
    max_prob = max(prob_home, prob_draw, prob_away)
    clarity = max_prob - 0.333  # ¿Qué tan claro es el favorito?
    
    if confidence >= 0.75 and clarity >= 0.30:
        return 'green'  # 🟢 Alta confianza + resultado claro
    elif confidence >= 0.55 and clarity >= 0.15:
        return 'yellow'  # 🟡 Confianza media
    else:
        return 'red'  # 🔴 Baja confianza / muy incierto
```

---

## 💾 Base de Datos SQLite

### Esquema

#### Tabla: `live_matches`

```sql
CREATE TABLE live_matches (
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
);
```

#### Tabla: `prematch_predictions`

```sql
CREATE TABLE prematch_predictions (
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
);
```

#### Tabla: `inplay_predictions`

```sql
CREATE TABLE inplay_predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id TEXT NOT NULL,
    minute INTEGER NOT NULL,
    prob_home REAL,
    prob_draw REAL,
    prob_away REAL,
    confidence REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (match_id) REFERENCES live_matches(match_id)
);
```

### Uso

```python
from src.data.database import db

# Guardar partido
db.save_live_match({
    'match_id': '12345',
    'home_team': 'Barcelona',
    'away_team': 'Real Madrid',
    'league': 'La Liga',
    'status': 'LIVE',
    'current_minute': 45,
    'home_score': 1,
    'away_score': 0
})

# Guardar predicción
db.save_inplay_prediction('12345', 45, {
    'prob_home': 0.72,
    'prob_draw': 0.18,
    'prob_away': 0.10,
    'confidence': 0.85
})

# Obtener partidos en vivo
live = db.get_live_matches()

# Limpiar antiguos (>24h)
db.cleanup_old_matches(hours=24)
```

---

## ⚙️ Variables de Entorno

### Archivo `.env`

```env
# API Configuration
FOOTBALL_API_KEY=tu_rapidapi_key_aqui
FOOTBALL_API_URL=https://betfair-sports-data-fast-and-reliable.p.rapidapi.com

# Dashboard Configuration
REFRESH_INTERVAL=900          # Segundos (15 minutos)
MIN_CONFIDENCE=0.60           # Filtro mínimo confianza

# Page Configuration
PAGE_TITLE=Football Predictor
PAGE_ICON=⚽
```

### Uso en Código

```python
# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    FOOTBALL_API_KEY = os.getenv('FOOTBALL_API_KEY', '')
    FOOTBALL_API_URL = os.getenv('FOOTBALL_API_URL', '')
    REFRESH_INTERVAL = int(os.getenv('REFRESH_INTERVAL', 900))
    MIN_CONFIDENCE = float(os.getenv('MIN_CONFIDENCE', 0.60))
    PAGE_TITLE = os.getenv('PAGE_TITLE', 'Football Predictor')
    PAGE_ICON = os.getenv('PAGE_ICON', '⚽')

config = Config()
```

---

## 📊 Rendimiento y Limitaciones

### Precisión Esperada

| Métrica | Valor |
|---------|-------|
| **Accuracy** | 50-55% |
| **Baseline** (siempre favorito) | ~45% |
| **Mejora vs baseline** | +5-10% |

⚠️ El modelo Poisson básico es un **punto de partida**. Versiones futuras incluirán modelos más sofisticados.

### Latencia

- **API call**: 200-500ms por request
- **Cálculo Poisson**: <10ms
- **Render Streamlit**: 100-300ms
- **Total por partido**: ~1s

### Escalabilidad

**Límites del MVP:**
- Máximo **50 partidos simultáneos** (limitación de Streamlit)
- Refresh cada **15 minutos** (para no exceder cuota de API)
- SQLite soporta hasta **~10GB** (suficiente para años de datos)

---

## 🔐 Seguridad

### API Key

- **Nunca commitear** `.env` a Git (incluido en `.gitignore`)
- Rotar API key periódicamente
- Usar variables de entorno en producción

### Base de Datos

- SQLite no requiere credenciales
- Archivo local: `data/predictions.db`
- Backup recomendado si se usa en producción

---

## 🚀 Evolución Futura

### Fase 2: API REST

```
MVP (actual)         Fase 2
--------------  →    -------------
Streamlit           FastAPI
    ↓                   ↓
SQLite              PostgreSQL
                        ↓
                   Streamlit (consume API)
```

### Fase 3: ML Avanzado

```
Poisson (actual)     Fase 3
--------------  →    -------------
Modelo simple       XGBoost + Features complejas
                    + Backtesting
                    + Ensemble models
```

### Fase 4: Producción
```
Local (actual)       Fase 4
--------------  →    -------------
Python script       Docker + K8s
SQLite              PostgreSQL + Redis
No CI/CD            GitHub Actions
                    + Monitoring (Grafana)
```

---

**Para más detalles**, ver:
- [README.md](README.md) - Documentación general
- [QUICKSTART.md](QUICKSTART.md) - Guía rápida
