import streamlit as st
import streamlit.components.v1 as components

# --- 1. CONFIG E ESTILO ---
st.set_page_config(page_title="GOAT TV - CT", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #0E0E2C; color: #FFFFFF; font-family: 'sans-serif'; }
    .ct-title { text-align: center; font-size: 24px; font-weight: 800; color: #FFD700; margin-bottom: 10px; }
    div.stButton > button {
        width: 100% !important; height: 50px !important; border-radius: 50px !important;
        border: none !important; color: white !important; font-weight: 700 !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4) !important; margin-bottom: 8px !important;
    }
    iframe { border-radius: 20px; border: 3px solid #1E3A8A; background: transparent; }
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
    if st.button("ENTRAR NO CT", use_container_width=True):
        if pin == "2026": st.session_state.pagina = 'hub'; st.rerun()

elif st.session_state.pagina == 'hub':
    st.markdown("<h1 class='ct-title'>CENTRO DE TREINAMENTO</h1>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⚽ DRIBLE"): st.session_state.pagina = 'drible'; st.rerun()
        if st.button("🎯 PASSE"): st.session_state.pagina = 'passe'; st.rerun()
    with c2:
        if st.button("⚡ VELOCIDADE"): st.session_state.pagina = 'vel'; st.rerun()

# SALA: PASSE PRO
elif st.session_state.pagina == 'passe':
    st.markdown("<h2 style='text-align:center;'>🎯 PRECISÃO TÁTICA</h2>", unsafe_allow_html=True)
    game_html = """
    <div id="f" style="height:460px; width:100%; background:#1B5E20; position:relative; overflow:hidden; border:4px solid #08306B; touch-action:none; border-radius:20px;">
        <div id="p" style="width:26px; height:26px; background:white; border-radius:50%; position:absolute; left:46%; bottom:30px; border:2px solid #333;"></div>
        <div id="tgt" style="width:32px; height:32px; background:rgba(255,215,0,0.5); border:2px dashed gold; border-radius:50%; position:absolute; left:20%; top:60px;"></div>
        <div id="ball" style="width:12px; height:12px; background:white; border-radius:50%; position:absolute; display:none;"></div>
        <div id="aim" style="width:2px; height:100px; background:rgba(255,255,255,0.3); position:absolute; left:50%; bottom:45px; transform-origin: bottom center; display:none;"></div>
        <div id="pb_bg" style="position:absolute; bottom:90px; right:20px; width:15px; height:100px; background:#333; border:2px solid white; border-radius:5px; overflow:hidden;">
            <div id="pb" style="width:100%; height:0%; background:linear-gradient(to top, #F44, #4CAF50 50%, #F44); position:absolute; bottom:0;"></div>
        </div>
        <div id="jb" style="position:absolute; bottom:15px; left:15px; width:80px; height:80px; background:rgba(255,255,255,0.1); border-radius:50%; border:2px solid rgba(255,255,255,0.2);">
            <div id="js" style="position:absolute; top:20px; left:20px; width:40px; height:40px; background:rgba(255,255,255,0.3); border-radius:50%;"></div>
        </div>
        <button id="btnA" style="position:absolute; bottom:15px; right:15px; width:60px; height:60px; background:#4A90E2; color:white; border-radius:50%; border:none; font-weight:bold; font-size:24px;">A</button>
    </div>
    <script>
        const p=document.getElementById('p'), f=document.getElementById('f'), tgt=document.getElementById('tgt'), ball=document.getElementById('ball'), btnA=document.getElementById('btnA'), pb=document.getElementById('pb'), jB=document.getElementById('jb'), jS=document.getElementById('js'), aim=document.getElementById('aim');
        let jX=0, jY=0, drag=false, hits=0, power=0, pAct=false, pass=false;
        jB.ontouchstart=(e)=>{drag=true; e.preventDefault();};
        window.ontouchmove=(e)=>{ if(!drag)return; let t=e.touches[0], r=jB.getBoundingClientRect(), dx=t.clientX-(r.left+40), dy=t.clientY-(r.top+40), d=Math.min(Math.sqrt(dx*dx+dy*dy),40), a=Math.atan2(dy,dx); jX=Math.cos(a); jY=Math.sin(a); jS.style.transform=`translate(${jX*(d/40)*25}px, ${jY*(d/40)*25}px)`; aim.style.display='block'; aim.style.transform=`rotate(${(a*180/Math.PI)+90}deg)`; };
        window.ontouchend=()=>{drag=false; aim.style.display='none';};
        btnA.onpointerdown=()=>{ if(!pass){pAct=true; power=0;} };
        window.onpointerup=()=>{ if(pAct){pAct=false; shoot();} };
        function shoot(){
            pass=true; ball.style.display='block'; let bx=p.offsetLeft+8, by=p.offsetTop+8, spd= (power>25 && power<75) ? 9 : (power>=75 ? 18 : 3);
            let vx=jX*spd, vy=jY*spd;
            let anim=setInterval(()=>{
                bx+=vx; by+=vy; ball.style.left=bx+'px'; ball.style.top=by+'px';
                let tr=tgt.getBoundingClientRect(), br=ball.getBoundingClientRect();
                if(!(br.right<tr.left || br.left>tr.right || br.bottom<tr.top || br.top>tr.bottom)){ hits++; reset(anim); }
                if(bx<0 || bx>f.offsetWidth || by<0 || by>f.offsetHeight){ clearInterval(anim); end(); }
            }, 20);
        }
        function reset(a){ clearInterval(a); ball.style.display='none'; pass=false; power=0; pb.style.height='0%'; tgt.style.left=Math.random()*70+15+'%'; tgt.style.top=Math.random()*150+50+'px'; }
        function end(){ window.parent.location.href=window.parent.location.href.split('?')[0]+"?p_score="+(hits*100); }
        setInterval(()=>{ if(pAct && power<100){ power+=4; pb.style.height=power+'%'; } }, 30);
    </script>
    """
    components.html(game_html, height=500)
    if st.button("⬅️ VOLTAR"): st.session_state.pagina = 'hub'; st.rerun()

# SALA: DRIBLE (RANDOM)
elif st.session_state.pagina == 'drible':
    st.markdown("<h2 style='text-align:center;'>⚽ RANDOM SLALOM</h2>", unsafe_allow_html=True)
    game_html = """
    <div id="f" style="height:480px; width:100%; background:#0D47A1; position:relative; border:4px solid #08306B; border-radius:20px; touch-action:none; overflow:hidden;">
        <div id="p" style="width:24px; height:24px; background:white; border-radius:50%; position:absolute; left:45%; bottom:50px; border:2px solid #333;"></div>
        <div id="gC"></div>
        <div id="jb" style="position:absolute; bottom:15px; left:15px; width:80px; height:80px; background:rgba(255,255,255,0.1); border-radius:50%; border:2px solid rgba(255,255,255,0.2);">
            <div id="js" style="position:absolute; top:20px; left:20px; width:40px; height:40px; background:rgba(255,255,255,0.3); border-radius:50%;"></div>
        </div>
        <button id="go" style="position:absolute; bottom:25px; right:25px; padding:10px; background:green; color:white; border:none; border-radius:10px;">GO!</button>
    </div>
    <script>
        const p=document.getElementById('p'), f=document.getElementById('f'), gC=document.getElementById('gCont'), jB=document.getElementById('jb'), jS=document.getElementById('js');
        let x=f.offsetWidth/2-12, y=380, run=false, jX=0, jY=0;
        jB.ontouchstart=(e)=>{this.drag=true; e.preventDefault();};
        window.ontouchmove=(e)=>{ if(!this.drag)return; let t=e.touches[0], r=jB.getBoundingClientRect(), dx=t.clientX-(r.left+40), dy=t.clientY-(r.top+40), d=Math.min(Math.sqrt(dx*dx+dy*dy),40); jX=Math.cos(Math.atan2(dy,dx)); jY=Math.sin(Math.atan2(dy,dx)); jS.style.transform=`translate(${jX*(d/40)*25}px, ${jY*(d/40)*25}px)`; };
        window.ontouchend=()=>{this.drag=false;};
        document.getElementById('go').onclick=()=>{ run=true; document.getElementById('go').style.display='none'; };
        function loop(){
            if(run){ x+=jX*5; y+=jY*5; x=Math.max(0,Math.min(x,f.offsetWidth-24)); y=Math.max(0,Math.min(y,f.offsetHeight-24)); p.style.left=x+'px'; p.style.top=y+'px'; if(y<10){ window.parent.location.href=window.parent.location.href.split('?')[0]+"?score=1000"; run=false; } }
            requestAnimationFrame(loop);
        }
        loop();
    </script>
    """
    components.html(game_html, height=500)
    if st.button("⬅️ VOLTAR"): st.session_state.pagina = 'hub'; st.rerun()

# SALA: VELOCIDADE
elif st.session_state.pagina == 'vel':
    st.markdown("<h2 style='text-align:center;'>⚡ GHOST SPRINT</h2>", unsafe_allow_html=True)
    game_html = """
    <div id="f" style="height:480px; width:100%; background:#0D47A1; position:relative; overflow:hidden; border:4px solid #08306B; border-radius:20px;">
        <div id="p" style="width:24px; height:24px; background:white; border-radius:50%; position:absolute; left:45%; bottom:40px; border:2px solid #333;"></div>
        <button id="go" style="position:absolute; bottom:25px; right:25px; padding:10px; background:green; color:white; border-radius:10px;">GO!</button>
    </div>
    <script>
        let run=false, y=410;
        document.getElementById('go').onclick=()=>{run=true; document.getElementById('go').style.display='none';};
        function loop(){ if(run){ y-=6; document.getElementById('p').style.top=y+'px'; if(y<10){ window.parent.location.href=window.parent.location.href.split('?')[0]+"?v_time=6.5"; run=false; } } requestAnimationFrame(loop); }
        loop();
    </script>
    """
    components.html(game_html, height=500)
    if st.button("⬅️ VOLTAR"): st.session_state.pagina = 'hub'; st.rerun()

# RELATÓRIOS
elif st.session_state.pagina == 'rel_d':
    st.markdown(f"<h2>DRIBLE: {st.session_state.pts_d} PTS</h2>", unsafe_allow_html=True)
    if st.button("HUB"): st.query_params.clear(); st.session_state.pagina = 'hub'; st.rerun()
elif st.session_state.pagina == 'rel_p':
    st.markdown(f"<h2>PASSE: {st.session_state.pts_p} PTS</h2>", unsafe_allow_html=True)
    if st.button("HUB"): st.query_params.clear(); st.session_state.pagina = 'hub'; st.rerun()
elif st.session_state.pagina == 'rel_v':
    st.markdown(f"<h2>VELOCIDADE: {st.session_state.tm_v}s</h2>", unsafe_allow_html=True)
    if st.button("HUB"): st.query_params.clear(); st.session_state.pagina = 'hub'; st.rerun()

# FIM DO CÓDIGO
