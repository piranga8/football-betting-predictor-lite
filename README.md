# ⚽ Football Betting Predictor - MVP

Dashboard de predicción de apuestas deportivas que combina datos externos con análisis en vivo usando modelos estadísticos.

## 🎯 Características del MVP

- **📈 Predicciones Pre-Match**: Consume probabilidades desde API de Betfair
- **⏱️ Predicciones In-Play**: Actualiza probabilidades durante el partido usando modelo Poisson
- **🚦 Sistema de Semáforo**: Verde (alta confianza) / Amarillo (media) / Rojo (baja)
- **🔄 Auto-Refresh**: Actualización automática cada 15 minutos
- **💾 SQLite**: Base de datos local, sin servidores externos
- **👀 Dashboard Interactivo**: Streamlit con visualizaciones en tiempo real

---

## 🛠️ Instalación Rápida

### Requisitos

- Python 3.9+
- pip
- Cuenta en [RapidAPI](https://rapidapi.com) (opcional para testing)

### Opción 1: Scripts Automáticos 🚀

**Windows:**
```cmd
run_mvp.bat
```

**Linux/Mac:**
```bash
chmod +x run_mvp.sh
./run_mvp.sh
```

### Opción 2: Instalación Manual

```bash
# 1. Clonar repositorio
git clone https://github.com/piranga8/football-betting-predictor-lite.git
cd football-betting-predictor-lite

# 2. Crear entorno virtual
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# 3. Actualizar herramientas base
python -m pip install --upgrade pip setuptools wheel

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Configurar variables de entorno
cp .env.example .env
# Editar .env con tu API key (o usar modo Mock para testing)

# 6. Ejecutar dashboard
streamlit run app.py
```

El dashboard abrirá automáticamente en `http://localhost:8501` 🎉

---

## 🔑 Configuración de API

### Obtener API Key de Betfair (RapidAPI)

1. Crear cuenta en [RapidAPI](https://rapidapi.com)
2. Buscar: **"Betfair Sports Data Fast and Reliable"**
3. Suscribirse al plan:
   - **Gratuito**: 100 requests/mes
   - **Básico**: $10/mes (1,000 requests)
4. Copiar tu **X-RapidAPI-Key**
5. Agregar en `.env`:

```env
FOOTBALL_API_KEY=tu_rapidapi_key_aqui
FOOTBALL_API_URL=https://betfair-sports-data-fast-and-reliable.p.rapidapi.com
REFRESH_INTERVAL=900
MIN_CONFIDENCE=0.60
```

### Modo Testing (Sin API Key)

1. Ejecutar: `streamlit run app.py`
2. En el **sidebar**, activar: ✅ **"Usar datos de prueba (Mock)"**
3. Ver partidos de ejemplo sin consumir API

---

## 🏛️ Arquitectura del MVP

```
football-betting-predictor-lite/
├── app.py                      # Dashboard Streamlit principal
├── config.py                   # Configuración global
├── requirements.txt            # Dependencias Python
├── .env.example                # Template de variables
├── .gitignore                  # Archivos ignorados por Git
├── run_mvp.sh                  # Script de inicio Linux/Mac
├── run_mvp.bat                 # Script de inicio Windows
├── README.md                   # Este archivo
├── QUICKSTART.md               # Guía rápida de 5 minutos
│
├── src/
│   ├── data/
│   │   ├── api_consumer.py     # Consumo de API Betfair
│   │   └── database.py         # Gestión SQLite local
│   │
│   └── models/
│       └── inplay_predictor.py # Predicción en vivo con Poisson
│
└── data/
    └── predictions.db          # Base de datos SQLite (se crea automáticamente)
```

---

## 📊 Cómo Funciona

### 1. Consumo de API Betfair

El sistema hace llamadas secuenciales:

```
getCompetitions (Sport ID: 1 = Fútbol)
    ↓
getEvents (Competition ID: ej. 228 = Champions League)
    ↓
geMarketsList (Event ID)
    ↓
GetMarketOdds (Market ID)
```

### 2. Cálculo de Probabilidades Pre-Match

Desde las **odds de Betfair**, se calculan probabilidades implícitas:

```python
Probabilidad = 1 / Odds
```

**Ejemplo:**
- Odds Casa: 1.82 → Prob = 54.9%
- Odds Empate: 3.48 → Prob = 28.7%
- Odds Visita: 6.06 → Prob = 16.5%

Se normalizan para que sumen 100%.

### 3. Predicción In-Play con Poisson

Durante el partido:

1. **Estimar lambdas** (λ = goles esperados) desde probabilidades pre-match
2. **Ajustar lambdas** según:
   - Marcador actual (equipo ganando → defiende más)
   - Minuto del partido (time decay)
3. **Calcular nuevas probabilidades** usando distribución de Poisson:

```
P(k goles) = (λ^k × e^-λ) / k!
```

4. **Generar matriz de resultados posibles** y sumar probabilidades por outcome (1/X/2)

### 4. Sistema de Semáforo

Cada predicción recibe un color:

| Color | Confianza | Claridad | Significado |
|-------|-----------|----------|-------------|
| 🟢 **Verde** | >75% | Alta | Resultado claro, alta confianza |
| 🟡 **Amarillo** | 55-75% | Media | Evaluar con cuidado |
| 🔴 **Rojo** | <55% | Baja | Evitar apostar |

---

## 💻 Uso del Dashboard

### Sidebar (Configuración)

- **⚙️ Modo Mock**: Testing sin API real
- **🏆 Ligas**: Seleccionar qué competiciones monitorear
  - Champions League
  - Premier League
  - La Liga
  - Bundesliga
  - Serie A
  - Ligue 1
- **🎯 Confianza Mínima**: Filtrar predicciones (0.0 - 1.0)

### Vista Principal

**Métricas Generales:**
- 📡 Total de partidos en vivo
- 🟢 Partidos con alta confianza
- 🟡 Partidos con confianza media
- 🔴 Partidos con baja confianza

**Por Cada Partido:**
- Equipos y marcador actual
- Minuto del partido
- Semáforo de confianza
- **Probabilidades Pre-Match** (desde Betfair)
- **Probabilidades In-Play** (modelo propio)
- **Cambios** (diferencias entre ambas)
- **Gráfico comparativo** interactivo

---

## 📚 Ejemplo de Código

### Uso Directo de Módulos

```python
from src.data.api_consumer import BetfairAPIConsumer
from src.models.inplay_predictor import predictor

# Inicializar API
api = BetfairAPIConsumer(api_key="tu_key")

# Obtener ligas
competitions = api.get_competitions()
print(f"Ligas disponibles: {len(competitions)}")

# Obtener partidos de Champions League
events = api.get_events(competition_id="228")

# Predicción pre-match
event_id = events[0]['event_id']
prematch = api.get_match_predictions(event_id)

print(f"Pre-Match:")
print(f"  Casa: {prematch['prob_home']:.1%}")
print(f"  Empate: {prematch['prob_draw']:.1%}")
print(f"  Visita: {prematch['prob_away']:.1%}")

# Predicción in-play (simular minuto 45, marcador 1-0)
inplay = predictor.predict(
    prematch_pred=prematch,
    current_minute=45,
    home_score=1,
    away_score=0
)

print(f"\nIn-Play (45', 1-0):")
print(f"  Casa: {inplay['prob_home']:.1%} (cambio: {inplay['prob_home'] - prematch['prob_home']:+.1%})")
print(f"  Empate: {inplay['prob_draw']:.1%}")
print(f"  Visita: {inplay['prob_away']:.1%}")
print(f"  Confianza: {inplay['confidence']:.1%}")
print(f"  Semáforo: {inplay['signal_color']}")
```

---

## ⚙️ Configuración Avanzada

### Cambiar Intervalo de Actualización

En `.env`:
```env
REFRESH_INTERVAL=600  # 10 minutos (en segundos)
```

### Filtro de Confianza Global

En `.env`:
```env
MIN_CONFIDENCE=0.70  # Solo mostrar >70%
```

### Consumo de API

Por cada actualización (cada 15 min) con 2 ligas y 5 partidos cada una:

```
2 ligas × 1 request (getEvents) = 2 requests
10 partidos × 1 request (getMarketsList) = 10 requests
10 partidos × 1 request (GetMarketOdds) = 10 requests

Total: ~22 requests cada 15 min
```

**En 1 hora**: 88 requests  
**Plan gratuito (100/mes)**: Usar con 1 liga y refrescar cada 30 min

---

## 🐛 Troubleshooting

### Error: "API Key no configurada"

```bash
# Verificar que existe .env
ls -la .env

# Verificar contenido
cat .env | grep FOOTBALL_API_KEY

# Si no existe, crear desde ejemplo
cp .env.example .env
```

### Error: "Rate limit alcanzado"

El sistema espera automáticamente 60 segundos y reintenta.  
Considerar:
- Aumentar `REFRESH_INTERVAL` en `.env`
- Reducir número de ligas monitoreadas
- Actualizar plan en RapidAPI

### Error al instalar dependencias (Windows)

```powershell
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

Si persiste, instalar [Microsoft Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/).

### Dashboard no responde

Presionar `Ctrl + C` en la terminal y reiniciar:
```bash
streamlit run app.py
```

---

## 🚀 Roadmap (Futuras Versiones)

- [ ] API REST con FastAPI
- [ ] Modelos ML avanzados (XGBoost, LightGBM)
- [ ] Detección de value bets
- [ ] Kelly Criterion para cálculo de stakes
- [ ] Backtesting framework
- [ ] Alertas por Telegram/Discord
- [ ] Soporte multi-deporte (NBA, NFL, Tennis)
- [ ] Móvil app (React Native)

---

## ❓ FAQ

**¿Puedo usar sin API key?**  
Sí, activa el modo Mock en el sidebar del dashboard.

**¿Qué tan preciso es el modelo?**  
El modelo Poisson básico tiene ~50-55% de precisión. Versiones futuras incluirán modelos más avanzados.

**¿Cómo actualizo el sistema?**
```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

**¿Cuánto espacio ocupa la base de datos SQLite?**  
Aproximadamente 1-5 MB para varios días de datos.

---

## ⚠️ Disclaimer

Este proyecto es **únicamente con fines educativos**. Las apuestas deportivas conllevan riesgos financieros significativos.

- **Nunca apuestes** más de lo que puedes permitirte perder
- Este sistema **NO garantiza ganancias**
- **No somos responsables** de pérdidas financieras
- Consulta las leyes locales sobre apuestas en línea

---

## 📝 Licencia

MIT License - Ver [LICENSE](LICENSE) para detalles.

---

## 👍 Contribuir

¡Las contribuciones son bienvenidas!

1. Fork el proyecto
2. Crear rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abrir Pull Request

---

## 📞 Soporte

- **Issues**: [GitHub Issues](https://github.com/piranga8/football-betting-predictor-lite/issues)
- **Guía rápida**: Ver [QUICKSTART.md](QUICKSTART.md)

---

**¡Buena suerte con tus predicciones!** ⚽📊👍
