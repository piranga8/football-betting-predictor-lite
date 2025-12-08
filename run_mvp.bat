@echo off
REM Script para ejecutar el MVP en Windows

echo ⚽ Football Betting Predictor MVP
echo ================================
echo.

REM Verificar si existe el entorno virtual
if not exist "venv" (
    echo ⚠️ Entorno virtual no encontrado. Creando...
    python -m venv venv
    echo ✅ Entorno virtual creado
)

REM Activar entorno virtual
echo 🔄 Activando entorno virtual...
call venv\Scripts\activate.bat

REM Actualizar pip
echo 🔄 Actualizando pip...
python -m pip install --upgrade pip setuptools wheel >nul 2>&1

REM Instalar dependencias
if not exist ".dependencies_installed" (
    echo 📦 Instalando dependencias...
    pip install -r requirements.txt >nul 2>&1
    echo. > .dependencies_installed
    echo ✅ Dependencias instaladas
) else (
    echo ✅ Dependencias ya instaladas
)

REM Verificar archivo .env
if not exist ".env" (
    echo ⚠️ Archivo .env no encontrado
    echo 🔧 Creando desde .env.example...
    copy .env.example .env >nul
    echo ❗ IMPORTANTE: Edita .env y agrega tu API key de RapidAPI
    echo.
    pause
)

REM Crear directorio de datos
if not exist "data" mkdir data

echo.
echo 🚀 Iniciando dashboard...
echo 🎯 Abre tu navegador en: http://localhost:8501
echo.
echo Tip: Activa 'Usar datos de prueba (Mock)' en el sidebar para testing sin API
echo.

REM Ejecutar Streamlit
streamlit run app.py
