import streamlit as st
import streamlit.components.v1 as components

# --- 1. CONFIGURAÇÃO E ESTILO ---
st.set_page_config(page_title="GOAT TV - CT", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0E0E2C; color: #FFFFFF; font-family: 'sans-serif'; }
    .ct-title { text-align: center; font-size: 38px; font-weight: bold; margin-bottom: 25px; }
    
    /* Estilo Pílula */
    div.stButton > button:first-child {
        height: 65px; width: 100%; border-radius: 35px; border: none;
        color: white; font-weight: bold; font-size: 16px; margin-bottom: 8px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    
    /* Box Verde de Atributos */
    .stats-box {
        background-color: #1B5E20; padding: 20px; border-radius: 15px; color: white;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. MOTOR DE ESTADOS ---
if 'pagina' not in st.session_state: st.session_state.pagina = 'login'
if 'treino_selecionado' not in st.session_state: st.session_state.treino_selecionado = None

# Sincronização via URL
params = st.query_params
if "score" in params:
    st.session_state.pontuacao_final = int(params["score"])
    st.session_state.pagina = 'relatorio_drible'

# --- 3. LÓGICA DE EVOLUÇÃO ---
def processar_drible(pontos):
    if pontos >= 2500: return "OURO (ELITE)", 3
    elif pontos >= 1500: return "PRATA (PROFISSIONAL)", 1
    else: return "BRONZE (INSUFICIENTE)", 0

# --- 4. FLUXO DE TELAS ---

# LOGIN
if st.session_state.pagina == 'login':
    st.markdown("<h1 class='ct-title'>🛡️ GOAT TV LOGIN</h1>", unsafe_allow_html=True)
    pin = st.text_input("PIN DE ATLETA:", type="password")
    if st.button("ACESSAR SISTEMA", use_container_width=True):
        if pin == "2026": st.session_state.pagina = 'hub'; st.rerun()

# HUB (FUNDAMENTOS)
elif st.session_state.pagina == 'hub':
    st.markdown("<h1 class='ct-title'>CENTRO DE TREINAMENTO</h1>", unsafe_allow_html=True)
    
    # Vamos focar no DRIBLE hoje
    st.markdown("<style>div.stButton > button[key='t_0'] { background: linear-gradient(90deg, #4A90E2, #50E3C2) !important; }</style>", unsafe_allow_html=True)
    if st.button("⚽ DRIBLE", key="t_0", use_container_width=True):
        st.session_state.pagina = 'treino_drible'
        st.rerun()
    
    st.info("Outros fundamentos em calibração...")

# SALA DE TREINO (O PERCURSO DE CONES)
elif st.session_state.pagina == 'treino_drible':
    st.markdown("<h2 style='text-align: center;'>TREINO DE DRIBLE (CONES)</h2>", unsafe_allow_html=True)
    
    # Mini-game de Drible: Arrastar a bola pelos cones
    game_html = """
    <div id="field" style="height:400px; width:100%; background-color:#0D47A1; border-radius:30px; position:relative; overflow:hidden; border: 4px solid #08306B;">
        <div id="player" style="width:40px; height:40px; background:white; border-radius:50%; position:absolute; left:20px; top:180px; z-index:10; border: 2px solid #333; cursor:grab;">⚽</div>
        <div id="finish" style="width:20px; height:100%; background:yellow; position:absolute; right:0; top:0;"></div>
        
        <div class="cone" style="width:30px; height:30px; background:orange; position:absolute; left:120px; top:100px; border-radius:50%;"></div>
        <div class="cone" style="width:30px; height:30px; background:orange; position:absolute; left:200px; top:250px; border-radius:50%;"></div>
        <div class="cone" style="width:30px; height:30px; background:orange; position:absolute; left:280px; top:100px; border-radius:50%;"></div>
        
        <div id="score-live" style="position:absolute; top:10px; left:10px; font-weight:bold;">Pontos: 0</div>
        <div id="timer" style="position:absolute; top:10px; right:10px; font-weight:bold;">Tempo: 10.0s</div>
    </div>

    <script>
        const player = document.getElementById('player');
        const field = document.getElementById('field');
        const scoreDisplay = document.getElementById('score-live');
        const timerDisplay = document.getElementById('timer');
        let score = 0;
        let timeLeft = 10.0;
        let active = false;
        let conesHit = new Set();

        player.onmousedown = () => { active = true; player.style.cursor = 'grabbing'; };
        window.onmouseup = () => { active = false; player.style.cursor = 'grab'; };

        window.onmousemove = (e) => {
            if(!active || timeLeft <= 0) return;
            const rect = field.getBoundingClientRect();
            let x = e.clientX - rect.left - 20;
            let y = e.clientY - rect.top - 20;
            
            player.style.left = Math.max(0, Math.min(x, rect.width - 40)) + 'px';
            player.style.top = Math.max(0, Math.min(y, rect.height - 40)) + 'px';

            // Detectar Cones
            document.querySelectorAll('.cone').forEach((cone, index) => {
                const cRect = cone.getBoundingClientRect();
                const pRect = player.getBoundingClientRect();
                if(!(pRect.right < cRect.left || pRect.left > cRect.right || pRect.bottom < cRect.top || pRect.top > cRect.bottom)) {
                    if(!conesHit.has(index)) {
                        conesHit.add(index);
                        score += 20;
                        cone.style.opacity = '0.3';
                        scoreDisplay.innerHTML = "Pontos: " + score;
                    }
                }
            });

            // Detectar Fim
            if(x > rect.width - 60) {
                const finalScore = score + 500 + Math.round(timeLeft * 100);
                window.parent.location.href = window.parent.location.href.split('?')[0] + "?score=" + finalScore;
            }
        };

        setInterval(() => {
            if(active && timeLeft > 0) {
                timeLeft -= 0.1;
                timerDisplay.innerHTML = "Tempo: " + timeLeft.toFixed(1) + "s";
                if(timeLeft <= 0) {
                   window.parent.location.href = window.parent.location.href.split('?')[0] + "?score=" + score;
                }
            }
        }, 100);
    </script>
    """
    components.html(game_html, height=450)
    st.write("Guie a bola (⚽) até a linha amarela passando pelos cones laranjas!")

# RELATÓRIO DE DRIBLE
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
    
    if val > 0: st.balloons()
    if st.button("FINALIZAR TREINO", use_container_width=True):
        st.query_params.clear()
        st.session_state.pagina = 'hub'
        st.rerun()
