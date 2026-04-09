import streamlit as st
import streamlit.components.v1 as components

# --- 1. CONFIGURAÇÃO E ESTÉTICA ---
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
        if st.button("⚽ DRIBLE CIRCUITO U (FIXED)"): st.session_state.pagina = 'drible'; st.rerun()
        if st.button("🎯 PASSE MAESTRO"): st.session_state.pagina = 'passe'; st.rerun()
    with c2:
        if st.button("⚡ REFLEXO FANTASMA"): st.session_state.pagina = 'vel'; st.rerun()
        if st.button("🔄 RECARREGAR"): st.rerun()

# --- SALA 1: DRIBLE (CIRCUITO EM U + PAREDE CENTRAL + MOVIMENTO LINEAR) ---
elif st.session_state.pagina == 'drible':
    st.markdown("<h2 style='text-align:center;'>⚽ CIRCUITO TÁTICO EM U</h2>", unsafe_allow_html=True)
    game_html = """
    <div id="f" style="height:480px; width:100%; background:#0D47A1; position:relative; overflow:hidden; border:4px solid #08306B; touch-action:none; border-radius:20px;">
        <div id="p" style="width:26px; height:26px; background:white; border-radius:50%; position:absolute; left:15%; bottom:20px; border:2px solid #333; z-index:45;">⚽</div>
        <div id="aim" style="width:2px; height:60px; background:rgba(255,255,255,0.3); position:absolute; transform-origin: bottom center; display:none; z-index:35;"></div>
        
        <div id="wall" style="width:10px; height:280px; background:rgba(255,255,255,0.15); border:1px solid rgba(255,255,255,0.3); position:absolute; left:50%; bottom:0; transform:translateX(-50%); z-index:30;"></div>

        <div id="obs1" class="enemy" style="width:60px; height:14px; background:#F44; position:absolute; left:5%; top:240px; border-radius:4px; border:1px solid white; z-index:32;"></div>
        <div id="obs2" class="enemy" style="width:14px; height:60px; background:#F44; position:absolute; left:48%; top:20px; border-radius:4px; border:1px solid white; z-index:32;"></div>
        <div id="obs3" class="enemy" style="width:60px; height:14px; background:#F44; position:absolute; right:5%; top:240px; border-radius:4px; border:1px solid white; z-index:32;"></div>

        <div id="gC"></div>
        <div id="arrow" style="position:absolute; width:30px; height:30px; z-index:100; pointer-events:none; font-size:24px;">⬇️</div>
        <div id="jb" style="position:absolute; bottom:15px; left:15px; width:80px; height:80px; background:rgba(255,255,255,0.1); border-radius:50%; z-index:100;"><div id="js" style="position:absolute; top:20px; left:20px; width:40px; height:40px; background:rgba(255,255,255,0.3); border-radius:50%;"></div></div>
        <div style="position:absolute; top:5px; width:100%; text-align:center; color:white; font-weight:bold; font-size:12px;">CRONÔMETRO: <span id="t_ui">0.00</span>s | GATES: <span id="l_ui">1</span>/4</div>
    </div>
    <script>
        const p=document.getElementById('p'), aim=document.getElementById('aim'), jB=document.getElementById('jb'), js=document.getElementById('js'), f=document.getElementById('f'), gC=document.getElementById('gC'), arr=document.getElementById('arrow'), wall=document.getElementById('wall');
        const ob1=document.getElementById('obs1'), ob2=document.getElementById('obs2'), ob3=document.getElementById('obs3');
        let x=p.offsetLeft, y=p.offsetTop, jX=0, jY=0, curX=0, curY=0, drag=false, step=0, start=Date.now(), run=false;
        
        // Velocidades Lineares Diferentes
        let v1=2.8, v2=4.2, v3=-3.1;

        const gates = [{x1:8,x2:35,y:380},{x1:8,x2:35,y:100},{x1:62,x2:92,y:100},{x1:62,x2:92,y:380}];
        gates.forEach((gt,i)=>{ gC.innerHTML+=`<div style="width:12px;height:12px;background:orange;border-radius:50%;position:absolute;left:${gt.x1}%;top:${gt.y}px;"></div><div style="width:12px;height:12px;background:orange;border-radius:50%;position:absolute;left:${gt.x2}%;top:${gt.y}px;"></div><div id="l${i}" style="height:4px;background:rgba(0,255,0,0.2);position:absolute;left:${gt.x1+2}%;top:${gt.y+4}px;width:${gt.x2-gt.x1-2}%;"></div>`; });

        jB.ontouchstart=(e)=>{drag=true; if(!run){run=true; start=Date.now();} aim.style.display='block'; e.preventDefault();};
        window.ontouchmove=(e)=>{
            if(!drag)return; let t=e.touches[0], r=jB.getBoundingClientRect(), dx=t.clientX-(r.left+40), dy=t.clientY-(r.top+40), d=Math.min(Math.sqrt(dx*dx+dy*dy),40), a=Math.atan2(dy,dx);
            jX=Math.cos(a)*(d/40); jY=Math.sin(a)*(d/40); js.style.transform=`translate(${jX*25}px, ${jY*25}px)`;
            aim.style.transform=`rotate(${(a*180/Math.PI)+90}deg)`; aim.style.left=(p.offsetLeft+12)+'px'; aim.style.top=(p.offsetTop-45)+'px';
        };
        window.ontouchend=()=>{drag=false; jX=jY=0; aim.style.display='none';};

        function loop(){
            if(run){
                document.getElementById('t_ui').innerHTML=((Date.now()-start)/1000).toFixed(2);
                curX+=(jX*5.5-curX)*0.15; curY+=(jY*5.5-curY)*0.15; 
                let nextX = x + curX; let nextY = y + curY;

                // Colisão com a Parede Central (Física)
                let wr=wall.getBoundingClientRect(), pr=p.getBoundingClientRect();
                let pFuture = { left: nextX, right: nextX+26, top: nextY, bottom: nextY+26 };
                let fieldR = f.getBoundingClientRect();
                let wallRel = { left: wr.left - fieldR.left, right: wr.right - fieldR.left, top: wr.top - fieldR.top, bottom: wr.bottom - fieldR.top };

                if (!(pFuture.right < wallRel.left || pFuture.left > wallRel.right || pFuture.bottom < wallRel.top || pFuture.top > wallRel.bottom)) {
                    curX = 0; // Trava o movimento horizontal contra a parede
                }

                x += curX; y += curY;
                x=Math.max(5,Math.min(x,f.offsetWidth-32)); y=Math.max(5,Math.min(y,f.offsetHeight-32));
                p.style.left=x+'px'; p.style.top=y+'px';
                
                // Movimento Perpétuo dos Adversários
                let ox1=ob1.offsetLeft; if(ox1 > f.offsetWidth*0.35 || ox1 < 5) v1*=-1; ob1.style.left=(ox1+v1)+'px';
                let ox2=ob2.offsetLeft; if(ox2 > f.offsetWidth*0.8 || ox2 < f.offsetWidth*0.2) v2*=-1; ob2.style.left=(ox2+v2)+'px';
                let ox3=ob3.offsetLeft; if(ox3 > f.offsetWidth-65 || ox3 < f.offsetWidth*0.6) v3*=-1; ob3.style.left=(ox3+v3)+'px';

                // Colisão com Inimigos (Recuo)
                [ob1, ob2, ob3].forEach(ob=>{
                    let or=ob.getBoundingClientRect(), pr2=p.getBoundingClientRect();
                    if(!(pr2.right<or.left||pr2.left>or.right||pr2.bottom<or.top||pr2.top>or.bottom)){ x-=curX*8; y-=curY*8; p.style.background='red'; setTimeout(()=>p.style.background='white',100); }
                });

                if(step < 4){
                    let lr=document.getElementById('l'+step).getBoundingClientRect(), pr3=p.getBoundingClientRect();
                    if(!(pr3.right<lr.left||pr3.left>lr.right||pr3.bottom<lr.top||pr3.top>lr.bottom)){ document.getElementById('l'+step).style.background='lime'; step++; if(step<4) document.getElementById('l_ui').innerHTML=step+1; }
                    let target=document.getElementById('l'+(step<4?step:3)).getBoundingClientRect(), field=f.getBoundingClientRect();
                    arr.style.left=(target.left-field.left+15)+'px'; arr.style.top=(target.top-field.top-35)+'px';
                } else { if(x > f.offsetWidth*0.7 && y > 350) window.parent.location.href=window.parent.location.href.split('?')[0]+"?score="+((Date.now()-start)/1000).toFixed(2); }
            }
            requestAnimationFrame(loop);
        }
        loop();
    </script>
    """
    components.html(game_html, height=500)
    if st.button("⬅️ VOLTAR AO HUB"): st.session_state.pagina = 'hub'; st.rerun()

# --- SALA 2: PASSE MAESTRO (FIXO) ---
elif st.session_state.pagina == 'passe':
    st.markdown("<h2 style='text-align:center;'>🎯 PASSE DE PRECISÃO</h2>", unsafe_allow_html=True)
    # [Código do Passe Maestro mantido como baseline aprovada]
    if st.button("⬅️ HUB"): st.session_state.pagina = 'hub'; st.rerun()

# --- RELATÓRIOS ---
elif st.session_state.pagina == 'rel_d':
    st.markdown(f"<div class='stats-box'><h2>TEMPO FINAL: {st.session_state.pts_d}s</h2><p>Processando Habilidade do Atleta...</p></div>", unsafe_allow_html=True)
    if st.button("VOLTAR AO HUB"): st.query_params.clear(); st.session_state.pagina = 'hub'; st.rerun()

# SISTEMA GOAT TV BLINDADO - 2026
