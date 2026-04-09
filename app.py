import streamlit as st
import streamlit.components.v1 as components

# --- 1. ESTILO PREMIUM (COMPACTO) ---
st.set_page_config(page_title="GOAT TV - MOBILE CT", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0E0E2C; color: #FFFFFF; font-family: 'sans-serif'; }
    .ct-title { text-align: center; font-size: 26px; font-weight: 800; color: #FFD700; margin-bottom: 15px; }
    
    div.stButton > button {
        width: 100% !important; height: 55px !important;
        border-radius: 50px !important; border: none !important;
        color: white !important; font-weight: 700 !important; font-size: 16px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4) !important;
        margin-bottom: 8px !important;
    }
    iframe { border-radius: 25px; border: 3px solid #1E3A8A; background: transparent; }
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

# --- 3. TELAS ---

if st.session_state.pagina == 'login':
    st.markdown("<h1 class='ct-title'>🛡️ ACESSO CT GOAT TV</h1>", unsafe_allow_html=True)
    pin = st.text_input("PIN:", type="password")
    if st.button("ENTRAR", use_container_width=True):
        if pin == "2026": st.session_state.pagina = 'hub'; st.rerun()

elif st.session_state.pagina == 'hub':
    st.markdown("<h1 class='ct-title'>CENTRO DE TREINAMENTO</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<style>div.stButton > button[key='btn_d'] { background: linear-gradient(135deg, #4A90E2, #357ABD) !important; }</style>", unsafe_allow_html=True)
        if st.button("⚽ DRIBLE", key="btn_d"): st.session_state.pagina = 'treino_drible'; st.rerun()
    with col2:
        st.markdown("<style>div.stButton > button[key='btn_v'] { background: linear-gradient(135deg, #7C5CFF, #5A3ECC) !important; }</style>", unsafe_allow_html=True)
        if st.button("⚡ VELOCIDADE", key="btn_v"): st.session_state.pagina = 'treino_velocidade'; st.rerun()

# --- SALA: DRIBLE (COMPACTO + MINI BOTÃO) ---
elif st.session_state.pagina == 'treino_drible':
    st.markdown("<h2 style='text-align:center;'>⚽ BRASILEIRO COMPACT</h2>", unsafe_allow_html=True)
    game_html = """
    <div id="f" style="height:480px; width:100%; background-color:#0D47A1; border-radius:20px; position:relative; overflow:hidden; border:4px solid #08306B; touch-action:none;">
        <div id="p" style="width:24px; height:24px; background:white; border-radius:50%; position:absolute; left:45%; bottom:50px; z-index:30; border:2px solid #333;">⚽</div>
        <div id="goal" style="width:80px; height:10px; background:yellow; position:absolute; bottom:0; right:0;"></div>
        
        <div class="c" style="left:15%; top:380px;"></div> <div class="c" style="left:35%; top:380px;"></div> <div class="gt" id="gA" style="left:16%; top:380px; width:18%"></div>
        <div class="c" style="left:65%; top:60px;"></div> <div class="c" style="left:85%; top:60px;"></div> <div class="gt" id="gB" style="left:66%; top:60px; width:18%"></div>
        <div class="c" style="left:15%; top:60px;"></div> <div class="c" style="left:35%; top:60px;"></div> <div class="gt" id="gC" style="left:16%; top:60px; width:18%"></div>
        <div class="c" style="left:48%; top:230px; background:red;"></div> <div class="c" style="left:65%; top:180px;"></div> <div class="c" style="left:85%; top:180px;"></div> <div class="gt" id="gE" style="left:66%; top:180px; width:18%"></div>
        <div class="c" style="left:65%; top:380px;"></div> <div class="c" style="left:85%; top:380px;"></div> <div class="gt" id="gF" style="left:66%; top:380px; width:18%"></div>

        <svg id="arr" style="position:absolute; width:30px; height:30px; z-index:5;" viewBox="0 0 24 24"><path fill="#FFD700" d="M12 2L4.5 10H8v12h8V10h3.5L12 2z"/></svg>

        <div id="jb" style="position:absolute; bottom:15px; left:15px; width:80px; height:80px; background:rgba(255,255,255,0.1); border-radius:50%; z-index:100; border:2px solid rgba(255,255,255,0.2);">
            <div id="js" style="position:absolute; top:20px; left:20px; width:40px; height:40px; background:rgba(255,255,255,0.4); border-radius:50%;"></div>
        </div>
        <button id="go" style="position:absolute; bottom:25px; right:25px; padding:10px 20px; background:green; color:white; border-radius:10px; border:none; font-weight:bold; z-index:100;">GO!</button>
        <div style="position:absolute; top:5px; width:100%; display:flex; justify-content:space-around; color:white; font-weight:bold; font-size:14px;">
            <span id="s_ui">PTS: 0</span> <span id="t_ui">15.0s</span>
        </div>
    </div>
    <style>.c{width:16px;height:16px;background:orange;border-radius:50%;position:absolute;border:1px solid #CC5500;}.gt{position:absolute;border-left:2px dashed rgba(255,255,255,0.1);height:16px;}</style>
    <script>
        const p=document.getElementById('p'), f=document.getElementById('f'), go=document.getElementById('go'), jB=document.getElementById('jb'), jS=document.getElementById('js'), arr=document.getElementById('arr');
        let x=f.offsetWidth/2-12, y=380, score=0, time=15.0, run=false, gates=new Set(), jX=0, jY=0, drag=false;
        const ckps = [{id:'gA',x:f.offsetWidth*0.25,y:380},{id:'gB',x:f.offsetWidth*0.75,y:60},{id:'gC',x:f.offsetWidth*0.25,y:60},{x:f.offsetWidth/2,y:230},{id:'gE',x:f.offsetWidth*0.75,y:180},{id:'gF',x:f.offsetWidth*0.75,y:380},{x:f.offsetWidth*0.8,y:470}];
        jB.ontouchstart=(e)=>{drag=true; e.preventDefault();};
        window.ontouchmove=(e)=>{ if(!drag)return; let t=e.touches[0], r=jB.getBoundingClientRect(), dx=t.clientX-(r.left+40), dy=t.clientY-(r.top+40), d=Math.min(Math.sqrt(dx*dx+dy*dy), 40), a=Math.atan2(dy,dx); jX=Math.cos(a)*(d/40); jY=Math.sin(a)*(d/40); jS.style.transform=`translate(${jX*25}px, ${jY*25}px)`; };
        window.ontouchend=()=>{drag=false; jX=0; jY=0; jS.style.transform='translate(0,0)';};
        go.onclick=()=>{run=true; go.style.display='none';};
        function loop(){
            if(run && time>0){
                time-=0.016; x+=jX*4.5; y+=jY*4.5;
                x=Math.max(0,Math.min(x,f.offsetWidth-24)); y=Math.max(0,Math.min(y,f.offsetHeight-24));
                p.style.left=x+'px'; p.style.top=y+'px';
                let tg=ckps[gates.size]||ckps[6]; let ang=Math.atan2(tg.y-(y+12), tg.x-(x+12));
                arr.style.transform=`translate(${x+12-15}px, ${y-30}px) rotate(${ang}rad)`;
                if(gates.size<6){
                    const nxt=document.getElementById(ckps[gates.size].id);
                    if(nxt){ const gr=nxt.getBoundingClientRect(), pr=p.getBoundingClientRect(); if(!(pr.right<gr.left||pr.left>gr.right||pr.bottom<gr.top||pr.top>gr.bottom)){ gates.add(gates.size); score+=500; } }
                    else { const d=Math.sqrt(Math.pow(x+12-f.offsetWidth/2,2)+Math.pow(y+12-230,2)); if(d<35) gates.add(3); }
                }
                if(y>450 && x>f.offsetWidth*0.7 && gates.size>=6){ window.parent.location.href=window.parent.location.href.split('?')[0]+"?score="+(score+Math.round(time*100)); run=false; }
                document.getElementById('s_ui').innerHTML="PTS: "+score; document.getElementById('t_ui').innerHTML=time.toFixed(1)+"s";
            }
            requestAnimationFrame(loop);
        }
        loop();
    </script>
    """
    components.html(game_html, height=520)
    if st.button("⬅️ HUB"): st.session_state.pagina='hub'; st.rerun()

# --- SALA: VELOCIDADE (COMPACTA) ---
elif st.session_state.pagina == 'treino_velocidade':
    st.markdown("<h2 style='text-align:center;'>⚡ GHOST SPRINT</h2>", unsafe_allow_html=True)
    game_html = """
    <div id="f" style="height:480px; width:100%; background-color:#0D47A1; border-radius:20px; position:relative; overflow:hidden; border:4px solid #08306B; touch-action:none;">
        <div id="p" style="width:24px; height:24px; background:white; border-radius:50%; position:absolute; left:45%; bottom:40px; border:2px solid #333;">⚽</div>
        <div style="width:100%; height:10px; background:yellow; position:absolute; top:0; left:0;"></div>
        <div id="tm_ui" style="position:absolute; top:10px; right:10px; font-weight:bold; color:white; font-size:18px;">0.00s</div>
        <div id="jb" style="position:absolute; bottom:15px; left:15px; width:80px; height:80px; background:rgba(255,255,255,0.1); border-radius:50%; border:2px solid rgba(255,255,255,0.2);">
            <div id="js" style="position:absolute; top:20px; left:20px; width:40px; height:40px; background:rgba(255,255,255,0.4); border-radius:50%;"></div>
        </div>
        <button id="go" style="position:absolute; bottom:25px; right:25px; padding:10px 20px; background:green; color:white; border-radius:10px; border:none; font-weight:bold;">GO!</button>
    </div>
    <script>
        const p=document.getElementById('p'), f=document.getElementById('f'), go=document.getElementById('go'), jB=document.getElementById('jb'), jS=document.getElementById('js');
        let x=f.offsetWidth/2-12, y=410, t=0, run=false, jX=0, jY=0, drag=false;
        const walls = []; for(let i=0; i<6; i++){
            let w=document.createElement('div'); w.style.position='absolute'; w.style.background='#0D47A1';
            w.style.width='50px'; w.style.height='30px'; w.style.left=Math.random()*(f.offsetWidth-50)+'px'; w.style.top=(50+Math.random()*300)+'px';
            f.appendChild(w); walls.push(w);
        }
        jB.ontouchstart=(e)=>{drag=true; e.preventDefault();};
        window.ontouchmove=(e)=>{ if(!drag)return; let touch=e.touches[0], r=jB.getBoundingClientRect(), dx=touch.clientX-(r.left+40), dy=touch.clientY-(r.top+40), d=Math.min(Math.sqrt(dx*dx+dy*dy), 40), a=Math.atan2(dy,dx); jX=Math.cos(a)*(d/40); jY=Math.sin(a)*(d/40); jS.style.transform=`translate(${jX*25}px, ${jY*25}px)`; };
        window.ontouchend=()=>{drag=false; jX=0; jY=0; jS.style.transform='translate(0,0)';};
        go.onclick=()=>{run=true; go.style.display='none';};
        function loop(){
            if(run){
                t+=0.016; document.getElementById('tm_ui').innerHTML=t.toFixed(2)+"s";
                let nx=x+jX*5, ny=y+jY*6;
                let col=false; for(let w of walls){ if(nx+20>w.offsetLeft && nx<w.offsetLeft+50 && ny+20>w.offsetTop && ny<w.offsetTop+30) col=true; }
                if(!col){ x=nx; y=ny; f.style.background='#0D47A1'; } else { f.style.background='#1A3A8A'; }
                x=Math.max(0,Math.min(x,f.offsetWidth-24)); y=Math.max(0,Math.min(y,f.offsetHeight-24));
                p.style.left=x+'px'; p.style.top=y+'px';
                if(y < 10){ window.parent.location.href=window.parent.location.href.split('?')[0]+"?time="+t.toFixed(2); run=false; }
            }
            requestAnimationFrame(loop);
        }
        loop();
    </script>
    """
    components.html(game_html, height=520)
    if st.button("⬅️ HUB"): st.session_state.pagina='hub'; st.rerun()

# --- RELATÓRIOS ---
elif st.session_state.pagina == 'relatorio_drible':
    st.markdown(f"<div class='stats-box'><h3>RESULTADO DRIBLE</h3><b>{st.session_state.pontos_drible} PTS</b></div>", unsafe_allow_html=True)
    if st.button("NOVO TREINO"): st.query_params.clear(); st.session_state.pagina='hub'; st.rerun()

elif st.session_state.pagina == 'relatorio_velocidade':
    st.markdown(f"<div class='stats-box'><h3>RESULTADO VELOCIDADE</h3><b>{st.session_state.tempo_velocidade}s</b></div>", unsafe_allow_html=True)
    if st.button("NOVO TREINO"): st.query_params.clear(); st.session_state.pagina='hub'; st.rerun()
