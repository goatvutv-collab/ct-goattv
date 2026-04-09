import streamlit as st
import streamlit.components.v1 as components

# --- 1. CONFIGURAÇÃO E ESTÉTICA GOAT TV ---
st.set_page_config(page_title="GOAT TV - CT BASE", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #0E0E2C; color: #FFF; font-family: sans-serif; }
    .ct-title { text-align: center; font-size: 26px; font-weight: 800; color: #FFD700; margin-bottom: 10px; }
    div.stButton > button { width: 100%!important; height: 48px!important; border-radius: 50px!important; border: none!important; color: white!important; font-weight: 700!important; box-shadow: 0 4px 10px rgba(0,0,0,0.5)!important; }
    iframe { border-radius: 20px; border: 3px solid #1E3A8A; background: transparent; }
    .stats-box { background-color: #1B5E20; padding: 20px; border-radius: 20px; text-align: center; border: 1px solid #FFD700; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 2. MOTOR DE NAVEGAÇÃO ---
if 'pagina' not in st.session_state: st.session_state.pagina = 'hub'
p_st = st.query_params

if "score" in p_st: st.session_state.pts_d = int(p_st["score"]); st.session_state.pagina = 'rel_d'
elif "v_time" in p_st: st.session_state.tm_v = float(p_st["v_time"]); st.session_state.pagina = 'rel_v'
elif "p_score" in p_st: 
    st.session_state.pts_p = int(p_st["p_score"]); st.session_state.hits_p = int(p_st.get("hits", 0))
    st.session_state.pagina = 'rel_p'

# --- 3. TELAS ---

# HUB DIRETO (SEM PIN)
if st.session_state.pagina == 'hub':
    st.markdown("<h1 class='ct-title'>CENTRO DE TREINAMENTO</h1>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⚽ DRIBLE FLUIDO"): st.session_state.pagina = 'drible'; st.rerun()
        if st.button("🎯 PASSE DE PRECISÃO"): st.session_state.pagina = 'passe'; st.rerun()
    with c2:
        if st.button("⚡ VELOCIDADE FPS"): st.session_state.pagina = 'vel'; st.rerun()
        if st.button("🔄 RECARREGAR"): st.rerun()

# SALA 1: DRIBLE (LERP PARA FLUIDEZ)
elif st.session_state.pagina == 'drible':
    st.markdown("<h2 style='text-align:center;'>⚽ CONTROLE DE BOLA</h2>", unsafe_allow_html=True)
    game_html = """
    <div id="f" style="height:480px; width:100%; background:#0D47A1; position:relative; overflow:hidden; border:4px solid #08306B; touch-action:none; border-radius:20px;">
        <div id="p" style="width:24px; height:24px; background:white; border-radius:50%; position:absolute; left:45%; bottom:50px; border:2px solid #333; z-index:30;">⚽</div>
        <div id="gC"></div>
        <div id="jb" style="position:absolute; bottom:15px; left:15px; width:80px; height:80px; background:rgba(255,255,255,0.1); border-radius:50%; border:2px solid rgba(255,255,255,0.2); z-index:100;"><div id="js" style="position:absolute; top:20px; left:20px; width:40px; height:40px; background:rgba(255,255,255,0.3); border-radius:50%;"></div></div>
        <button id="go" style="position:absolute; bottom:25px; right:25px; padding:10px 20px; background:green; color:white; border-radius:10px; border:none; font-weight:bold; z-index:100;">GO!</button>
        <div style="position:absolute; top:5px; width:100%; text-align:center; color:white; font-weight:bold;">TEMPO: <span id="t_ui">15.0</span>s</div>
    </div>
    <style>.c{width:16px;height:16px;background:orange;border-radius:50%;position:absolute;border:1px solid #CC5500;}</style>
    <script>
        const p=document.getElementById('p'), f=document.getElementById('f'), jB=document.getElementById('jb'), jS=document.getElementById('js');
        let x=f.offsetWidth/2-12, y=380, time=15.0, run=false, jX=0, jY=0, curX=0, curY=0, drag=false;
        function build(){
            document.getElementById('gC').innerHTML='';
            for(let i=0; i<6; i++){
                let rx=Math.random()*70+5;
                document.getElementById('gC').innerHTML+=`<div class="c" style="left:${rx}%; top:${60+i*50}px;"></div>`;
            }
        }
        jB.ontouchstart=(e)=>{drag=true; e.preventDefault();};
        window.ontouchmove=(e)=>{ if(!drag)return; let t=e.touches[0], r=jB.getBoundingClientRect(), dx=t.clientX-(r.left+40), dy=t.clientY-(r.top+40), d=Math.min(Math.sqrt(dx*dx+dy*dy),40), a=Math.atan2(dy,dx); jX=Math.cos(a)*(d/40); jY=Math.sin(a)*(d/40); jS.style.transform=`translate(${jX*25}px, ${jY*25}px)`; };
        window.ontouchend=()=>{drag=false; jX=0; jY=0; jS.style.transform='translate(0,0)';};
        document.getElementById('go').onclick=()=>{ build(); run=true; document.getElementById('go').style.display='none'; };
        function loopD(){
            if(run && time>0){
                time-=0.016; document.getElementById('t_ui').innerHTML=time.toFixed(1);
                curX += (jX * 5.5 - curX) * 0.12; curY += (jY * 5.5 - curY) * 0.12;
                x += curX; y += curY;
                x=Math.max(0,Math.min(x,f.offsetWidth-24)); y=Math.max(0,Math.min(y,f.offsetHeight-24));
                p.style.left=x+'px'; p.style.top=y+'px';
                if(y<10) window.parent.location.href=window.parent.location.href.split('?')[0]+"?score="+Math.round(time*100);
            }
            requestAnimationFrame(loopD);
        }
        loopD();
    </script>
    """
    components.html(game_html, height=500)
    if st.button("⬅️ VOLTAR"): st.session_state.pagina = 'hub'; st.rerun()

# SALA 2: PASSE (COM BARRA DE PRECISÃO REAL)
elif st.session_state.pagina == 'passe':
    st.markdown("<h2 style='text-align:center;'>🎯 PASSE DE PRECISÃO</h2>", unsafe_allow_html=True)
    game_html = """
    <div id="f" style="height:460px; width:100%; background:#1B5E20; position:relative; overflow:hidden; border:4px solid #08306B; touch-action:none; border-radius:20px;">
        <div id="ui" style="position:absolute; top:10px; width:100%; text-align:center; color:white; font-weight:bold; z-index:50;">ACERTOS: <span id="h_ui">0</span>/10 | BOLAS: <span id="t_ui">10</span></div>
        <div id="p" style="width:26px; height:26px; background:white; border-radius:50%; position:absolute; left:46%; bottom:40px; border:2px solid #333; z-index:35;">⚽</div>
        <div id="tgt" style="width:35px; height:35px; background:rgba(255,215,0,0.6); border:2px dashed gold; border-radius:50%; position:absolute; left:46%; top:50px;"></div>
        <div id="ball" style="width:12px; height:12px; background:white; border-radius:50%; position:absolute; display:none; z-index:40;"></div>
        
        <div id="pb_bg" style="position:absolute; bottom:90px; right:25px; width:16px; height:100px; background:#333; border:2px solid white; border-radius:8px; overflow:hidden;">
            <div id="pb" style="width:100%; height:0%; background:linear-gradient(to top, #F44, #4CAF50 50%, #F44); position:absolute; bottom:0;"></div>
            <div style="position:absolute; top:45%; width:100%; height:10%; border-top:2px solid gold; border-bottom:2px solid gold; box-sizing:border-box;"></div>
        </div>
        
        <div id="opp" style="width:60px; height:16px; background:#F44; position:absolute; left:10%; top:152px; border-radius:4px; border:1px solid white; z-index:32;"></div>
        <div id="jb" style="position:absolute; bottom:15px; left:15px; width:80px; height:80px; background:rgba(255,255,255,0.1); border-radius:50%; border:2px solid rgba(255,255,255,0.2); z-index:100;"><div id="js" style="position:absolute; top:20px; left:20px; width:40px; height:40px; background:rgba(255,255,255,0.3); border-radius:50%;"></div></div>
        <button id="btnA" style="position:absolute; bottom:15px; right:15px; width:65px; height:65px; background:#4A90E2; color:white; border-radius:50%; font-weight:bold; font-size:24px; border:none; z-index:100;">A</button>
    </div>
    <script>
        const p=document.getElementById('p'), f=document.getElementById('f'), ball=document.getElementById('ball'), btnA=document.getElementById('btnA'), jB=document.getElementById('jb'), pb=document.getElementById('pb'), opp=document.getElementById('opp'), tgt=document.getElementById('tgt');
        let jX=0, jY=0, hits=0, tries=10, passing=false, pwr=0, pAct=false, oD=3.5;
        jB.ontouchstart=(e)=>{this.dr=true; e.preventDefault();};
        window.ontouchmove=(e)=>{ if(!this.dr)return; let t=e.touches[0], r=jB.getBoundingClientRect(), dx=t.clientX-(r.left+40), dy=t.clientY-(r.top+40), d=Math.min(Math.sqrt(dx*dx+dy*dy),40), a=Math.atan2(dy,dx); jX=Math.cos(a); jY=Math.sin(a); document.getElementById('js').style.transform=`translate(${jX*(d/40)*25}px, ${jY*(d/40)*25}px)`; };
        window.ontouchend=()=>{this.dr=false;};
        
        btnA.onpointerdown=()=>{ if(!passing && tries>0){ pAct=true; pwr=0; } };
        window.onpointerup=()=>{ if(pAct){ pAct=false; shoot(); } };

        function shoot(){
            passing=true; tries--; document.getElementById('t_ui').innerHTML=tries; ball.style.display='block';
            let bx=p.offsetLeft+8, by=p.offsetTop+8;
            // PRECISÃO: Verde (40-60%) dá velocidade ideal. Fora disso, a bola erra.
            let spd = (pwr > 40 && pwr < 60) ? 12 : (pwr >= 60 ? 18 : 5);
            let vx=jX*spd, vy=jY*spd;
            let anim=setInterval(()=>{
                bx+=vx; by+=vy; ball.style.left=bx+'px'; ball.style.top=by+'px';
                let tr=tgt.getBoundingClientRect(), br=ball.getBoundingClientRect(), or=opp.getBoundingClientRect();
                if(!(br.right<tr.left||br.left>tr.right||br.bottom<tr.top||br.top>tr.bottom)){ hits++; endB(anim); }
                else if(!(br.right<or.left||br.left>or.right||br.bottom<or.top||br.top>or.bottom)||bx<0||bx>f.offsetWidth||by<0||by>f.offsetHeight){ endB(anim); }
            }, 20);
        }
        function endB(a){ clearInterval(a); ball.style.display='none'; passing=false; pwr=0; pb.style.height='0%'; document.getElementById('h_ui').innerHTML=hits; if(tries<=0) endGame(); }
        function endGame(){ window.parent.location.href=window.parent.location.href.split('?')[0]+"?p_score="+(hits*200); }
        function loop(){
            if(pAct && pwr<100){ pwr+=3; pb.style.height=pwr+'%'; }
            let ox=opp.offsetLeft; if(ox>f.offsetWidth*0.85||ox<f.offsetWidth*0.06) oD*=-1;
            opp.style.left=(ox+oD)+'px'; requestAnimationFrame(loop);
        }
        loop();
    </script>
    """
    components.html(game_html, height=500)
    if st.button("⬅️ VOLTAR AO HUB"): st.session_state.pagina = 'hub'; st.rerun()

# SALA 3: VELOCIDADE (FPS TURBO + PAREDES LATERAIS)
elif st.session_state.pagina == 'vel':
    st.markdown("<h2 style='text-align:center;'>⚡ TURBO & REFLEXO</h2>", unsafe_allow_html=True)
    game_html = """
    <div id="f" style="height:480px; width:100%; background:#0D47A1; position:relative; overflow:hidden; border:6px solid #1E3A8A; border-radius:20px; touch-action:none;">
        <div id="p" style="width:24px; height:24px; background:white; border-radius:50%; position:absolute; left:45%; bottom:40px; border:2px solid #333;">⚽</div>
        <div style="width:100%; height:10px; background:yellow; position:absolute; top:0;"></div>
        <div id="tm" style="position:absolute; top:10px; right:10px; font-weight:bold; color:white;">0.00s</div>
        <div id="jb" style="position:absolute; bottom:15px; left:15px; width:80px; height:80px; background:rgba(255,255,255,0.1); border-radius:50%; border:2px solid rgba(255,255,255,0.2); z-index:100;"><div id="js" style="position:absolute; top:20px; left:20px; width:40px; height:40px; background:rgba(255,255,255,0.3); border-radius:50%;"></div></div>
    </div>
    <script>
        const p=document.getElementById('p'), f=document.getElementById('f'), jB=document.getElementById('jb');
        let x=f.offsetWidth/2-12, y=410, run=false, jX=0, jY=0, drag=false, mult=3, start=0;
        jB.ontouchstart=(e)=>{drag=true; if(!run){run=true; start=Date.now();} e.preventDefault();};
        window.ontouchmove=(e)=>{
            if(!drag)return; let touch=e.touches[0], r=jB.getBoundingClientRect(), dx=touch.clientX-(r.left+40), dy=touch.clientY-(r.top+40);
            let d=Math.min(Math.sqrt(dx*dx+dy*dy), 40), a=Math.atan2(dy,dx);
            jX=Math.cos(a)*(d/40); jY=Math.sin(a)*(d/40);
            if(d > 37){ p.style.background='gold'; p.style.boxShadow='0 0 15px gold'; mult=10; } else { p.style.background='white'; p.style.boxShadow='none'; mult=3; }
        };
        window.ontouchend=()=>{drag=false; jX=0; jY=0;};
        function loopV(){
            if(run){
                x+=jX*mult; y+=jY*mult; x=Math.max(8, Math.min(x, f.offsetWidth-32)); y=Math.max(0, Math.min(y, f.offsetHeight-24));
                p.style.left=x+'px'; p.style.top=y+'px';
                if(y<10) window.parent.location.href=window.parent.location.href.split('?')[0]+"?v_time="+((Date.now()-start)/1000).toFixed(2);
            }
            requestAnimationFrame(loopV);
        }
        loopV();
    </script>
    """
    components.html(game_html, height=500)
    if st.button("⬅️ VOLTAR"): st.session_state.pagina = 'hub'; st.rerun()

# RELATÓRIOS
elif st.session_state.pagina == 'rel_d':
    st.markdown(f"<div class='stats-box'><h2>DRIBLE: {st.session_state.pts_d} PTS</h2></div>", unsafe_allow_html=True)
    if st.button("HUB"): st.query_params.clear(); st.session_state.pagina = 'hub'; st.rerun()
elif st.session_state.pagina == 'rel_v':
    st.markdown(f"<div class='stats-box'><h2>VELOCIDADE: {st.session_state.tm_v}s</h2></div>", unsafe_allow_html=True)
    if st.button("HUB"): st.query_params.clear(); st.session_state.pagina = 'hub'; st.rerun()
elif st.session_state.pagina == 'rel_p':
    st.markdown(f"<div class='stats-box'><h2>PASSE: {st.session_state.pts_p} PTS</h2></div>", unsafe_allow_html=True)
    if st.button("HUB"): st.query_params.clear(); st.session_state.pagina = 'hub'; st.rerun()

# FIM DO CÓDIGO - GOAT TV 2026
