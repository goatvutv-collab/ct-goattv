import streamlit as st
import streamlit.components.v1 as components

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="GOAT TV - CT DIGITAL", layout="centered")

# --- ESTADOS DO SISTEMA ---
if 'pagina' not in st.session_state:
    st.session_state.pagina = 'login'
if 'arquetipo' not in st.session_state:
    st.session_state.arquetipo = None

# --- LÓGICA DE EVOLUÇÃO ---
def calcular_evolucao(media_ms):
    if media_ms < 350: return 3, 3   # Elite (< 0.35s)
    elif media_ms < 550: return 1, 1 # Padrão (< 0.55s)
    else: return 0, 0               # Lento

# --- TELA DE LOGIN ---
if st.session_state.pagina == 'login':
    st.title("🛡️ PORTAL GOAT TV")
    pin = st.text_input("PIN de Atleta:", type="password")
    if st.button("ENTRAR NO CT", use_container_width=True):
        if pin == "2026": 
            st.session_state.pagina = 'hub'
            st.rerun()

# --- HUB DE ARQUÉTIPOS ---
elif st.session_state.pagina == 'hub':
    st.title("🏟️ HUB DE ARQUÉTIPOS")
    arqs = ["Pivô", "Finalizador", "Ponta", "2º Atacante", "Maestro", "Motorzinho", 
            "Pitbull", "Organizador", "Muralha", "Zagueiro Técnico", "Lateral Ala", "Goleiro"]
    
    col1, col2, col3 = st.columns(3)
    for i, nome in enumerate(arqs):
        with [col1, col2, col3][i % 3]:
            if st.button(nome, use_container_width=True):
                st.session_state.arquetipo = nome
                st.session_state.pagina = 'treino'
                st.rerun()

# --- SALA DE TREINO (GOLEIRO COM MINI-GAME) ---
elif st.session_state.pagina == 'treino':
    st.title(f"🏠 SALA: {st.session_state.arquetipo}")

    if st.session_state.arquetipo == "Goleiro":
        st.subheader("🎯 Teste de Reflexo PES 2020")
        st.write("Clique nas bolinhas o mais rápido que puder!")

        # --- CÓDIGO DO MINI-GAME (HTML/JS) ---
        game_html = """
        <div id="game-container" style="height: 300px; width: 100%; border: 2px solid #4CAF50; position: relative; background: #111; overflow: hidden; border-radius: 15px;">
            <div id="ball" style="width: 50px; height: 50px; background: red; border-radius: 50%; position: absolute; display: none; cursor: pointer;"></div>
            <p id="msg" style="color: white; text-align: center; margin-top: 130px;">Clique em INICIAR para começar</p>
        </div>
        <button id="start-btn" style="width: 100%; margin-top: 10px; height: 40px; background: #4CAF50; color: white; border: none; border-radius: 5px;">INICIAR TESTE</button>
        
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
                    // Envia o resultado para o Streamlit
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
                msg.innerHTML = "";
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
        
        # Renderiza o mini-game e captura o valor
        resultado_ms = components.html(game_html, height=400)
        
        # Campo para o jogador confirmar o valor que apareceu no game
        st.write("---")
        val_final = st.number_input("Confirme sua Média Final (ms) mostrada no jogo:", min_value=0)
        
        if st.button("CALIBRAR FICHA PES 2020", use_container_width=True):
            if val_final > 0:
                s, d = calcular_evolucao(val_final)
                if s > 0:
                    st.success(f"✅ Média: {val_final}ms | GANHOU: +{s} Reflexos | PERDEU: -{d} Chute Rasteiro")
                else:
                    st.error(f"❌ Média: {val_final}ms. Muito lento para o nível profissional!")
            else:
                st.warning("Primeiro complete o mini-game acima!")

    else:
        st.info(f"A sala do {st.session_state.arquetipo} está aguardando seu mini-game exclusivo.")

    if st.button("⬅️ VOLTAR AO HUB", use_container_width=True):
        st.session_state.pagina = 'hub'
        st.rerun()
