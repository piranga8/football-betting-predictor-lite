# ⚽ Football Live Tracker + Predictions

**Dashboard en tiempo real de partidos de fútbol con predicciones automáticas**

## 🎯 Características

### 📊 Datos en Tiempo Real
- 🔴 **Partidos en Vivo**: Seguimiento en tiempo real con marcadores actualizados
- ⏱️ **Minuto a Minuto**: Muestra el minuto exacto del partido
- 🟥 **Tarjetas Rojas**: Visualización de expulsiones por equipo
- 🏆 **Todas las Competiciones**: Premier League, La Liga, Champions League y más

### 🎯 Predicciones Inteligentes
- 💡 **Predicciones Pre-Match**: Scraping automático desde PrimaTips
- 💰 **Cuotas (Odds)**: Visualización de odds para 1, X, 2
- 📊 **Probabilidades**: Cálculo de probabilidades implícitas
- 🤝 **Matching Inteligente**: Emparejamiento automático de partidos
- 📈 **Barra Visual**: Representación gráfica de probabilidades

### ⚙️ Funcionalidades
- 📅 **Selección de Fecha**: Ver partidos de cualquier día
- 🔍 **Filtros**: Solo en vivo, con/sin predicciones
- 🔄 **Auto-Refresh**: Actualización automática cada 5 minutos
- 💥 **Dos Fuentes**: Football API 7 + PrimaTips

## 🚀 Inicio Rápido

### 1. Clonar el repositorio

```bash
git clone https://github.com/piranga8/football-betting-predictor-lite.git
cd football-betting-predictor-lite
```

### 2. Crear entorno virtual e instalar

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configurar API Key

```bash
cp .env.example .env
# Editar .env con tu API key de RapidAPI
```

### 4. Ejecutar

```bash
streamlit run app.py
```

Ver [QUICKSTART.md](QUICKSTART.md) para guía detallada.

## 🛠️ Stack Tecnológico

| Componente | Tecnología |
|------------|------------|
| **Frontend** | Streamlit |
| **API Partidos** | Football API 7 (RapidAPI) |
| **Predicciones** | PrimaTips (Web Scraping) |
| **Scraping** | BeautifulSoup4 |
| **Backend** | Python 3.9+ |
| **Base de Datos** | SQLite |
| **Matching** | difflib |

## 📊 Fuentes de Datos

### Football API 7 - Partidos en Vivo
- Marcadores en tiempo real
- Minuto del partido
- Tarjetas rojas
- Estado (Live/Scheduled/Finished)

### PrimaTips - Predicciones
- Predicción favorita (1, X, 2)
- Cuotas (odds)
- Probabilidades implícitas
- Link al análisis completo

**Matching:** El sistema empareja automáticamente partidos entre ambas fuentes con 60-80% de tasa de éxito.

## 📚 Documentación

- [QUICKSTART.md](QUICKSTART.md) - Inicio en 5 minutos
- [docs/PREDICTIONS.md](docs/PREDICTIONS.md) - 🎯 Guía de predicciones
- [docs/CONFIGURATION.md](docs/CONFIGURATION.md) - Variables de configuración
- [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) - Solución de problemas
- [ARCHITECTURE.md](ARCHITECTURE.md) - Arquitectura del sistema

## 🚀 Roadmap

### v1.1 (Actual)
- ✅ Integración Football API 7
- ✅ Scraping de predicciones PrimaTips
- ✅ Matching automático
- ✅ Visualización de odds y probabilidades

### v2.0 (Futuro)
- ⏳ Predicciones Poisson propias
- ⏳ Predicciones in-play dinámicas
- ⏳ Gráficos de probabilidades
- ⏳ Notificaciones de eventos

## ⚠️ Disclaimer

Este proyecto es **solo para fines educativos e informativos**. Las predicciones NO son consejos de apuestas. Apostar conlleva riesgos.

## 🔗 Enlaces

- [Football API 7](https://rapidapi.com/codechno/api/football-api-7)
- [Streamlit Docs](https://docs.streamlit.io)
- [BeautifulSoup Docs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

---

**Hecho con ❤️ por [Ignacio Miranda](https://github.com/piranga8)**
