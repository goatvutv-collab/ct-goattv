import streamlit as st
import streamlit.components.v1 as components

# --- 1. CONFIG E ESTILO ---
st.set_page_config(page_title="GOAT TV - CT OFICIAL", layout="centered")

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

# --- 2. MOTOR DE ESTADOS ---
if 'pagina' not in st.session_state: st.session_state.pagina = 'login'
params = st.query_params

if "score" in params:
    st.session_state.pts_d = int(params["score"]); st.session_state.pagina = 'rel_d'
elif "p_score" in params:
    st.session_state.pts_p = int(params["p_score"]); st.session_state.pagina = 'rel_p'
elif "v_time" in params:
    st.session_state.tm_v = float(params["v_time"]); st.session_state.pagina = 'rel_v'

# --- 3. TELAS ---

# LOGIN
if st.session_state.pagina == 'login':
    st.markdown("<h1 class='ct-title'>🛡️ ACESSO CT GOAT TV
