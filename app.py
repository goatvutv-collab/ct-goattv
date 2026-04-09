import streamlit as st
import streamlit.components.v1 as components

# --- 1. CONFIGURAÇÃO E ESTILO ---
st.set_page_config(page_title="GOAT TV - CT", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0E0E2C; color: #FFFFFF; font-family: 'sans-serif'; }
    .ct-title { text-align: center; font-size: 38px; font-weight: bold; margin-bottom: 25px; }
    
    /* Estilo das Pílulas */
    div.stButton > button:first-child {
        height: 65px; width: 100%; border-radius: 35px; border: none;
        color: white; font-weight: bold; font-size: 16px; margin-bottom: 8px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    
    /* Box de Atributos */
    .stats-box {
        background-color: #1B5E20; padding: 20px; border-radius: 15px; color: white;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. MOTOR DE ESTADOS ---
if 'pagina' not in st.session_state: st.session_state.pagina = 'login'

# Sincronização via URL
params = st.query_params
if "score" in params:
    st.session_state.pontuacao_final = int(params["score"])
    st.session_state.pagina = 'relatorio_drible'

def processar_drible(pontos):
    if pontos >= 2500: return "OURO (ELITE)", 3
    elif pontos >= 1500: return "PRATA (PROFISSIONAL)", 1
    else: return "BRONZE (INSUFICIENTE)", 0

# --- 3. FLUXO DE TELAS ---

# LOGIN
if st.session_state.pagina == 'login':
    st.markdown("<h1 class='ct-title'>🛡️ GOAT TV LOGIN</h1>", unsafe_allow_html=True)
    pin = st.text_input("PIN DE ATLETA:", type="password")
    if st.button("ACESSAR SISTEMA", use_container_width=True):
        if pin == "2026": st.session_state.pagina = 'hub'; st.rerun()

# HUB
elif st.session_state.pagina == 'hub':
    st.markdown("<h1 class='ct-title'>CENTRO DE TREINAMENTO</h1>", unsafe_allow_html=True)
    st.markdown("<style>div.stButton > button[key='t_0'] { background: linear-gradient(90deg, #4A90E2, #50E3C2) !important; }</style>", unsafe_allow_html=True)
    if st.button("⚽ DRIBLE", key="t_0", use_container_width=True):
        st.session_state.pagina = 'treino_drible'
        st.rerun()

# SALA DE TREINO (COM DIRECIONAIS)
elif st.session_state.pagina == 'treino_drible':
    st.markdown("<h2 style='text-align: center;'>TREINO DE DRIBLE (DIRECIONAL)</h2>", unsafe_allow_html=True)
    
    game_html = """
    <div id="container" style="width:100%; text-align:center; font-family:sans-serif;">
        <div id="field" style="height:350px; width:100%; background-color:#0D47A1; border-radius:25px; position:relative; overflow:hidden; border: 4px solid #08306B; margin-bottom:15px;">
            <div id="player" style="width:40px; height:40px; background:white; border-radius:50%; position:absolute; left:20px; top:150px; z-index:10; border: 2px solid #333; display:flex; justify-content:center; align-items:center; font-size:20px;">⚽</div>
            <div id="finish" style="width:15px; height:100%; background:yellow; position:absolute; right:0; top:0;"></div>
            
            <div class="cone" style="width:25px; height:25px; background:orange; position:absolute; left:100px; top:80px; border-radius:50%;"></div>
            <div class="cone" style="width:25px; height:25px; background:orange; position:absolute; left:180px; top:220px; border-radius:50%;"></div>
            <div class="cone" style="width:25px; height:25px; background:orange; position:absolute; left:260px; top:80px; border-radius:50%;"></div>
            
            <div id="hud" style="position:absolute; top:10px; width:100%; display:flex; justify-content:space-around; font-weight:bold; color:white; text-shadow:1px 1px 2px black;">
                <span id="score-live">PONTOS: 0</span>
                <span id="timer">TEMPO: 15.0s</span>
            </div>
        </div>

        <div id="controls" style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; width: 180px; margin: 0 auto;">
            <div></div>
            <button class="d-btn" id="up" style="height:50px; background:#444; color:white; border-radius:10px; border:none;">▲</button>
            <div></div>
            <button class="d-btn" id="left" style="height:50px; background:#444; color:white; border-radius:10px; border:none;">◀</button>
            <button id="start-btn" style="height:50px; background:#4CAF50; color:white; border-radius:10px; border:none; font-weight:bold;">GO!</button>
            <button class="d-btn" id="right" style="height:50px; background:#444; color:white; border-radius:10px; border:none;">▶</button>
            <div></div>
            <button class="d-btn" id="down" style="height:50px; background:#444; color:white; border-radius:10px; border:none;">▼</button>
            <div></div>
        </div>
    </div>

    <script>
        const player = document.getElementById('player');
        const field = document.getElementById('field');
        const startBtn = document.getElementById('start-btn');
        let x = 20, y = 150, score = 0, timeLeft = 15.0, running = false;
        let move = { up: false, down: false, left: false, right: false };
        let conesHit = new Set();

        const updateHUD = () => {
            document.getElementById('score-live').innerHTML = "PONTOS: " + score;
            document.getElementById('timer').innerHTML = "TEMPO: " + timeLeft.toFixed(1) + "s";
        };

        const setupBtn = (id, dir) => {
            const btn = document.getElementById(id);
            const start = (e) => { e.preventDefault(); if(running) move[dir] = true; };
            const stop = (e) => { e.preventDefault(); move[dir] = false; };
            btn.addEventListener('pointerdown', start);
            btn.addEventListener('pointerup', stop);
            btn.addEventListener('pointerleave', stop);
        };

        setupBtn('up', 'up'); setupBtn('down', 'down');
        setupBtn('left', 'left'); setupBtn('right', 'right');

        startBtn.onclick = () => { if(!running) { running = true; startBtn.style.opacity = '0.5'; } };

        function gameLoop() {
            if(running && timeLeft > 0) {
                timeLeft -= 0.02;
                if(move.up && y > 0) y -= 4;
                if(move.down && y < field.offsetHeight - 40) y += 4;
                if(move.left && x > 0) x -= 4;
                if(move.right && x < field.offsetWidth - 40) x += 4;

                player.style.left = x + 'px';
                player.style.top = y + 'px';

                // Colisão Cones
                document.querySelectorAll('.cone').forEach((cone, i) => {
                    const cR = cone.getBoundingClientRect();
                    const pR = player.getBoundingClientRect();
                    if(!(pR.right < cR.left || pR.left > cR.right || pR.bottom < cR.top || pR.top > cR.bottom)) {
                        if(!conesHit.has(i)) {
                            conesHit.add(i); score += 100; cone.style.opacity = '0.2';
                        }
                    }
                });

                // Chegada
                if(x > field.offsetWidth - 55) {
                    const final = score + 500 + Math.round(timeLeft * 100);
                    window.parent.location.href = window.parent.location.href.split('?')[0] + "?score=" + final;
                    running = false;
                }
                updateHUD();
            } else if (timeLeft <= 0 && running) {
                window.parent.location.href = window.parent.location.href.split('?')[0] + "?score=" + score;
                running = false;
            }
            requestAnimationFrame(gameLoop);
        }
        gameLoop();
    </script>
    """
    components.html(game_html, height=600)

# RELATÓRIO
elif st.session_state.pagina == 'relatorio_drible':
    pontos = st.session_state.pontuacao_final
    nivel, val = processar_drible(pontos)
    
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 30px;">
        <div style="flex: 1; font-size: 28px; font-weight: bold;">TREINO DE<br>DRIBLE<br>
        <span style="font-size:18px; color:#FFD700;">{nivel}</span></div>
        <div class="stats-box" style="flex: 1.2;">
            ✔️ Controle de bola<br>✔️ Drible (PES 2020)<br>
            <b style="font-size:20px;">+ {val} Pontos</b><br><br>
            <span style="opacity:0.7">Força Física<br>Resistência</span><br>
            <b style="font-size:20px;">- {val} Pontos</b>
        </div>
    </div>
    <h1 style='text-align:center;'>{pontos} PTS</h1>
    """, unsafe_allow_html=True)
    
    if st.button("CONCLUIR TREINO", use_container_width=True):
        st.query_params.clear()
        st.session_state.pagina = 'hub'
        st.rerun()
