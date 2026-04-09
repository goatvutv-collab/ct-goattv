import streamlit as st
import streamlit.components.v1 as components

# --- 1. CONFIG E DESIGN ---
st.set_page_config(page_title="GOAT TV - CT OFICIAL", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #0E0E2C; color: #FFF; font-family: sans-serif; }
    .ct-title { text-align: center; font-size: 24px; font-weight: 800; color: #FFD700; margin-bottom: 10px; }
    div.stButton > button { width: 100%!important; height: 45px!important; border-radius: 50px!important; border: none!important; color: white!important; font-weight: 700!important; box-shadow: 0 4px 10px rgba(0,0,0,0.4)!important; }
    iframe { border-radius: 20px; border: 3px solid #1E3A8A; background: transparent; }
    .stats-box { background-color: #1B5E20; padding: 20px; border-radius: 20px; border: 1px solid #2E7D32; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# --- 2. MOTOR DE ESTADOS ---
if 'pagina' not in st.session_state: st.session_state.pagina = 'login'
p_st = st.query_params

if "score" in p_st: st.session_state.pts_d = int(p_st["score"]); st.session_state.pagina = 'rel_d'
elif "v_time" in p_st: st.session_state.tm_v = float(p_st["v_time"]); st.session_state.pagina = 'rel_v'
elif "p_score" in p_st: 
    st.session_state.pts_p = int(p_st["p_score"])
    st.session_state.hits_p = int(p_st.get("hits", 0))
    st.session_state.pagina = 'rel_p'

# --- 3. TELAS ---
if st.session_state.pagina == 'login':
    st.markdown("<h1 class='ct-title'>🛡️ ACESSO CT GOAT TV</h1>", unsafe_allow_html=True)
    if st.button("ENTRAR NO CT"): st.session_state.pagina = 'hub'; st.rerun()

elif st.session_state.pagina == 'hub':
    st.markdown("<h1 class='ct-title'>CENTRO DE TREINAMENTO</h1>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⚽ DRIBLE"): st.session_state.pagina = 'drible'; st.rerun()
        if st.button("🎯 PASSE MAESTRO"): st.session_state.pagina = 'passe'; st.rerun()
    with c2:
        if st.button("⚡ VELOCIDADE"): st.session_state.pagina = 'vel'; st.rerun()

# SALA: PASSE MAESTRO (1 MARCADOR + 10 TENTATIVAS)
elif st.session_state.pagina == 'passe':
    st.markdown("<h2 style='text-align:center;'>🎯 PASSE DE PRECISÃO</h2>", unsafe_allow_html=True)
    game_html = """
    <div id="f" style="height:460px; width:100%; background:#1B5E20; position:relative; overflow:hidden; border:4px solid #08306B; touch-action:none; border-radius:20px;">
        <div id="ui" style="position:absolute; top:10px; width:100%; text-align:center; color:white; font-weight:bold; z-index:50; font-size:12px;">ACERTOS: <span id="h_ui">0</span>/10 | TENTATIVAS: <span id="t_ui">10</span></div>
        <div id="p" style="width:26px; height:26px; background:white; border-radius:50%; position:absolute; left:46%; bottom:35px; border:2px solid #333; z-index:35;"></div>
        <div id="t0" class="tgt" style="left:15%; top:60px;"></div><div id="t1" class="tgt" style="left:46%; top:40px;"></div><div id="t2" class="tgt" style="left:75%; top:60px;"></div>
        <div id="ball" style="width:12px; height:12px; background:white; border-radius:50%; position:absolute; display:none; z-index:40;"></div>
        <div id="aim" style="width:2px; height:80px; background:rgba(255,255,255,0.3); position:absolute; left:50%; bottom:50px; transform-origin: bottom center; display:none; z-index:30;"></div>
        <div id="o1" class="opp" style="left:10%; top:150px;"></div>
        <div id="jb" style="position:absolute; bottom:15px; left:15px; width:80px; height:80px; background:rgba(255,255,255,0.1); border-radius:50%; border:2px solid rgba(255,255,255,0.2); z-index:100;"><div id="js" style="position:absolute; top:20px; left:20px; width:40px; height:40px; background:rgba(255,255,255,0.3); border-radius:50%;"></div></div>
        <button id="btnA" style="position:absolute; bottom:15px; right:15px; width:65px; height:65px; background:#4A90E2; color:white; border-radius:50%; font-weight:bold; font-size:24px; border:none; z-index:100;">A</button>
    </div>
    <style>.tgt{width:32px;height:32px;background:rgba(255,215,0,0.2);border:2px dashed gold;border-radius:50%;position:absolute;}.act{background:rgba(255,215,0,0.7);opacity:1;}.opp{width:60px;height:16px;background:#F44;position:absolute;border-radius:4px;border:1px solid white;z-index:32;}</style>
    <script>
        const p=document.getElementById('p'), f=document.getElementById('f'), ball=document.getElementById('ball'), btnA=document.getElementById('btnA'), jB=document.getElementById('jb'), jS=document.getElementById('js'), aim=document.getElementById('aim'), op1=document.getElementById('o1'), tgts=document.querySelectorAll('.tgt');
        let jX=0, jY=0, hits=0, tries=10, pass=false, o1D=1, curT=0, start=0, sttd=false;
        function upT(){ tgts.forEach((t,i)=>{t.className=i===curT?'tgt act':'tgt';}); }
        jB.ontouchstart=(e)=>{this.dr=true; e.preventDefault(); if(!sttd){sttd=true; start=Date.now();}};
        window.ontouchmove=(e)=>{ if(!this.dr)return; let t=e.touches[0], r=jB.getBoundingClientRect(), dx=t.clientX-(r.left+40), dy=t.clientY-(r.top+40), d=Math.min(Math.sqrt(dx*dx+dy*dy),40), a=Math.atan2(dy,dx); jX=Math.cos(a); jY=Math.sin(a); jS.style.transform=`translate(${jX*(d/40)*25}px, ${jY*(d/40)*25}px)`; aim.style.display='block'; aim.style.transform=`rotate(${(a*180/Math.PI)+90}deg)`; };
        window.ontouchend=()=>{this.dr=false; aim.style.display='none';};
        btnA.onclick=()=>{ if(!pass && tries>0){ if(!sttd){sttd=true; start=Date.now();} shoot(); } };
        function shoot(){
            pass=true; tries--; ball.style.display='block'; let bx=p.offsetLeft+8, by=p.offsetTop+8, vx=jX*12, vy=jY*12;
            let anim=setInterval(()=>{
                bx+=vx; by+=vy; ball.style.left=bx+'px'; ball.style.top=by+'px';
                let tr=tgts[curT].getBoundingClientRect(), br=ball.getBoundingClientRect(), or1=op1.getBoundingClientRect();
                if(!(br.right<tr.left||br.left>tr.right||br.bottom<tr.top||br.top>tr.bottom)){ hits++; curT=(curT+1)%3; upT(); endB(anim); }
                else if(!(br.right<or1.left||br.left>or1.right||br.bottom<or1.top||br.top>or1.bottom)||bx<0||bx>f.offsetWidth||by<0||by>f.offsetHeight){ endB(anim); }
            }, 20);
        }
        function endB(a){ clearInterval(a); ball.style.display='none'; pass=false; document.getElementById('h_ui').innerHTML=hits; document.getElementById('t_ui').innerHTML=tries; if(tries<=0) endG(); }
        function endG(){ let ft=(Date.now()-start)/1000; let bn=ft<12?Math.round((12-ft)*400):0; window.parent.location.href=window.parent.location.href.split('?')[0]+"?p_score="+((hits*200)+bn)+"&hits="+hits; }
        function loop(){
            let x1=op1.offsetLeft; if(x1>f.offsetWidth-65||x1<10) o1D*=-1; op1.style.left=(x1+o1D*3.5)+'px';
            requestAnimationFrame(loop);
        }
        upT(); loop();
    </script>
    """
    components.html(game_html, height=500)
    if st.button("⬅️ HUB"): st.session_state.pagina = 'hub'; st.rerun()

# --- RELATÓRIO DE ATRIBUTOS ---
elif st.session_state.pagina == 'rel_p':
    st.markdown("<h1 class='ct-title'>ANÁLISE DO MAESTRO</h1>", unsafe_allow_html=True)
    hits = st.session_state.get('hits_p', 0)
    pts = st.session_state.get('pts_p', 0)
    st.markdown(f"""
        <div class='stats-box'>
            <h2 style='color:#FFD700;'>{pts} PONTOS</h2>
            <hr>
            <p style='color:#4CAF50;'>✔️ <b>Passe Curto:</b> +{hits * 4}%</p>
            <p style='color:#4CAF50;'>✔️ <b>Decisão:</b> +{hits * 2}%</p>
            <p style='color:#F44336;'>❌ <b>Finalização:</b> -1% (Foco Técnico)</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("HUB"): st.query_params.clear(); st.session_state.pagina = 'hub'; st.rerun()

# --- SESSÃO DRIBLE E VELOCIDADE (INTEGRADAS) ---
elif st.session_state.pagina == 'vel':
    st.markdown("<h2 style='text-align:center;'>⚡ GHOST SPRINT</h2>", unsafe_allow_html=True)
    if st.button("SIMULAR VELOCIDADE"): st.query_params.update(v_time=6.8); st.rerun()
    if st.button("⬅️ HUB"): st.session_state.pagina = 'hub'; st.rerun()

elif st.session_state.pagina == 'drible':
    st.markdown("<h2 style='text-align:center;'>⚽ SLALOM</h2>", unsafe_allow_html=True)
    if st.button("SIMULAR DRIBLE"): st.query_params.update(score=2200); st.rerun()
    if st.button("⬅️ HUB"): st.session_state.pagina = 'hub'; st.rerun()
