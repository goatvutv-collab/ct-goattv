import streamlit as st
import time
import random

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="GOAT TV - CT DIGITAL", layout="centered")

# CSS para deixar os botões grandes e quadrados no celular
st.markdown("""
    <style>
    div.stButton > button:first-child {
        height: 110px;
        font-size: 24px;
        border-radius: 15px;
        background-color: #1E1E1E;
        color: white;
        border: 2px solid #333;
    }
    /* Destaque para a bolinha */
    div.stButton > button:active, div.stButton > button:focus {
        border-color: #4CAF50;
    }
    </style>
""", unsafe_allow_html=True)

# --- MEMÓRIA DO SISTEMA ---
if 'pagina' not in st.session_state: st.session_state.pagina = 'login'
if 'arquetipo' not in st.session_state: st.session_state.arquetipo = None
if 'game_active' not in st.session_state: st.session_state.game_active = False
if 'rodada' not in st.session_state: st.session_state.rodada = 0
if 'target' not in st.session_state: st.session_state.target = random.randint(0, 8)
if 'tempos' not in st.session_state: st.session_state.tempos = []
if 'start_time' not in st.session_state: st.session_state.start_time = 0

def calcular_evolucao(media):
    if media < 450: return 3, 3 # Elite
    elif media < 650: return 1, 1 # Padrão
    else: return 0, 0

# --- TELA DE LOGIN ---
if st.session_state.pagina == 'login':
    st.title("🛡️ PORTAL GOAT TV")
    pin = st.text_input("PIN de Atleta:", type="password")
    if st.button("ACESSAR CT", use_container_width=True):
        if pin == "2026": 
            st.session_state.pagina = 'hub'
            st.rerun()

# --- HUB DE ARQUÉTIPOS ---
elif st.session_state.pagina == 'hub':
    st.title("🏟️ HUB DE ARQUÉTIPOS")
    arqs = ["Pivô", "Finalizador", "Ponta", "2º Atacante", "Maestro", "Motorzinho", 
            "Pitbull", "Organizador", "Muralha", "Zagueiro Técnico", "Lateral Ala", "Goleiro"]
    
    cols = st.columns(2)
    for i, nome in enumerate(arqs):
        if cols[i%2].button(f"➔ {nome}", use_container_width=True):
            st.session_state.arquetipo = nome
            st.session_state.pagina = 'treino'
            st.session_state.game_active = False
            st.rerun()

# --- SALA DE TREINO (REFLEXO 3x3) ---
elif st.session_state.pagina == 'treino':
    st.title(f"🏠 SALA: {st.session_state.arquetipo}")

    if st.session_state.arquetipo == "Goleiro":
        st.subheader("🎯 Reflexo Ninja (Grade 3x3)")
        
        if not st.session_state.game_active:
            st.info("A bolinha 🔴 aparecerá em um dos 9 quadrados. Clique nela 5 vezes o mais rápido possível!")
            if st.button("🚀 INICIAR TREINO", use_container_width=True):
                st.session_state.game_active = True
                st.session_state.rodada = 1
                st.session_state.tempos = []
                st.session_state.start_time = time.time()
                st.session_state.target = random.randint(0, 8)
                st.rerun()
        
        elif st.session_state.rodada <= 5:
            st.write(f"**Rodada: {st.session_state.rodada} / 5**")
            
            # Criando a grade 3x3
            for r in range(3):
                cols = st.columns(3)
                for c in range(3):
                    idx = r * 3 + c
                    label = "🔴" if idx == st.session_state.target else ""
                    
                    if cols[c].button(label, key=f"btn_{idx}", use_container_width=True):
                        if idx == st.session_state.target:
                            # Acertou a bolinha!
                            fim = time.time()
                            st.session_state.tempos.append((fim - st.session_state.start_time) * 1000)
                            st.session_state.rodada += 1
                            st.session_state.target = random.randint(0, 8)
                            st.session_state.start_time = time.time()
                            st.rerun()
        
        else:
            # FIM DO JOGO
            media = int(sum(st.session_state.tempos) / 5)
            st.success(f"🏁 FIM DE TREINO! Média: {media}ms")
            
            s, d = calcular_evolucao(media)
            if s > 0:
                st.balloons()
                st.markdown(f"### ✅ FICHA PES 2020: +{s} Reflexo | -{d} Chute Rasteiro")
            else:
                st.error("❌ Muito lento! Tente novamente.")
            
            if st.button("REFAZER TESTE"):
                st.session_state.game_active = False
                st.rerun()

    if st.button("⬅️ VOLTAR AO HUB", use_container_width=True):
        st.session_state.game_active = False
        st.session_state.pagina = 'hub'
        st.rerun()
