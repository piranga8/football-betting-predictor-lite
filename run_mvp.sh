#!/bin/bash
# Script para ejecutar el MVP del Football Betting Predictor

echo "⚽ Football Betting Predictor MVP"
echo "================================"
echo ""

# Verificar si existe el entorno virtual
if [ ! -d "venv" ]; then
    echo "⚠️ Entorno virtual no encontrado. Creando..."
    python3 -m venv venv
    echo "✅ Entorno virtual creado"
fi

# Activar entorno virtual
echo "🔄 Activando entorno virtual..."
source venv/bin/activate

# Actualizar pip
echo "🔄 Actualizando pip..."
python -m pip install --upgrade pip setuptools wheel --quiet

# Instalar dependencias
if [ ! -f ".dependencies_installed" ]; then
    echo "📦 Instalando dependencias..."
    pip install -r requirements.txt --quiet
    touch .dependencies_installed
    echo "✅ Dependencias instaladas"
else
    echo "✅ Dependencias ya instaladas"
fi

# Verificar archivo .env
if [ ! -f ".env" ]; then
    echo "⚠️ Archivo .env no encontrado"
    echo "🔧 Creando desde .env.example..."
    cp .env.example .env
    echo "❗ IMPORTANTE: Edita .env y agrega tu API key de RapidAPI"
    echo ""
    read -p "Presiona Enter para continuar con modo Mock (testing)..."
fi

# Crear directorio de datos
mkdir -p data

echo ""
echo "🚀 Iniciando dashboard..."
echo "🎯 Abre tu navegador en: http://localhost:8501"
echo ""
echo "Tip: Activa 'Usar datos de prueba (Mock)' en el sidebar para testing sin API"
echo ""

# Ejecutar Streamlit
streamlit run app.py
