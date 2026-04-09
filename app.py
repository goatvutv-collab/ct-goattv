import streamlit as st
import streamlit.components.v1 as components

# --- 1. CONFIGURAÇÃO GOAT TV ---
st.set_page_config(page_title="GOAT TV - CT CIRCUITO U", layout="centered")
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

if "score" in p_st: st.session_state.pts_d = float(p_st["score"]); st.session_state.pagina = 'rel_d'
elif "v_time" in p_st: st.session_state.tm_v = float(p_st["v_time"]); st.session_state.pagina = 'rel_v'
elif "p_score" in p_st: st.session_state.pts_p = int(p_st["p_score"]); st.session_state.pagina = 'rel_p'

# --- 3. TELAS ---

if st.session_state.pagina == 'hub':
    st.markdown("<h1 class='ct-title'>CENTRO DE TREINAMENTO</h1>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⚽ DRIBLE CIRCUITO U"): st.session_state.pagina = 'drible'; st.rerun()
        if st.button("🎯 PASSE MAESTRO"): st.session_state.pagina = 'passe'; st.rerun()
    with c2:
        if st.button("⚡ REFLEXO FANTASMA"): st.session_state.pagina = 'vel'; st.rerun()
        if st.button("🔄 RECARREGAR"): st.rerun()

