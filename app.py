import streamlit as st
import streamlit.components.v1 as components

# --- 1. ESTILO PREMIUM MOBILE ---
st.set_page_config(page_title="GOAT TV - CT", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0E0E2C; color: #FFFFFF; font-family: 'sans-serif'; }
    .ct-title { text-align: center; font-size: 26px; font-weight: 800; color: #FFD700; margin-bottom: 15px; }
    div.stButton > button {
        width: 100% !important; height: 55px !important; border-radius: 50px !important;
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
elif "time" in params:
    st.session_state.tempo_velocidade = float(params["time"])
    st.session_state.pagina = 'relatorio_velocidade'

# --- 3. TELAS ---

if st.session_state.pagina == 'login':
    st.markdown("<h1 class='ct-title'>🛡️ ACESSO CT GOAT TV</h1>", unsafe_allow_html=True)
    pin = st.text_input("PIN:", type="password")
