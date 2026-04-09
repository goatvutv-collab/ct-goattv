import streamlit as st
import streamlit.components.v1 as components

# --- 1. ESTILO PREMIUM (CANVA + SIMETRIA) ---
st.set_page_config(page_title="GOAT TV - ANALOG CT", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0E0E2C; color: #FFFFFF; font-family: 'sans-serif'; }
    .ct-title { text-align: center; font-size: 32px; font-weight: 800; color: #FFD700; margin-bottom: 20px; }
    
    div.stButton > button {
        width: 100% !important; height: 65px !important;
        border-radius: 50px !important; border: none !important;
        color: white !important; font-weight: 700 !important; font-size: 18px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4) !important;
        margin-bottom: 10px !important;
    }
    .stats-box { background-color: #1B5E20; padding: 25px; border-radius: 20px; border: 1px solid #2E7D32; }
    iframe { border-radius: 30px; border: none; }
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

# --- 3. LÓGICAS DE PONTUAÇÃO ---
def calc_drible(pts):
    if pts >= 2800: return "🏆 OURO (ELITE)", 3
    elif pts >= 1800: return "✅ PRATA (PROFISS.)", 1
    return "❌ BRONZE", 0

def calc_vel(t):
    if t < 6.5: return "🏆 ELITE (OURO)", 3
    elif t < 9.5: return "✅ PROFISS. (PRATA)", 1
    return "❌ LENTO (BRONZE)", 0

# --- 4. FLUXO DE TELAS ---

if st.session_state.pagina == 'login':
    st.markdown("<h1 class='ct-title'>🛡️ ACESSO CT GOAT TV</h1>", unsafe_allow_html=True)
    pin = st.text_input("PIN DO ATLETA:", type="password")
    if st.button("ENTRAR", use_container_width=True):
        if pin == "2026": st.session_state.pagina = 'hub'; st.rerun()

elif st.session_state.pagina == 'hub':
    st.markdown("<h1 class='ct-title'>CT DE TREINAMENTO</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<style>div.stButton > button[key='btn_d'] { background: linear-gradient(135deg, #4A90E2, #357ABD) !important; }</style>", unsafe_allow_html=True)
        if st.button("⚽ DRIBLE (SLALOM)", key="btn_d"):
            st.session_state.pagina = 'treino_drible'; st.rerun()
    with col2:
        st.markdown("<style>div.stButton > button[key='btn_v'] { background: linear-gradient(135deg, #7C5CFF, #5A3ECC) !important; }</style>", unsafe_allow_html=True)
        if st.button("⚡ VELOCIDADE (SPRINT)", key="btn_v"):
            st.session_state.pagina = 'treino_velocidade'; st.rerun()

# --- SALA: DRIBLE (HORIZONTAL + ANALÓGICO) ---
elif st.session_state.pagina == 'treino_drible':
    st.markdown("<h2 style='text-align: center;'>⚽ SLALOM ANALÓGICO</h2>", unsafe_allow_html=True)
    game_html = """
    <div id="f" style="height:380px; width:100%; background-color:#0D47A1; border-radius:25px; position:relative; overflow:hidden; border:4px solid #08306B; touch-action:none;">
        <div id="p" style="width:34px; height:34px; background:white; border-radius:50%; position:absolute; left:20px; top:170px; z-index:30; border:2px solid #333;">⚽</div>
        <div style="width:15px; height:100%; background:yellow; position:absolute; right:0; top:0;"></div>
        <div class="c" style="left:120px; top:60px;"></div> <div class="c" style="left:120px; top:280px;"></div>
        <div class="c" style="left:220px; top:60px;"></div> <div class="c" style="left:220px; top:280px;"></div>
        <div class="c" style="left:320px; top:60px;"></div> <div class="c" style="left:320px; top:280px;"></div>
        <div class="gate" id="g1" style="left:125px; top:130px; height:100px;"></div>
        <div class="gate" id="g2" style="left:225px; top:130px; height:100px;"></div>
        <div
