"""Dashboard de partidos en vivo"""
import streamlit as st
import pandas as pd
from datetime import datetime
import time

from config import config
from src.data.api_consumer import FootballAPI7Consumer

# Configuración de la página
st.set_page_config(
    page_title=config.PAGE_TITLE,
    page_icon=config.PAGE_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
.live-badge {
    background-color: #ff4444;
    color: white;
    padding: 4px 8px;
    border-radius: 4px;
    font-weight: bold;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.6; }
}

.match-card {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 15px;
    margin: 10px 0;
    background-color: #f8f9fa;
}

.score-large {
    font-size: 2em;
    font-weight: bold;
    color: #333;
}

.red-card {
    color: #ff0000;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# Título
st.title("⚽ Football Live Tracker")
st.markdown(f"**Actualización automática cada {config.REFRESH_INTERVAL // 60} minutos**")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuración")
    
    st.subheader("📅 Fecha")
    selected_date = st.date_input("Seleccionar fecha", datetime.now())
    date_str = selected_date.strftime('%d/%m/%Y')
    
    st.subheader("🔍 Filtros")
    show_only_live = st.checkbox("Solo partidos en vivo", value=True)
    
    st.divider()
    st.caption(f"🕐 Última actualización: {datetime.now().strftime('%H:%M:%S')}")

# Inicializar API
@st.cache_resource
def get_api_client():
    api_key = config.FOOTBALL_API_KEY
    if not api_key:
        st.error("❌ API Key no configurada. Por favor configura FOOTBALL_API_KEY en tu archivo .env")
        st.stop()
    return FootballAPI7Consumer(api_key)

api = get_api_client()

# Obtener partidos
@st.cache_data(ttl=config.REFRESH_INTERVAL)
def fetch_matches(date_str, only_live):
    with st.spinner('🔄 Obteniendo partidos...'):
        if only_live:
            matches = api.get_live_matches(date_str)
        else:
            matches = api.get_matches_by_date(date_str)
    return matches

matches = fetch_matches(date_str, show_only_live)

# Métricas generales
col1, col2, col3, col4 = st.columns(4)

total_matches = len(matches)
live_matches = len([m for m in matches if m['status']['is_live']])
total_goals = sum(m['home_team']['score'] + m['away_team']['score'] for m in matches)
red_cards = sum(m['home_team']['red_cards'] + m['away_team']['red_cards'] for m in matches)

with col1:
    st.metric("📊 Total Partidos", total_matches)

with col2:
    st.metric("🔴 En Vivo", live_matches)

with col3:
    st.metric("⚽ Goles", total_goals)

with col4:
    st.metric("🟥 Tarjetas Rojas", red_cards)

st.divider()

# Mostrar partidos
if not matches:
    st.info("ℹ️ No hay partidos disponibles para los filtros seleccionados")
else:
    # Agrupar por competición
    competitions = {}
    for match in matches:
        comp_name = match['competition']['name']
        if comp_name not in competitions:
            competitions[comp_name] = []
        competitions[comp_name].append(match)
    
    # Mostrar por competición
    for comp_name, comp_matches in competitions.items():
        st.subheader(f"🏆 {comp_name}")
        
        for match in comp_matches:
            with st.container():
                # Header del partido
                col_live, col_teams, col_score, col_time = st.columns([1, 4, 2, 1])
                
                with col_live:
                    if match['status']['is_live']:
                        st.markdown('<span class="live-badge">🔴 LIVE</span>', unsafe_allow_html=True)
                    else:
                        st.write(match['status']['short_status'])
                
                with col_teams:
                    st.write(f"**{match['home_team']['name']}**")
                    st.write(f"**{match['away_team']['name']}**")
                
                with col_score:
                    home_score = match['home_team']['score']
                    away_score = match['away_team']['score']
                    st.markdown(f'<p class="score-large">{home_score} - {away_score}</p>', unsafe_allow_html=True)
                
                with col_time:
                    if match['status']['is_live']:
                        st.write(f"⏱️ {match['status']['game_time_display']}")
                    else:
                        # Mostrar hora de inicio
                        try:
                            start_time = datetime.fromisoformat(match['start_time'].replace('Z', '+00:00'))
                            st.write(start_time.strftime('%H:%M'))
                        except:
                            st.write("-")
                
                # Información adicional
                col_info1, col_info2, col_info3 = st.columns(3)
                
                with col_info1:
                    if match['home_team']['red_cards'] > 0:
                        st.markdown(f'<span class="red-card">🟥 {match["home_team"]["name"]}: {match["home_team"]["red_cards"]}</span>', unsafe_allow_html=True)
                    if match['away_team']['red_cards'] > 0:
                        st.markdown(f'<span class="red-card">🟥 {match["away_team"]["name"]}: {match["away_team"]["red_cards"]}</span>', unsafe_allow_html=True)
                
                with col_info2:
                    if match['round_name']:
                        st.caption(f"📅 {match['round_name']}")
                
                with col_info3:
                    if match['has_video']:
                        st.caption("📹 Video disponible")
                
                st.divider()

# Auto-refresh
st.markdown("---")
st.caption("🔄 El dashboard se actualiza automáticamente")

time.sleep(config.REFRESH_INTERVAL)
st.rerun()
