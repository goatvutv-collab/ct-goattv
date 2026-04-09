import streamlit as st
import streamlit.components.v1 as components

# --- 1. CONFIGURAÇÃO E DESIGN PREMIUM ---
st.set_page_config(page_title="GOAT TV - CT OFICIAL", layout="centered")
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

# --- 2. MOTOR DE ESTADOS ---
if 'pagina' not in st.session_state: st.session_state.pagina = 'hub'
p_st = st.query_params

if "score" in p_st: st.session_state.pts_d = int(p_st["score"]); st.session_state.pagina = 'rel_d'
elif "v_time" in p_st: st.session_state.tm_v = float(p_st["v_time"]); st.session_state.pagina = 'rel_v'
elif "p_score" in p_st: st.session_state.pts_p = int(p_st["p_score"]); st.session_state.pagina = 'rel_p'

# --- 3. TELAS ---

if st.session_state.pagina == 'hub':
    st.markdown("<h1 class='ct-title'>CENTRO DE TREINAMENTO</h1>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⚽ DRIBLE (CHECKPOINTS)"): st.session_state.pagina = 'drible'; st.rerun()
        if st.button("🎯 PASSE (3 ALVOS)"): st.session_state.pagina = 'passe'; st.rerun()
    with c2:
        if st.button("⚡ VELOCIDADE (INVISÍVEL)"): st.session_state.pagina = 'vel'; st.rerun()
        if st.button("🔄 RECARREGAR CT"): st.rerun()

# SALA 1: DRIBLE (CHECKPOINTS + LERP)
elif st.session_state.pagina == 'drible':
    st.markdown("<h2 style='text-align:center;'>⚽ CIRCUITO DE BALIZAS</h2>", unsafe_allow_html=True)
    game_html = """
    <div id="f" style="height:480px; width:100%; background:#0D47A1; position:relative; overflow:hidden; border:4px solid #08306B; touch-action:none; border-radius:20px;">
        <div id="p" style="width:26px; height:26px; background:white; border-radius:50%; position:absolute; left:15px; bottom:15px; border:2px solid #333; z-index:40;">⚽</div>
        <div id="goal" style="width:60px; height:60px; background:rgba(0,255,0,0.1); border:2px dashed lime; position:absolute; bottom:15px; right:15px; display:flex; align-items:center; justify-content:center; color:lime; font-size:10px;">CHEGADA</div>
        <div id="gC"></div>
        <div id="jb" style="position:absolute; bottom:15px; left:15px; width:80px; height:80px; background:rgba(255,255,255,0.1); border-radius:50%; z-index:100;"><div id="js" style="position:absolute; top:20px; left:20px; width:40px; height:40px; background:rgba(255,255,255,0.3); border-radius:50%;"></div></div>
        <div style="position:absolute; top:5px; width:100%; text-align:center; color:white; font-weight:bold; font-size:12px;">CHECKPOINTS: <span id="l_ui">0</span>/4</div>
    </div>
    <style>.c{width:12px;height:12px;background:orange;border-radius:50%;position:absolute;}.line{height:4px;background:rgba(0,255,0,0.2);position:absolute;z-index:10;}</style>
    <script>
        const p=document.getElementById('p'), f=document.getElementById('f'), gC=document.getElementById('gC');
        let x=15, y=440, jX=0, jY=0, curX=0, curY=0, linesGot=0, start=Date.now();
        const gates = [{x1:10,x2:35,y:300,g:0},{x1:40,x2:65,y:150,g:0},{x1:70,x2:95,y:300,g:0},{x1:40,x2:65,y:400,g:0}];
        function build(){
            gates.forEach((gt,i)=>{
                gC.innerHTML+=`<div class="c" style="left:${gt.x1}%; top:${gt.y}px;"></div><div class="c" style="left:${gt.x2}%; top:${gt.y}px;"></div>`;
                gC.innerHTML+=`<div id="l${i}" class="line" style="left:${gt.x1+2}%; top:${gt.y+4}px; width:${gt.x2-gt.x1-2}%;"></div>`;
            });
        }
        document.getElementById('jb').ontouchstart=(e)=>{this.dr=true; e.preventDefault();};
        window.ontouchmove=(e)=>{ if(!this.dr)return; let t=e.touches[0], r=document.getElementById('jb').getBoundingClientRect(), dx=t.clientX-(r.left+40), dy=t.clientY-(r.top+40), d=Math.min(Math.sqrt(dx*dx+dy*dy),40), a=Math.atan2(dy,dx); jX=Math.cos(a)*(d/40); jY=Math.sin(a)*(d/40); document.getElementById('js').style.transform=`translate(${jX*25}px, ${jY*25}px)`; };
        window.ontouchend=()=>{this.dr=false; jX=0; jY=0; document.getElementById('js').style.transform='translate(0,0)';};
        function loop(){
            curX+=(jX*5.5-curX)*0.15; curY+=(jY*5.5-curY)*0.15; x+=curX; y+=curY;
            x=Math.max(0,Math.min(x,f.offsetWidth-26)); y=Math.max(0,Math.min(y,f.offsetHeight-26));
            p.style.left=x+'px'; p.style.top=y+'px';
            gates.forEach((gt,i)=>{
                let lr=document.getElementById('l'+i).getBoundingClientRect(), pr=p.getBoundingClientRect();
                if(!gt.g && !(pr.right<lr.left||pr.left>lr.right||pr.bottom<lr.top||pr.top>lr.bottom)){ gt.g=1; linesGot++; document.getElementById('l'+i).style.background='lime'; document.getElementById('l_ui').innerHTML=linesGot; }
            });
            if(linesGot>=4 && x>f.offsetWidth-70 && y>f.offsetHeight-70){ window.parent.location.href=window.parent.location.href.split('?')[0]+"?score="+Math.round(2000-((Date.now()-start)/10)); }
            requestAnimationFrame(loop);
        }
        build(); loop();
    </script>
    """
    components.html(game_html, height=500)
    if st.button("⬅️ VOLTAR"): st.session_state.pagina = 'hub'; st.rerun()

