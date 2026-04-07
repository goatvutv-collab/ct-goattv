import streamlit as st

# 1. Configuração de Elite
st.set_page_config(page_title="CT GOAT TV - Portal Global", page_icon="⚽", layout="centered")

# 2. Estilo Visual (Neon/Dark Mode)
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; background-color: #00ff00; color: black; font-weight: bold; border-radius: 10px; }
    .stTextInput>div>div>input { background-color: #1a1c23; color: #00ff00; border: 1px solid #00ff00; }
    h2, h3 { color: #00ff00; text-align: center; font-family: 'Courier New', Courier, monospace; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h2>🏟️ CT VIRTUAL GOAT TV</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Portal de Treinamento e Evolução de Atletas</p>", unsafe_allow_html=True)

# --- ÁREA DE LOGIN ---
with st.container():
    st.write("---")
    player_id = st.text_input("🆔 ID DO ATLETA (Ex: GT-BR-01)", placeholder="Digite seu ID")
    pin = st.text_input("🔑 PIN DE ACESSO", type="password", placeholder="****")

    # Botão de Entrada
    if st.button("ENTRAR NO CT"):
        # Lógica de Teste (Conta Mestre)
        if player_id == "GT-ADMIN" and pin == "2026":
            st.success("🟢 ACESSO AUTORIZADO! BEM-VINDO, COMISSÁRIO.")
            st.write("---")
            
            # SELEÇÃO DE ARQUÉTIPOS (Os 14 Tipos)
            arquetipo = st.selectbox("🎯 SELECIONE SEU ARQUÉTIPO PARA TREINAR:", 
                ["Maestro (MC)", "Muralha (ZAG)", "Pitbull (VOL)", "Ponta Raio (PE/PD)", 
                 "Finalizador (CA)", "Pivô (CA)", "Goleiro Líbero (GL)", "Garçom (MAT)", 
                 "Lateral Moderno (LAT)", "Coringa (UTL)", "Falso 9", "Destruidor", "Orquestrador", "Tanque"])
            
            st.info(f"Treino disponível para: **{arquetipo}**")
            
            if st.button("🚀 INICIAR SESSÃO DE TREINO"):
                st.warning("⚠️ Carregando simulador de lances... Prepare o Print do resultado!")
        else:
            st.error("🔴 ID ou PIN incorretos. Tente novamente.")

# --- ÁREA DE RECUPERAÇÃO (ESQUECI A SENHA) ---
st.write("---")
with st.expander("🔓 Esqueceu seu PIN? (Recuperação Automática)"):
    st.write("Informe seus dados de segurança cadastrados:")
    rec_id = st.text_input("Confirmar seu ID", key="rec_id")
    safe_word = st.text_input("Sua Palavra-Chave de Segurança", key="safe")
    
    if st.button("RECURERAR MEU PIN"):
        # Lógica de Teste para a Conta Mestre
        if rec_id == "GT-ADMIN" and safe_word.upper() == "GOAT":
            st.success("✅ Identidade Confirmada!")
            st.info("Seu PIN de acesso é: **2026**")
        else:
            st.error("❌ Dados de segurança não conferem. Procure a gerência da Goat TV.")

st.write("---")
st.caption("© 2026 Goat TV Global Federation - Sistema de Evolução Pro")
