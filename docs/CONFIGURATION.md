# ⚙️ Guía de Configuración del MVP

## 📝 Resumen

El MVP utiliza **un único archivo de configuración** para simplicidad:

- **`.env`**: Variables de entorno (API keys, parámetros configurables)
- **`config.py`**: Carga `.env` y define valores por defecto

### ❌ Archivos NO Usados

- `src/config.py` - Vacío (no se usa)
- `src/constants.py` - Vacío (no se usa)

Estos archivos están presentes pero vacíos para mantener compatibilidad con versiones futuras.

---

## 📂 Estructura de Configuración

```
.env (tu archivo local, NO se sube a Git)
  ↓
config.py (carga .env y define clase Config)
  ↓
app.py / api_consumer.py / database.py (importan desde config)
```

---

## 📝 Variables de Entorno (.env)

### Crear tu archivo .env

```bash
cp .env.example .env
```

### Variables Disponibles

#### 🌐 API Configuration

```env
# Tu API key de RapidAPI (Betfair Sports Data)
FOOTBALL_API_KEY=tu_rapidapi_key_aqui

# URL base de la API (ya configurada por defecto)
FOOTBALL_API_URL=https://betfair-sports-data-fast-and-reliable.p.rapidapi.com
```

**🔑 Cómo obtener tu API Key:**
1. Ir a [RapidAPI](https://rapidapi.com)
2. Buscar "Betfair Sports Data Fast and Reliable"
3. Suscribirse (hay plan gratuito)
4. Copiar tu X-RapidAPI-Key

#### 📺 Dashboard Settings

```env
# Intervalo de auto-refresh en SEGUNDOS
REFRESH_INTERVAL=900  # 15 minutos

# Título de la página
PAGE_TITLE=Football Betting Predictor - Live

# Icono (emoji)
PAGE_ICON=⚽
```

#### 🎯 Prediction Settings

```env
# Confianza mínima para mostrar predicciones (0.0 - 1.0)
MIN_CONFIDENCE=0.60  # 60%
```

#### 💾 Database Settings

```env
# Ruta a la base de datos SQLite
DB_PATH=data/predictions.db
```

#### 📦 Cache Settings

```env
# Cuántas horas cachear las ligas antes de refrescar desde la API
COMPETITIONS_CACHE_HOURS=24
```

**Beneficio del cache:**
- La primera vez que ejecutas el dashboard, llama a la API para obtener las ligas
- Las guarda en SQLite
- Por 24 horas, las lee desde SQLite (sin gastar cuota de API)
- Después de 24h, refresca automáticamente desde la API

---

## 🐍 Uso en Código

### Importar configuración

```python
from config import config

# Acceder a valores
api_key = config.FOOTBALL_API_KEY
refresh = config.REFRESH_INTERVAL
min_conf = config.MIN_CONFIDENCE
```

### Ejemplo completo

```python
from config import config
from src.data.api_consumer import BetfairAPIConsumer

# Inicializar API con key desde config
api = BetfairAPIConsumer(api_key=config.FOOTBALL_API_KEY)

# Usar intervalo de refresh
import time
while True:
    # Tu lógica aquí
    time.sleep(config.REFRESH_INTERVAL)
```

---

## 📦 Cache de Competiciones

### Cómo funciona

```python
from config import config
from src.data.database import db
from src.data.api_consumer import BetfairAPIConsumer

api = BetfairAPIConsumer(config.FOOTBALL_API_KEY)

# 1. Intentar obtener desde cache
competitions = db.get_cached_competitions(
    max_age_hours=config.COMPETITIONS_CACHE_HOURS
)

if competitions is None:
    # 2. Cache vencido o vacío, llamar a API
    print("🔄 Obteniendo ligas desde API...")
    competitions = api.get_competitions()
    
    # 3. Guardar en cache
    db.save_competitions(competitions)
    print(f"✅ {len(competitions)} ligas guardadas en cache")
else:
    print(f"✅ Usando {len(competitions)} ligas desde cache local")

# 4. Usar competitions
for comp in competitions:
    print(f"{comp['name']} ({comp['region']})")
```

### Limpiar cache manualmente

```python
from src.data.database import db

db.clear_competitions_cache()
print("Cache de competiciones limpiado")
```

---

## 🔧 Configuración por Ambiente

### Desarrollo (Local)

```env
FOOTBALL_API_KEY=tu_key_de_prueba
REFRESH_INTERVAL=300  # 5 min (más frecuente para testing)
MIN_CONFIDENCE=0.50
COMPETITIONS_CACHE_HOURS=1  # Refrescar cada 1h en desarrollo
```

### Producción
```env
FOOTBALL_API_KEY=tu_key_de_produccion
REFRESH_INTERVAL=900  # 15 min
MIN_CONFIDENCE=0.65
COMPETITIONS_CACHE_HOURS=24
```

---

## ⚠️ Constantes NO Configurables

Estas están hardcodeadas en `config.py` porque no necesitan cambiar:

```python
class Config:
    SPORT_ID_SOCCER = "1"  # ID de fútbol en Betfair
    
    # IDs de ligas principales (backup si la API falla)
    DEFAULT_COMPETITION_IDS = [
        "228",       # UEFA Champions League
        "10932509",  # Premier League
        "117",       # La Liga
        "59",        # Bundesliga
        "81",        # Serie A
        "55"         # Ligue 1
    ]
```

Estas **no se deben cambiar** a menos que Betfair cambie sus IDs (muy raro).

---

## 📊 Consumo de API vs Cache

### Sin cache (llamadas cada vez)

```
Ejecución 1: 1 request a getCompetitions
Ejecución 2: 1 request a getCompetitions
Ejecución 3: 1 request a getCompetitions
...

Total en 24h: 96 requests (si refrescas cada 15 min)
```

### Con cache (24 horas)

```
Ejecución 1: 1 request a getCompetitions (guarda en SQLite)
Ejecución 2-96: Lee desde SQLite (0 requests)
Ejecución 97 (24h después): 1 request a getCompetitions

Total en 24h: 1 request 🎉
```

**Ahorro:** 95 requests/día = **~2,850 requests/mes**

---

## 🤔 FAQ

### ¿Por qué existen src/config.py y src/constants.py si están vacíos?

Para mantener compatibilidad con versiones futuras del proyecto. Si en el futuro se agregan módulos ML o FastAPI, podrán usar esos archivos sin romper la estructura.

### ¿Puedo cambiar la ruta del .env?

No es recomendable. `config.py` usa `load_dotenv()` que busca `.env` en la raíz del proyecto por defecto.

### ¿Qué pasa si no configuro FOOTBALL_API_KEY?

El dashboard detecta que no hay key y automáticamente activa el **modo Mock** (datos de prueba).

### ¿Cómo sé qué variables se están usando?

Revisa `config.py` - solo las variables definidas en la clase `Config` se usan.

---

## 📚 Referencias

- [python-dotenv documentation](https://github.com/theskumar/python-dotenv)
- [SQLite3 Python docs](https://docs.python.org/3/library/sqlite3.html)
- [Betfair Sports Data API](https://rapidapi.com/msilvabr18/api/betfair-sports-data-fast-and-reliable)

---

**Última actualización**: Diciembre 2025
