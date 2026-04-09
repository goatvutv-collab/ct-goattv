import streamlit as st
import streamlit.components.v1 as components

# --- 1. CONFIGURAÇÃO E ESTILO (DESIGN CANVA PRO) ---
st.set_page_config(page_title="GOAT TV - CT DIGITAL", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0E0E2C; color: #FFFFFF; font-family: 'sans-serif'; }
    .ct-title { text-align: center; font-size: 38px; font-weight: bold; margin-bottom: 25px; }
    
    /* Estilo Pílulas do Hub */
    div.stButton > button:first-child {
        height: 70px; width: 100%; border-radius: 35px; border: none;
        color: white; font-weight: bold; font-size: 18px; margin-bottom: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4);
        transition: 0.3s;
    }
    div.stButton > button:hover { transform: translateY(-5px); filter: brightness(1.2); }

    /* Box de Atributos do Relatório */
    .stats-box { background-color: #1B5E20; padding: 20px; border-radius: 15px; color: white; }
    iframe { border-radius: 30px; border: none; }
    </style>
""", unsafe_allow_html=True)

# --- 2. MOTOR DE ESTADOS ---
if 'pagina' not in st.session_state: st.session_state.pagina = 'login'
if 'resultado_ms' not in st.session_state: st.session_state.resultado_ms = None

# Sincronização via URL (Pega pontos ou tempo)
params = st.query_params
if "score" in params:
    st.session_state.pontos_drible = int(params["score"])
    st.session_state.pagina = 'relatorio_drible'
elif "time" in params:
    st.session_state.tempo_velocidade = float(params["time"])
    st.session_state.pagina = 'relatorio_velocidade'

# --- 3. LÓGICAS DE EVOLUÇÃO ---
def calcular_drible(pts):
    if pts >= 2500: return "OURO (ELITE)", 3
    elif pts >= 1500: return "PRATA (PROFISS.)", 1
    else: return "BRONZE", 0

def calcular_velocidade(t):
    if t < 6.0: return "OURO (ELITE)", 3
    elif t < 9.0: return "PRATA (PROFISS.)", 1
    else: return "BRONZE", 0

# --- 4. FLUXO DE TELAS ---

# LOGIN
if st.session_state.pagina == 'login':
    st.markdown("<h1 class='ct-title'>🛡️ GOAT TV LOGIN</h1>", unsafe_allow_html=True)
    pin = st.text_input("PIN DE ATLETA:", type="password")
    if st.button("ACESSAR CT", use_container_width=True):
        if pin == "2026": st.session_state.pagina = 'hub'; st.rerun()

# HUB UNIFICADO (IMAGEM 1 DO CANVA)
elif st.session_state.pagina == 'hub':
    st.markdown("<h1 class='ct-title'>CT DE TREINAMENTO</h1>", unsafe_allow_html=True)
    
    cols = st.columns(2)
    
    # Pílula 1: Drible
    st.markdown("<style>div.stButton > button[key='btn_d'] { background: linear-gradient(90deg, #4A90E2, #50E3C2) !important; }</style>", unsafe_allow_html=True)
    if cols[0].button("⚽ DRIBLE", key="btn_d"):
        st.session_state.pagina = 'treino_drible'
        st.rerun()

    # Pílula 2: Velocidade
    st.markdown("<style>div.stButton > button[key='btn_v'] { background: linear-gradient(90deg, #7C5CFF, #C75CFF) !important; }</style>", unsafe_allow_html=True)
    if cols[1].button("⚡ VELOCIDADE", key="btn_v"):
        st.session_state.pagina = 'treino_velocidade'
        st.rerun()

    st.info("Mais fundamentos sendo instalados pelo Comissário...")

# SALA 1: DRIBLE (CONES)
elif st.session_state.pagina == 'treino_drible':
    st.markdown("<h2 style='text-align: center;'>FUNDAMENTO: DRIBLE</h2>", unsafe_allow_html=True)
    game_html = """
    <div id="field" style="height:350px; width:100%; background-color:#0D47A1; border-radius:25px; position:relative; overflow:hidden; border:4px solid #08306B;">
        <div id="player" style="width:40px; height:40px; background:white; border-radius:50%; position:absolute; left:20px; top:150px; z-index:10; border:2px solid #333; display:flex; justify-content:center; align-items:center;">⚽</div>
        <div id="finish" style="width:15px; height:100%; background:yellow; position:absolute; right:0; top:0;"></div>
        <div class="cone" style="width:25px; height:25px; background:orange; position:absolute; left:100px; top:80px; border-radius:50%;"></div>
        <div class="cone" style="width:25px; height:25px; background:orange; position:absolute; left:180px; top:220px; border-radius:50%;"></div>
        <div class="cone" style="width:25px; height:25px; background:orange; position:absolute; left:260px; top:80px; border-radius:50%;"></div>
        <div id="hud" style="position:absolute; top:10px; width:100%; display:flex; justify-content:space-around; color:white; font-weight:bold;">
            <span id="s">PONTOS: 0</span> <span id="t">TEMPO: 15.0s</span>
        </div>
    </div>
    <div id="ctrls" style="display:grid; grid-template-columns: repeat(3, 1fr); gap:10px; width:180px; margin:15px auto;">
        <div></div><button class="b" id="up" style="height:50px; background:#444; color:white; border-radius:10px; border:none;">▲</button><div></div>
        <button class="b" id="left" style="height:50px; background:#444; color:white; border-radius:10px; border:none;">◀</button>
        <button id="go" style="height:50px; background:#4CAF50; color:white; border-radius:10px; border:none; font-weight:bold;">GO!</button>
        <button class="b" id="right" style="height:50px; background:#444; color:white; border-radius:10px; border:none;">▶</button>
        <div></div><button class="b" id="down" style="height:50px; background:#444; color:white; border-radius:10px; border:none;">▼</button><div></div>
    </div>
    <script>
        const p = document.getElementById('player'); const f = document.getElementById('field'); const go = document.getElementById('go');
        let x=20, y=150, score=0, time=15.0, run=false, cones=new Set(), move={up:false,down:false,left:false,right:false};
        const setup = (id, d) => { 
            const b = document.getElementById(id); 
            b.onpointerdown=()=>{if(run)move[d]=true}; b.onpointerup=()=>move[d]=false; b.onpointerleave=()=>move[d]=false;
        };
        setup('up','up'); setup('down','down'); setup('left','left'); setup('right','right');
        go.onclick=()=>{if(!run){run=true; go.style.opacity='0.5';}};
        function loop(){
            if(run && time>0){
                time-=0.02; if(move.up && y>0)y-=4; if(move.down && y<f.offsetHeight-40)y+=4;
                if(move.left && x>0)x-=4; if(move.right && x<f.offsetWidth-40)x+=4;
                p.style.left=x+'px'; p.style.top=y+'px';
                document.querySelectorAll('.cone').forEach((c,i)=>{
                    const cr=c.getBoundingClientRect(); const pr=p.getBoundingClientRect();
                    if(!(pr.right<cr.left||pr.left>cr.right||pr.bottom<cr.top||pr.top>cr.bottom)){
                        if(!cones.has(i)){cones.add(i); score+=100; c.style.opacity='0.2';}
                    }
                });
                if(x > f.offsetWidth-55){
                    const final = score + 500 + Math.round(time*100);
                    window.parent.location.href = window.parent.location.href.split('?')[0] + "?score=" + final;
                    run=false;
                }
                document.getElementById('s').innerHTML="PONTOS: "+score; document.getElementById('t').innerHTML="TEMPO: "+time.toFixed(1)+"s";
            }
            requestAnimationFrame(loop);
        }
        loop();
    </script>
    """
    components.html(game_html, height=600)
    if st.button("⬅️ VOLTAR"): st.session_state.pagina='hub'; st.rerun()

# SALA 2: VELOCIDADE (SPRINT)
elif st.session_state.pagina == 'treino_velocidade':
    st.markdown("<h2 style='text-align: center;'>FUNDAMENTO: VELOCIDADE</h2>", unsafe_allow_html=True)
    game_html = """
    <div id="f" style="height:350px; width:100%; background-color:#0D47A1; border-radius:25px; position:relative; overflow:hidden; border:4px solid #08306B;">
        <div id="p" style="width:40px; height:40px; background:white; border-radius:50%; position:absolute; left:20px; top:150px; border:2px solid #333;">⚽</div>
        <div style="width:15px; height:100%; background:yellow; position:absolute; right:0; top:0;"></div>
        <div id="tm" style="position:absolute; top:10px; right:10px; font-weight:bold; color:white; font-size:24px;">0.00s</div>
    </div>
    <div id="ctrls" style="display:grid; grid-template-columns: repeat(3, 1fr); gap:10px; width:180px; margin:15px auto;">
        <div></div><button class="b" id="up" style="height:50px; background:#444; border:none; border-radius:10px; color:white;">▲</button><div></div>
        <button class="b" id="left" style="height:50px; background:#444; border:none; border-radius:10px; color:white;">◀</button>
        <button id="go" style="height:50px; background:#4CAF50; border:none; border-radius:10px; color:white; font-weight:bold;">GO!</button>
        <button class="b" id="right" style="height:50px; background:#444; border:none; border-radius:10px; color:white;">▶</button>
        <div></div><button class="b" id="down" style="height:50px; background:#444; border:none; border-radius:10px; color:white;">▼</button><div></div>
    </div>
    <script>
        const p=document.getElementById('p'); const f=document.getElementById('f'); const go=document.getElementById('go');
        let x=20, y=150, t=0.00, run=false, mv={up:false,down:false,left:false,right:false};
        const s=(id,d)=>{const b=document.getElementById(id); b.onpointerdown=()=>{if(run)mv[d]=true}; b.onpointerup=()=>mv[d]=false; b.onpointerleave=()=>mv[d]=false;};
        s('up','up'); s('down','down'); s('left','left'); s('right','right');
        go.onclick=()=>{if(!run){run=true; go.style.opacity='0.5';}};
        function loop(){
            if(run){
                t+=0.016; document.getElementById('tm').innerHTML=t.toFixed(2)+"s";
                if(mv.up && y>0)y-=5; if(mv.down && y<f.offsetHeight-40)y+=5;
                if(mv.left && x>0)x-=5; if(mv.right && x<f.offsetWidth-40)x+=8;
                p.style.left=x+'px'; p.style.top=y+'px';
                if(x > f.offsetWidth-55){ window.parent.location.href = window.parent.location.href.split('?')[0] + "?time=" + t.toFixed(2); run=false; }
            }
            requestAnimationFrame(loop);
        }
        loop();
    </script>
    """
    components.html(game_html, height=600)
    if st.button("⬅️ VOLTAR"): st.session_state.pagina='hub'; st.rerun()

# RELATÓRIOS ESPECÍFICOS
elif st.session_state.pagina == 'relatorio_drible':
    pts = st.session_state.pontos_drible
    nivel, val = calcular_drible(pts)
    st.markdown(f"<h2>RESULTADO: DRIBLE</h2>", unsafe_allow_html=True)
    st.markdown(f"<div class='stats-box'>✔️ Drible / Controle<br><b>+ {val} Pontos</b><br><br>❌ Defesa / Físico<br><b>- {val} Pontos</b></div>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align:center;'>{pts} PTS ({nivel})</h1>", unsafe_allow_html=True)
    if st.button("CONCLUIR"): st.query_params.clear(); st.session_state.pagina='hub'; st.rerun()

elif st.session_state.pagina == 'relatorio_velocidade':
    tm = st.session_state.tempo_velocidade
    nivel, val = calcular_velocidade(tm)
    st.markdown(f"<h2>RESULTADO: VELOCIDADE</h2>", unsafe_allow_html=True)
    st.markdown(f"<div class='stats-box'>✔️ Velocidade / Explosão<br><b>+ {val} Pontos</b><br><br>❌ Contato Físico<br><b>- {val} Pontos</b></div>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align:center;'>{tm}s ({nivel})</h1>", unsafe_allow_html=True)
    if st.button("CONCLUIR"): st.query_params.clear(); st.session_state.pagina='hub'; st.rerun()
