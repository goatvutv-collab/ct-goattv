import streamlit as st
import streamlit.components.v1 as components

# --- 1. ESTILO E SIMETRIA (GOAT TV CT) ---
st.set_page_config(page_title="GOAT TV - CT ANALÓGICO", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0E0E2C; color: #FFFFFF; font-family: 'sans-serif'; }
    .ct-title { text-align: center; font-size: 32px; font-weight: 800; color: #FFD700; margin-bottom: 20px; }
    
    /* Pílulas do Hub */
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

# --- 3. TELAS ---

# LOGIN
if st.session_state.pagina == 'login':
    st.markdown("<h1 class='ct-title'>🛡️ ACESSO CT GOAT TV</h1>", unsafe_allow_html=True)
    pin = st.text_input("PIN DO ATLETA:", type="password")
    if st.button("ENTRAR", use_container_width=True):
        if pin == "2026": 
            st.session_state.pagina = 'hub'
            st.rerun()

# HUB
elif st.session_state.pagina == 'hub':
    st.markdown("<h1 class='ct-title'>CENTRO DE TREINAMENTO</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<style>div.stButton > button[key='btn_d'] { background: linear-gradient(135deg, #4A90E2, #357ABD) !important; }</style>", unsafe_allow_html=True)
        if st.button("⚽ DRIBLE (SLALOM)", key="btn_d"):
            st.session_state.pagina = 'treino_drible'
            st.rerun()
    with col2:
        st.markdown("<style>div.stButton > button[key='btn_v'] { background: linear-gradient(135deg, #7C5CFF, #5A3ECC) !important; }</style>", unsafe_allow_html=True)
        if st.button("⚡ VELOCIDADE (SPRINT)", key="btn_v"):
            st.session_state.pagina = 'treino_velocidade'
            st.rerun()

# SALA: DRIBLE (HORIZONTAL + ANALÓGICO)
elif st.session_state.pagina == 'treino_drible':
    st.markdown("<h2 style='text-align:center;'>⚽ SLALOM ANALÓGICO</h2>", unsafe_allow_html=True)
    game_html = """
    <div id="f" style="height:380px; width:100%; background-color:#0D47A1; border-radius:25px; position:relative; overflow:hidden; touch-action:none;">
        <div id="p" style="width:34px; height:34px; background:white; border-radius:50%; position:absolute; left:20px; top:170px; z-index:30; border:2px solid #333; display:flex; justify-content:center; align-items:center;">⚽</div>
        <div style="width:15px; height:100%; background:yellow; position:absolute; right:0; top:0; z-index:10;"></div>
        <div class="c" style="left:120px; top:60px;"></div> <div class="c" style="left:120px; top:280px;"></div>
        <div class="c" style="left:220px; top:60px;"></div> <div class="c" style="left:220px; top:280px;"></div>
        <div class="c" style="left:320px; top:60px;"></div> <div class="c" style="left:320px; top:280px;"></div>
        <div class="gt" style="left:125px; top:130px; height:100px;"></div>
        <div class="gt" style="left:225px; top:130px; height:100px;"></div>
        <div class="gt" style="left:325px; top:130px; height:100px;"></div>
        <div id="jb" style="position:absolute; bottom:20px; left:20px; width:90px; height:90px; background:rgba(255,255,255,0.1); border-radius:50%; z-index:100; border:2px solid rgba(255,255,255,0.2);">
            <div id="js" style="position:absolute; top:20px; left:20px; width:50px; height:50px; background:rgba(255,255,255,0.4); border-radius:50%;"></div>
        </div>
        <button id="go" style="position:absolute; bottom:30px; right:30px; padding:15px 30px; background:#4CAF50; color:white; border-radius:15px; border:none; font-weight:bold; z-index:100;">GO!</button>
        <div style="position:absolute; top:10px; width:100%; display:flex; justify-content:space-around; color:white; font-weight:bold; z-index:40;">
            <span id="s_ui">PONTOS: 0</span> <span id="t_ui">TEMPO: 15.0s</span>
        </div>
    </div>
    <style>.c{width:22px;height:22px;background:orange;border-radius:50%;position:absolute;border:2px solid #CC5500;}.gt{width:10px;background:rgba(255,255,255,0.05);position:absolute;border-left:2px dashed rgba(255,255,255,0.2);}</style>
    <script>
        const p=document.getElementById('p'), f=document.getElementById('f'), go=document.getElementById('go'), jB=document.getElementById('jb'), jS=document.getElementById('js');
        let x=20, y=170, score=0, time=15.0, run=false, gates=new Set(), jX=0, jY=0, drag=false;
        jB.ontouchstart=(e)=>{drag=true;e.preventDefault();};
        window.ontouchmove=(e)=>{ if(!drag)return; let t=e.touches[0], r=jB.getBoundingClientRect(), dx=t.clientX-(r.left+45), dy=t.clientY-(r.top+45), d=Math.min(Math.sqrt(dx*dx+dy*dy), 45), a=Math.atan2(dy,dx); jX=Math.cos(a)*(d/45); jY=Math.sin(a)*(d/45); jS.style.transform=`translate(${jX*35}px, ${jY*35}px)`; };
        window.ontouchend=()=>{drag=false; jX=0; jY=0; jS.style.transform='translate(0,0)';};
        go.onclick=()=>{if(!run){run=true; go.style.display='none';}};
        function checkC(nx,ny){ const cones=document.querySelectorAll('.c'); for(let c of cones){ if(nx+30>c.offsetLeft && nx<c.offsetLeft+22 && ny+30>c.offsetTop && ny<c.offsetTop+22) return true; } return false; }
        function loop(){
            if(run && time>0){
                time-=0.02; let nx=x+jX*5, ny=y+jY*5; if(!checkC(nx,y))x=nx; if(!checkC(x,ny))y=ny;
                x=Math.max(0,Math.min(x,f.offsetWidth-34)); y=Math.max(0,Math.min(y,f.offsetHeight-34));
                p.style.left=x+'px'; p.style.top=y+'px';
                document.querySelectorAll('.gt').forEach((g,i)=>{ const gr=g.getBoundingClientRect(), pr=p.getBoundingClientRect(); if(!(pr.right<gr.left||pr.left>gr.right||pr.bottom<gr