# SALA 2: PASSE (3 ALVOS + BARRA + MARCADOR)
elif st.session_state.pagina == 'passe':
    st.markdown("<h2 style='text-align:center;'>🎯 RODA DE PASSE ELITE</h2>", unsafe_allow_html=True)
    game_html = """
    <div id="f" style="height:460px; width:100%; background:#1B5E20; position:relative; overflow:hidden; border:4px solid #08306B; touch-action:none; border-radius:20px;">
        <div id="ui" style="position:absolute; top:10px; width:100%; text-align:center; color:white; font-weight:bold; z-index:50; font-size:12px;">ACERTOS: <span id="h_ui">0</span>/10 | BOLAS: <span id="t_ui">10</span></div>
        <div id="p" style="width:26px; height:26px; background:white; border-radius:50%; position:absolute; left:46%; bottom:40px; border:2px solid #333; z-index:35;">⚽</div>
        <div id="t0" class="tgt" style="left:15%; top:60px;"></div><div id="t1" class="tgt" style="left:46%; top:40px;"></div><div id="t2" class="tgt" style="left:75%; top:60px;"></div>
        
        <div id="opp" style="width:60px; height:16px; background:#F44; position:absolute; left:10%; top:170px; border-radius:4px; border:1px solid white; z-index:32;"></div>
        
        <div id="pb_bg" style="position:absolute; bottom:90px; right:20px; width:16px; height:100px; background:#333; border:2px solid white; border-radius:8px; overflow:hidden;">
            <div id="pb" style="width:100%; height:0%; background:linear-gradient(to top, #F44, #4CAF50 50%, #F44); position:absolute; bottom:0;"></div>
            <div style="position:absolute; top:45%; width:100%; height:10%; border-top:2px solid gold; border-bottom:2px solid gold;"></div>
        </div>
        <div id="jb" style="position:absolute; bottom:15px; left:15px; width:80px; height:80px; background:rgba(255,255,255,0.1); border-radius:50%; z-index:100;"><div id="js" style="position:absolute; top:20px; left:20px; width:40px; height:40px; background:rgba(255,255,255,0.3); border-radius:50%;"></div></div>
        <button id="btnA" style="position:absolute; bottom:15px; right:15px; width:65px; height:65px; background:#4A90E2; color:white; border-radius:50%; font-weight:bold; font-size:24px; border:none; z-index:100;">A</button>
    </div>
    <style>.tgt{width:32px;height:32px;background:rgba(255,215,0,0.2);border:2px dashed gold;border-radius:50%;position:absolute;}.act{background:rgba(255,215,0,0.8);box-shadow:0 0 15px gold;}</style>
    <script>
        const p=document.getElementById('p'), f=document.getElementById('f'), btnA=document.getElementById('btnA'), pb=document.getElementById('pb'), opp=document.getElementById('opp'), tgts=document.querySelectorAll('.tgt');
        const ball=document.createElement('div'); ball.style.cssText="width:12px;height:12px;background:white;border-radius:50%;position:absolute;display:none;z-index:40;"; f.appendChild(ball);
        let jX=0, jY=0, hits=0, tries=10, passing=false, pwr=0, pAct=false, oD=4, curT=0;
        function upT(){ tgts.forEach((t,i)=>{t.className=i===curT?'tgt act':'tgt';}); }
        document.getElementById('jb').ontouchstart=(e)=>{this.dr=true; e.preventDefault();};
        window.ontouchmove=(e)=>{ if(!this.dr)return; let t=e.touches[0], r=document.getElementById('jb').getBoundingClientRect(), dx=t.clientX-(r.left+40), dy=t.clientY-(r.top+40), d=Math.min(Math.sqrt(dx*dx+dy*dy),40), a=Math.atan2(dy,dx); jX=Math.cos(a); jY=Math.sin(a); document.getElementById('js').style.transform=`translate(${jX*25}px, ${jY*25}px)`; };
        btnA.onpointerdown=()=>{ if(!passing && tries>0){ pAct=true; pwr=0; } };
        window.onpointerup=()=>{ if(pAct){ pAct=false; shoot(); } };
        function shoot(){
            passing=true; tries--; document.getElementById('t_ui').innerHTML=tries; ball.style.display='block';
            let bx=p.offsetLeft+8, by=p.offsetTop+8, spd=(pwr>40&&pwr<60)?14:(pwr>=60?22:6), vx=jX*spd, vy=jY*spd;
            let anim=setInterval(()=>{
                bx+=vx; by+=vy; ball.style.left=bx+'px'; ball.style.top=by+'px';
                let tr=tgts[curT].getBoundingClientRect(), br=ball.getBoundingClientRect(), or=opp.getBoundingClientRect();
                if(!(br.right<tr.left||br.left>tr.right||br.bottom<tr.top||br.top>tr.bottom)){ hits++; curT=(curT+1)%3; upT(); endB(anim); }
                else if(!(br.right<or.left||br.left>or.right||br.bottom<or.top||br.top>or.bottom)||bx<0||bx>f.offsetWidth||by<0||by>f.offsetHeight){ endB(anim); }
            }, 20);
        }
        function endB(a){ clearInterval(a); ball.style.display='none'; passing=false; pwr=0; pb.style.height='0%'; document.getElementById('h_ui').innerHTML=hits; if(tries<=0) window.parent.location.href=window.parent.location.href.split('?')[0]+"?p_score="+hits*200; }
        function loop(){
            if(pAct && pwr<100){ pwr+=3.5; pb.style.height=pwr+'%'; }
            let ox=opp.offsetLeft; if(ox>f.offsetWidth*0.85||ox<f.offsetWidth*0.06) oD*=-1;
            opp.style.left=(ox+oD)+'px'; requestAnimationFrame(loop);
        }
        upT(); loop();
    </script>
    """
    components.html(game_html, height=500)
    if st.button("⬅️ VOLTAR"): st.session_state.pagina = 'hub'; st.rerun()

