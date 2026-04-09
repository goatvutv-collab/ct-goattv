import streamlit as st
import streamlit.components.v1 as components

# --- 1. CONFIG E ESTILO ---
st.set_page_config(page_title="GOAT TV - CT", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #0E0E2C; color: #FFFFFF; font-family: 'sans-serif'; }
    .ct-title { text-align: center; font-size: 24px; font-weight: 800; color: #FFD700; margin-bottom: 10px; }
    div.stButton > button {
        width: 100% !important; height: 50px !important; border-radius: 50px !important;
        border: none !important; color: white !important; font-weight: 700 !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4) !important; margin-bottom: 8px !important;
    }
    iframe { border-radius: 20px; border: 3px solid #1E3A8A; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 2. ESTADOS ---
if 'pagina' not in st.session_state: st.session_state.pagina = 'login'
params = st.query_params
if "score" in params:
    st.session_state.pts_d = int(params["score"]); st.session_state.pagina = 'rel_d'
elif "p_score" in params:
    st.session_state.pts_p = int(params["p_score"]); st.session_state.pagina = 'rel_p'
elif "v_time" in params:
    st.session_state.tm_v = float(params["v_time"]); st.session_state.pagina = 'rel_v'

# --- 3. TELAS ---
if st.session_state.pagina == 'login':
    st.markdown("<h1 class='ct-title'>🛡️ ACESSO CT GOAT TV</h1>", unsafe_allow_html=True)
    pin = st.text_input("PIN:", type="password")
    if st.button("ENTRAR NO CT", use_container_width=True):
        if pin == "2026": st.session_state.pagina = 'hub'; st.rerun()

elif st.session_state.pagina == 'hub':
    st.markdown("<h1 class='ct-title'>CENTRO DE TREINAMENTO</h1>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⚽ DRIBLE"): st.session_state.pagina = 'drible'; st.rerun()
        if st.button("🎯 PASSE"): st.session_state.pagina = 'passe'; st.rerun()
    with c2:
        if st.button("⚡ VELOCIDADE"): st.session_state.pagina = 'vel'; st.rerun()

# --- SALA: PASSE PRO (GUIA + BARRA 8 OU 80) ---
elif st.session_state.pagina == 'passe':
    st.markdown("<h2 style='text-align:center;'>🎯 PRECISÃO TÁTICA</h2>", unsafe_allow_html=True)
    game_html = """
    <div id="f" style="height:460px; width:100%; background:#1B5E20; position:relative; overflow:hidden; border:4px solid #08306B; touch-action:none;">
        <div id="p" style="width:26px; height:26px; background:white; border-radius:50%; position:absolute; left:46%; bottom:30px; border:2px solid #333; z-index:30;"></div>
        <div id="tgt" style="width:32px; height:32px; background:rgba(255,
