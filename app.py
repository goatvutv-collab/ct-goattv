import streamlit as st
import streamlit.components.v1 as components
import time

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="GOAT TV - CT DIGITAL", page_icon="⚽", layout="centered")

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
def calcular_evolucao(media_ms):
    if media_ms < 350: return 3, 3   # Nível Elite
    elif media_ms < 550: return 1, 1 # Nível Padrão
    else: return 0, 0               # Insuficiente

# --- 4. TELA DE LOGIN ---
if st.session_state.pagina == 'login':
    st.title("🛡️ PORTAL GOAT TV")
    st.subheader("Centro de Treinamento")
    
    pin = st.text_input("PIN de Atleta:", type="password")
    
    if st.button("ACESSAR PORTAL", use_container_width=True):
        if pin == "2026": 
            st.session_state.pagina = 'hub'
            st.rerun()
        else:
            st.error("PIN incorreto!")

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

# --- 6. SALA DE TREINO DINÂMICA (FOCO PES 2020 AUTOMÁTICO) ---
elif st.session_state.pagina == 'treino':
    arq = st.session_state.arquetipo
    st.title(f"🏠 SALA DE TREINO: {arq}")

    # --- LÓGICA AUTOMÁTICA: GOLEIRO (NÃO TEM OPÇÃO DE DIGITAR) ---
    if arq == "Goleiro":
        st.subheader("🎯 Teste de Reflexo PES 2020")
        st.write("Clique nas bolinhas o mais rápido que puder!")

        # --- CÓDIGO DO MINI-GAME (HTML/JS) COM ENVIO AUTOMÁTICO ---
        game_html = """
        <div id="game-container" style="height: 300px; width: 100%; border: 2px solid #4CAF50; position: relative; background: #111; overflow: hidden; border-radius: 15px;">
            <div id="ball" style="width: 50px; height: 50px; background: red; border-radius: 50%; position: absolute; display: none; cursor: pointer;"></div>
            <p id="msg" style="color: white; text-align: center; margin-top: 130px; font-size: 1.2em; font-weight: bold;">Clique em INICIAR para começar</p>
        </div>
        <button id="start-btn" style="width: 100%; margin-top: 10px; height: 40px; background: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer;">INICIAR TESTE</button>
        
        <script>
            const ball = document.getElementById('ball');
            const btn = document.getElementById('start-btn');
            const msg = document.getElementById('msg');
            let times = [];
            let start;
            let count = 0;

            function spawnBall() {
                if (count >= 5) {
                    const avg = times.reduce((a, b) => a + b, 0) / times.length;
                    msg.innerHTML = "Fim! Média: " + Math.round(avg) + "ms";
                    ball.style.display = 'none';
                    // Envia o resultado para o Streamlit AUTOMATICAMENTE
                    window.parent.postMessage({type: 'streamlit:setComponentValue', value: avg}, '*');
                    return;
                }
                const x = Math.random() * (document.getElementById('game-container').offsetWidth - 50);
                const y = Math.random() * (250);
                ball.style.left = x + 'px';
                ball.style.top = y + 'px';
                ball.style.display = 'block';
                start = Date.now();
            }

            btn.onclick = () => {
                count = 0; times = [];
                msg.innerHTML = "Atenção!";
                btn.style.display = 'none';
                setTimeout(spawnBall, 1000);
            };

            ball.onclick = () => {
                const end = Date.now();
                times.push(end - start);
                count++;
                ball.style.display = 'none';
                setTimeout(spawnBall, 500);
            };
        </script>
        """
        
        # Renderiza o mini-game e captura o valor automaticamente
        # O valor ficará guardado na variável resultado_ms
        resultado_ms = components.html(game_html, height=400)
        
        st.write("---")
        # Placeholder para mostrar o status final
        status_container = st.empty()
        
        # O Botão agora usa o valor capturado do jogo, sem entrada manual
        if st.button("CALIBRAR FICHA PES 2020", use_container_width=True):
            if resultado_ms is not None:
                # Converte o valor para inteiro e usa na lógica
                media_final = int(resultado_ms)
                s, d = calcular_evolucao(media_final)
                
                if s > 0:
                    status_container.success(f"✅ Treino Finalizado! Média: {media_final}ms | GANHOU: +{s} Reflexos | PERDEU: -{d} Chute Rasteiro")
                else:
                    status_container.error(f"❌ Média: {media_final}ms. Muito lento para o nível profissional! Tente novamente.")
            else:
                status_container.warning("Primeiro complete o mini-game acima!")

    # --- SALAS EM CONSTRUÇÃO ---
    else:
        st.info(f"Sala do {arq} em calibração.")
        st.write("Aguardando as fichas técnicas do PES 2020.")

    if st.button("⬅️ VOLTAR AO HUB", use_container_width=True):
        st.session_state.pagina = 'hub'
        st.rerun()
