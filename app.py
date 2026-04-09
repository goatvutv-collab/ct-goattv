import streamlit as st
import streamlit.components.v1 as components

# --- 1. ESTILO PREMIUM (CANVA + SIMETRIA) ---
st.set_page_config(page_title="GOAT TV - CT DIGITAL", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0E0E2C; color: #FFFFFF; font-family: 'sans-serif'; }
    .ct-title { text-align: center; font-size: 32px; font-weight: 800; color: #FFD700; margin-bottom: 20px; }
    
    /* Pílulas Simétricas */
    div.stButton > button {
        width: 100% !important; height: 65px !important;
        border-radius: 50px !important; border: none !important;
        color: white !important; font-weight: 700 !important; font-size: 18px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4) !important;
        margin-bottom: 10px !important;
    }
    .stats-box { background-color: #1B5E20; padding: 25px; border-radius: 20px; border: 1px solid #2E7D32; }
    iframe { border-radius: 30px; border: 3px solid #1E3A8A; }
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
    if pts >= 2500: return "🏆 OURO", 3
    elif pts >= 1500: return "✅ PRATA", 1
    return "❌ BRONZE", 0

def calc_vel(t):
    if t < 7.0: return "🏆 ELITE (OURO)", 3
    elif t < 10.0: return "✅ PROFISS. (PRATA)", 1
    return "❌ LENTO (BRONZE)", 0

# --- 4. FLUXO DE TELAS ---

# LOGIN
if st.session_state.pagina == 'login':
    st.markdown("<h1 class='ct-title'>🛡️ ACESSO CT GOAT TV</h1>", unsafe_allow_html=True)
    pin = st.text_input("PIN DO ATLETA:", type="password")
    if st.button("ENTRAR", use_container_width=True):
        if pin == "2026": st.session_state.pagina = 'hub'; st.rerun()

# HUB (SIMÉTRICO)
elif st.session_state.pagina == 'hub':
    st.markdown("<h1 class='ct-title'>CT DE TREINAMENTO</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<style>div.stButton > button[key='btn_d'] { background: linear-gradient(135deg, #4A90E2, #357ABD) !important; }</style>", unsafe_allow_html=True)
        if st.button("⚽ DRIBLE", key="btn_d"):
            st.session_state.pagina = 'treino_drible'; st.rerun()
    with col2:
        st.markdown("<style>div.stButton > button[key='btn_v'] { background: linear-gradient(135deg, #7C5CFF, #5A3ECC) !important; }</style>", unsafe_allow_html=True)
        if st.button("⚡ VELOCIDADE", key="btn_v"):
            st.session_state.pagina = 'treino_velocidade'; st.rerun()

# SALA: DRIBLE (HORIZONTAL COM CONES VISÍVEIS)
elif st.session_state.pagina == 'treino_drible':
    st.markdown("<h2 style='text-align: center;'>⚽ DRIBLE DE PRECISÃO</h2>", unsafe_allow_html=True)
    game_html = """
    <div id="f" style="height:350px; width:100%; background-color:#0D47A1; border-radius:25px; position:relative; overflow:hidden;">
        <div id="p" style="width:40px; height:40px; background:white; border-radius:50%; position:absolute; left:20px; top:150px; border:2px solid #333; display:flex; justify-content:center; align-items:center;">⚽</div>
        <div style="width:15px; height:100%; background:yellow; position:absolute; right:0; top:0;"></div>
        <div class="cone" style="width:25px; height:25px; background:orange; position:absolute; left:100px; top:80px; border-radius:50%;"></div>
        <div class="cone" style="width:25px; height:25px; background:orange; position:absolute; left:180px; top:220px; border-radius:50%;"></div>
        <div class="cone" style="width:25px; height:25px; background:orange; position:absolute; left:260px; top:80px; border-radius:50%;"></div>
        <div id="hud" style="position:absolute; top:10px; width:100%; display:flex; justify-content:space-around; color:white; font-weight:bold;">
            <span id="s">PONTOS: 0</span> <span id="t">TEMPO: 15.0s</span>
        </div>
    </div>
    <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:10px; width:180px; margin:15px auto;">
        <div></div><button class="b" id="up" style="height:55px; background:#444; border-radius:15px; color:white; border:none;">▲</button><div></div>
        <button class="b" id="left" style="height:55px; background:#444; border-radius:15px; color:white; border:none;">◀</button>
        <button id="go" style="height:55px; background:#4CAF50; border-radius:15px; color:white; font-weight:bold; border:none;">GO!</button>
        <button class="b" id="right" style="height:55px; background:#444; border-radius:15px; color:white; border:none;">▶</button>
        <div></div><button class="b" id="down" style="height:55px; background:#444; border-radius:15px; color:white; border:none;">▼</button><div></div>
    </div>
    <script>
        const p=document.getElementById('p'); const f=document.getElementById('f'); const go=document.getElementById('go');
        let x=20, y=150, score=0, time=15.0, run=false, cones=new Set(), mv={up:false,down:false,left:false,right:false};
        const s=(id,d)=>{ const b=document.getElementById(id); b.onpointerdown=()=>{if(run)mv[d]=true}; b.onpointerup=()=>mv[d]=false; b.onpointerleave=()=>mv[d]=false; };
        s('up','up'); s('down','down'); s('left','left'); s('right','right');
        go.onclick=()=>{if(!run){run=true; go.style.opacity='0.5';}};
        function loop(){
            if(run && time>0){
                time-=0.02; if(mv.up && y>0)y-=4; if(mv.down && y<f.offsetHeight-40)y+=4;
                if(mv.left && x>0)x-=4; if(mv.right && x<f.offsetWidth-40)x+=4;
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

# SALA: VELOCIDADE (VERTICAL COM BARREIRAS FANTASMAS)
elif st.session_state.pagina == 'treino_velocidade':
    st.markdown("<h2 style='text-align: center;'>⚡ GHOST GAUNTLET</h2>", unsafe_allow_html=True)
    game_html = """
    <div id="f" style="height:500px; width:100%; background-color:#0D47A1; border-radius:30px; position:relative; overflow:hidden; transition: background 0.1s;">
        <div id="p" style="width:34px; height:34px; background:white; border-radius:50%; position:absolute; left:45%; bottom:20px; border:2px solid #333; z-index:20;">⚽</div>
        <div id="finish" style="width:100%; height:15px; background:yellow; position:absolute; top:0; left:0;"></div>
        <div id="tm" style="position:absolute; top:20px; right:20px; font-weight:bold; color:white; font-size:24px;">0.00s</div>
    </div>
    <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:10px; width:180px; margin:15px auto;">
        <div></div><button class="b" id="up" style="height:55px; background:#444; border-radius:15px; color:white; border:none;">▲</button><div></div>
        <button class="b" id="left" style="height:55px; background:#444; border-radius:15px; color:white; border:none;">◀</button>
        <button id="go" style="height:55px; background:#4CAF50; border-radius:15px; color:white; font-weight:bold; border:none;">GO!</button>
        <button class="b" id="right" style="height:55px; background:#444; border-radius:15px; color:white; border:none;">▶</button>
        <div></div><button class="b" id="down" style="height:55px; background:#444; border-radius:15px; color:white; border:none;">▼</button><div></div>
    </div>
    <script>
        const p=document.getElementById('p'); const f=document.getElementById('f'); const go=document.getElementById('go');
        let x=f.offsetWidth/2-17, y=450, t=0.00, run=false, mv={up:false,down:false,left:false,right:false};
        const walls = [];
        for(let i=0; i<8; i++){
            let w = document.createElement('div'); w.className='w'; w.style.position='absolute'; w.style.background='#0D47A1';
            w.style.width=(40+Math.random()*60)+'px'; w.style.height='40px';
            w.style.left=Math.random()*(f.offsetWidth-60)+'px'; w.style.top=(60+Math.random()*340)+'px';
            f.appendChild(w); walls.push(w);
        }
        const s=(id,d)=>{ const b=document.getElementById(id); b.onpointerdown=()=>{if(run)mv[d]=true}; b.onpointerup=()=>mv[d]=false; b.onpointerleave=()=>mv[d]=false; };
        s('up','up'); s('down','down'); s('left','left'); s('right','right');
        go.onclick=()=>{if(!run){run=true; go.style.opacity='0.5';}};
        function checkCol(nx, ny) {
            const pr = {l: nx, r: nx+34, t: ny, b: ny+34};
            for(let w of walls){
                const wr = {l: w.offsetLeft, r: w.offsetLeft+w.offsetWidth, t: w.offsetTop, b: w.offsetTop+w.offsetHeight};
                if (!(pr.r < wr.l || pr.l > wr.r || pr.b < wr.t || pr.t > wr.b)) return true;
            }
            return false;
        }
        function loop(){
            if(run){
                t+=0.016; document.getElementById('tm').innerHTML=t.toFixed(2)+"s";
                let dx=0, dy=0;
                if(mv.up) dy-=7; if(mv.down) dy+=5; if(mv.left) dx-=6; if(mv.right) dx+=6;
                if(!checkCol(x+dx, y)) x+=dx; else f.style.background='#1A3A8A';
                if(!checkCol(x, y+dy)) y+=dy; else f.style.background='#1A3A8A';
                if(!mv.up && !mv.down && !mv.left && !mv.right) f.style.background='#0D47A1';
                x=Math.max(0,Math.min(x,f.offsetWidth-34)); y=Math.max(0,Math.min(y,f.offsetHeight-34));
                p.style.left=x+'px'; p.style.top=y+'px';
                if(y < 10){ window.parent.location.href=window.parent.location.href.split('?')[0]+"?time="+t.toFixed(2); run=false; }
            }
            requestAnimationFrame(loop);
        }
        loop();
    </script>
    """
    components.html(game_html, height=750)
    if st.button("⬅️ VOLTAR"): st.session_state.pagina='hub'; st.rerun()

# RELATÓRIOS
elif st.session_state.pagina == 'relatorio_drible':
    pts = st.session_state.pontos_drible
    nivel, val = calc_drible(pts)
    st.markdown(f"<div class='stats-box'><h3>SISTEMA GOAT TV: {nivel}</h3>✔️ Drible / Controle<br><b>+ {val} Pontos</b><br><br>❌ Defesa / Físico<br><b>- {val} Pontos</b></div>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align:center;'>{pts} PTS</h1>", unsafe_allow_html=True)
    if st.button("CONCLUIR"): st.query_params.clear(); st.session_state.pagina='hub'; st.rerun()

elif st.session_state.pagina == 'relatorio_velocidade':
    tm = st.session_state.tempo_velocidade
    nivel, val = calc_vel(tm)
    st.markdown(f"<div class='stats-box'><h3>SISTEMA GOAT TV: {nivel}</h3>✔️ Velocidade / Explosão<br><b>+ {val} Pontos</b><br><br>❌ Contato Físico<br><b>- {val} Pontos</b></div>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align:center;'>{tm}s</h1>", unsafe_allow_html=True)
    if st.button("CONCLUIR"): st.query_params.clear(); st.session_state.pagina='hub'; st.rerun()
