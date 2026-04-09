import streamlit as st
import streamlit.components.v1 as components

# --- 1. CONFIGURAÇÃO E ESTILO (SIMETRIA E DESIGN PREMIUM) ---
st.set_page_config(page_title="GOAT TV - CT DIGITAL", layout="centered")

st.markdown("""
    <style>
    /* Fundo Dark Mode Profundo */
    .stApp { background-color: #0E0E2C; color: #FFFFFF; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    
    .ct-title { text-align: center; font-size: 32px; font-weight: 800; margin-bottom: 30px; letter-spacing: 1px; color: #FFD700; }

    /* FORÇAR SIMETRIA NAS PÍLULAS */
    div.stButton > button {
        width: 100% !important;
        height: 70px !important;
        border-radius: 50px !important; /* Formato Balão/Pílula Perfeito */
        border: none !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 18px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4) !important;
        transition: all 0.3s ease !important;
        margin-bottom: 10px !important;
    }
    
    div.stButton > button:hover { transform: translateY(-3px); box-shadow: 0 6px 20px rgba(0,0,0,0.6); filter: brightness(1.2); }

    /* Estilo dos Boxes de Relatório */
    .stats-box { background-color: #1B5E20; padding: 25px; border-radius: 20px; border: 1px solid #2E7D32; }
    
    /* Iframe do Jogo */
    iframe { border-radius: 30px; border: 2px solid #1E3A8A; background-color: #0D47A1; }
    
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 2. MOTOR DE ESTADOS ---
if 'pagina' not in st.session_state: st.session_state.pagina = 'login'

params = st.query_params
if "score" in params:
    st.session_state.pontos_drible = int(params["score"])
    st.session_state.pagina = 'relatorio_drible'
elif "time" in params:
    st.session_state.tempo_velocidade = float(params["time"])
    st.session_state.pagina = 'relatorio_velocidade'

# --- 3. LÓGICAS DE CÁLCULO ---
def calc_drible(pts):
    if pts >= 2500: return "OURO", 3
    elif pts >= 1500: return "PRATA", 1
    return "BRONZE", 0

def calc_vel(t):
    if t < 5.5: return "ELITE", 3
    elif t < 8.5: return "PROFISS.", 1
    return "LENTO", 0

# --- 4. FLUXO DE TELAS ---

# LOGIN
if st.session_state.pagina == 'login':
    st.markdown("<h1 class='ct-title'>🛡️ ACESSO CT GOAT TV</h1>", unsafe_allow_html=True)
    pin = st.text_input("PIN DO ATLETA:", type="password")
    if st.button("ENTRAR", use_container_width=True):
        if pin == "2026": st.session_state.pagina = 'hub'; st.rerun()

# HUB (SIMÉTRICO E BONITO)
elif st.session_state.pagina == 'hub':
    st.markdown("<h1 class='ct-title'>CENTRO DE TREINAMENTO</h1>", unsafe_allow_html=True)
    
    # Criando colunas para garantir que os botões fiquem alinhados
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<style>div.stButton > button[key='btn_d'] { background: linear-gradient(135deg, #4A90E2, #357ABD) !important; }</style>", unsafe_allow_html=True)
        if st.button("⚽ DRIBLE", key="btn_d"):
            st.session_state.pagina = 'treino_drible'; st.rerun()

    with col2:
        st.markdown("<style>div.stButton > button[key='btn_v'] { background: linear-gradient(135deg, #7C5CFF, #5A3ECC) !important; }</style>", unsafe_allow_html=True)
        if st.button("⚡ VELOCIDADE", key="btn_v"):
            st.session_state.pagina = 'treino_velocidade'; st.rerun()
            
    st.info("💡 Fundamentos de Passe, Chute e Defesa em calibração técnica.")

# SALA: VELOCIDADE (LABIRINTO INVISÍVEL)
elif st.session_state.pagina == 'treino_velocidade':
    st.markdown("<h2 style='text-align: center;'>⚡ SPRINT COGNITIVO</h2>", unsafe_allow_html=True)
    game_html = """
    <div id="f" style="height:350px; width:100%; background-color:#0D47A1; border-radius:25px; position:relative; overflow:hidden;">
        <div id="p" style="width:36px; height:36px; background:white; border-radius:50%; position:absolute; left:15px; top:150px; border:2px solid #333; z-index:20;">⚽</div>
        <div style="width:15px; height:100%; background:yellow; position:absolute; right:0; top:0;"></div>
        <div id="tm" style="position:absolute; top:10px; right:10px; font-weight:bold; color:white; font-size:24px;">0.00s</div>
        <div class="wall" style="position:absolute; background:#0D47A1; width:30px; height:120px; left:120px; top:0;"></div>
        <div class="wall" style="position:absolute; background:#0D47A1; width:30px; height:120px; left:120px; bottom:0;"></div>
        <div class="wall" style="position:absolute; background:#0D47A1; width:30px; height:120px; left:250px; top:110px;"></div>
    </div>
    <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:10px; width:180px; margin:20px auto;">
        <div></div><button class="b" id="up" style="height:55px; background:#444; border-radius:15px; color:white; border:none;">▲</button><div></div>
        <button class="b" id="left" style="height:55px; background:#444; border-radius:15px; color:white; border:none;">◀</button>
        <button id="go" style="height:55px; background:#4CAF50; border-radius:15px; color:white; font-weight:bold; border:none;">GO!</button>
        <button class="b" id="right" style="height:55px; background:#444; border-radius:15px; color:white; border:none;">▶</button>
        <div></div><button class="b" id="down" style="height:55px; background:#444; border-radius:15px; color:white; border:none;">▼</button><div></div>
    </div>
    <script>
        const p=document.getElementById('p'); const f=document.getElementById('f'); const go=document.getElementById('go');
        let x=15, y=150, t=0.00, run=false, mv={up:false,down:false,left:false,right:false};
        const walls = document.querySelectorAll('.wall');
        const s=(id,d)=>{const b=document.getElementById(id); b.onpointerdown=()=>{if(run)mv[d]=true}; b.onpointerup=()=>mv[d]=false; b.onpointerleave=()=>mv[d]=false;};
        s('up','up'); s('down','down'); s('left','left'); s('right','right');
        go.onclick=()=>{if(!run){run=true; go.style.opacity='0.5';}};
        function checkCollision(nx, ny) {
            let collision = false;
            const pr = {left: nx, right: nx+36, top: ny, bottom: ny+36};
            walls.forEach(w => {
                const wr = {left: w.offsetLeft, right: w.offsetLeft+30, top: w.offsetTop, bottom: w.offsetTop+w.offsetHeight};
                if (!(pr.right < wr.left || pr.left > wr.right || pr.bottom < wr.top || pr.top > wr.bottom)) collision = true;
            });
            return collision;
        }
        function loop(){
            if(run){
                t+=0.016; document.getElementById('tm').innerHTML=t.toFixed(2)+"s";
                let dx=0, dy=0;
                if(mv.up) dy-=5; if(mv.down) dy+=5; if(mv.left) dx-=5; if(mv.right) dx+=8;
                if(!checkCollision(x + dx, y)) x += dx;
                if(!checkCollision(x, y + dy)) y += dy;
                x = Math.max(0, Math.min(x, f.offsetWidth - 36));
                y = Math.max(0, Math.min(y, f.offsetHeight - 36));
                p.style.left=x+'px'; p.style.top=y+'px';
                if(x > f.offsetWidth-50){ window.parent.location.href = window.parent.location.href.split('?')[0] + "?time=" + t.toFixed(2); run=false; }
            }
            requestAnimationFrame(loop);
        }
        loop();
    </script>
    """
    components.html(game_html, height=600)
    if st.button("⬅️ VOLTAR AO HUB"): st.session_state.pagina='hub'; st.rerun()

# RELATÓRIOS
elif st.session_state.pagina == 'relatorio_velocidade':
    tm = st.session_state.tempo_velocidade
    nivel, val = calc_vel(tm)
    st.markdown(f"<div class='stats-box'><h3>RELATÓRIO: {nivel}</h3>✔️ Velocidade / Aceleração<br><b>+ {val} Pontos</b><br><br>❌ Contato Físico<br><b>- {val} Pontos</b></div>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align:center;'>{tm}s</h1>", unsafe_allow_html=True)
    if st.button("CONCLUIR TREINO"): st.query_params.clear(); st.session_state.pagina='hub'; st.rerun()

# O Treino de Drible segue a mesma lógica simétrica...
