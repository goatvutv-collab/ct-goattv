import streamlit as st
import streamlit.components.v1 as components

# --- 1. ESTILO VISUAL (DARK & GOLD) ---
st.set_page_config(page_title="GOAT TV - CT", page_icon="⚽", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    div.stButton > button:first-child {
        height: 100px;
        background: #1E1E1E;
        border: 2px solid #FFD700;
        color: #FFD700;
        border-radius: 15px;
        font-weight: bold;
    }
    .resultado-box {
        padding: 20px;
        border-radius: 15px;
        background-color: #161b22;
        border: 1px solid #30363d;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. GERENCIAMENTO DE ESTADOS ---
if 'pagina' not in st.session_state: st.session_state.pagina = 'login'
if 'arquetipo' not in st.session_state: st.session_state.arquetipo = None

# Captura automática do resultado via URL
params = st.query_params
if "ms" in params:
    st.session_state.resultado_ms = int(params["ms"])
    st.session_state.pagina = 'resultado'

# Lógica de Pontuação Proporcional
def calcular_evolucao(ms):
    if ms < 450: return 3, 3 # Elite
    elif ms < 650: return 1, 1 # Padrão
    else: return 0, 0

# --- 3. NAVEGAÇÃO ---

# LOGIN
if st.session_state.pagina == 'login':
    st.title("🛡️ PORTAL GOAT TV")
    pin = st.text_input("PIN DE ACESSO:", type="password")
    if st.button("ENTRAR", use_container_width=True):
        if pin == "2026": 
            st.session_state.pagina = 'hub'
            st.rerun()

# HUB
elif st.session_state.pagina == 'hub':
    st.title("🏟️ HUB DE ARQUÉTIPOS")
    arqs = ["Pivô", "Finalizador", "Ponta", "2º Atacante", "Maestro", "Motorzinho", 
            "Pitbull", "Organizador", "Muralha", "Zagueiro Técnico", "Lateral Ala", "Goleiro"]
    
    col1, col2 = st.columns(2)
    for i, nome in enumerate(arqs):
        with [col1, col2][i % 2]:
            if st.button(nome, use_container_width=True):
                st.session_state.arquetipo = nome
                st.session_state.pagina = 'jogar'
                st.rerun()

# SALA DO JOGO
elif st.session_state.pagina == 'jogar':
    st.markdown(f"<h1 style='color:#FFD700;'>🏠 SALA: {st.session_state.arquetipo}</h1>", unsafe_allow_html=True)
    
    game_html = """
    <div id="box" style="height:350px; width:100%; border:3px solid #FFD700; position:relative; background:#000; overflow:hidden; border-radius:15px; display:flex; justify-content:center; align-items:center;">
        <div id="ball" style="width:55px; height:55px; background:red; border-radius:50%; position:absolute; display:none; cursor:pointer; box-shadow: 0 0 20px red; border: 2px solid white;"></div>
        <div id="ui">
            <button id="start" style="padding:20px 40px; font-size:20px; background:#4CAF50; color:white; border:none; border-radius:12px; cursor:pointer; font-weight:bold;">INICIAR TESTE</button>
            <p id="info" style="color:white; font-family:sans-serif; text-align:center; font-weight:bold;"></p>
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

        function play() {
            if (count >= 5) {
                const avg = Math.round(times.reduce((a, b) => a + b, 0) / 5);
                info.innerHTML = "Sincronizando Média: " + avg + "ms...";
                ball.style.display = 'none';
                setTimeout(() => {
                    const currentUrl = window.parent.location.href.split('?')[0];
                    window.parent.location.href = currentUrl + "?ms=" + avg;
                }, 1000);
                return;
            }
            ball.style.display = 'none';
            setTimeout(() => {
                const x = Math.random() * (box.offsetWidth - 60);
                const y = Math.random() * (box.offsetHeight - 60);
                ball.style.left = x + 'px';
                ball.style.top = y + 'px';
                ball.style.display = 'block';
                start = Date.now();
            }, 500 + Math.random() * 1000);
        }
        startBtn.onclick = () => { count = 0; times = []; startBtn.style.display = 'none'; play(); };
        ball.onclick = () => { times.push(Date.now() - start); count++; ball.style.display = 'none'; play(); };
    </script>
    """
    components.html(game_html, height=450)
    
    if st.button("⬅️ VOLTAR AO HUB"):
        st.session_state.pagina = 'hub'
        st.rerun()

# TELA DE RESULTADO (O RELATÓRIO QUE VOCÊ QUERIA)
elif st.session_state.pagina == 'resultado':
    st.markdown("<h2 style='text-align: center; color: #FFD700;'>📊 RELATÓRIO DE EVOLUÇÃO</h2>", unsafe_allow_html=True)
    
    media = st.session_state.resultado_ms
    s, d = calcular_evolucao(media)
    
    st.markdown(f"<div class='resultado-box'><h3 style='text-align:center;'>Média Final: {media}ms</h3></div>", unsafe_allow_