# --- SALA 1: DRIBLE (CIRCUITO EM U + BLOCOS MÓVEIS + TEMPO) ---
elif st.session_state.pagina == 'drible':
    st.markdown("<h2 style='text-align:center;'>⚽ CIRCUITO EM U</h2>", unsafe_allow_html=True)
    game_html = """
    <div id="f" style="height:480px; width:100%; background:#0D47A1; position:relative; overflow:hidden; border:4px solid #08306B; touch-action:none; border-radius:20px;">
        <div id="p" style="width:26px; height:26px; background:white; border-radius:50%; position:absolute; left:15%; bottom:20px; border:2px solid #333; z-index:40;">⚽</div>
        <div id="aim" style="width:2px; height:60px; background:rgba(255,255,255,0.3); position:absolute; transform-origin: bottom center; display:none; z-index:35;"></div>
        
        <div id="obs1" style="width:50px; height:14px; background:#F44; position:absolute; left:8%; top:240px; border-radius:4px; border:1px solid white; z-index:32;"></div>
        <div id="obs2" style="width:14px; height:50px; background:#F44; position:absolute; left:46%; top:35px; border-radius:4px; border:1px solid white; z-index:32;"></div>
        <div id="obs3" style="width:50px; height:14px; background:#F44; position:absolute; right:8%; top:240px; border-radius:4px; border:1px solid white; z-index:32;"></div>

        <div id="gC"></div>
        <div id="arrow" style="position:absolute; width:30px; height:30px; z-index:100; pointer-events:none; font-size:24px;">⬇️</div>
        <div id="jb" style="position:absolute; bottom:15px; left:15px; width:80px; height:80px; background:rgba(255,255,255,0.1); border-radius:50%; z-index:100;"><div id="js" style="position:absolute; top:20px; left:20px; width:40px; height:40px; background:rgba(255,255,255,0.3); border-radius:50%;"></div></div>
        <div style="position:absolute; top:5px; width:100%; text-align:center; color:white; font-weight:bold; font-size:12px;">TIME: <span id="t_ui">0.00</span>s | GATES: <span id="l_ui">1</span>/4</div>
    </div>
    <style>.c{width:12px;height:12px;background:orange;border-radius:50%;position:absolute;}.line{height:4px;background:rgba(0,255,0,0.2);position:absolute;}</style>
    <script>
        const p=document.getElementById('p'), aim=document.getElementById('aim'), jB=document.getElementById('jb'), js=document.getElementById('js'), f=document.getElementById('f'), gC=document.getElementById('gC'), arr=document.getElementById('arrow');
        const ob1=document.getElementById('obs1'), ob2=document.getElementById('obs2'), ob3=document.getElementById('obs3');
        let x=p.offsetLeft, y=p.offsetTop, jX=0, jY=0, curX=0, curY=0, drag=false, step=0, start=Date.now(), run=false;
        let d1=2.5, d2=3.5, d3=-2.5;

        const gates = [
            {x1:10,x2:35,y:350}, // Esquerda Inferior
            {x1:10,x2:35,y:80},  // Esquerda Superior
            {x1:65,x2:90,y:80},  // Direita Superior
            {x1:65,x2:90,y:350}  // Direita Inferior (FIM)
        ];
        
        gates.forEach((gt,i)=>{ gC.innerHTML+=`<div class="c" style="left:${gt.x1}%; top:${gt.y}px;"></div><div class="c" style="left:${gt.x2}%; top:${gt.y}px;"></div><div id="l${i}" class="line" style="left:${gt.x1+2}%; top:${gt.y+4}px; width:${gt.x2-gt.x1-2}%;"></div>`; });

        jB.ontouchstart=(e)=>{drag=true; run=true; aim.style.display='block'; e.preventDefault();};
        window.ontouchmove=(e)=>{
            if(!drag)return; let t=e.touches[0], r=jB.getBoundingClientRect(), dx=t.clientX-(r.left+40), dy=t.clientY-(r.top+40), d=Math.min(Math.sqrt(dx*dx+dy*dy),40), a=Math.atan2(dy,dx);
            jX=Math.cos(a)*(d/40); jY=Math.sin(a)*(d/40); js.style.transform=`translate(${jX*25}px, ${jY*25}px)`;
            aim.style.transform=`rotate(${(a*180/Math.PI)+90}deg)`; aim.style.left=(p.offsetLeft+12)+'px'; aim.style.top=(p.offsetTop-45)+'px';
        };
        window.ontouchend=()=>{drag=false; jX=jY=0; aim.style.display='none';};

        function loop(){
            if(run){
                document.getElementById('t_ui').innerHTML=((Date.now()-start)/1000).toFixed(2);
                curX+=(jX*5.5-curX)*0.15; curY+=(jY*5.5-curY)*0.15; x+=curX; y+=curY;
                x=Math.max(5,Math.min(x,f.offsetWidth-30)); y=Math.max(5,Math.min(y,f.offsetHeight-30));
                p.style.left=x+'px'; p.style.top=y+'px';
                
                // Movimento Obstáculos (Bouncing)
                let oy1=ob1.offsetTop; if(oy1>340||oy1<90) d1*=-1; ob1.style.top=(oy1+d1)+'px';
                let ox2=ob2.offsetLeft; if(ox2>f.offsetWidth*0.7||ox2<f.offsetWidth*0.2) d2*=-1; ob2.style.left=(ox2+d2)+'px';
                let oy3=ob3.offsetTop; if(oy3>340||oy3<90) d3*=-1; ob3.style.top=(oy3+d3)+'px';

                // Colisão com Obstáculos
                [ob1, ob2, ob3].forEach(ob=>{
                    let or=ob.getBoundingClientRect(), pr=p.getBoundingClientRect();
                    if(!(pr.right<or.left||pr.left>or.right||pr.bottom<or.top||pr.top>or.bottom)){ x-=curX*5; y-=curY*5; p.style.background='red'; setTimeout(()=>p.style.background='white',100); }
                });

                if(step < 4){
                    let lr=document.getElementById('l'+step).getBoundingClientRect(), pr=p.getBoundingClientRect();
                    if(!(pr.right<lr.left||pr.left>lr.right||pr.bottom<lr.top||pr.top>lr.bottom)){ document.getElementById('l'+step).style.background='lime'; step++; if(step<4) document.getElementById('l_ui').innerHTML=step+1; }
                    let target=document.getElementById('l'+(step<4?step:3)).getBoundingClientRect(), field=f.getBoundingClientRect();
                    arr.style.left=(target.left-field.left+15)+'px'; arr.style.top=(target.top-field.top-35)+'px';
                } else { window.parent.location.href=window.parent.location.href.split('?')[0]+"?score="+((Date.now()-start)/1000).toFixed(2); run=false; }
            }
            requestAnimationFrame(loop);
        }
        loop();
    </script>
    """
    components.html(game_html, height=500)
    if st.button("⬅️ HUB"): st.session_state.pagina = 'hub'; st.rerun()

