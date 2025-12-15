# 🚀 Guía de Inicio Rápido - 5 Minutos

## 🎯 Objetivo

Tener el **Football Live Tracker** funcionando en tu máquina en menos de 5 minutos.

---

## ✅ Requisitos

- Python 3.9 o superior
- Cuenta en [RapidAPI](https://rapidapi.com) (gratis)
- 5 minutos de tu tiempo

---

## 👣 Pasos

### 1️⃣ Clonar el Repositorio (30 segundos)

```bash
git clone https://github.com/piranga8/football-betting-predictor-lite.git
cd football-betting-predictor-lite
```

### 2️⃣ Crear Entorno Virtual (1 minuto)

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Instalar Dependencias (2 minutos)

```bash
pip install -r requirements.txt
```

### 4️⃣ Configurar API Key (1 minuto)

**Obtener la API Key:**

1. Ir a [Football API 7 en RapidAPI](https://rapidapi.com/codechno/api/football-api-7)
2. Click en **Subscribe to Test**
3. Elegir el plan **Basic (Free)** - 100 requests/día gratis
4. Copiar tu **X-RapidAPI-Key**

**Configurar el archivo .env:**

```bash
cp .env.example .env
```

Editar `.env` con tu editor favorito:

```env
FOOTBALL_API_KEY=pega_tu_key_aqui
```

### 5️⃣ Ejecutar el Dashboard (30 segundos)

```bash
streamlit run app.py
```

🎉 **¡Listo!** El dashboard se abrirá automáticamente en `http://localhost:8501`

---

## 👀 Qué Verás

### Dashboard Principal

```
⚽ Football Live Tracker
___________________________________________

📊 Total Partidos: 15
🔴 En Vivo: 3
⚽ Goles: 12
🟥 Tarjetas Rojas: 1

🏆 Premier League
  🔴 LIVE   Manchester United  2 - 1  Bournemouth  ⏱️ 67'
  Sched.    Arsenal vs Chelsea               20:00

🏆 La Liga
  🔴 LIVE   Barcelona  2 - 2  Real Madrid  ⏱️ 82'
  🟥 Real Madrid: 1
```

### Sidebar (Izquierda)

- **📅 Fecha**: Selector de fecha
- **🔍 Filtros**: 
  - ☑️ Solo partidos en vivo

---

## ⚙️ Configuración Opcional

### Cambiar Intervalo de Actualización

En `.env`:

```env
REFRESH_INTERVAL=300  # 5 minutos (default)
REFRESH_INTERVAL=600  # 10 minutos (ahorra requests)
REFRESH_INTERVAL=180  # 3 minutos (más frecuente)
```

### Cambiar Zona Horaria

```env
DEFAULT_TIMEZONE=america/santiago  # Chile
DEFAULT_TIMEZONE=america/mexico_city  # México
DEFAULT_TIMEZONE=europe/madrid  # España
```

---

## 🐛 ¿Problemas?

### Error: "API Key no configurada"

```bash
# Verificar que .env existe y tiene contenido
cat .env

# Debe mostrar:
FOOTBALL_API_KEY=tu_key_aqui
```

### Error 403: "You are not subscribed"

1. Verifica que te suscribiste a **Football API 7** (no otra API de fútbol)
2. Confirma que copiaste la key correcta
3. Revisa en RapidAPI Dashboard que la suscripción esté activa

### No se muestran partidos

- 🕒 Puede que no haya partidos en vivo ahora
- ☑️ Desactiva "Solo partidos en vivo" para ver todos los del día
- 📅 Cambia la fecha a un día con más actividad (sábado/domingo)

### Más ayuda

Ver [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)

---

## 📚 Siguiente Paso

Ahora que funciona, explora:

- [docs/CONFIGURATION.md](docs/CONFIGURATION.md) - Todas las variables de configuración
- [ARCHITECTURE.md](ARCHITECTURE.md) - Cómo funciona por dentro
- [README.md](README.md) - Documentación completa

---

## 🎉 ¡Felicidades!

Ya tienes tu tracker de partidos en vivo funcionando. Disfruta viendo fútbol con datos en tiempo real.

---

**⏱️ Tiempo total:** ~5 minutos

**💰 Costo:** $0 (plan gratuito de RapidAPI)
