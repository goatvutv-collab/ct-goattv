import streamlit as st
import streamlit.components.v1 as components

# --- 1. ESTILO VISUAL GOAT TV PRO (CSS DARK & GOLD) ---
st.set_page_config(page_title="GOAT TV - CT", page_icon="⚽", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; font-family: sans-serif; }
    h1, h2, h3 { text-align: center; color: #FFD700; font-weight: bold; }
    
    /* Botões do Hub */
    div.stButton > button:first-child {
        height: 100px;
        background: #1E1E1E;
        border: 2px solid #FFD700;
        color: #FFD700;
        border-radius: 15px;
        font-weight: bold;
    }

    /* Cards de Habilidades (O que você queria) */
    .skill-card {
        padding: 20px;
        border-radius: 20px;
        margin-bottom: 15px;
        border: 2px solid #333;
    }
    .gain { border-color: #4CAF50; background-color: rgba(76, 175, 80, 0.1); }
    .loss { border-color: #F44336; background-color: rgba(244, 67, 54, 0.1); }
    
    .skill-name { font-size: 20px; font-weight: bold; }
    .skill-value { float: right; font-size: 22px; font-weight: bold; }

    /* Ajuste do Iframe do Jogo */
    iframe { border-radius: 20px; border: 3px solid #FFD700; background-color: #000; }
    </style>
""", unsafe_allow_html=True)

# --- 2. GERENCIAMENTO DE ESTADOS ---
if 'pagina' not in st.session_state: st.session_state.pagina = 'login'
if 'arquetipo' not in st.session_state: st.session_state.arquetipo = None

# Captura automática de resultados vindos da URL
params = st.query_params
if "ms" in params:
    st.session_state.resultado_ms = int(params["ms"])
    st.session_state.pagina = 'relatorio'

# Definição exata das habilidades que sobem e descem (PES 2020)
def obter_ficha_evolucao(ms):
    if ms < 450: # ELITE
        ganhos = {"Reflexos do GL": "+3", "Alcance do GL": "+3", "Defensor de Pênaltis": "ATIVADO", "Consciência de GO": "+1"}
        perdas = {"Chute Rasteiro": "-3", "Força de Chute": "-2", "Chute Alto": "-1"}
        return ganhos, perdas
    elif ms < 650: # PADRÃO
        ganhos = {"Reflexos do GL": "+1", "Alcance do GL": "+1", "Consciência de GO": "+1"}
        perdas = {"Chute Rasteiro": "-1", "Força de Chute": "-1"}
        return ganhos, perdas
    return None, None

# --- 3. TELAS ---

# LOGIN
if st.session_state.pagina == 'login':
    st.markdown("<h1>🛡️ PORTAL GOAT TV</h1>", unsafe_allow_html=True)
    pin = st.text_input("PIN DE ACESSO:", type="password")
    if st.button("ACESSAR SISTEMA", use_container_width=True):
        if pin == "2026": 
            st.session_state.pagina = 'hub'
            st.rerun()

# HUB
elif st.session_state.pagina == 'hub':
    st.markdown("<h2>🏟️ HUB DE ARQUÉTIPOS</h2>", unsafe_allow_html=True)
    arqs = ["Pivô", "Finalizador", "Ponta", "2º Atacante", "Maestro", "Motorzinho", 
            "Pitbull", "Organizador", "Muralha", "Zagueiro Técnico", "Lateral Ala", "Goleiro"]
    col1, col2 = st.columns(2)
    for i, nome in enumerate(arqs):
        with [col1, col2][i % 2]:
            if st.button(nome, use_container_width=True):
                st.session_state.arquetipo = nome
                st.session_state.pagina = 'jogar'
                st.rerun()

# JOGO (O QUADRADÃO RUDEZÃO)
elif st.session_state.pagina == 'jogar':
    st.markdown(f"<h2>🏠 SALA: {st.session_state.arquetipo}</h2>", unsafe_allow_html=True)
    
    game_html = """
    <div id="box" style="height:350px; width:100%; position:relative; background:#000; overflow:hidden; border-radius:15px; display:flex; justify-content:center; align-items:center;">
        <div id="ball" style="width:55px; height:55px; background:red; border-radius:50%; position:absolute; display:none; cursor:pointer; box-shadow: 0 0 20px red; border: 2px solid white;"></div>
        <div id="ui"><button id="start" style="padding:20px 40px; font-size:20px; background:#4CAF50; color:white; border:none; border-radius:12px; cursor:pointer; font-weight:bold;">INICIAR TREINO</button>
        <p id="info" style="color:white; font-family:sans-serif; text-align:center; font-weight:bold;"></p></div>
    </div>
    <script>
        const ball = document.getElementById('ball'); const startBtn = document.getElementById('start'); const info = document.getElementById('info'); const box = document.getElementById('box');
        let times = []; let start; let count = 0;
        function play() {
            if (count >= 5) {
                const avg = Math.round(times.reduce((a, b) => a + b, 0) / 5);
                info.innerHTML = "Sincronizando: " + avg + "ms";
                setTimeout(() => { window.parent.location.href = window.parent.location.href.split('?')[0] + "?ms=" + avg; }, 1000);
                return;
            }
            ball.style.display = 'none';
            setTimeout(() => {
                ball.style.left = Math.random() * (box.offsetWidth - 60) + 'px';
                ball.style.top = Math.random() * (box.offsetHeight - 60) + 'px';
                ball.style.display = 'block'; start = Date.now();
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

# RELATÓRIO DE HABILIDADES (AQUI É ONDE APARECE O QUE SOBE E DESCE)
elif st.session_state.pagina == 'relatorio':
    st.markdown("<h2>📊 RELATÓRIO TÉCNICO</h2>", unsafe_allow_html=True)
    media = st.session_state.resultado_ms
    ganhos, perdas = obter_ficha_evolucao(media)
    
    st.markdown(f"<h3 style='color:#FFD700;'>Média: {media}ms</h3>", unsafe_allow_html=True)

    if ganhos:
        st.balloons()
        # Coluna de Ganhos
        st.markdown("### 📈 Habilidades que SUBIRAM")
        for hab, valor in ganhos.items():
            st.markdown(f"""<div class='skill-card gain'>
                <span class='skill-name'>✅ {hab}</span>
                <span class='skill-value'>{valor}</span>
            </div>""", unsafe_allow_html=True)

        # Coluna de Perdas
        st.markdown("### 📉 Habilidades que DESCERAM")
        for hab, valor in perdas.items():
            st.markdown(f"""<div class='skill-card loss'>
                <span class='skill-name'>❌ {hab}</span>
                <span class='skill-value'>{valor}</span>
            </div>""", unsafe_allow_html=True)
    else:
        st.error(f"❌ TREINO INSUFICIENTE ({media}ms).")
        st.write("O nível profissional exige reflexos abaixo de 650ms. Tente novamente!")

    if st.button("CONCLUIR E VOLTAR AO CT", use_container_width=True):
        st.query_params.clear()
        st.session_state.pagina = 'hub'
        st.rerun()