# --- SALA 2: PASSE MAESTRO (HOMOLOGADO 100%) ---
elif st.session_state.pagina == 'passe':
    st.markdown("<h2 style='text-align:center;'>🎯 PASSE MAESTRO</h2>", unsafe_allow_html=True)
    game_html = """
    <div id="f" style="height:460px; width:100%; background:#1B5E20; position:relative; overflow:hidden; border:4px solid #08306B; touch-action:none; border-radius:20px;">
        <div id="ui" style="position:absolute; top:10px; width:100%; text-align:center; color:white; font-weight:bold; z-index:50;">ACERTOS: <span id="h_ui">0</span>/10 | BOLAS: <span id="t_ui">10</span></div>
        <div id="p" style="width:26px; height:26px; background:white; border-radius:50%; position:absolute; left:46%; bottom:40px; border:2px solid #333; z-index:40;">⚽</div>
        <div id="aim" style="width:2px; height:70px; background:rgba(255,255,255,0.3); position:absolute; transform-origin: bottom center; display:none; z-index:35;"></div>
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
        const p=document.getElementById('p'), aim=document.getElementById('aim'), btnA=document.getElementById('btnA'), pb=document.getElementById('pb'), opp=document.getElementById('opp'), tgts=document.querySelectorAll('.tgt');
        const ball=document.createElement('div'); ball.style.cssText="width:12px;height:12px;background:white;border-radius:50%;position:absolute;display:none;z-index:40;"; f.appendChild(ball);
        let jX=0, jY=0, hits=0, tries=10, passing=false, pwr=0, pAct=false, oD=4, curT=1;
        function upT(){ tgts.forEach((t,i)=>{t.className=i===curT?'tgt act':'tgt';}); }
        document.getElementById('jb').ontouchstart=(e)=>{this.dr=true; aim.style.display='block'; e.preventDefault();};
        window.ontouchmove=(e)=>{
            if(!this.dr)return; let t=e.touches[0], r=document.getElementById('jb').getBoundingClientRect(), dx=t.clientX-(r.left+40), dy=t.clientY-(r.top+40), d=Math.min(Math.sqrt(dx*dx+dy*dy),40), a=Math.atan2(dy,dx);
            jX=Math.cos(a)*(d/40); jY=Math.sin(a)*(d/40); document.getElementById('js').style.transform=`translate(${jX*25}px, ${jY*25}px)`;
            aim.style.transform=`rotate(${(a*180/Math.PI)+90}deg)`;
        };
        window.ontouchend=()=>{this.dr=false; aim.style.display='none';};
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
        function loop(){ if(pAct && pwr<100){ pwr+=3.5; pb.style.height=pwr+'%'; } let ox=opp.offsetLeft; if(ox>f.offsetWidth*0.85||ox<f.offsetWidth*0.06) oD*=-1; opp.style.left=(ox+oD)+'px'; requestAnimationFrame(loop); }
        upT(); loop();
    </script>
    """
    components.html(game_html, height=500)
    if st.button("⬅️ HUB"): st.session_state.pagina = 'hub'; st.rerun()

# --- RELATÓRIOS ---
elif st.session_state.pagina == 'rel_d':
    st.markdown(f"<div class='stats-box'><h2>TEMPO: {st.session_state.pts_d}s</h2><p>Federação Goat TV: Treino Concluído.</p></div>", unsafe_allow_html=True)
    if st.button("VOLTAR AO HUB"): st.query_params.clear(); st.session_state.pagina = 'hub'; st.rerun()

# FIM DO SISTEMA GOAT TV 2026
