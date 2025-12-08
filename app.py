"""Dashboard principal de predicciones en vivo"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time
import os

# Importar módulos propios
from config import config
from src.data.database import db
from src.data.api_consumer import BetfairAPIConsumer, MockBetfairAPI
from src.models.inplay_predictor import predictor

# Configuración de la página
st.set_page_config(
    page_title=config.PAGE_TITLE,
    page_icon=config.PAGE_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para semáforo
st.markdown("""
<style>
.green-signal {
    background-color: #28a745;
    color: white;
    padding: 10px;
    border-radius: 5px;
    text-align: center;
    font-weight: bold;
}
.yellow-signal {
    background-color: #ffc107;
    color: black;
    padding: 10px;
    border-radius: 5px;
    text-align: center;
    font-weight: bold;
}
.red-signal {
    background-color: #dc3545;
    color: white;
    padding: 10px;
    border-radius: 5px;
    text-align: center;
    font-weight: bold;
}
.match-card {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 15px;
    margin: 10px 0;
    background-color: #f8f9fa;
}
</style>
""", unsafe_allow_html=True)

# Título principal
st.title("⚽ Football Betting Predictor - Live Dashboard")
st.markdown("**Predicciones en tiempo real con actualización automática cada 15 minutos**")

# Sidebar - Configuración
with st.sidebar:
    st.header("⚙️ Configuración")
    
    # Modo de operación
    use_mock = st.checkbox("Usar datos de prueba (Mock)", value=True, 
                           help="Activar para testing sin API real")
    
    # Ligas a monitorear
    st.subheader("🏆 Ligas")
    leagues_options = {
        'UEFA Champions League': '228',
        'Premier League': '10932509',
        'La Liga': '117',
        'Bundesliga': '59',
        'Serie A': '81',
        'Ligue 1': '55'
    }
    
    selected_leagues = st.multiselect(
        "Seleccionar ligas:",
        options=list(leagues_options.keys()),
        default=['UEFA Champions League', 'Premier League']
    )
    
    competition_ids = [leagues_options[league] for league in selected_leagues]
    
    # Filtros de confianza
    st.subheader("🎯 Filtros")
    min_confidence = st.slider(
        "Confianza mínima:",
        min_value=0.0,
        max_value=1.0,
        value=config.MIN_CONFIDENCE,
        step=0.05
    )
    
    # Información
    st.divider()
    st.caption(f"⏱️ Actualiza cada {config.REFRESH_INTERVAL // 60} minutos")
    st.caption(f"📊 Última actualización: {datetime.now().strftime('%H:%M:%S')}")

# Inicializar API
@st.cache_resource
def get_api_client():
    if use_mock:
        return MockBetfairAPI()
    else:
        api_key = config.FOOTBALL_API_KEY
        if not api_key:
            st.error("❌ API Key no configurada. Usa el modo Mock o configura FOOTBALL_API_KEY en .env")
            return MockBetfairAPI()
        return BetfairAPIConsumer(api_key)

api = get_api_client()

# Función para obtener partidos en vivo
@st.cache_data(ttl=config.REFRESH_INTERVAL)
def fetch_live_matches(comp_ids):
    """Obtener partidos en vivo de las competiciones seleccionadas"""
    matches = []
    
    with st.spinner('🔄 Obteniendo partidos en vivo...'):
        for comp_id in comp_ids:
            try:
                events = api.get_events(comp_id)
                
                for event in events:
                    event_id = event['event_id']
                    
                    # Obtener predicción pre-match
                    prematch = api.get_match_predictions(event_id)
                    
                    if prematch:
                        # Por ahora simulamos estado in-play
                        # En producción, aquí obtendrías minuto y marcador real
                        import random
                        is_live = random.choice([True, False])
                        
                        if is_live:
                            minute = random.randint(10, 85)
                            home_score = random.randint(0, 3)
                            away_score = random.randint(0, 3)
                            
                            # Generar predicción in-play
                            inplay = predictor.predict(
                                prematch,
                                minute,
                                home_score,
                                away_score
                            )
                            
                            match = {
                                'event_id': event_id,
                                'home_team': event['home_team'],
                                'away_team': event['away_team'],
                                'competition': comp_id,
                                'minute': minute,
                                'score': f"{home_score}-{away_score}",
                                'prematch': prematch,
                                'inplay': inplay
                            }
                            matches.append(match)
            except Exception as e:
                st.warning(f"⚠️ Error obteniendo datos de competición {comp_id}: {str(e)}")
                continue
    
    return matches

# Obtener datos
if not competition_ids:
    st.warning("⚠️ Selecciona al menos una liga en el sidebar")
    st.stop()

matches = fetch_live_matches(competition_ids)

# Filtrar por confianza
matches_filtered = [
    m for m in matches 
    if m['inplay']['confidence'] >= min_confidence
]

# Métricas generales
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📡 Partidos en Vivo", len(matches))

with col2:
    high_conf = len([m for m in matches if m['inplay']['signal_color'] == 'green'])
    st.metric("🟢 Alta Confianza", high_conf)

with col3:
    med_conf = len([m for m in matches if m['inplay']['signal_color'] == 'yellow'])
    st.metric("🟡 Media Confianza", med_conf)

with col4:
    low_conf = len([m for m in matches if m['inplay']['signal_color'] == 'red'])
    st.metric("🔴 Baja Confianza", low_conf)

st.divider()

# Mostrar partidos
if not matches_filtered:
    st.info("🔍 No hay partidos que cumplan los criterios de filtrado")
else:
    st.subheader(f"🎮 Partidos en Vivo ({len(matches_filtered)})")
    
    for match in matches_filtered:
        with st.container():
            # Semáforo
            signal_color = match['inplay']['signal_color']
            signal_emoji = {
                'green': '🟢',
                'yellow': '🟡',
                'red': '🔴'
            }[signal_color]
            
            # Header del partido
            col_header1, col_header2, col_header3 = st.columns([3, 1, 1])
            
            with col_header1:
                st.markdown(f"### {match['home_team']} vs {match['away_team']}")
            
            with col_header2:
                st.markdown(f"**{match['score']}** | {match['minute']}'")
            
            with col_header3:
                st.markdown(f"{signal_emoji} **Confianza: {match['inplay']['confidence']:.0%}**")
            
            # Contenido del partido
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                st.markdown("**📄 Pre-Match**")
                st.write(f"Casa: {match['prematch']['prob_home']:.1%}")
                st.write(f"Empate: {match['prematch']['prob_draw']:.1%}")
                st.write(f"Visita: {match['prematch']['prob_away']:.1%}")
            
            with col2:
                st.markdown("**⏱️ In-Play (Actualizado)**")
                st.write(f"Casa: {match['inplay']['prob_home']:.1%}")
                st.write(f"Empate: {match['inplay']['prob_draw']:.1%}")
                st.write(f"Visita: {match['inplay']['prob_away']:.1%}")
            
            with col3:
                st.markdown("**📊 Cambios**")
                delta_home = match['inplay']['prob_home'] - match['prematch']['prob_home']
                delta_draw = match['inplay']['prob_draw'] - match['prematch']['prob_draw']
                delta_away = match['inplay']['prob_away'] - match['prematch']['prob_away']
                
                st.write(f"Casa: {delta_home:+.1%}")
                st.write(f"Empate: {delta_draw:+.1%}")
                st.write(f"Visita: {delta_away:+.1%}")
            
            # Gráfico de probabilidades
            fig = go.Figure()
            
            categories = ['Pre-Match', 'In-Play']
            
            fig.add_trace(go.Bar(
                name='Casa',
                x=categories,
                y=[match['prematch']['prob_home'], match['inplay']['prob_home']],
                marker_color='#1f77b4'
            ))
            
            fig.add_trace(go.Bar(
                name='Empate',
                x=categories,
                y=[match['prematch']['prob_draw'], match['inplay']['prob_draw']],
                marker_color='#ff7f0e'
            ))
            
            fig.add_trace(go.Bar(
                name='Visita',
                x=categories,
                y=[match['prematch']['prob_away'], match['inplay']['prob_away']],
                marker_color='#d62728'
            ))
            
            fig.update_layout(
                barmode='group',
                height=250,
                margin=dict(l=0, r=0, t=20, b=0),
                yaxis_title="Probabilidad",
                yaxis_tickformat='.0%'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.divider()

# Auto-refresh
st.markdown("---")
st.caption("🔄 El dashboard se actualiza automáticamente cada 15 minutos")

# Programar auto-refresh (rerun after interval)
time.sleep(config.REFRESH_INTERVAL)
st.rerun()
