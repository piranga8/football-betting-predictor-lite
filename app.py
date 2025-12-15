"""Dashboard de partidos en vivo con predicciones"""
import streamlit as st
import pandas as pd
from datetime import datetime
import time

from config import config
from src.data.api_consumer import FootballAPI7Consumer
from src.data.primatips_scraper import PrimaTipsScraper
from src.utils.match_matcher import enrich_matches_with_predictions

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

.prediction-badge {
    background-color: #4CAF50;
    color: white;
    padding: 4px 8px;
    border-radius: 4px;
    font-weight: bold;
    font-size: 0.9em;
}

.odds-box {
    background-color: #f0f0f0;
    padding: 8px;
    border-radius: 4px;
    font-size: 0.85em;
    margin-top: 5px;
}

.probability-bar {
    height: 20px;
    background-color: #e0e0e0;
    border-radius: 10px;
    overflow: hidden;
    margin: 5px 0;
}

.probability-fill {
    height: 100%;
    background: linear-gradient(90deg, #4CAF50, #8BC34A);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 0.75em;
    font-weight: bold;
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
st.title("⚽ Football Live Tracker + Predictions")
st.markdown(f"**Actualización automática cada {config.REFRESH_INTERVAL // 60} minutos**")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuración")
    
    st.subheader("📅 Fecha")
    selected_date = st.date_input("Seleccionar fecha", datetime.now())
    date_str = selected_date.strftime('%d/%m/%Y')
    
    st.subheader("🔍 Filtros")
    show_only_live = st.checkbox("Solo partidos en vivo", value=True)
    show_predictions = st.checkbox("Mostrar predicciones", value=True)
    
    st.divider()
    
    st.subheader("🎯 Fuentes de Datos")
    st.caption("⚽ Partidos: Football API 7")
    st.caption("📊 Predicciones: PrimaTips")
    
    st.divider()
    st.caption(f"🕐 Última actualización: {datetime.now().strftime('%H:%M:%S')}")

# Inicializar APIs
@st.cache_resource
def get_api_clients():
    api_key = config.FOOTBALL_API_KEY
    if not api_key:
        st.error("❌ API Key no configurada. Por favor configura FOOTBALL_API_KEY en tu archivo .env")
        st.stop()
    
    football_api = FootballAPI7Consumer(api_key)
    primatips = PrimaTipsScraper()
    
    return football_api, primatips

football_api, primatips = get_api_clients()

# Obtener datos
@st.cache_data(ttl=config.REFRESH_INTERVAL)
def fetch_data(date_str, only_live, include_predictions):
    with st.spinner('🔄 Obteniendo partidos...'):
        if only_live:
            matches = football_api.get_live_matches(date_str)
        else:
            matches = football_api.get_matches_by_date(date_str)
    
    if include_predictions:
        with st.spinner('🎯 Obteniendo predicciones...'):
            # Convertir fecha a formato YYYY-MM-DD para PrimaTips
            date_parts = date_str.split('/')
            primatips_date = f"{date_parts[2]}-{date_parts[1]}-{date_parts[0]}"
            predictions = primatips.get_predictions_by_date(primatips_date)
            
            # Enriquecer partidos con predicciones
            matches = enrich_matches_with_predictions(matches, predictions)
    else:
        # Sin predicciones
        for match in matches:
            match['prediction'] = None
    
    return matches

matches = fetch_data(date_str, show_only_live, show_predictions)

# Métricas generales
col1, col2, col3, col4, col5 = st.columns(5)

total_matches = len(matches)
live_matches = len([m for m in matches if m['status']['is_live']])
total_goals = sum(m['home_team']['score'] + m['away_team']['score'] for m in matches)
red_cards = sum(m['home_team']['red_cards'] + m['away_team']['red_cards'] for m in matches)
with_predictions = len([m for m in matches if m.get('prediction')])

with col1:
    st.metric("📊 Total Partidos", total_matches)

with col2:
    st.metric("🔴 En Vivo", live_matches)

with col3:
    st.metric("⚽ Goles", total_goals)

with col4:
    st.metric("🟥 Tarjetas Rojas", red_cards)

with col5:
    st.metric("🎯 Con Predicción", with_predictions)

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
                        try:
                            start_time = datetime.fromisoformat(match['start_time'].replace('Z', '+00:00'))
                            st.write(start_time.strftime('%H:%M'))
                        except:
                            st.write("-")
                
                # Información adicional y predicciones
                if match.get('prediction') and show_predictions:
                    st.markdown("---")
                    
                    pred = match['prediction']
                    
                    col_pred, col_odds, col_probs = st.columns([2, 3, 3])
                    
                    with col_pred:
                        st.markdown(f'<span class="prediction-badge">🎯 Predicción: {pred["predicted_name"]}</span>', unsafe_allow_html=True)
                        st.caption(f"[Ver en PrimaTips]({pred['link']})")
                    
                    with col_odds:
                        if pred['odds']:
                            odds_text = f"**Cuotas:** 1: {pred['odds']['home'] or '-'} | X: {pred['odds']['draw'] or '-'} | 2: {pred['odds']['away'] or '-'}"
                            st.markdown(f'<div class="odds-box">{odds_text}</div>', unsafe_allow_html=True)
                    
                    with col_probs:
                        if pred['probabilities']:
                            probs = pred['probabilities']
                            
                            # Barra de probabilidad para la predicción favorita
                            if pred['predicted'] == '1':
                                prob_value = probs['home']
                                prob_label = f"Local: {prob_value*100:.1f}%"
                            elif pred['predicted'] == 'X':
                                prob_value = probs['draw']
                                prob_label = f"Empate: {prob_value*100:.1f}%"
                            elif pred['predicted'] == '2':
                                prob_value = probs['away']
                                prob_label = f"Visitante: {prob_value*100:.1f}%"
                            else:
                                prob_value = max(probs['home'], probs['draw'], probs['away'])
                                prob_label = f"Máxima: {prob_value*100:.1f}%"
                            
                            prob_percent = prob_value * 100
                            st.markdown(f'''
                            <div class="probability-bar">
                                <div class="probability-fill" style="width: {prob_percent}%">
                                    {prob_label}
                                </div>
                            </div>
                            ''', unsafe_allow_html=True)
                            
                            st.caption(f"Local: {probs['home']*100:.0f}% | Empate: {probs['draw']*100:.0f}% | Visitante: {probs['away']*100:.0f}%")
                
                # Tarjetas rojas y otras info
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