# SALA 3: VELOCIDADE (INVISÍVEL + PISCADA + ANTI-CHEAT)
elif st.session_state.pagina == 'vel':
    st.markdown("<h2 style='text-align:center;'>⚡ REFLEXO FANTASMA</h2>", unsafe_allow_html=True)
    game_html = """
    <div id="f" style="height:480px; width:100%; background:#0D47A1; position:relative; overflow:hidden; border:8px solid #1E3A8A; border-radius:20px; touch-action:none;">
        <div id="p" style="width:24px; height:24px; background:white; border-radius:50%; position:absolute; left:45%; bottom:40px; border:2px solid #333; z-index:50;">⚽</div>
        <div style="width:100%; height:10px; background:yellow; position:absolute; top:0;"></div>
        <div id="tm" style="position:absolute; top:10px; right:10px; font-weight:bold; color:white;">0.00s</div>
        <div id="gC"></div>
        <div id="jb" style="position:absolute; bottom:15px; left:15px; width:80px; height:80px; background:rgba(255,255,255,0.1); border-radius:50%; z-index:100;"><div id="js" style="position:absolute; top:20px; left:20px; width:40px; height:40px; background:rgba(255,255,255,0.3); border-radius:50%;"></div></div>
    </div>
    <style>
        .wall{position:absolute; background:#0D47A1; border:1px solid rgba(255,255,255,0.01); transition: 0.2s;}
        .blink{background:rgba(255,255,255,0.15) !important; border:1px solid white !important;}
    </style>
    <script>
        const p=document.getElementById('p'), f=document.getElementById('f'), gC=document.getElementById('gC');
        let x=f.offsetWidth/2-12, y=410, run=false, jX=0, jY=0, mult=3.5, start=0, walls=[];
        for(let i=0; i<8; i++){
            let w=document.createElement('div'); w.className='wall';
            let ww=75, wx=Math.random()*25;
            w.style.cssText=`width:${ww}%; height:16px; left:${wx}%; top:${50+i*45}px;`;
            gC.appendChild(w); walls.push(w);
        }
        setInterval(()=>{ walls.forEach(w=>{ if(Math.random()>0.5) w.classList.add('blink'); setTimeout(()=>w.classList.remove('blink'), 300); }); }, 1500);
        document.getElementById('jb').ontouchstart=(e)=>{this.dr=true; if(!run){run=true; start=Date.now();} e.preventDefault();};
        window.ontouchmove=(e)=>{
            if(!this.dr)return; let t=e.touches[0], r=document.getElementById('jb').getBoundingClientRect(), dx=t.clientX-(r.left+40), dy=t.clientY-(r.top+40), d=Math.min(Math.sqrt(dx*dx+dy*dy), 40), a=Math.atan2(dy,dx);
            jX=Math.cos(a)*(d/40); jY=Math.sin(a)*(d/40);
            if(d > 37){ p.style.background='gold'; p.style.boxShadow='0 0 15px gold'; mult=11; } else { p.style.background='white'; mult=4; }
        };
        function loop(){
            if(run){
                x+=jX*mult; y+=jY*mult; x=Math.max(10, Math.min(x, f.offsetWidth-35)); y=Math.max(0, Math.min(y, f.offsetHeight-24));
                p.style.left=x+'px'; p.style.top=y+'px';
                walls.forEach(w=>{
                    let wr=w.getBoundingClientRect(), pr=p.getBoundingClientRect();
                    if(!(pr.right<wr.left||pr.left>wr.right||pr.bottom<wr.top||pr.top>wr.bottom)){ x=f.offsetWidth/2-12; y=410; p.style.background='red'; setTimeout(()=>p.style.background='white',200); }
                });
                if(y<10) window.parent.location.href=window.parent.location.href.split('?')[0]+"?v_time="+((Date.now()-start)/1000).toFixed(2);
            }
            requestAnimationFrame(loop);
        }
        loop();
    </script>
    """
    components.html(game_html, height=500)
    if st.button("⬅️ VOLTAR"): st.session_state.pagina = 'hub'; st.rerun()

# RELATÓRIOS
elif st.session_state.pagina == 'rel_d':
    st.markdown(f"<div class='stats-box'><h2>RESULTADO DRIBLE: {st.session_state.pts_d} PTS</h2></div>", unsafe_allow_html=True)
    if st.button("HUB"): st.query_params.clear(); st.session_state.pagina = 'hub'; st.rerun()
elif st.session_state.pagina == 'rel_v':
    st.markdown(f"<div class='stats-box'><h2>TEMPO VELOCIDADE: {st.session_state.tm_v}s</h2></div>", unsafe_allow_html=True)
    if st.button("HUB"): st.query_params.clear(); st.session_state.pagina = 'hub'; st.rerun()
elif st.session_state.pagina == 'rel_p':
    st.markdown(f"<div class='stats-box'><h2>PONTOS DE PASSE: {st.session_state.pts_p} PTS</h2></div>", unsafe_allow_html=True)
    if st.button("HUB"): st.query_params.clear(); st.session_state.pagina = 'hub'; st.rerun()

# FIM DO CÓDIGO - GOAT TV 2026
