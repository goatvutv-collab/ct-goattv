import streamlit as st
import streamlit.components.v1 as components

# --- 1. CONFIGURAÇÃO E ESTILO (DESIGN CANVA) ---
st.set_page_config(page_title="GOAT TV - CT DIGITAL", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0E0E2C; color: #FFFFFF; font-family: 'sans-serif'; }
    
    /* Título do CT */
    .ct-title { text-align: center; font-size: 38px; font-weight: bold; margin-bottom: 25px; color: #FFFFFF; }

    /* Estilo das Pílulas (Botões do Hub) */
    div.stButton > button:first-child {
        height: 65px;
        width: 100%;
        border-radius: 35px;
        border: none;
        color: white;
        font-weight: bold;
        font-size: 16px;
        margin-bottom: 8px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        transition: 0.2s;
    }
    div.stButton > button:hover { transform: scale(1.05); filter: brightness(1.2); }

    /* Layout do Relatório de Resultados (Imagem 2 do Canva) */
    .result-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #0E0E2C;
        padding: 20px;
        border-radius: 20px;
    }
    .treino-info-title { flex: 1; font-size: 30px; font-weight: bold; line-height: 1.1; color: white; }
    .stats-box {
        flex: 1.2;
        background-color: #1B5E20; /* Verde escuro do Canva */
        padding: 20px;
        border-radius: 15px;
        color: white;
    }
    .stats-line { margin-bottom: 5px; font-size: 15px; }
    .points-highlight { font-size: 20px; font-weight: bold; display: block; margin-top: 5px; }
    
    /* Estilo do Iframe do Jogo */
    iframe { border-radius: 30px; border: none; }
    
    /* Esconder elementos desnecessários */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 2. MOTOR DE ESTADOS ---
if 'pagina' not in st.session_state: st.session_state.pagina = 'login'
if 'arquetipo' not in st.session_state: st.session_state.arquetipo = None

# Sincronização Automática via URL
params = st.query_params
if "ms" in params:
    st.session_state.resultado_ms = int(params["ms"])
    st.session_state.pagina = 'relatorio'

# --- 3. LÓGICA DE NÍVEIS (3 TÓPICOS) ---
def processar_niveis(ms):
    if ms < 350: # ELITE
        return "ELITE", 3, "Extraordinário"
    elif ms < 550: # PROFISSIONAL
        return "PROFISSIONAL", 1, "Eficiente"
    else: # INSUFICIENTE
        return "INSUFICIENTE", 0, "Lento"

# --- 4. FLUXO DE TELAS ---

# TELA DE LOGIN
if st.session_state.pagina == 'login':
    st.markdown("<h1 class='ct-title'>🛡️ GOAT TV LOGIN</h1>", unsafe_allow_html=True)
    pin = st.text_input("PIN DE ATLETA:", type="password")
    if st.button("ACESSAR SISTEMA", use_container_width=True):
        if pin == "2026": 
            st.session_state.pagina = 'hub'
            st.rerun()

# HUB DE PÍLULAS (IMAGEM 1)
elif st.session_state.pagina == 'hub':
    st.markdown("<h1 class='ct-title'>CT DE TREINAMENTO</h1>", unsafe_allow_html=True)
    
    arqs = ["Pivô", "Finalizador", "Ponta", "2º Atacante", "Maestro", "Motorzinho", 
            "Pitbull", "Organizador", "Muralha", "Zagueiro Técnico", "Lateral Ala", "Goleiro"]
    
    # Gradientes do Canva
    cores = [
        "linear-gradient(90deg, #5C7CFF, #4FAAFF)", "linear-gradient(90deg, #1DBB9B, #6DDB92)", 
        "linear-gradient(90deg, #FF5C8A, #A65CFF)", "linear-gradient(90deg, #3B4DFF, #965CFF)",
        "linear-gradient(90deg, #965CFF, #FF5C9D)", "linear-gradient(90deg, #FFD05C, #FFAA5C)",
        "linear-gradient(90deg, #8CFF5C, #D6FF5C)", "linear-gradient(90deg, #145CFF, #5C96FF)",
        "linear-gradient(90deg, #1DBBBA, #4FAAFF)", "linear-gradient(90deg, #7C5CFF, #C75CFF)",
        "linear-gradient(90deg, #FFEF5C, #FFD05C)", "linear-gradient(90deg, #FF5C5C, #FF3B3B)"
    ]

    for i in range(0, len(arqs), 3):
        cols = st.columns(3)
        for j in range(3):
            idx = i + j
            if idx < len(arqs):
                nome = arqs[idx]
                st.markdown(f"<style>div.stButton > button[key='btn_{idx}'] {{ background: {cores[idx]} !important; }}</style>", unsafe_allow_html=True)
                if cols[j].button(nome, key=f"btn_{idx}"):
                    st.session_state.arquetipo = nome
                    st.session_state.pagina = 'jogar'
                    st.rerun()

# SALA DE TREINO (IMAGEM 2 - QUADRADO AZUL)
elif st.session_state.pagina == 'jogar':
    st.markdown(f"<h2 style='text-align: center;'>TREINAMENTO: {st.session_state.arquetipo}</h2>", unsafe_allow_html=True)
    
    game_html = """
    <div id="canvas" style="height:380px; width:100%; background-color:#0D47A1; border-radius:30px; position:relative; overflow:hidden; display:flex; justify-content:center; align-items:center; border: 4px solid #08306B;">
        <div id="ball" style="width:60px; height:60px; background:red; border-radius:50%; position:absolute; display:none; cursor:pointer; box-shadow: 0 0 20px rgba(255,0,0,0.8); border: 3px solid white;"></div>
        <div id="ms-bg" style="color:rgba(255,255,255,0.15); font-size:60px; font-weight:bold; font-family:sans-serif; pointer-events:none; position:absolute;">000ms</div>
        <button id="start" style="padding:15px 40px; font-size:22px; background:#FFFFFF; color:#0D47A1; border:none; border-radius:15px; cursor:pointer; font-weight:bold; z-index:10;">INICIAR</button>
    </div>
    <script>
        const ball = document.getElementById('ball'); const startBtn = document.getElementById('start'); const canvas = document.getElementById('canvas'); const msText = document.getElementById('ms-bg');
        let times = []; let start; let count = 0;
        function play() {
            if (count >= 5) {
                const avg = Math.round(times.reduce((a, b) => a + b, 0) / 5);
                msText.innerHTML = avg + "ms"; msText.style.color = "white";
                setTimeout(() => { window.parent.location.href = window.parent.location.href.split('?')[0] + "?ms=" + avg; }, 1000);
                return;
            }
            ball.style.display = 'none';
            setTimeout(() => {
                ball.style.left = Math.random() * (canvas.offsetWidth - 80) + 'px';
                ball.style.top = Math.random() * (canvas.offsetHeight - 80) + 'px';
                ball.style.display = 'block'; start = Date.now();
            }, 600 + Math.random() * 800);
        }
        startBtn.onclick = () => { count = 0; times = []; startBtn.style.display = 'none'; play(); };
        ball.onclick = () => { times.push(Date.now() - start); count++; ball.style.display = 'none'; play(); };
    </script>
    """
    components.html(game_html, height=420)
    if st.button("⬅️ VOLTAR"):
        st.session_state.pagina = 'hub'
        st.rerun()

# RELATÓRIO TÉCNICO (LAYOUT IMAGEM 2)
elif st.session_state.pagina == 'relatorio':
    media = st.session_state.resultado_ms
    nivel, pontos, desc = processar_niveis(media)
    
    st.markdown(f"""
    <div class="result-container">
        <div class="treino-info-title">
            TREINO DE<br>PRECISÃO<br>
            <span style="font-size:18px; color:#FFD700; letter-spacing:1px;">NÍVEL {nivel}</span>
        </div>
        <div class="stats-box">
            <div class="stats-line">✔️ Reflexo de goleiro</div>
            <div class="stats-line">✔️ Talento defensivo</div>
            <span class="points-highlight" style="color:#AFFFAB;">+ {pontos} Pontos</span>
            <br>
            <div class="stats-line" style="opacity:0.7;">Condução firme</div>
            <div class="stats-line" style="opacity:0.7;">Passe rasteiro</div>
            <span class="points-highlight" style="color:#FFBABA;">- {pontos} Pontos</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"<h1 style='text-align:center; margin-top:0;'>{media}ms</h1>", unsafe_allow_html=True)

    if pontos > 0: st.balloons()
    
    if st.button("SALVAR E FINALIZAR", use_container_width=True):
        st.query_params.clear()
        st.session_state.pagina = 'hub'
        st.rerun()
