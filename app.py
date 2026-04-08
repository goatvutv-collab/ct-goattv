import streamlit as st

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="GOAT TV - CT", page_icon="⚽", layout="centered")

# --- 2. MEMÓRIA E CAPTURA DE DADOS (A PONTE) ---
# O segredo está aqui: o Python lê o que o jogo escreve na URL
params = st.query_params

if 'pagina' not in st.session_state:
    st.session_state.pagina = 'login'
if 'arquetipo' not in st.session_state:
    st.session_state.arquetipo = None

# Se o jogo acabou e enviou o resultado (ms), a gente captura na hora!
if "ms" in params:
    st.session_state.resultado_ms = int(params["ms"])
    st.session_state.pagina = 'treino_finalizado'

# --- 3. LÓGICA DE EVOLUÇÃO ---
def calcular_evolucao(media_ms):
    if media_ms < 450: return 3, 3   # Elite
    elif media_ms < 650: return 1, 1 # Padrão
    else: return 0, 0               # Insuficiente

# --- 4. TELAS DO PORTAL ---

# TELA DE LOGIN
if st.session_state.pagina == 'login':
    st.title("🛡️ PORTAL GOAT TV")
    pin = st.text_input("PIN de Atleta:", type="password")
    if st.button("ENTRAR", use_container_width=True):
        if pin == "2026": 
            st.session_state.pagina = 'hub'
            st.rerun()

# HUB DE ARQUÉTIPOS
elif st.session_state.pagina == 'hub':
    st.title("🏟️ HUB DE ARQUÉTIPOS")
    arqs = ["Pivô", "Finalizador", "Ponta", "2º Atacante", "Maestro", "Motorzinho", 
            "Pitbull", "Organizador", "Muralha", "Zagueiro Técnico", "Lateral Ala", "Goleiro"]
    
    col1, col2 = st.columns(2)
    for i, nome in enumerate(arqs):
        with [col1, col2][i % 2]:
            if st.button(f"➔ {nome}", use_container_width=True):
                st.session_state.arquetipo = nome
                st.session_state.pagina = 'jogar'
                st.rerun()

# TELA DO JOGO (HTML/JS)
elif st.session_state.pagina == 'jogar':
    st.title(f"🏠 SALA: {st.session_state.arquetipo}")
    st.subheader("🎯 Teste de Reflexo Ninja")
    
    # O JOGO AGORA USA UM REDIRECT FORÇADO (TARGET='_TOP')
    game_html = f"""
    <div id="box" style="height:350px; width:100%; border:3px solid #4CAF50; position:relative; background:#111; overflow:hidden; border-radius:15px; display:flex; justify-content:center; align-items:center;">
        <div id="ball" style="width:55px; height:55px; background:red; border-radius:50%; position:absolute; display:none; cursor:pointer; box-shadow: 0 0 15px red;"></div>
        <div id="ui">
            <button id="start" style="padding:15px 30px; font-size:18px; background:#4CAF50; color:white; border:none; border-radius:10px; cursor:pointer; font-weight:bold;">INICIAR TREINO</button>
            <p id="info" style="color:white; font-family:sans-serif; text-align:center; font-size:1.2em; font-weight:bold;"></p>
        </div>
    </div>

    <script>
        const ball = document.getElementById('ball');
        const startBtn = document.getElementById('start');
        const info = document.getElementById('info');
        const box = document.getElementById('box');
        let times = [];
        let start;
        let count = 0;

        function play() {{
            if (count >= 5) {{
                const avg = Math.round(times.reduce((a, b) => a + b, 0) / 5);
                info.innerHTML = "🏁 Fim! Média: " + avg + "ms<br><br>Sincronizando...";
                ball.style.display = 'none';
                
                // AQUI ESTÁ A "API" DE REDIRECIONAMENTO:
                // Ele força o navegador a recarregar o site já com o resultado na URL
                const currentUrl = window.parent.location.href.split('?')[0];
                window.parent.location.href = currentUrl + "?ms=" + avg;
                return;
            }}
            ball.style.display = 'none';
            setTimeout(() => {{
                const x = Math.random() * (box.offsetWidth - 60);
                const y = Math.random() * (box.offsetHeight - 60);
                ball.style.left = x + 'px';
                ball.style.top = y + 'px';
                ball.style.display = 'block';
                start = Date.now();
            }}, 500 + Math.random() * 1000);
        }}

        startBtn.onclick = () => {{
            count = 0; times = [];
            startBtn.style.display = 'none';
            info.innerHTML = "Atenção...";
            play();
        }};

        ball.onclick = () => {{
            times.push(Date.now() - start);
            count++;
            ball.style.display = 'none';
            play();
        }};
    </script>
    """
    st.components.v1.html(game_html, height=450)
    
    if st.button("⬅️ VOLTAR AO HUB"):
        st.session_state.pagina = 'hub'
        st.rerun()

# TELA DE RESULTADO (ONDE O PYTHON PROCESSA TUDO)
elif st.session_state.pagina == 'treino_finalizado':
    st.title("📊 Resultado do Treino")
    media = st.session_state.resultado_ms
    s, d = calcular_evolucao(media)
    
    st.success(f"🏁 Média de Reflexo: {media}ms")
    
    if s > 0:
        st.balloons()
        st.markdown(f"### ✅ FICHA PES 2020 ATUALIZADA")
        st.write(f"📈 GANHOU: +{s} Reflexo / Alcance")
        st.warning(f"📉 PERDEU: -{d} Chute Rasteiro")
    else:
        st.error(f"❌ Desempenho insuficiente ({media}ms). O mínimo para evoluir é 650ms.")
        
    if st.button("VOLTAR PARA O CT", use_container_width=True):
        st.query_params.clear() # Limpa a URL
        st.session_state.pagina = 'hub'
        st.rerun()
