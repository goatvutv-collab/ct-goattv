import streamlit as st
import streamlit.components.v1 as components

# --- 1. ESTILO GOAT TV ---
st.set_page_config(page_title="GOAT TV - CT TESTE", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #0E0E2C; color: #FFF; font-family: sans-serif; }
    .ct-title { text-align: center; font-size: 26px; font-weight: 800; color: #FFD700; margin-bottom: 10px; }
    div.stButton > button { width: 100%!important; height: 48px!important; border-radius: 50px!important; border: none!important; color: white!important; font-weight: 700!important; box-shadow: 0 4px 10px rgba(0,0,0,0.5)!important; }
    iframe { border-radius: 20px; border: 3px solid #1E3A8A; background: transparent; }
    .stats-box { background-color: #1B5E20; padding: 20px; border-radius: 20px; text-align: center; }
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

if st.session_state.pagina == 'hub':
    st.markdown("<h1 class='ct-title'>CENTRO DE TREINAMENTO</h1>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⚽ DRIBLE SLALOM"): st.session_state.pagina = 'drible'; st.rerun()
        if st.button("🎯 PASSE MAESTRO"): st.session_state.pagina = 'passe'; st.rerun()
    with c2:
        if st.button("⚡ VELOCIDADE FPS"): st.session_state.pagina = 'vel'; st.rerun()
        if st.button("🔄 RECARREGAR CT"): st.rerun()

# SALA 1: DRIBLE (RANDOM SLALOM + COLISÃO)
elif st.session_state.pagina == 'drible':
    st.markdown("<h2 style='text-align:center;'>⚽ SLALOM TESTE</h2>", unsafe_allow_html=True)
    game_html = """
    <div id="f" style="height:480px; width:100%; background:#0D47A1; position:relative; overflow:hidden; border:4px solid #08306B; touch-action:none; border-radius:20px;">
        <div id="p" style="width:24px; height:24px; background:white; border-radius:50%; position:absolute; left:45%; bottom:50px; border:2px solid #333; z-index:30;">⚽</div>
        <div id="goal" style="width:80px; height:10px; background:yellow; position:absolute; bottom:0; right:0;"></div>
        <div id="gC"></div>
        <svg id="ta" style="position:absolute; width:24px; height:24px; z-index:100; display:none;" viewBox="0 0 24 24"><path fill="#FFD700" d="M12 21l-12-18h24z"/></svg>
        <div id="jb" style="position:absolute; bottom:15px; left:15px; width:80px; height:80px; background:rgba(255,255,255,0.1); border-radius:50%; border:2px solid rgba(255,255,255,0.2); z-index:100;"><div id="js" style="position:absolute; top:20px; left:20px; width:40px; height:40px; background:rgba(255,255,255,0.3); border-radius:50%;"></div></div>
        <button id="go" style="position:absolute; bottom:25px; right:25px; padding:10px 20px; background:green; color:white; border-radius:10px; border:none; font-weight:bold; z-index:100;">GO!</button>
        <div style="position:absolute; top:5px; width:100%; text-align:center; color:white; font-weight:bold;">TEMPO: <span id="t_ui">15.0s</span></div>
    </div>
    <style>.c{width:16px;height:16px;background:orange;border-radius:50%;position:absolute;border:1px solid #CC5500;}.gt{position:absolute;border-left:2px dashed rgba(255,255,255,0.1);height:16px;}</style>
    <script>
        const p=document.getElementById('p'), f=document.getElementById('f'), go=document.getElementById('go'), jB=document.getElementById('jb'), jS=document.getElementById('js'), ta=document.getElementById('ta'), gC=document.getElementById('gC');
        let x=f.offsetWidth/2-12, y=380, time=15.0, run=false, gts=new Set(), jX=0, jY=0, drag=false, ck=[];
        function build(){
            gC.innerHTML=''; ck=[]; const rs=[340, 240, 140, 40, 140];
            for(let i=0; i<5; i++){
                let rx=15+Math.random()*60;
                gC.innerHTML+=`<div class="c" style="left:${rx}%; top:${rs[i]}px;"></div><div class="c" style="left:${rx+20}%; top:${rs[i]}px;"></div><div class="gt" id="g${i}" style="left:${rx+1}%; top:${rs[i]}px; width:18%"></div>`;
                ck.push({id:`g${i}`, x:(f.offsetWidth*(rx+10)/100), y:rs[i]});
            }
            ck.push({id:'goal', x:f.offsetWidth*0.8, y:460});
        }
        function upA(){ let t=ck[gts.size]; if(t){ ta.style.left=(t.x-12)+'px'; ta.style.top=(t.y-30)+'px'; } }
        jB.ontouchstart=(e)=>{drag=true; e.preventDefault();};
        window.ontouchmove=(e)=>{ if(!drag)return; let t=e.touches[0], r=jB.getBoundingClientRect(), dx=t.clientX-(r.left+40), dy=t.clientY-(r.top+40), d=Math.min(Math.sqrt(dx*dx+dy*dy),40), a=Math.atan2(dy,dx); jX=Math.cos(a); jY=Math.sin(a); jS.style.transform=`translate(${jX*(d/40)*25}px, ${jY*(d/40)*25}px)`; };
        window.ontouchend=()=>{drag=false; jX=0; jY=0; jS.style.transform='translate(0,0)';};
        go.onclick=()=>{ build(); run=true; go.style.display='none'; ta.style.display='block'; upA(); };
        function loopD(){
            if(run && time>0){
                time-=0.016; document.getElementById('t_ui').innerHTML=time.toFixed(1);
                x+=jX*4.5; y+=jY*4.5;
                x=Math.max(0,Math.min(x,f.offsetWidth-24)); y=Math.max(0,Math.min(y,f.offsetHeight-24));
                p.style.left=x+'px'; p.style.top=y+'px';
                const cones=document.querySelectorAll('.c');
                cones.forEach(c=>{ let cr=c.getBoundingClientRect(), pr=p.getBoundingClientRect(); if(!(pr.right<cr.left||pr.left>cr.right||pr.bottom<cr.top||pr.top>cr.bottom)){ x=f.offsetWidth/2-12; y=380; jX=0; jY=0; } });
                if(gts.size<5){
                    const n=document.getElementById(ck[gts.size].id); const gr=n.getBoundingClientRect(), pr=p.getBoundingClientRect();
                    if(!(pr.right<gr.left||pr.left>gr.right||pr.bottom<gr.top||pr.top>gr.bottom)){ gts.add(gts.size); upA(); }
                }
                if(y>440 && x>f.offsetWidth*0.6 && gts.size>=5){ window.parent.location.href=window.parent.location.href.split('?')[0]+"?score="+Math.round(time*100); run=false; }
            }
            requestAnimationFrame(loopD);
        }
        loopD();
    </script>
    """
    components.html(game_html, height=500)
    if st.button("⬅️ VOLTAR"): st.session_state.pagina = 'hub'; st.rerun()

# SALA 2: VELOCIDADE (SISTEMA FPS)
elif st.session_state.pagina == 'vel':
    st.markdown("<h2 style='text-align:center;'>⚡ BURST SPRINT FPS</h2>", unsafe_allow_html=True)
    game_html = """
    <div id="f" style="height:480px; width:100%; background:#0D47A1; position:relative; overflow:hidden; border:4px solid #08306B; border-radius:20px; touch-action:none;">
        <div id="p" style="width:24px; height:24px; background:white; border-radius:50%; position:absolute; left:45%; bottom:40px; border:2px solid #333; transition: box-shadow 0.1s;">⚽</div>
        <div style="width:100%; height:10px; background:yellow; position:absolute; top:0; left:0;"></div>
        <div id="tm" style="position:absolute; top:10px; right:10px; font-weight:bold; color:white;">0.00s</div>
        <div id="jb" style="position:absolute; bottom:15px; left:15px; width:80px; height:80px; background:rgba(255,255,255,0.1); border-radius:50%; border:2px solid rgba(255,255,255,0.2); z-index:100;"><div id="js" style="position:absolute; top:20px; left:20px; width:40px; height:40px; background:rgba(255,255,255,0.3); border-radius:50%;"></div></div>
    </div>
    <script>
        const p=document.getElementById('p'), f=document.getElementById('f'), jB=document.getElementById('jb'), jS=document.getElementById('js');
        let x=f.offsetWidth/2-12, y=410, t=0, run=false, jX=0, jY=0, drag=false, mult=2, start=0;
        jB.ontouchstart=(e)=>{drag=true; if(!run){run=true; start=Date.now();} e.preventDefault();};
        window.ontouchmove=(e)=>{
            if(!drag)return; let touch=e.touches[0], r=jB.getBoundingClientRect(), dx=touch.clientX-(r.left+40), dy=touch.clientY-(r.top+40);
            let d=Math.sqrt(dx*dx+dy*dy), a=Math.atan2(dy,dx), limD=Math.min(d, 40);
            jX=Math.cos(a)*(limD/40); jY=Math.sin(a)*(limD/40);
            jS.style.transform=`translate(${jX*25}px, ${jY*25}px)`;
            if(limD > 37) { p.style.background='gold'; p.style.boxShadow='0 0 15px gold'; mult=9; } else { p.style.background='white'; p.style.boxShadow='none'; mult=3; }
        };
        window.ontouchend=()=>{drag=false; jX=0; jY=0; jS.style.transform='translate(0,0)';};
        function loopV(){
            if(run){ t=(Date.now()-start)/1000; document.getElementById('tm').innerHTML=t.toFixed(2)+'s'; x+=jX*mult; y+=jY*mult; x=Math.max(0,Math.min(x,f.offsetWidth-24)); y=Math.max(0,Math.min(y,f.offsetHeight-24)); p.style.left=x+'px'; p.style.top=y+'px'; if(y<10) window.parent.location.href=window.parent.location.href.split('?')[0]+"?v_time="+t.toFixed(2); }
            requestAnimationFrame(loopV);
        }
        loopV();
    </script>
    """
    components.html(game_html, height=500)
    if st.button("⬅️ VOLTAR"): st.session_state.pagina = 'hub'; st.rerun()

# SALA 3: PASSE MAESTRO (1 MARCADOR MÓVEL + 10 TENTATIVAS)
elif st.session_state.pagina == 'passe':
    st.markdown("<h2 style='text-align:center;'>🎯 RODA DE PASSE PRO</h2>", unsafe_allow_html=True)
    game_html = """
    <div id="f" style="height:460px; width:100%; background:#1B5E20; position:relative; overflow:hidden; border:4px solid #08306B; touch-action:none; border-radius:20px;">
        <div id="ui" style="position:absolute; top:10px; width:100%; text-align:center; color:white; font-weight:bold; z-index:50; font-size:12px;">ACERTOS: <span id="h_ui">0</span>/10 | BOLAS: <span id="t_ui">10</span></div>
        <div id="p" style="width:26px; height:26px; background:white; border-radius:50%; position:absolute; left:46%; bottom:40px; border:2px solid #333; z-index:35;">⚽</div>
        <div id="t0" class="tgt" style="left:15%; top:60px;"></div><div id="t1" class="tgt" style="left:46%; top:40px;"></div><div id="t2" class="tgt" style="left:75%; top:60px;"></div>
        <div id="ball" style="width:12px; height:12px; background:white; border-radius:50%; position:absolute; display:none; z-index:40;"></div>
        <div id="aim" style="width:2px; height:80px; background:rgba(255,255,255,0.3); position:absolute; left:50%; bottom:50px; transform-origin: bottom center; display:none; z-index:30;"></div>
        <div id="opp" style="width:60px; height:15px; background:#F44; position:absolute; left:10%; top:150px; border-radius:4px; border:1px solid white; z-index:32;"></div>
        <div id="jb" style="position:absolute; bottom:15px; left:15px; width:80px; height:80px; background:rgba(255,255,255,0.1); border-radius:50%; border:2px solid rgba(255,255,255,0.2); z-index:100;"><div id="js" style="position:absolute; top:20px; left:20px; width:40px; height:40px; background:rgba(255,255,255,0.3); border-radius:50%;"></div></div>
        <button id="btnA" style="position:absolute; bottom:15px; right:15px; width:65px; height:65px; background:#4A90E2; color:white; border-radius:50%; font-weight:bold; font-size:24px; border:none; z-index:100;">A</button>
    </div>
    <style>.tgt{width:32px;height:32px;background:rgba(255,215,0,0.2);border:2px dashed gold;border-radius:50%;position:absolute;}.act{background:rgba(255,215,0,0.7);opacity:1;}</style>
    <script>
        const p=document.getElementById('p'), f=document.getElementById('f'), ball=document.getElementById('ball'), btnA=document.getElementById('btnA'), jB=document.getElementById('jb'), jS=document.getElementById('js'), aim=document.getElementById('aim'), opp=document.getElementById('opp'), tgts=document.querySelectorAll('.tgt');
        let jX=0, jY=0, hits=0, tries=10, pass=false, oD=1, curT=0, start=0, sttd=false;
        function upT(){ tgts.forEach((t,i)=>{t.className=i===curT?'tgt act':'tgt';}); }
        jB.ontouchstart=(e)=>{this.dr=true; e.preventDefault(); if(!sttd){sttd=true; start=Date.now();}};
        window.ontouchmove=(e)=>{ if(!this.dr)return; let t=e.touches[0], r=jB.getBoundingClientRect(), dx=t.clientX-(r.left+40), dy=t.clientY-(r.top+40), d=Math.min(Math.sqrt(dx*dx+dy*dy),40), a=Math.atan2(dy,dx); jX=Math.cos(a); jY=Math.sin(a); jS.style.transform=`translate(${jX*(d/40)*25}px, ${jY*(d/40)*25}px)`; aim.style.display='block'; aim.style.transform=`rotate(${(a*180/Math.PI)+90}deg)`; };
        window.ontouchend=()=>{this.dr=false; aim.style.display='none';};
        btnA.onclick=()=>{ if(!pass && tries>0){ if(!sttd){sttd=true; start=Date.now();} shoot(); } };
        function shoot(){
            pass=true; tries--; ball.style.display='block'; let bx=p.offsetLeft+8, by=p.offsetTop+8, vx=jX*12, vy=jY*12;
            let anim=setInterval(()=>{
                bx+=vx; by+=vy; ball.style.left=bx+'px'; ball.style.top=by+'px';
                let tr=tgts[curT].getBoundingClientRect(), br=ball.getBoundingClientRect(), or=opp.getBoundingClientRect();
                if(!(br.right<tr.left||br.left>tr.right||br.bottom<tr.top||br.top>tr.bottom)){ hits++; curT=(curT+1)%3; upT(); endB(anim); }
                else if(!(br.right<or.left||br.left>or.right||br.bottom<or.top||br.top>or.bottom)||bx<0||bx>f.offsetWidth||by<0||by>f.offsetHeight){ endB(anim); }
            }, 20);
        }
        function endB(a){ clearInterval(a); ball.style.display='none'; pass=false; document.getElementById('h_ui').innerHTML=hits; document.getElementById('t_ui').innerHTML=tries; if(tries<=0||hits>=10) endG(); }
        function endG(){ let ft=(Date.now()-start)/1000; let bn=ft<12?Math.round((12-ft)*400):0; window.parent.location.href=window.parent.location.href.split('?')[0]+"?p_score="+((hits*200)+bn)+"&hits="+hits; }
        function loopP(){
            let ox=opp.offsetLeft; if(ox>f.offsetWidth-65||ox<10) oD*=-1; opp.style.left=(ox+oD*3.5)+'px';
            requestAnimationFrame(loopP);
        }
        upT(); loopP();
    </script>
    """
    components.html(game_html, height=500)
    if st.button("⬅️ VOLTAR AO HUB"): st.session_state.pagina = 'hub'; st.rerun()

# RELATÓRIOS
elif st.session_state.pagina == 'rel_d':
    st.markdown(f"<div class='stats-box'><h2>DRIBLE: {st.session_state.pts_d} PTS</h2></div>", unsafe_allow_html=True)
    if st.button("VOLTAR AO HUB"): st.query_params.clear(); st.session_state.pagina = 'hub'; st.rerun()
elif st.session_state.pagina == 'rel_v':
    st.markdown(f"<div class='stats-box'><h2>VELOCIDADE: {st.session_state.tm_v}s</h2></div>", unsafe_allow_html=True)
    if st.button("VOLTAR AO HUB"): st.query_params.clear(); st.session_state.pagina = 'hub'; st.rerun()
elif st.session_state.pagina == 'rel_p':
    hits = st.session_state.get('hits_p', 0); st.markdown(f"<div class='stats-box'><h2>PASSE: {st.session_state.pts_p} PTS</h2><p>Acertos: {hits}/10</p></div>", unsafe_allow_html=True)
    if st.button("VOLTAR AO HUB"): st.query_params.clear(); st.session_state.pagina = 'hub'; st.rerun()
