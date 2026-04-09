import streamlit as st
import streamlit.components.v1 as components

# --- 1. ESTILO PREMIUM MOBILE (DESIGN GOAT TV) ---
st.set_page_config(page_title="GOAT TV - CT OFICIAL", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0E0E2C; color: #FFFFFF; font-family: 'sans-serif'; }
    .ct-title { text-align: center; font-size: 26px; font-weight: 800; color: #FFD700; margin-bottom: 15px; }
    div.stButton > button {
        width: 100% !important; height: 50px !important; border-radius: 50px !important;
        border: none !important; color: white !important; font-weight: 700 !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4) !important; margin-bottom: 10px !important;
    }
    iframe { border-radius: 25px; border: 3px solid #1E3A8A; background: transparent; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 2. MOTOR DE ESTADOS ---
if 'pagina' not in st.session_state: st.session_state.pagina = 'login'

params = st.query_params
if "score" in params:
    st.session_state.pontos_drible = int(params["score"])
    st.session_state.pagina = 'relatorio_drible'
elif "pass_score" in params:
    st.session_state.pontos_passe = int(params["pass_score"])
    st.session_state.pagina = 'relatorio_passe'

# --- 3. TELAS ---

if st.session_state.pagina == 'login':
    st.markdown("<h1 class='ct-title'>🛡️ ACESSO CT GOAT TV</h1>", unsafe_allow_html=True)
    pin = st.text_input("PIN DO ATLETA:", type="password")
    if st.button("ENTRAR NO CT", use_container_width=True):
        if pin == "2026": st.session_state.pagina = 'hub'; st.rerun()

elif st.session_state.pagina == 'hub':
    st.markdown("<h1 class='ct-title'>CENTRO DE TREINAMENTO</h1>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⚽ DRIBLE", key="btn_d"): st.session_state.pagina = 'treino_drible'; st.rerun()
        if st.button("🎯 PASSE", key="btn_p"): st.session_state.pagina = 'treino_passe'; st.rerun()
    with c2:
        if st.button("⚡ VELOCIDADE", key="btn_v"): st.session_state.pagina = 'treino_velocidade'; st.rerun()

# --- SALA 3: PASSE PRO (GUIA TÁTICA + POWER BAR "8 OU 80") ---
elif st.session_state.pagina == 'treino_passe':
    st.markdown("<h2 style='text-align:center;'>🎯 PRECISÃO TÁTICA</h2>", unsafe_allow_html=True)
    game_html = """
    <div id="f" style="height:480px; width:100%; background-color:#1B5E20; border-
