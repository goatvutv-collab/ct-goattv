import streamlit as st
import streamlit.components.v1 as components

# --- 1. CONFIG E DESIGN ---
st.set_page_config(page_title="GOAT TV - CT OFICIAL", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #0E0E2C; color: #FFF; font-family: sans-serif; }
    .ct-title { text-align: center; font-size: 24px; font-weight: 800; color: #FFD700; }
    div.stButton > button { width: 100%!important; height: 45px!important; border-radius: 50px!important; border: none!important; color: white!important; font-weight: 700!important; box-shadow: 0 4px 10px rgba(0,0,0,0.4)!important; margin-bottom: 5px!important; }
    iframe { border-radius: 20px; border: 3px solid #1E3A8A; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 2. MOTOR DE ESTADOS ---
if 'pagina' not in st.session_state: st.session_state.pagina = 'login'
p = st.query_params
if "score" in p: st.session_state.pts_d = int(p["score"]); st.session_state.pagina = 'rel_d'
elif "p_score" in p: st.session_state.pts_p = int(p["p_score"]); st.session_state.pagina = 'rel_p'
elif "v_time" in p: st.session_state.tm_v = float(p["v_time"]); st.session_state.pagina = 'rel_v'

# --- 3. TELAS ---
if st.session_state.pagina == 'login':
    st.markdown("<h1 class='ct-title'>🛡️ ACESSO CT GOAT TV</h1>", unsafe_allow_html=True)
    pin = st.text_input("PIN:", type="password")
    if st.button("ENTRAR NO CT"):
        if pin == "2026": st.session_state.pagina = 'hub'; st.rerun()

elif st.session_state.pagina == 'hub':
    st.markdown("<h1 class='ct-title'>CENTRO DE TREINAMENTO</h1>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⚽ DRIBLE"): st.session_state.pagina = 'drible'; st.rerun()
        if st.button("🎯 PASSE PRO"): st.session_state.pagina = 'passe'; st.rerun()
    with c2:
        if st.button("⚡ VELOCIDADE"): st.session_state.pagina = 'vel'; st.rerun()

# SALA: PASSE PRO (MOVIMENTAÇÃO + PRESSÃO)
elif st.session_state.pagina == 'passe':
    st.markdown("<h2 style='text-align:center;'>🎯 PASSE SOB PRESSÃO</h2>", unsafe_allow_html=True)
    game_html = """
    <div id="f" style="height:460px; width:100%; background:#1B5E20; position:relative; overflow:hidden; border:4px solid #08306B; touch-action:none; border-radius:20px;">
        <div id="ui" style="position:absolute; top:10px; width:100%; text-align:center; color:white; font-weight:bold; z-index:50;">META: <span id="h_ui">0</span>/10</div>
        <div id="p" style="width:26px; height:26px; background:white; border-radius:50%; position:absolute; left:46%; bottom:60px; border:2px solid #333; z-index:35;"></div>
        <div id="tgt" style="width:32px; height:32px; background:rgba(255,215,0,0.6); border:2px dashed gold; border-radius:50%; position:absolute; left:20%; top:40px;"></div>
        <div id="ball" style="width:12px; height:12px; background:white; border-radius:50%; position:absolute; display:none; z-index:40;"></div>
        <div id="aim" style="width:2px; height:80px; background:rgba(255,255,255,0.3); position:absolute; transform-origin: bottom center; display:none; z-index:30;"></div>
        <div id="pb_bg" style="position:absolute; bottom:90px; right:20px; width:12px; height:80px; background:#333; border:1px solid white; border-radius:3px; overflow:hidden;">
            <div id="pb" style="width:100%; height:0%; background:linear-gradient(to top, #F44, #4CAF50 50%, #F44); position:absolute; bottom:0;"></div>
        </div>
        <div id="opp" style="width:40px; height:15px; background:#F44; position:absolute; left:50%; top:150px; border-radius:5px; border:1px solid white; z-index:32;"></div>
        <div id="jb" style="position:absolute; bottom:15px; left:15px; width:80px; height:80px; background:rgba(255,255,255,0.1); border-radius:50%; border:2px solid rgba(255,255,255,0.2); z-index:100;">
            <div id="js" style="position:absolute; top:20px; left:20px; width:40px; height:40px; background:rgba(255,255,255,0.3); border-radius:50%;"></div>
        </div>
        <button id="btnA" style="position:absolute; bottom:15px; right:15px; width:65px; height:65px; background:#4A90E2; color:white; border-radius:50%; font-weight:bold; font-size:24px; border:none; z-index:100;">A</button>
    </div>
    <script>
        const p=document.getElementById('p'), f=document.getElementById('f'), tgt=document.getElementById('tgt'), ball=document.getElementById('ball'), btnA=document.getElementById('btnA'), pb=document.getElementById('pb'), jB=document.getElementById('jb'), jS=document.getElementById('js'), aim=document.getElementById('aim'), opp=document.getElementById('opp');
        let jX=0, jY=0, x=f.offsetWidth/2-13, y=340, drag=false, hits=0, power=0, pAct=false, pass=false, oDir=1;
        jB.ontouchstart=(e)=>{drag=true; e.preventDefault();};
        window.ontouchmove=(e)=>{ if(!drag)return; let t=e.touches[0], r=jB.getBoundingClientRect(), dx=t.clientX-(r.left+40), dy=t.clientY-(r.top+40), d=Math.min(Math.sqrt(dx*dx+dy*dy),40), a=Math.atan2(dy,dx); jX=Math.cos(a); jY=Math.sin(a); jS.style.transform=`translate(${jX*(d/40)*25}px, ${jY*(d/40)*25}px)`; aim.style.display='block'; aim.style.left=(x+13)+'px'; aim.style.top=(y-67)+'px'; aim.style.transform=`rotate(${(a*180/Math.PI)+90}deg)`; };
        window.ontouchend=()=>{drag=false; aim.style.display='none'; jX=0; jY=0; jS.style.transform='translate(0,0)';};
        btnA.onpointerdown=()=>{ if(!pass){pAct=true; power=0;} };
        window.onpointerup=()=>{ if(pAct){pAct=false; shoot();} };
        function shoot(){
            pass=true; ball.style.display='block'; let bx=x+8, by=y+8, spd=(power>25 && power<75)?9:(power>=75?18:3), vx=jX*spd, vy=jY*spd;
            let anim=setInterval(()=>{
                bx+=vx; by+=vy; ball.style.left=bx+'px'; ball.style.top=by+'px';
                let tr=tgt.getBoundingClientRect(), br=ball.getBoundingClientRect(), or=opp.getBoundingClientRect();
                if(!(br.right<tr.left||br.left>tr.right||br.bottom<tr.top||br.top>tr.bottom)){ hits++; reset(anim); }
                if(!(br.right<or.left||br.left>or.right||br.bottom<or.top||br.top>or.bottom)){ reset(anim); }
                if(bx<0||bx>f.offsetWidth||by<0||by>f.offsetHeight){ reset(anim); }
            }, 20);
        }
        function reset(a){ clearInterval(a); ball.style.display='none'; pass=false; power=0; pb.style.height='0%'; document.getElementById('h_ui').innerHTML=hits; tgt.style.left=Math.random()*70+15+'%'; if(hits>=10) window.parent.location.href=window.parent.location.href.split('?')[0]+"?p_score="+(hits*100); }
        function loop(){
            if(!pAct && !pass && drag){ x+=jX*3; y+=jY*3; x=Math.max(0,Math.min(x,f.offsetWidth-26)); y=Math.max(180,Math.min(y,f.offsetHeight-26)); p.style.left=x+'px'; p.style.top=y+'px'; }
            let ox=opp.offsetLeft; if(ox>f.offsetWidth-50||ox<10)oDir*=-1; opp.style.left=(ox+oDir*3)+'px';
            if(pAct && power<100){ power+=4; pb.style.height=power+'%'; }
            requestAnimationFrame(loop);
        }
        loop();
    </script>
    """
    components.html(game_html, height=500)
    if st.button("⬅️ VOLTAR AO HUB"): st.session_state.pagina = 'hub'; st.rerun()

# --- RELATÓRIOS (Simplificados para evitar corte) ---
elif st.session_state.pagina == 'rel_p':
    st.markdown(f"<div style='background:#1B5E20;padding:20px;border-radius:15px;text-align:center;'><h2>PONTO DE CONTROLE: {st.session_state.pts_p}</h2></div>", unsafe_allow_html=True)
    if st.button("NOVO TREINO"): st.query_params.clear(); st.session_state.pagina = 'hub'; st.rerun()
