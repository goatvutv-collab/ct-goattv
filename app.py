import streamlit as st
import time

# --- CONFIGURAÇÃO DA PÁGINA (MOBILE FIRST) ---
st.set_page_config(page_title="GOAT TV - CT", page_icon="⚽", layout="centered")

# --- ESTADOS DO SISTEMA ---
if 'pagina' not in st.session_state:
    st.session_state.pagina = 'login'
if 'arquetipo' not in st.session_state:
    st.session_state.arquetipo = None

# --- FUNÇÃO DE CALIBRAGEM PROPORCIONAL ---
def calcular_evolucao_equivalente(score):
    if score >= 90:
        return 3, 3  # Elite: Sobe 3, Desce 3
    elif score >= 70:
        return 1, 1  # Padrão: Sobe 1, Desce 1
    else:
        return 0, 0  # Insuficiente: Nada muda

# --- 1. TELA DE LOGIN ---
if st.session_state.pagina == 'login':
    st.title("🛡️ PORTAL GOAT TV")
    st.subheader("Acesso ao Centro de Treinamento")
    
    pin = st.text_input("Insira seu PIN de Atleta:", type="password")
    
    if st.button("ENTRAR NO CT", use_container_width=True):
        if pin == "2026": 
            st.session_state.pagina = 'hub'
            st.rerun()
        else:
            st.error("PIN Incorreto. Tente novamente.")

# --- 2. HUB DE ARQUÉTIPOS (MENU PRINCIPAL) ---
elif st.session_state.pagina == 'hub':
    st.title("🏟️ HUB DE ARQUÉTIPOS")
    st.write("Selecione sua especialidade para treinar:")
    
    # Lista dos 12 Arquétipos Oficiais
    arquetipos_lista = [
        "Pivô", "Finalizador", "Ponta", "2º Atacante",
        "Maestro", "Motorzinho", "Pitbull", "Organizador",
        "Muralha", "Zagueiro Técnico", "Lateral Ala", "Goleiro"
    ]
    
    # Criando botões em duas colunas para o celular
    col1, col2 = st.columns(2)
    for i, nome in enumerate(arquetipos_lista):
        target_col = col1 if i % 2 == 0 else col2
        if target_col.button(f"➔ {nome}", use_container_width=True):
            st.session_state.arquetipo = nome
            st.session_state.pagina = 'treino'
            st.rerun()

# --- 3. SALA DE TREINO DINÂMICA ---
elif st.session_state.pagina == 'treino':
    arq = st.session_state.arquetipo
    st.title(f"🏠 SALA DE TREINO: {arq}")
    
    # --- LÓGICA ESPECÍFICA: GOLEIRO ---
    if arq == "Goleiro":
        st.subheader("Treino de Reflexo e Alcance")
        st.info("Simule abaixo o desempenho do seu mini-game (em breve interativo).")
        
        # Simulador de performance (Slider)
        score_obtido = st.slider("Seu Desempenho (%)", 0, 100, 70)
        
        if st.button("FINALIZAR E CALIBRAR", use_container_width=True):
            sobe, desce = calcular_evolucao_equivalente(score_obtido)
            
            if sobe > 0:
                st.success(f"🔥 Treino Validado! Score: {score_obtido}%")
                st.markdown(f"**📈 GANHOS:** +{sobe} em Reflexo / Alcance")
                st.markdown(f"**📉 PERDAS:** -{desce} em Velocidade / Passe")
            else:
                st.warning(f"⚠️ Treino Insuficiente (Abaixo de 70%). Nada foi alterado.")

    # --- SALAS EM CONSTRUÇÃO (OUTROS ARQUÉTIPOS) ---
    else:
        st.warning(f"A sala do {arq} está sendo calibrada pelo Comissário.")
        st.write("Em breve, os mini-games de aumento e diminuição estarão ativos aqui.")

    # Botão de Voltar
    if st.button("⬅️ VOLTAR AO HUB", use_container_width=True):
        st.session_state.pagina = 'hub'
        st.rerun()
