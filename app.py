import streamlit as st
import streamlit.components.v1 as components

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="GOAT TV - CT DIGITAL", page_icon="⚽", layout="centered")

# CSS para o visual mobile
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
    </style>
""", unsafe_allow_html=True)

# --- MEMÓRIA DO SISTEMA ---
if 'pagina' not in st.session_state:
    st.session_state.pagina = 'login'
if 'arquetipo' not in st.session_state:
    st.session_state.arquetipo = None
# Aqui guardamos o resultado do jogo para não dar erro
if 'resultado_ms' not in st.session_state:
    st.session_state.resultado_ms = 0

def calcular_evolucao(media_ms):
    if media_ms <= 0: return 0, 0
    if media_ms < 350: return 3, 3
    elif media_ms < 550: return 1, 1
    else: return 0, 0

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
    
    col1, col2 = st.columns(2)
    for i, nome in enumerate(arqs):
        with [col1, col2][i % 2]:
            if st.button(f"➔ {nome}", use_container_width=True):
                st.session_state.arquetipo = nome
                st.session_state.pagina = 'treino'
                st.rerun()

# --- SALA DE TREINO (CORREÇÃO AQUI) ---
elif st.session_state.pagina == 'treino':
    st.title(f"🏠 SALA: {st.session_state.arquetipo}")

    if st.session_state.arquetipo == "Goleiro":
        st.subheader("🎯 Teste de Reflexo PES 2020")
        
        # O JOGO (HTML + JS)
        # Ele agora envia o dado via URL para o Python ler
        game_html = """
        <div id="game-container" style="height: 300px; width: 100%; border: 3px solid #4CAF50; position: relative; background: #111; overflow: hidden; border-radius: 15px;">
            <div id="ball" style="width: 50px; height: 50px; background: red; border-radius: 50%; position: absolute; display: none; cursor: pointer;"></div>
            <p id="msg" style="color: white; text-align: center; margin-top: 130px; font-weight: bold;">Clique em INICIAR</p>
        </div>
        <button id="start-btn" style="width: 100%; margin-top: 10px; height: 50px; background: #4CAF50; color: white; border: none; border-radius: 10px; font-weight: bold;">INICIAR TESTE</button>
        
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
                    const media = Math.round(avg);
                    msg.innerHTML = "Fim! Média: " + media + "ms";
                    ball.style.display = 'none';
                    
                    // Envia para a URL para o Python capturar
                    const url = new URL(window.parent.location.href);
                    url.searchParams.set('ms', media);
                    window.parent.location.href = url.href;
                    return;
                }
                const x = Math.random() * (document.getElementById('game-container').offsetWidth - 60);
                const y = Math.random() * (240);
                ball.style.left = x + 'px';
                ball.style.top = y + 'px';
                ball.style.display = 'block';
                start = Date.now();
            }

            btn.onclick = () => {
                count = 0; times = [];
                msg.innerHTML = "Prepare-se...";
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
        components.html(game_html, height=450)

        # LER O RESULTADO QUE O JOGO ENVIOU
        # Agora o Python pega direto da URL
        params = st.query_params
        if "ms" in params:
            media_detectada = int(params["ms"])
            st.session_state.resultado_ms = media_detectada
            
            st.success(f"📺 Resultado Detectado: {media_detectada}ms")
            
            if st.button("CALIBRAR FICHA PES 2020", use_container_width=True):
                s, d = calcular_evolucao(media_detectada)
                if s > 0:
                    st.balloons()
                    st.success(f"✅ GANHOU: +{s} Reflexos | PERDEU: -{d} Chute Rasteiro")
                else:
                    st.error("❌ Desempenho insuficiente para o nível Profissional.")
        else:
            st.info("Aguardando finalização do mini-game...")

    if st.button("⬅️ VOLTAR AO HUB", use_container_width=True):
        st.query_params.clear() # Limpa o resultado para o próximo treino
        st.session_state.pagina = 'hub'
        st.rerun()
