import streamlit as st
import streamlit.components.v1 as components

# --- 1. ESTILO PREMIUM MOBILE (FIXO E BLINDADO) ---
st.set_page_config(page_title="GOAT TV - CT OFICIAL", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0E0E2C; color: #FFFFFF; font-family: 'sans-serif'; }
    .ct-title { text-align: center; font-size: 26px; font-weight: 800; color: #FFD700; margin-bottom: 15px; }
    
    /* Botões Pílula Simétricos */
    div.stButton > button {
        width: 100% !important; height: 55px !important;
        border-radius: 50px !important; border: none !important;
        color: white !important; font-weight: 700 !important; font-size: 16px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4) !important;
        margin-bottom: 12px !important;
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

# --- 3. FLUXO DE TELAS ---

# TELA DE LOGIN (FIXADA COM BOTÃO)
if st.session_state.pagina == 'login':
    st.markdown("<h1 class='ct-title'>🛡️ ACESSO CT GOAT TV</h1>", unsafe_allow_html=True)
    pin = st.text_input("PIN DO ATLETA:", type="password")
    # O BOTÃO DE ACESSO QUE NÃO PODE SUMIR:
    if st.button("ENTRAR NO CT", use_container_width=True):
        if pin == "2026": 
            st.session_state.pagina = 'hub'
            st.rerun()

# HUB UNIFICADO
elif st.session_state.pagina == 'hub':
    st.markdown("<h1 class='ct-title'>CENTRO DE TREINAMENTO</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<style>div.stButton > button[key='btn_d'] { background: linear-gradient(135deg, #4A90E2, #357ABD) !important; }</style>", unsafe_allow_html=True)
        if st.button("⚽ DRIBLE", key="btn_d"):
            st.session_state.pagina = 'treino_drible'; st.rerun()
    with col2:
        st.markdown("<style>div.stButton > button[key='btn_v'] { background: linear-gradient(135deg, #7C5CFF, #5A3ECC) !important; }</style>", unsafe_allow_html=True)
        if st.button("⚡ VELOCIDADE", key="btn_v"):
            st.session_state.pagina = 'treino_velocidade'; st.rerun()

# SALA 1: DRIBLE (TARGET ARROW + ANALÓGICO COMPACTO)
elif st.session_state.pagina == 'treino_drible':
    st.markdown("<h2 style='text-align:center;'>⚽ SLALOM GOAT TV</h2>", unsafe_allow_html=True)
    game_html = """
    <div id="f" style="height:480px; width:100%; background-color:#0D47A1; border-radius:20px; position:relative; overflow:hidden; border:4px solid #08306B; touch-action:none;">
        <div id="p" style="width:24px; height:24px; background:white; border-radius:50%; position:absolute; left:45%; bottom:50px; z-index:30; border:2px solid #333;">⚽</div>
        <div id="goal" style="width:80px; height:10px; background:yellow; position:absolute; bottom:0; right:0;"></div>
        <div class="c" style="left:15%; top:360px;"></div> <div class="c" style="left:35%; top:360px;"></div> <div class="gt" id="g0" style="left:16%; top:360px; width:18%"></div>
        <div class="c" style="left:65%; top:60px;"></div> <div class="c" style="left:85%; top:60px;"></div> <div class="gt" id="g1" style="left:66%; top:60px; width:18%"></div>
        <div class="c" style="left:15%; top:60px;"></div> <div class="c" style="left:35%; top:60px;"></div> <div class="gt" id="g2" style="left:16%; top:60px; width:18%"></div>
        <div class="c" style="left:65%; top:200px;"></div> <div class="c" style="left:85%; top:200px;"></div> <div class="gt" id="g3" style="left:66%; top:200px; width:18%"></div>
        <div class="c" style="left:65%; top:360px;"></div> <div class="c" style="left:85%; top:360px;"></div> <div class="gt" id="g4" style="left:66%; top:360px; width:18%"></div>
        <svg id="tArr" style="position:absolute; width:24px; height:24px; z-index:100;" viewBox="0 0 24 24"><path fill="#FFD700" d="M12 21l-12-18h24z"/></svg>
        <div id="jb" style="position:absolute; bottom:15px; left:15px; width:80px; height:80px; background:rgba(255,255,255,0.1); border-radius:50%; z-index:100; border:2px solid rgba(255,255,255,0.2);">
            <div id="js" style="position:absolute; top:20px; left:20px; width:40px; height:40px; background:rgba(255,255,255,0.4); border-radius:50%;"></div>
        </div>
        <button id="go" style="position:absolute; bottom:25px; right:25px; padding:10px 20px; background:green; color:white; border-radius:10px; border:none; font-weight:bold; z-index:100;">GO!</button>
        <div style="position:absolute; top:5px; width:100%; display:flex; justify-content:space-around; color:white; font-weight:bold; font-size:14px;"><span id="s_ui">PTS: 0</span> <span id="t_ui">15.0s</span></div>
    </div>
    <style>.c{width:16px;height:16px;background:orange;border-radius:50%;position:absolute;border:1px solid #CC5500;}.gt{position:absolute;border-left:2px dashed rgba(255,255,255,0.1);height:16px;} #tArr{filter: drop-shadow(0 0 5px gold); animation: pulse 0.8s infinite alternate;} @keyframes pulse { from {transform: translateY(0);} to {transform: translateY(-8px);}}</style>
    <script>
        const p=document.getElementById('p'), f=document.getElementById('f'), go=document.getElementById('go'), jB=document.getElementById('jb'), jS=document.getElementById('js'), ta=document.getElementById('tArr');
        let x=f.offsetWidth/2-12, y=380, score=0, time=15.0, run=false, gts=new Set(), jX=0, jY=0, drag=false;
        const ck = [{id:'g0',x:f.offsetWidth*0.25,y:340},{id:'g1',x:f.offsetWidth*0.75,y:40},{id:'g2',x:f.offsetWidth*0.25,y:40},{id:'g3',x:f.offsetWidth*0.75,y:160},{id:'g4',x:f.offsetWidth*0.75,y:340},{x:f.offsetWidth*0.8,y:460}];
        function upA(){ let t=ck[gts.size]; if(t){ ta.style.left=(t.x-4)+'px'; ta.style.top=(t.y-30)+'px'; } }
        jB.ontouchstart=(e)=>{drag=true; e.preventDefault();};
        window.ontouchmove=(e)=>{ if(!drag)return; let touch=e.touches[0], r=jB.getBoundingClientRect(), dx=touch.clientX-(r.left+40), dy=touch.clientY-(r.top+40), d=Math.min(Math.sqrt(dx*dx+dy*dy), 40), a=Math.atan2(dy,dx); jX=Math.cos(a)*(d/40); jY=Math.sin(a)*(d/40); jS.style.transform=`translate(${jX*25}px, ${jY*25}px)`; };
        window.ontouchend=()=>{drag=false; jX=0; jY=0; jS.style.transform='translate(0,0)';};
        go.onclick=()=>{run=true; go.style.display='none'; upA();};
        function loop(){
            if(run && time>0){
                time-=0.016; x+=jX*4.5; y+=jY*4.5;
                x=Math.max(0,Math.min(x,f.offsetWidth-24)); y=Math.max(0,Math.min(y,f.offsetHeight-24));
                p.style.left=x+'px'; p.style.top=y+'px';
                if(gts.size<5){
                    const n=document.getElementById(ck[gts.size].id);
                    const gr=n.getBoundingClientRect(), pr=p.getBoundingClientRect();
                    if(!(pr.right<gr.left||pr.left>gr.right||pr.bottom<gr.top||pr.top>gr.bottom)){ gts.add(gts.size); score+=500; upA(); }
                }
                if(y>440 && x>f.offsetWidth*0.6 && gts.size>=5){ window.parent.location.href=window.parent.location.href.split('?')[0]+"?score="+(score+Math.round(time*100)); run=false; }
                document.getElementById('s_ui').innerHTML="PTS: "+score; document.getElementById('t_ui').innerHTML=time.toFixed(1)+"s";
            }
            requestAnimationFrame(loop);
        }
        loop();
    </script>
    """
    components.html(game_html, height=520)
    if st.button("⬅️ VOLTAR AO HUB"): st.session_state.pagina='hub'; st.rerun()

# SALA 2: VELOCIDADE (GHOST SPRINT - ANALÓGICO + FANTASMAS)
elif st.session_state.pagina == 'treino_velocidade':
    st.markdown("<h2 style='text-align:center;'>⚡ GHOST SPRINT</h2>", unsafe_allow_html=True)
    game_html = """
    <div id="f" style="height:480px; width:100%; background-color:#0D47A1; border-radius:20px; position:relative; overflow:hidden; border:4px solid #08306B; touch-action:none; transition: background 0.1s;">
        <div id="p" style="width:24px; height:24px; background:white; border-radius:50%; position:absolute; left:45%; bottom:40px; border:2px solid #333; z-index:20;">⚽</div>
        <div style="width:100%; height:10px; background:yellow; position:absolute; top:0; left:0;"></div>
        <div id="tm_ui" style="position:absolute; top:10px; right:10px; font-weight:bold; color:white; font-size:18px;">0.00s</div>
        <div id="jb" style="position:absolute; bottom:15px; left:15px; width:80px; height:80px; background:rgba(255,255,255,0.1); border-radius:50%; border:2px solid rgba(255,255,255,0.2);">
            <div id="js" style="position:absolute; top:20px; left:20px; width:40px; height:40px; background:rgba(255,255,255,0.4); border-radius:50%;"></div>
        </div>
        <button id="go" style="position:absolute; bottom:25px; right:25px; padding:10px 20px; background:green; color:white; border-radius:10px; border:none; font-weight:bold; z-index:100;">GO!</button>
    </div>
    <script>
        const p=document.getElementById('p'), f=document.getElementById('f'), go=document.getElementById('go'), jB=document.getElementById('jb'), jS=document.getElementById('js');
        let x=f.offsetWidth/2-12, y=410, t=0, run=false, jX=0, jY=0, drag=false;
        const ws = []; for(let i=0; i<6; i++){
            let w=document.createElement('div'); w.style.position='absolute'; w.style.background='#0D47A1';
            w.style.width='50px'; w.style.height='30px'; w.style.left=Math.random()*(f.offsetWidth-50)+'px'; w.style.top=(50+Math.random()*300)+'px';
            f.appendChild(w); ws.push(w);
        }
        jB.ontouchstart=(e)=>{drag=true; e.preventDefault();};
        window.ontouchmove=(e)=>{ if(!drag)return; let touch=e.touches[0], r=jB.getBoundingClientRect(), dx=touch.clientX-(r.left+40), dy=touch.clientY-(r.top+40), d=Math.min(Math.sqrt(dx*dx+dy*dy), 40), a=Math.atan2(dy,dx); jX=Math.cos(a)*(d/40); jY=Math.sin(a)*(d/40); jS.style.transform=`translate(${jX*25}px, ${jY*25}px)`; };
        window.ontouchend=()=>{drag=false; jX=0; jY=0; jS.style.transform='translate(0,0)';};
        go.onclick=()=>{run=true; go.style.display='none';};
        function loop(){
            if(run){
                t+=0.016; document.getElementById('tm_ui').innerHTML=t.toFixed(2)+"s";
                let nx=x+jX*5, ny=y+jY*6;
                let c=false; for(let w of ws){ if(nx+20>w.offsetLeft && nx<w.offsetLeft+50 && ny+20>w.offsetTop && ny<w.offsetTop+30) c=true; }
                if(!c){ x=nx; y=ny; f.style.background='#0D47A1'; } else { f.style.background='#1A3A8A'; }
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
    if st.button("⬅️ VOLTAR AO HUB"): st.session_state.pagina='hub'; st.rerun()

# --- RELATÓRIOS ---
elif st.session_state.pagina == 'relatorio_drible':
    st.markdown(f"<div style='background: #1B5E20; padding: 25px; border-radius: 20px; text-align:center;'><h2>PONTUAÇÃO DRIBLE</h2><h1>{st.session_state.pontos_drible} PTS</h1></div>", unsafe_allow_html=True)
    if st.button("NOVO TREINO"): st.query_params.clear(); st.session_state.pagina='hub'; st.rerun()

elif st.session_state.pagina == 'relatorio_velocidade':
    st.markdown(f"<div style='background: #1B5E20; padding: 25px; border-radius: 20px; text-align:center;'><h2>TEMPO VELOCIDADE</h2><h1>{st.session_state.tempo_velocidade}s</h1></div>", unsafe_allow_html=True)
    if st.button("NOVO TREINO"): st.query_params.clear(); st.session_state.pagina='hub'; st.rerun()
