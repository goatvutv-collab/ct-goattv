import streamlit as st
import time
import random

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="GOAT TV - CT", layout="centered")

# --- MEMÓRIA DO SISTEMA (A PROVA DE ERROS) ---
if 'pagina' not in st.session_state: st.session_state.pagina = 'login'
if 'arquetipo' not in st.session_state: st.session_state.arquetipo = None
if 'game_state' not in st.session_state: st.session_state.game_state = 'parado'
if 'rodada' not in st.session_state: st.session_state.rodada = 0
if 'tempos' not in st.session_state: st.session_state.tempos = []
if 'ultimo_click' not in st.session_state: st.session_state.ultimo_click = 0

# --- LÓGICA DE EVOLUÇÃO ---
def calcular_evolucao(media_ms):
    if media_ms < 400: return 3, 3 # Elite
    elif media_ms < 600: return 1, 1 # Padrão
    else: return 0, 0 # Lento

# --- 1. LOGIN ---
if st.session_state.pagina == 'login':
    st.title("🛡️ PORTAL GOAT TV")
    pin = st.text_input("PIN de Atleta:", type="password")
    if st.button("ENTRAR", use_container_width=True):
        if pin == "2026": 
            st.session_state.pagina = 'hub'
            st.rerun()

# --- 2. HUB ---
elif st.session_state.pagina == 'hub':
    st.title("🏟️ HUB DE ARQUÉTIPOS")
    arqs = ["Pivô", "Finalizador", "Ponta", "2º Atacante", "Maestro", "Motorzinho", 
            "Pitbull", "Organizador", "Muralha", "Zagueiro Técnico", "Lateral Ala", "Goleiro"]
    cols = st.columns(2)
    for i, nome in enumerate(arqs):
        if cols[i%2].button(f"➔ {nome}", use_container_width=True):
            st.session_state.arquetipo = nome
            st.session_state.pagina = 'treino'
            st.rerun()

# --- 3. SALA DE TREINO (JOGO AUTOMÁTICO) ---
elif st.session_state.pagina == 'treino':
    st.title(f"🏠 SALA: {st.session_state.arquetipo}")

    if st.session_state.arquetipo == "Goleiro":
        st.subheader("🎯 Teste de Reflexo Ninja")
        
        # LOGICA DO JOGO EM PYTHON (AUTOMÁTICA)
        if st.session_state.game_state == 'parado':
            st.info("O teste consiste em 5 cliques rápidos. O tempo será medido automaticamente.")
            if st.button("🔥 INICIAR TREINO AGORA", use_container_width=True):
                st.session_state.game_state = 'jogando'
                st.session_state.rodada = 1
                st.session_state.tempos = []
                st.session_state.ultimo_click = time.time()
                st.rerun()

        elif st.session_state.game_state == 'jogando':
            progresso = st.session_state.rodada / 5
            st.progress(progresso, text=f"Rodada {st.session_state.rodada} de 5")
            
            # Cria 3 colunas para a bolinha aparecer em lugares diferentes
            c1, c2, c3 = st.columns(3)
            posicao = random.randint(1, 3)
            
            # O botão aparece em uma coluna aleatória
            col_alvo = [c1, c2, c3][posicao-1]
            if col_alvo.button("🔴 CLIQUE!", use_container_width=True):
                agora = time.time()
                diff = (agora - st.session_state.ultimo_click) * 1000 # Converte pra ms
                st.session_state.tempos.append(diff)
                
                if st.session_state.rodada < 5:
                    st.session_state.rodada += 1
                    st.session_state.ultimo_click = time.time()
                    st.rerun()
                else:
                    st.session_state.game_state = 'finalizado'
                    st.rerun()

        elif st.session_state.game_state == 'finalizado':
            media = sum(st.session_state.tempos) / len(st.session_state.tempos)
            media = int(media)
            st.success(f"🏁 TREINO CONCLUÍDO! Média: {media}ms")
            
            s, d = calcular_evolucao(media)
            if s > 0:
                st.balloons()
                st.markdown(f"### ✅ RESULTADO: +{s} Reflexo | -{d} Chute Rasteiro")
            else:
                st.error("❌ Muito lento! Tente novamente para subir de nível.")
            
            if st.button("REFAZER TESTE"):
                st.session_state.game_state = 'parado'
                st.rerun()

    if st.button("⬅️ VOLTAR AO HUB", use_container_width=True):
        st.session_state.game_state = 'parado'
        st.session_state.pagina = 'hub'
        st.rerun()
