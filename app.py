import streamlit as st
import time

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="GOAT TV - PORTAL CT", page_icon="⚽", layout="centered")

# CSS para transformar botões em "quadradinhos" estilo App Mobile
st.markdown("""
    <style>
    div.stButton > button:first-child {
        height: 100px;
        white-space: normal;
        font-weight: bold;
        border-radius: 15px;
        border: 2px solid #4CAF50;
        background-color: #1E1E1E;
        color: white;
    }
    div.stButton > button:hover {
        border: 2px solid #FFD700;
        color: #FFD700;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. ESTADOS DO SISTEMA (MEMÓRIA) ---
if 'pagina' not in st.session_state:
    st.session_state.pagina = 'login'
if 'arquetipo' not in st.session_state:
    st.session_state.arquetipo = None

# --- 3. LÓGICA DE EVOLUÇÃO PROPORCIONAL (PES 2020) ---
def calcular_evolucao(score):
    if score >= 90: return 3, 3  # Nível Elite
    elif score >= 70: return 1, 1 # Nível Padrão
    else: return 0, 0           # Insuficiente

# --- 4. TELA DE LOGIN ---
if st.session_state.pagina == 'login':
    st.title("🛡️ GOAT TV - LOGIN")
    st.write("Bem-vindo ao Centro de Treinamento Digital")
    
    pin = st.text_input("PIN de Atleta:", type="password")
    
    if st.button("ACESSAR PORTAL", use_container_width=True):
        if pin == "2026": 
            st.session_state.pagina = 'hub'
            st.rerun()
        else:
            st.error("PIN incorreto! Verifique com o Comissário.")

# --- 5. HUB DE ARQUÉTIPOS (O MENU EM GRADE) ---
elif st.session_state.pagina == 'hub':
    st.title("🏟️ HUB DE ARQUÉTIPOS")
    st.write("Selecione sua especialidade para treinar:")

    arqs = ["Pivô", "Finalizador", "Ponta", "2º Atacante", 
            "Maestro", "Motorzinho", "Pitbull", "Organizador", 
            "Muralha", "Zagueiro Técnico", "Lateral Ala", "Goleiro"]

    # Grade de 3 colunas para visual mobile
    for i in range(0, len(arqs), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(arqs):
                nome = arqs[i + j]
                if cols[j].button(nome, use_container_width=True):
                    st.session_state.arquetipo = nome
                    st.session_state.pagina = 'treino'
                    st.rerun()

# --- 6. SALA DE TREINO DINÂMICA (FOCO PES 2020) ---
elif st.session_state.pagina == 'treino':
    arq = st.session_state.arquetipo
    st.title(f"🏠 SALA DE TREINO: {arq}")

    # --- ATUALIZAÇÃO: GOLEIRO (SISTEMA COMPLETO) ---
    if arq == "Goleiro":
        st.subheader("🧤 Treinamento de Goleiros PES 2020")
        
        aba1, aba2, aba3 = st.tabs(["🎯 Reflexos", "🚀 Reposição", "🧠 Consciência"])

        with aba1:
            st.write("### Foco: Reflexos e Pênaltis")
            st.info("Aumenta: Reflexos do GL e Defensor de Pênaltis | Diminui: Chute Rasteiro")
            score_ref = st.slider("Desempenho no Teste de Reação (%)", 0, 100, 70, key="gk_ref")
            if st.button("REGISTRAR REFLEXO", use_container_width=True):
                s, d = calcular_evolucao(score_ref)
                if s > 0:
                    st.success(f"📈 SUBIU: +{s} Reflexos / +{s} Defesa de Pênaltis | 📉 CAIU: -{d} Chute Rasteiro")
                else: st.warning("Treino insuficiente.")

        with aba2:
            st.write("### Foco: Reposição (Lançamentos)")
            st.info("Aumenta: Força de Chute e Chute Rasteiro | Diminui: Firmeza")
            score_rep = st.slider("Precisão do Lançamento (%)", 0, 100, 70, key="gk_rep")
            if st.button("REGISTRAR REPOSIÇÃO", use_container_width=True):
                s, d = calcular_evolucao(score_rep)
                if s > 0:
                    st.success(f"🚀 SUBIU: +{s} Força de Chute / +{s} Chute Rasteiro | 📉 CAIU: -{d} Firmeza")
                else: st.warning("Ajuste a pontaria!")

        with aba3:
            st.write("### Foco: Consciência e Saída")
            st.info("Aumenta: Consciência de GO e Talento GL | Diminui: Alcance")
            score_con = st.slider("Eficácia de Posicionamento (%)", 0, 100, 70, key="gk_con")
            if st.button("REGISTRAR POSICIONAMENTO", use_container_width=True):
                s, d = calcular_evolucao(score_con)
                if s > 0:
                    st.success(f"🧠 SUBIU: +{s} Consciência GO / +{s} Talento GL | 📉 CAIU: -{d} Alcance")
                else: st.warning("Treine o seu posicionamento!")

    # --- OUTRAS SALAS (PENDENTES) ---
    else:
        st.info(f"Sala do {arq} em calibração.")
        st.write("Aguardando as fichas técnicas do PES 2020 para este arquétipo.")

    if st.button("⬅️ VOLTAR AO HUB", use_container_width=True):
        st.session_state.pagina = 'hub'
        st.rerun()
