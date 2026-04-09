import streamlit as st
import streamlit.components.v1 as components

# --- 1. CONFIGURAÇÃO E ESTILO (DESIGN CANVA - HUB DE PÍLULAS) ---
st.set_page_config(page_title="GOAT TV - CT DIGITAL", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0E0E2C; color: #FFFFFF; font-family: 'sans-serif'; }
    .ct-title { text-align: center; font-size: 38px; font-weight: bold; margin-bottom: 25px; color: #FFFFFF; }

    /* Estilo das Pílulas do Hub */
    div.stButton > button:first-child {
        height: 65px;
        width: 100%;
        border-radius: 35px;
        border: none;
        color: white;
        font-weight: bold;
        font-size: 16px;
        margin-bottom: 8px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        transition: 0.2s;
    }
    div.stButton > button:hover { transform: scale(1.05); filter: brightness(1.2); }

    /* Esconder menus do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 2. MOTOR DE ESTADOS (MEMÓRIA) ---
if 'pagina' not in st.session_state: st.session_state.pagina = 'login'
if 'arquetipo' not in st.session_state: st.session_state.arquetipo = None

# Sincronização via URL para futuros treinos
params = st.query_params
if "ms" in params:
    st.session_state.resultado_ms = int(params["ms"])
    st.session_state.pagina = 'relatorio'

# --- 3. FLUXO DE TELAS ---

# TELA DE LOGIN
if st.session_state.pagina == 'login':
    st.markdown("<h1 class='ct-title'>🛡️ GOAT TV LOGIN</h1>", unsafe_allow_html=True)
    pin = st.text_input("PIN DE ATLETA:", type="password")
    if st.button("ACESSAR SISTEMA", use_container_width=True):
        if pin == "2026": 
            st.session_state.pagina = 'hub'
            st.rerun()

# HUB DE PÍLULAS (ORGANIZAÇÃO VISUAL)
elif st.session_state.pagina == 'hub':
    st.markdown("<h1 class='ct-title'>CT DE TREINAMENTO</h1>", unsafe_allow_html=True)
    
    # Lista para estruturar o Hub - Salas vazias por enquanto
    arqs = ["Pivô", "Finalizador", "Ponta", "2º Atacante", "Maestro", "Motorzinho", 
            "Pitbull", "Organizador", "Muralha", "Zagueiro Técnico", "Lateral Ala", "Goleiro"]
    
    cores = [
        "linear-gradient(90deg, #5C7CFF, #4FAAFF)", "linear-gradient(90deg, #1DBB9B, #6DDB92)", 
        "linear-gradient(90deg, #FF5C8A, #A65CFF)", "linear-gradient(90deg, #3B4DFF, #965CFF)",
        "linear-gradient(90deg, #965CFF, #FF5C9D)", "linear-gradient(90deg, #FFD05C, #FFAA5C)",
        "linear-gradient(90deg, #8CFF5C, #D6FF5C)", "linear-gradient(90deg, #145CFF, #5C96FF)",
        "linear-gradient(90deg, #1DBBBA, #4FAAFF)", "linear-gradient(90deg, #7C5CFF, #C75CFF)",
        "linear-gradient(90deg, #FFEF5C, #FFD05C)", "linear-gradient(90deg, #FF5C5C, #FF3B3B)"
    ]

    for i in range(0, len(arqs), 3):
        cols = st.columns(3)
        for j in range(3):
            idx = i + j
            if idx < len(arqs):
                nome = arqs[idx]
                st.markdown(f"<style>div.stButton > button[key='btn_{idx}'] {{ background: {cores[idx]} !important; }}</style>", unsafe_allow_html=True)
                if cols[j].button(nome, key=f"btn_{idx}"):
                    st.session_state.arquetipo = nome
                    st.session_state.pagina = 'sala_vazia' # Encaminha para construção
                    st.rerun()

# TELA DE CONSTRUÇÃO (SALA VAZIA)
elif st.session_state.pagina == 'sala_vazia':
    st.markdown(f"<h2 style='text-align: center;'>SALA: {st.session_state.arquetipo}</h2>", unsafe_allow_html=True)
    st.warning(f"O treinamento para **{st.session_state.arquetipo}** está sendo estruturado pelo Comissário.")
    
    if st.button("⬅️ VOLTAR AO HUB"):
        st.session_state.pagina = 'hub'
        st.rerun()

# TELA DE RELATÓRIO (RECEPTOR DE DADOS)
elif st.session_state.pagina == 'relatorio':
    st.title("📊 RELATÓRIO TÉCNICO")
    st.write(f"Resultado processado: {st.session_state.resultado_ms}ms")
    
    if st.button("FINALIZAR"):
        st.query_params.clear()
        st.session_state.pagina = 'hub'
        st.rerun()
