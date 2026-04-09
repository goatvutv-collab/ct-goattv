import streamlit as st
import streamlit.components.v1 as components

# --- 1. ESTILO PREMIUM (CANVA + SIMETRIA) ---
st.set_page_config(page_title="GOAT TV - ANALOG CT", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0E0E2C; color: #FFFFFF; font-family: 'sans-serif'; }
    .ct-title { text-align: center; font-size: 32px; font-weight: 800; color: #FFD700; margin-bottom: 20px; }
    
    div.stButton > button {
        width: 100% !important; height: 65px !important;
        border-radius: 50px !important; border: none !important;
        color: white !important; font-weight: 700 !important; font-size: 18px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4) !important;
        margin-bottom: 10px !important;
        display: flex !important; align-items: center !important; justify-content: center !important;
    }
    .stats-box { background-color: #1B5E20; padding: 25px; border-radius: 20px; border: 1px solid #2E7D32; }
    iframe { border-radius: 30px; border: none; background: transparent; }
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

# --- 3. LÓGICAS DE PONTUAÇÃO ---
def calc_drible(pts):
    if pts >= 2800: return "🏆 OURO (ELITE)", 3
    elif pts >= 1800: return "✅ PRATA (PROFISS.)", 1
    return "❌ BRONZE", 0

def calc_vel(t):
    if t < 6.5: return "🏆 ELITE (OURO)", 3
    elif t < 9.5: return "✅ PROFISS. (PRATA)", 1
    return "❌ LENTO (BRONZE)", 0

# --- 4. FLUXO DE TELAS ---

if st.session_state.pagina == 'login':
    st.markdown("<h1 class='ct-title'>🛡️ ACESSO CT GOAT TV</h1>", unsafe_allow_html=True)
    pin = st.text_input("PIN DO ATLETA:", type="password")
    if st.button("ENTRAR", use_container_width=True):
        if pin == "2026": st.session_state.pagina = 'hub'; st.rerun()

elif st.session_state.pagina == 'hub':
    st.markdown("<h1 class='ct-title'>CENTRO DE TREINAMENTO</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<style>div.stButton > button[key='btn_d'] { background: linear-gradient(135deg, #4A90E2, #357ABD) !important; }</style>", unsafe_allow_html=True)
        if st.button("⚽ DRIBLE (SLALOM VERTICAL)", key="btn_d"):
            st.session_state.pagina = 'treino_drible'; st.rerun()
    with col2:
        st.markdown("<style>div.stButton > button[key='btn_v'] { background: linear-gradient(135deg, #7C5CFF, #5A3ECC) !important; }</style>", unsafe_allow_html=True)
        if st.button("⚡ VELOCIDADE (SPRINT)", key="btn_v"):
            st.session_state.pagina = 'treino_velocidade'; st.rerun()

# SALA: DRIBLE (VERTICAL EXPANDIDO + ANALÓGICO + TRAJETO E SETA)
elif st.session_state.pagina == 'treino_drible':
    st.markdown("<h2 style='text-align:center;'>⚽ SLALOM TÁTICO</h2>", unsafe_allow_html=True)
    game_html = """
    <div id="f" style="height:600px; width:100%; background-color:#0D47A1; border-radius:25px; position:relative; overflow:hidden; border:4px solid #08306B; touch-action:none;">
        <div id="p" style="width:34px; height:34px; background:white; border-radius:50%; position:absolute; left:45%; bottom:20px; z-index:30; border:2px solid #333;">⚽</div>
        <div style="width:100%; height:15px; background:yellow; position:absolute; top:0; left:0; z-index:10;"></div>
        
        <div class="c_g" style="left: 45%; top: 200px;"></div> <div class="gate" id="g1" style="left: 46%; top: 200px;"></div>
        <div class="c" style="left: 20%; top: 350px;"></div> <div class="cone_pair" style="left: 35%; top: 350px;"></div> <div class="gate" id="g2" style="left: 21%; top: 350px; width:15%"></div>
        <div class="c" style="left: 80%; top: 500px;"></div> <div class="cone_pair" style="left: 65%; top: 500px;"></div> <div class="gate" id="g3" style="left: 66%; top: 500px; width:15%"></div>

        <svg id="arrow" style="position:absolute; width:40px; height:40px; left:46%; top:280px; z-index:5; opacity:0.8; transform:rotate(-90deg); transition:transform 0.2s;" viewBox="0 0 24 24">
            <path fill="#FFD700" d="M12 2L4.5 10H8v12h8V10h3.5L12 2z"/>
        </svg>

        <div id="joy_base" style="position:absolute; bottom:20px; left:20px; width:90px; height:90px; background:rgba(255,255,255,0.1); border-radius:50%; z-index:100; border:2px solid rgba(255,255,255,0.2);">
            <div id="joy_stick" style="position:absolute; top:20px; left:20px; width:50px; height:50px; background:rgba(255,255,255,0.4); border-radius:50%;"></div>
        </div>
        <button id="go" style="position:absolute; bottom:30px; right:30px; padding:15px 30px; background:#4CAF50; color:white; border-radius:15px; border:none; font-weight:bold; z-index:100;">GO!</button>
        <div style="position:absolute; top:10px; width:100%; display:flex; justify-content:space-around; color:white; font-weight:bold; z-index:40;">
            <span id="s_val">PONTOS: 0</span> <span id="t_val">15.0s</span>
        </div>
    </div>
    <style>
        .c{width:22px;height:22px;background:orange;border-radius:50%;position:absolute;border:2px solid #CC5500; z-index:20;}
        .c_g{width:22px;height:22px;background:orange;border-radius:50%;position:absolute;border:2px solid #CC5500; z-index:20;}
        .cone_pair{width:22px;height:22px;background:orange;border-radius:50%;position:absolute;border:2px solid #CC5500; z-index:20;}
        .gate{width:10px;background:rgba(255,255,255,0.05);position:absolute;border-left:2px dashed rgba(255,255,255,0.2); height:22px;}
    </style>
    <script>
        const p=document.getElementById('p'), f=document.getElementById('f'), go=document.getElementById('go'), jB=document.getElementById('joy_base'), jS=document.getElementById('joy_stick'), arrow=document.getElementById('arrow');
        let x=f.offsetWidth/2-17, y=540, score=0, time=15.0, run=false, gates=new Set(), jX=0, jY=0, drag=false;
        
        // Checkpoints dos portões (x, y centro de cada portão)
        const checkpoints = [{x: f.offsetWidth/2-11, y: 200}, {x: f.offsetWidth*0.27, y: 350}, {x: f.offsetWidth*0.72, y: 500}, {x: f.offsetWidth/2-17, y: 0}];

        jB.ontouchstart=(e)=>{drag=true; e.preventDefault();};
        window.ontouchmove=(e)=>{ 
            if(!drag)return; 
            let t=e.touches[0], r=jB.getBoundingClientRect(), dx=t.clientX-(r.left+45), dy=t.clientY-(r.top+45), d=Math.min(Math.sqrt(dx*dx+dy*dy), 45), a=Math.atan2(dy,dx); 
            jX=Math.cos(a)*(d/45); jY=Math.sin(a)*(d/45); jS.style.transform=`translate(${jX*35}px, ${jY*35}px)`; 
        };
        window.ontouchend=()=>{drag=false; jX=0; jY=0; jS.style.transform='translate(0,0)';};
        go.onclick=()=>{if(!run){run=true; go.style.display='none';}};

        function checkConeCollision(nx, ny) {
            const cones = [...document.querySelectorAll('.c'), ...document.querySelectorAll('.cone_pair'), ...document.querySelectorAll('.c_g')];
            for(let c of cones) {
                const cx=c.offsetLeft, cy=c.offsetTop, cr=22/2;
                const dist = Math.sqrt(Math.pow(nx+17-(cx+cr),2) + Math.pow(ny+17-(cy+cr),2));
                if(dist < 17+cr) return true;
            }
            return false;
        }

        function rotateArrow() {
            let target = checkpoints[gates.size];
            if(!target) target = checkpoints[3]; // Fim
            let dx = target.x - x;
            let dy = target.y - y;
            let angle = Math.atan2(dy, dx);
            arrow.style.transform = `rotate(${angle}rad)`;
        }

        function loop(){
            if(run && time>0){
                time-=0.016; 
                let nx=x+jX*5.5, ny=y+jY*5.5; // Velocidade tática 360°
                
                if(!checkConeCollision(nx, y)) x=nx;
                if(!checkConeCollision(x, ny)) y=ny;
                
                x=Math.max(0,Math.min(x,f.offsetWidth-34)); y=Math.max(0,Math.min(y,f.offsetHeight-34));
                p.style.left=x+'px'; p.style.top=y+'px';
                
                rotateArrow(); // Seta dinâmica 360°

                // Check Gates
                document.querySelectorAll('.gate').forEach((g,i)=>{
                    const gr=g.getBoundingClientRect(), pr=p.getBoundingClientRect();
                    if(!(pr.right<gr.left||pr.left>gr.right||pr.bottom<gr.top||pr.top>gr.bottom)){
                        if(!gates.has(i)){gates.add(i); score+=400; g.style.background='rgba(0,255,0,0.2)'; g.style.border='none';}
                    }
                });
                if(y<15){ window.parent.location.href=window.parent.location.href.split('?')[0]+"?score="+(score+500+Math.round(time*100)); run=false; }
                document.getElementById('s_val').innerHTML="PONTOS: "+score; document.getElementById('t_val').innerHTML=time.toFixed(1)+"s";
            }
            requestAnimationFrame(loop);
        }
        loop();
    </script>
    """
    components.html(game_html, height=750)
    if st.button("⬅️ VOLTAR AO HUB"): st.session_state.pagina='hub'; st.rerun()

# --- SALA: VELOCIDADE (VERTICAL + ANALÓGICO + FANTASMAS) ---
elif st.session_state.pagina == 'treino_velocidade':
    st.markdown("<h2 style='text-align:center;'>⚡ GHOST GAUNTLET 360°</h2>", unsafe_allow_html=True)
    game_html = """
    <div id="f" style="height:500px; width:100%; background-color:#0D47A1; border-radius:30px; position:relative; overflow:hidden; touch-action:none; transition: background 0.1s;">
        <div id="p" style="width:34px; height:34px; background:white; border-radius:50%; position:absolute; left:45%; bottom:20px; border:2px solid #333; z-index:20;">⚽</div>
        <div style="width:100%; height:15px; background:yellow; position:absolute; top:0; left:0;"></div>
        <div id="tm_ui" style="position:absolute; top:20px; right:20px; font-weight:bold; color:white; font-size:24px;">0.00s</div>
        <div id="jb" style="position:absolute; bottom:20px; left:20px; width:90px; height:90px; background:rgba(255,255,255,0.1); border-radius:50%; z-index:100; border:2px solid rgba(255,255,255,0.2);">
            <div id="js" style="position:absolute; top:20px; left:20px; width:50px; height:50px; background:rgba(255,255,255,0.4); border-radius:50%;"></div>
        </div>
        <button id="go" style="position:absolute; bottom:30px; right:30px; padding:15px 30px; background:#4CAF50; color:white; border-radius:15px; border:none; font-weight:bold; z-index:100;">GO!</button>
    </div>
    <script>
        const p=document.getElementById('p'), f=document.getElementById('f'), go=document.getElementById('go'), jB=document.getElementById('jb'), jS=document.getElementById('js');
        let x=f.offsetWidth/2-17, y=450, t=0, run=false, jX=0, jY=0, drag=false;
        const walls = [];
        for(let i=0; i<8; i++){
            let w=document.createElement('div'); w.style.position='absolute'; w.style.background='#0D47A1';
            w.style.width=(40+Math.random()*60)+'px'; w.style.height='40px';
            w.style.left=Math.random()*(f.offsetWidth-60)+'px'; w.style.top=(60+Math.random()*340)+'px';
            f.appendChild(w); walls.push(w);
        }
        jB.ontouchstart=(e)=>{drag=true; e.preventDefault();};
        window.ontouchmove=(e)=>{ if(!drag)return; let t=e.touches[0], r=jB.getBoundingClientRect(), dx=t.clientX-(r.left+45), dy=t.clientY-(r.top+45), d=Math.min(Math.sqrt(dx*dx+dy*dy), 45), a=Math.atan2(dy,dx); jX=Math.cos(a)*(d/45); jY=Math.sin(a)*(d/45); jS.style.transform=`translate(${jX*35}px, ${jY*35}px)`; };
        window.ontouchend=()=>{drag=false; jX=0; jY=0; jS.style.transform='translate(0,0)';};
        go.onclick=()=>{if(!run){run=true; go.style.display='none';}};
        function checkW(nx,ny){ const pr={l:nx, r:nx+34, t:ny, b:ny+34}; for(let w of walls){ const wr={l:w.offsetLeft, r:w.offsetLeft+w.offsetWidth, t:w.offsetTop, b:w.offsetTop+40}; if(!(pr.r<wr.l||pr.l>wr.r||pr.b<wr.t||pr.t>wr.b)) return true; } return false; }
        function loop(){
            if(run){
                t+=0.016; document.getElementById('tm_ui').innerHTML=t.toFixed(2)+"s";
                let nx=x+jX*6, ny=y+jY*7;
                if(!checkW(nx,y)) x=nx; else f.style.background='#1A3A8A';
                if(!checkW(x,ny)) y=ny; else f.style.background='#1A3A8A';
                if(jX==0 && jY==0) f.style.background='#0D47A1';
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
    if st.button("⬅️ VOLTAR AO HUB"): st.session_state.pagina='hub'; st.rerun()

# --- RELATÓRIOS ---
elif st.session_state.pagina == 'relatorio_drible':
    pts = st.session_state.get('pontos_drible', 0)
    n, v = calc_drible(pts)
    st.markdown(f"<div class='stats-box'><h3>SISTEMA GOAT TV: {n}</h3>✔️ Slalom Analógico Dinâmico<br><b>+ {v} Pontos</b><br><br>❌ Defesa / Físico<br><b>- {v} Pontos</b></div>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align:center;'>{pts} PTS</h1>", unsafe_allow_html=True)
    if st.button("CONCLUIR"): st.query_params.clear(); st.session_state.pagina='hub'; st.rerun()

elif st.session_state.pagina == 'relatorio_velocidade':
    tm = st.session_state.get('tempo_velocidade', 0)
    n, v = calc_vel(tm)
    st.markdown(f"<div class='stats-box'><h3>SISTEMA GOAT TV: {n}</h3>✔️ Explosão Vertical Analógica<br><b>+ {v} Pontos</b><br><br>❌ Contato Físico<br><b>- {v} Pontos</b></div>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align:center;'>{tm}s</h1>", unsafe_allow_html=True)
    if st.button("CONCLUIR"): st.query_params.clear(); st.session_state.pagina='hub'; st.rerun()
