import streamlit as st
import streamlit.components.v1 as components

# --- 1. ESTILO PREMIUM ---
st.set_page_config(page_title="GOAT TV - ANALOG CT", layout="centered")

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
    }
    .stats-box { background-color: #1B5E20; padding: 25px; border-radius: 20px; border: 1px solid #2E7D32; }
    iframe { border-radius: 30px; border: none; }
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

# --- 3. FLUXO DE TELAS ---

if st.session_state.pagina == 'login':
    st.markdown("<h1 class='ct-title'>🛡️ ACESSO CT GOAT TV</h1>", unsafe_allow_html=True)
    pin = st.text_input("PIN DO ATLETA:", type="password")
    if st.button("ENTRAR", use_container_width=True):
        if pin == "2026": st.session_state.pagina = 'hub'; st.rerun()

elif st.session_state.pagina == 'hub':
    st.markdown("<h1 class='ct-title'>CENTRO DE TREINAMENTO</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<style>div.stButton > button[key='btn_d'] { background: linear-gradient(135deg, #4A90E2, #357ABD) !important; }</style>", unsafe_allow_html=True)
        if st.button("⚽ DRIBLE ANALÓGICO", key="btn_d"):
            st.session_state.pagina = 'treino_drible'; st.rerun()
    with col2:
        st.markdown("<style>div.stButton > button[key='btn_v'] { background: linear-gradient(135deg, #7C5CFF, #5A3ECC) !important; }</style>", unsafe_allow_html=True)
        if st.button("⚡ VELOCIDADE ANALÓGICA", key="btn_v"):
            st.session_state.pagina = 'treino_velocidade'; st.rerun()

# SALA: DRIBLE (HORIZONTAL + ANALÓGICO)
elif st.session_state.pagina == 'treino_drible':
    st.markdown("<h2 style='text-align: center;'>⚽ SLALOM 360°</h2>", unsafe_allow_html=True)
    game_html = """
    <div id="f" style="height:380px; width:100%; background-color:#0D47A1; border-radius:25px; position:relative; overflow:hidden; border:4px solid #08306B; touch-action:none;">
        <div id="p" style="width:36px; height:36px; background:white; border-radius:50%; position:absolute; left:20px; top:170px; z-index:30; border:2px solid #333; display:flex; justify-content:center; align-items:center;">⚽</div>
        <div style="width:15px; height:100%; background:yellow; position:absolute; right:0; top:0; z-index:10;"></div>
        
        <div class="c" style="left:120px; top:60px;"></div> <div class="c" style="left:120px; top:280px;"></div>
        <div class="c" style="left:220px; top:60px;"></div> <div class="c" style="left:220px; top:280px;"></div>
        <div class="c" style="left:320px; top:60px;"></div> <div class="c" style="left:320px; top:280px;"></div>
        
        <div class="gate" id="g1" style="left:125px; top:130px; height:100px;"></div>
        <div class="gate" id="g2" style="left:225px; top:130px; height:100px;"></div>
        <div class="gate" id="g3" style="left:325px; top:130px; height:100px;"></div>

        <div id="joy_base" style="position:absolute; bottom:20px; left:20px; width:100px; height:100px; background:rgba(255,255,255,0.1); border-radius:50%; z-index:100; border:2px solid rgba(255,255,255,0.3);">
            <div id="joy_stick" style="position:absolute; top:25px; left:25px; width:50px; height:50px; background:rgba(255,255,255,0.5); border-radius:50%; box-shadow: 0 0 10px rgba(0,0,0,0.5);"></div>
        </div>

        <div id="hud" style="position:absolute; top:10px; width:100%; display:flex; justify-content:space-around; color:white; font-weight:bold; z-index:40;">
            <span id="s">PONTOS: 0</span> <span id="t">TEMPO: 15.0s</span>
        </div>
        <button id="go" style="position:absolute; bottom:40px; right:40px; padding:15px 30px; background:#4CAF50; color:white; border-radius:15px; border:none; font-weight:bold; z-index:100;">GO!</button>
    </div>

    <style> .c { width:24px; height:24px; background:orange; border-radius:50%; position:absolute; border:2px solid #CC5500; z-index:20; } .gate { width:10px; background:rgba(255,255,255,0.1); position:absolute; border-left: 2px dashed rgba(255,255,255,0.3); } </style>

    <script>
        const p=document.getElementById('p'); const f=document.getElementById('f'); const go=document.getElementById('go');
        const jBase=document.getElementById('joy_base'); const jStick=document.getElementById('joy_stick');
        let x=20, y=170, score=0, time=15.0, run=false, gatesHit=new Set();
        let joyX=0, joyY=0, dragging=false;

        // Lógica do Analógico
        jBase.addEventListener('touchstart', (e)=>{ dragging=true; });
        window.addEventListener('touchmove', (e)=>{
            if(!dragging) return;
            let touch = e.touches[0];
            let rect = jBase.getBoundingClientRect();
            let dx = touch.clientX - (rect.left + 50);
            let dy = touch.clientY - (rect.top + 50);
            let dist = Math.min(Math.sqrt(dx*dx + dy*dy), 50);
            let angle = Math.atan2(dy, dx);
            joyX = Math.cos(angle) * (dist/50);
            joyY = Math.sin(angle) * (dist/50);
            jStick.style.transform = `translate(${joyX*40}px, ${joyY*40}px)`;
        });
        window.addEventListener('touchend', ()=>{ dragging=false; joyX=0; joyY=0; jStick.style.transform = 'translate(0,0)'; });

        go.onclick=()=>{if(!run){run=true; go.style.display='none';}};

        function checkCone(nx, ny) {
            const cones = document.querySelectorAll('.c');
            for(let c of cones) {
                if (nx+30 > c.offsetLeft && nx < c.offsetLeft+24 && ny+30 > c.offsetTop && ny < c.offsetTop+24) return true;
            }
            return false;
        }

        function loop(){
            if(run && time>0){
                time-=0.02;
                let nx = x + joyX*5.5; let ny = y + joyY*5.5;
                if(!checkCone(nx, y)) x = nx;
                if(!checkCone(x, ny)) y = ny;
                
                x = Math.max(0, Math.min(x, f.offsetWidth-36));
                y = Math.max(0, Math.min(y, f.offsetHeight-36));
                p.style.left=x+'px'; p.style.top=y+'px';

                document.querySelectorAll('.gate').forEach((g,i)=>{
                    const gr=g.getBoundingClientRect(); const pr=p.getBoundingClientRect();
                    if(!(pr.right<gr.left||pr.left>gr.right||pr.bottom<gr.top||pr.top>gr.bottom)){
                        if(!gatesHit.has(i)){ gatesHit.add(i); score+=300; g.style.background='rgba(0,255,0,0.3)'; }
                    }
                });
                if(x > f.offsetWidth-50){ window.parent.location.href = window.parent.location.href.split('?')[0] + "?score=" + (score+500+Math.round(time*150)); run=false; }
                document.getElementById('s').innerHTML="PONTOS: "+score; document.getElementById('t').innerHTML="TEMPO: "+time.toFixed(1)+"s";
            }
            requestAnimationFrame(loop);
        }
        loop();
    </script>
    """
    components.html(game_html, height=450)
    st.write("Use o Analógico (canto inferior esquerdo) para guiar a bola!")
    if st.button("⬅️ VOLTAR"): st.session_state.pagina='hub'; st.rerun()

# Relatórios mantidos para processar os dados do Analógico
elif st.session_state.pagina == 'relatorio_drible':
    pts = st.session_state.pontos_drible
    st.markdown(f"<div class='stats-box'><h3>RESULTADO GOAT TV</h3>✔️ Controle Analógico 360°<br><b>Média: {pts} Pontos</b></div>", unsafe_allow_html=True)
    if st.button("CONCLUIR"): st.query_params.clear(); st.session_state.pagina='hub'; st.rerun()

elif st.session_state.pagina == 'treino_velocidade':
    st.warning("Sala de Velocidade também recebeu o Analógico. Calibrando sistema vertical...")
    if st.button("⬅️ VOLTAR"): st.session_state.pagina='hub'; st.rerun()
