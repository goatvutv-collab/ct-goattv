import streamlit as st

# Configuração da página para parecer um App Mobile
st.set_page_config(page_title="CT Goat TV", page_icon="⚽", layout="centered")

# Estética simples e direta
st.markdown("<h2 style='text-align: center;'>🏟️ CT VIRTUAL GOAT TV</h2>", unsafe_allow_html=True)

# O "Quadradinho" de Acesso
with st.container():
    st.write("---")
    
    # 1. Campos de Identificação
    player_id = st.text_input("🆔 ID DO ATLETA", placeholder="Ex: GT-X8Y2")
    pin = st.text_input("🔑 PIN DE ACESSO", type="password", placeholder="****")

    # 2. Lógica de Status Simulada
    pode_treinar = True 

    if player_id and pin:
        if pode_treinar:
            st.success("🟢 STATUS: APTO PARA TREINAR")
            
            # 3. Seletor de Arquétipo
            arquetipo = st.selectbox("🎯 QUAL SEU ARQUÉTIPO?", 
                ["Maestro", "Muralha", "Pitbull", "Ponta (Raio)", "Finalizador", "Pivô", "Goleiro Líbero"])
            
            # 4. Botão de Ação
            if st.button("🚀 INICIAR TREINAMENTO"):
                st.write(f"A carregar sala de treino: {arquetipo}...")
        else:
            st.error("🔴 STATUS: EM RECUPERAÇÃO")
            st.warning("⏳ Ainda não completaste as 72h de descanso.")
            
    st.write("---")

