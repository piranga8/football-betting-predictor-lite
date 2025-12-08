# 🚀 Guía Rápida - MVP

## Inicio Rápido (5 minutos)

### Opción 1: Ejecutar con Scripts Automáticos

**Windows:**
```cmd
run_mvp.bat
```

**Linux/Mac:**
```bash
chmod +x run_mvp.sh
./run_mvp.sh
```

El script hará automáticamente:
1. ✅ Crear entorno virtual
2. ✅ Instalar dependencias
3. ✅ Crear archivo .env
4. ✅ Iniciar dashboard

### Opción 2: Manual

```bash
# 1. Crear entorno virtual
python -m venv venv

# 2. Activar
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Actualizar herramientas
python -m pip install --upgrade pip setuptools wheel

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Configurar .env
cp .env.example .env
# Editar .env con tu API key

# 6. Ejecutar
streamlit run app.py
```

---

## 🎯 Modo Testing (Sin API Key)

1. Ejecutar el dashboard
2. En el **sidebar**, activar: ✅ **"Usar datos de prueba (Mock)"**
3. Listo! Verás partidos de ejemplo

Esto te permite probar el sistema sin gastar cuota de API.

---

## 🔑 Obtener API Key (RapidAPI)

1. Ir a [RapidAPI](https://rapidapi.com)
2. Registrarse / Iniciar sesión
3. Buscar: **"Betfair Sports Data Fast and Reliable"**
4. Suscribirse al plan (hay plan gratuito)
5. Copiar tu **X-RapidAPI-Key**
6. Pegar en `.env`:

```env
FOOTBALL_API_KEY=tu_key_aqui
```

---

## 📺 Cómo Usar el Dashboard

### Sidebar (Configuración)

1. **Modo Mock**: Testing sin API
2. **Ligas**: Seleccionar qué ligas monitorear
   - Champions League
   - Premier League
   - La Liga
   - Bundesliga
   - Serie A
   - Ligue 1
3. **Confianza Mínima**: Filtrar predicciones (0.0 a 1.0)

### Vista Principal

**Métricas Generales:**
- 📡 Partidos en Vivo
- 🟢 Alta Confianza (verde)
- 🟡 Media Confianza (amarillo)
- 🔴 Baja Confianza (rojo)

**Por Cada Partido:**
- **Equipos y Marcador**
- **Minuto actual**
- **Semáforo de confianza**
- **Probabilidades Pre-Match** (desde API externa)
- **Probabilidades In-Play** (calculadas por nuestro modelo)
- **Cambios** (diferencias entre pre-match e in-play)
- **Gráfico comparativo**

---

## 💡 Tips

### ¿Cómo Interpretar el Semáforo?

- **🟢 Verde**: Alta confianza (>75%) + resultado claro
  - ✅ Buena señal para considerar apuesta
- **🟡 Amarillo**: Confianza media (55-75%)
  - ⚠️ Evaluar con cuidado
- **🔴 Rojo**: Baja confianza (<55%)
  - ❌ Evitar apostar

### ¿Qué Son las Probabilidades?

**Pre-Match (Externas):**
- Calculadas desde las **cuotas de Betfair** antes del partido
- Representan el consenso del mercado

**In-Play (Nuestro Modelo):**
- Actualizadas durante el partido usando:
  - Marcador actual
  - Minuto del partido
  - Modelo Poisson ajustado
- Reflejan cómo el marcador cambia las probabilidades

### Ejemplo Práctico

**Pre-Match:**
- Casa: 55%
- Empate: 28%
- Visita: 17%

**Marcador en minuto 30: 1-0 (casa gana)**

**In-Play actualizado:**
- Casa: 72% (↑ +17%)
- Empate: 18% (↓ -10%)
- Visita: 10% (↓ -7%)

➡️ El marcador favorable aumenta las probabilidades del local.

---

## ⚙️ Configuración Avanzada

### Cambiar Intervalo de Actualización

En `.env`:
```env
REFRESH_INTERVAL=600  # 10 minutos
```

### Filtro de Confianza Global

En `.env`:
```env
MIN_CONFIDENCE=0.70  # Solo >70%
```

---

## ❓ Preguntas Frecuentes

### ¿Puedo usar sin API key?

Sí, activa el **modo Mock** en el sidebar. Verás datos de ejemplo.

### ¿Cuánto cuesta la API?

[Betfair Sports Data API](https://rapidapi.com/msilvabr18/api/betfair-sports-data-fast-and-reliable) tiene:
- Plan **gratuito**: 100 requests/mes
- Plan **básico**: $10/mes (1000 requests)

### ¿Cuántas requests consume el MVP?

Por cada actualización (cada 15 min):
- 1 request por liga (getEvents)
- 1 request por partido (getMarketsList)
- 1 request por mercado (GetMarketOdds)

**Ejemplo:** 2 ligas con 5 partidos cada una:
- 2 + (10 × 2) = **22 requests cada 15 min**
- En 1 hora: 88 requests

➡️ **Recomendación**: Seleccionar 1-2 ligas principales para no exceder cuota.

### ¿Cómo actualizo el sistema?

```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

---

## 🐛 Problemas Comunes

### Error: "ModuleNotFoundError"

```bash
pip install -r requirements.txt
```

### Error: "API Key no configurada"

1. Verificar `.env` existe
2. Verificar `FOOTBALL_API_KEY` tiene valor
3. Reiniciar dashboard

### Dashboard se congela

Presiona `Ctrl + C` en la terminal y reinicia:
```bash
streamlit run app.py
```

---

## 📞 Soporte

- **Issues**: [GitHub Issues](https://github.com/piranga8/football-betting-predictor-lite/issues)
- **Documentación completa**: Ver [README.md](README.md)

---

¡**Listo para empezar!** 🎉
