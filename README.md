# ⚽ Football Live Tracker

**Dashboard en tiempo real de partidos de fútbol usando Football API 7**

## 🎯 Características

- 🔴 **Partidos en Vivo**: Seguimiento en tiempo real con marcadores actualizados
- ⏱️ **Minuto a Minuto**: Muestra el minuto exacto del partido
- 🟥 **Tarjetas Rojas**: Visualización de expulsiones por equipo
- 🏆 **Todas las Competiciones**: Premier League, La Liga, Champions League y más
- 📅 **Selección de Fecha**: Ver partidos de cualquier día
- 🔄 **Auto-Refresh**: Actualización automática cada 5 minutos

## 🚀 Inicio Rápido

### 1. Clonar el repositorio

```bash
git clone https://github.com/piranga8/football-betting-predictor-lite.git
cd football-betting-predictor-lite
```

### 2. Crear entorno virtual

```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar API Key

```bash
cp .env.example .env
```

Editar `.env` y agregar tu API key de RapidAPI:

```env
FOOTBALL_API_KEY=tu_rapidapi_key_aqui
```

**🔑 Cómo obtener tu API Key:**

1. Ir a [RapidAPI](https://rapidapi.com)
2. Buscar "Football API 7"
3. Suscribirse (hay plan gratuito)
4. Copiar tu X-RapidAPI-Key

### 5. Ejecutar el dashboard

```bash
streamlit run app.py
```

El dashboard se abrirá automáticamente en `http://localhost:8501`

## 📚 Documentación

- [QUICKSTART.md](QUICKSTART.md) - Guía de inicio en 5 minutos
- [docs/CONFIGURATION.md](docs/CONFIGURATION.md) - Variables de configuración
- [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) - Solución de problemas
- [ARCHITECTURE.md](ARCHITECTURE.md) - Arquitectura del sistema

## 📸 Capturas de Pantalla

### Dashboard Principal
- Métricas generales: Total partidos, en vivo, goles, tarjetas rojas
- Agrupación por competición
- Indicador LIVE parpadeante para partidos en curso
- Marcadores en tiempo real

### Filtros Disponibles
- 📅 Selección de fecha
- 🔍 Solo partidos en vivo
- 🏆 Por competición

## 🛠️ Stack Tecnológico

| Componente | Tecnología |
|------------|------------|
| **Frontend** | Streamlit |
| **API** | Football API 7 (RapidAPI) |
| **Backend** | Python 3.9+ |
| **Base de Datos** | SQLite |
| **Timezone** | pytz |

## 📊 Datos Disponibles

Por cada partido:

- ✅ ID del partido
- ✅ Competición (nombre, logo, país)
- ✅ Equipos (local y visitante)
- ✅ Marcador actual
- ✅ Minuto del partido
- ✅ Status (En vivo, Programado, Finalizado)
- ✅ Tarjetas rojas por equipo
- ✅ Jornada/Round
- ✅ Disponibilidad de video
- ✅ Hora de inicio

## ⚙️ Configuración

### Variables de Entorno (.env)

```env
# API
FOOTBALL_API_KEY=tu_key_aqui

# Dashboard
REFRESH_INTERVAL=300  # segundos
PAGE_TITLE=Football Live Tracker
PAGE_ICON=⚽

# Timezone
DEFAULT_TIMEZONE=america/santiago
DEFAULT_LANG=en
```

## 🔄 Actualización Automática

El dashboard se actualiza automáticamente cada 5 minutos (configurable). Esto significa:

- ✅ Marcadores actualizados
- ✅ Nuevos partidos en vivo
- ✅ Tarjetas rojas en tiempo real
- ✅ Minuto actual del partido

## 🐛 Solución de Problemas

### Error: "API Key no configurada"

```bash
# Verificar que existe .env
cat .env

# Debe contener:
FOOTBALL_API_KEY=tu_key_aqui
```

### Error 403: "You are not subscribed"

1. Verifica que estés suscrito a **Football API 7** en RapidAPI
2. Confirma que tu API key es correcta
3. Revisa que no hayas excedido tu cuota

### No se muestran partidos

- Verifica la fecha seleccionada
- Puede que no haya partidos en vivo en ese momento
- Desactiva el filtro "Solo partidos en vivo" para ver todos los partidos del día

Ver [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) para más ayuda.

## 📁 Estructura del Proyecto

```
football-betting-predictor-lite/
├── app.py                      # Dashboard principal
├── config.py                   # Configuración
├── requirements.txt            # Dependencias
├── .env.example                # Template de variables
├── README.md                   # Este archivo
├── QUICKSTART.md               # Guía rápida
├── ARCHITECTURE.md             # Arquitectura
│
├── src/
│   ├── data/
│   │   ├── api_consumer.py    # Cliente Football API 7
│   │   └── database.py        # Gestión SQLite
│   └── models/
│       └── inplay_predictor.py # Predictor Poisson
│
├── docs/
│   ├── CONFIGURATION.md       # Guía de configuración
│   └── TROUBLESHOOTING.md     # Solución de problemas
│
└── data/
    ├── .gitkeep
    └── predictions.db         # Base de datos SQLite
```

## 🚀 Roadmap

### Versión Actual (v1.0)
- ✅ Integración con Football API 7
- ✅ Dashboard de partidos en vivo
- ✅ Métricas en tiempo real
- ✅ Filtros por fecha y estado

### Próximas Versiones
- ⏳ Predicciones en vivo con modelo Poisson
- ⏳ Historial de partidos
- ⏳ Estadísticas por equipo
- ⏳ Notificaciones de eventos (goles, tarjetas)
- ⏳ Gráficos de probabilidades
- ⏳ Comparación de equipos

## 👥 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📝 Licencia

MIT License - ver [LICENSE](LICENSE) para más detalles.

## 🔗 Enlaces Útiles

- [Football API 7 Documentation](https://rapidapi.com/codechno/api/football-api-7)
- [Streamlit Documentation](https://docs.streamlit.io)
- [RapidAPI](https://rapidapi.com)

## ℹ️ Notas

- La API tiene límites de requests según tu plan de RapidAPI
- El plan gratuito incluye 100 requests/día
- Cada actualización del dashboard consume 1 request
- Configurar `REFRESH_INTERVAL` apropiadamente para no exceder la cuota

---

**Hecho con ❤️ por [Ignacio Miranda](https://github.com/piranga8)**
