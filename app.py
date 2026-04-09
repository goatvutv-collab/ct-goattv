import streamlit as st
import streamlit.components.v1 as components

# --- 1. ESTILO PREMIUM MOBILE ---
st.set_page_config(page_title="GOAT TV - CT OFICIAL", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0E0E2C; color: #FFFFFF; font-family: 'sans-serif'; }
    .ct-title { text-align: center; font-size: 26px; font-weight: 800; color: #FFD700; margin-bottom: 15px; }
    div.stButton > button {
        width: 100% !important; height: 50px !important; border-radius: 50px !important;
        border: none !important; color: white !important; font-weight: 700 !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4) !important; margin-bottom: 10px !important;
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
elif "pass_score" in params:
    st.session_state.pontos_passe = int(params["pass_score"])
    st.session_state.pagina = 'relatorio_passe'

# --- 3. TELAS ---

if st.session_state.pagina == 'login':
    st.markdown("<h1 class='ct-title'>🛡️ ACESSO CT GOAT TV</h1>", unsafe_allow_html=True)
    pin = st.text_input("PIN DO ATLETA:", type="password")
    if st.button("ENTRAR NO CT", use_container_width=True):
        if pin == "2026": st.session_state.pagina = 'hub'; st.rerun()

elif st.session_state.pagina == 'hub':
    st.markdown("<h1 class='ct-title'>CENTRO DE TREINAMENTO</h1>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⚽ DRIBLE", key="btn_d"): st.session_state.pagina = 'treino_drible'; st.rerun()
        if st.button("🎯 PASSE", key="btn_p"): st.session_state.pagina = 'treino_passe'; st.rerun()
    with c2:
        if st.button("⚡ VELOCIDADE", key="btn_v"): st.session_state.pagina = 'treino_velocidade'; st.rerun()

# --- SALA 3: PASSE (BARRA DE FORÇA + ADVERSÁRIOS) ---
elif st.session_state.pagina == 'treino_passe':
    st.markdown("<h2 style='text-align:center;'>🎯 PRECISÃO DE PASSE</h2>", unsafe_allow_html=True)
    game_html = """
    <div id="f" style="height:480px; width:100%; background-color:#1B5E20; border-radius:20px; position:relative; overflow:hidden; border:4px solid #08306B; touch-action:none;">
        <div id="p" style="width:26px; height:26px; background:white; border-radius:50%; position:absolute; left:46%; bottom:30px; z-index:30; border:2px solid #333;">⚽</div>
        <div id="target" style="width:32px; height:32px; background:rgba(255,215,0,0.6); border:2px dashed gold; border-radius:50%; position:absolute; left:20%; top:60px;"></div>
        <div id="ball" style="width:12px; height:12px; background:white; border-radius:50%; position:absolute; display:none; z-index:40;"></div>
        <div id="opp_cont"></div>

        <div style="position:absolute; bottom:100px; right:25px; width:15px; height:100px; background:#333; border:2px solid white; border-radius:5px; overflow:hidden;">
            <div id="p_bar" style="width:100%; height:0%; background:linear-gradient(to top, #4CAF50, #FFEB3B, #F44336); position:absolute; bottom:0;"></div>
        </div>

        <div id="jb" style="position:absolute; bottom:15px; left:15px; width:80px; height:80px; background:rgba(255,255,255,0.1); border-radius:50%; z-index:100; border:2px solid rgba(255,255,255,0.2);">
            <div id="js" style="position:absolute; top:20px; left:20px; width:40px; height:40px; background:rgba(255,255,255,0.4); border-radius:50%;"></div>
        </div>
        <button id="btn_a" style="position:absolute; bottom:20px; right:20px; width:65px; height:65px; background:#4A90E2; color:white; border-radius:50%; border:4px solid #2171C1; font-weight:bold; font-size:24px; z-index:100;">A</button>
        <div style="position:absolute; top:5px; width:100%; text-align:center; color:white; font-weight:bold; font-size:14px;">PASSE: <span id="h_ui">0</span> | <span id="m_ui">GAUNTLET</span></div>
    </div>
    <script>
        const p=document.getElementById('p'), f=document.getElementById('f'), target=document.getElementById('target'), ball=document.getElementById('ball'), btnA=document.getElementById('btn_a'), pBar=document.getElementById('p_bar'), jB=document.getElementById('jb'), jS=document.getElementById('js'), oCont=document.getElementById('opp_cont');
        let jX=0, jY=0, drag=false, hits=0, power=0, pActive=false, passing=false, opps=[];

        function spawnOpp() {
            let o = document.createElement('div');
            o.style.cssText = `width:40px; height:10px; background:#F44336; position:absolute; left:${Math.random()*60+20}%; top:${Math.random()*150+150}px; border-radius:5px; border:1px solid white;`;
            oCont.appendChild(o); opps.push(o);
        }

        jB.ontouchstart=(e)=>{drag=true; e.preventDefault();};
        window.ontouchmove=(e)=>{ if(!drag)return; let t=e.touches[0], r=jB.getBoundingClientRect(), dx=t.clientX-(r.left+40), dy=t.clientY-(r.top+40), d=Math.min(Math.sqrt(dx*dx+dy*dy), 40), a=Math.atan2(dy,dx); jX=Math.cos(a)*(d/40); jY=Math.sin(a)*(d/40); jS.style.transform=`translate(${jX*25}px, ${jY*25}px)`; };
        window.ontouchend=()=>{drag=false; jX=0; jY=0; jS.style.transform='translate(0,0)';};

        btnA.onpointerdown=()=>{ if(!passing){ pActive=true; power=0; } };
        window.onpointerup=()=>{ if(pActive){ pActive=false; shoot(); } };

        function shoot(){
            passing=true; ball.style.display='block';
            let bx=p.offsetLeft+8, by=p.offsetTop+8, curP=power;
            let vx=jX*(curP/5), vy=jY*(curP/5);
            let anim = setInterval(()=>{
                bx+=vx; by+=vy; ball.style.left=bx+'px'; ball.style.top=by+'px';
                let tr=target.getBoundingClientRect(), br=ball.getBoundingClientRect();
                if(!(br.right<tr.left || br.left>tr.right || br.bottom<tr.top || br.top>tr.bottom)){
                    hits++; clearInterval(anim); success();
                }
                for(let o of opps){
                    let or=o.getBoundingClientRect();
                    if(!(br.right<or.left || br.left>or.right || br.bottom<or.top || br.top>or.bottom)){ clearInterval(anim); gameOver(); }
                }
                if(bx<0 || bx>f.offsetWidth || by<0 || by>f.offsetHeight){ clearInterval(anim); gameOver(); }
            }, 20);
        }

        function success(){
            ball.style.display='none'; passing=false; power=0; pBar.style.height='0%';
            document.getElementById('h_ui').innerHTML=hits;
            target.style.left=(Math.random()*70+10)+'%'; target.style.top=(Math.random()*100+50)+'px';
            if(hits % 4 === 0) spawnOpp();
        }

        function gameOver(){ window.parent.location.href=window.parent.location.href.split('?')[0]+"?pass_score="+(hits*100); }

        setInterval(()=>{
            if(pActive && power<100){ power+=2; pBar.style.height=power+'%'; }
        }, 20);
    </script>
    """
    components.html(game_html, height=520)
    if st.button("⬅️ VOLTAR AO HUB"): st.session_state.pagina='hub'; st.rerun()

# --- RELATÓRIOS ---
elif st.session_state.pagina == 'relatorio_passe':
    pts = st.session_state.get('pontos_passe', 0)
    st.markdown(f"<div style='background: #1B5E20; padding: 25px; border-radius: 20px; text-align:center;'><h2>PONTUAÇÃO PASSE</h2><h1>{pts} PTS</h1></div>", unsafe_allow_html=True)
    if st.button("NOVO TREINO"): st.query_params.clear(); st.session_state.pagina='hub'; st.rerun()

# (Mantenha Drible e Velocidade conforme as versões anteriores integradas)
