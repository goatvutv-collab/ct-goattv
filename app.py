import streamlit as st
import streamlit.components.v1 as components

# --- 1. ESTILO PREMIUM (CANVA + SIMETRIA) ---
st.set_page_config(page_title="GOAT TV - ANALOG CT", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0E0E2C; color: #FFFFFF; font-family: 'sans-serif'; }
    .ct-title { text-align: center; font-size: 32px; font-weight: 800; color: #FFD700; margin-bottom: 20px; }
    
    div.stButton > button {
        width: 100% !important; height: 65px !important;
        border-radius: 50px !important; border: none !important;
        color: white !important; font-weight: 700 !important; font-size: 18px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4) !important;
        margin-bottom: 10px !important;
        display: flex !important; align-items: center !important; justify-content: center !important;
    }
    .stats-box { background-color: #1B5E20; padding: 25px; border-radius: 20px; border: 1px solid #2E7D32; }
    iframe { border-radius: 30px; border: none; background: transparent; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 2. MOTOR DE ESTADOS ---
if 'pagina' not in st.session_state: st.session_state.pagina = 'login'

params = st.query_params
if "score" in params:
    st.session_state.pontos_drible = int(params["score"])
    st.session_state.pagina = 'relatorio_drible'

# --- 3. LÓGICAS DE PONTUAÇÃO ---
def calc_drible(pts):
    if pts >= 3500: return "🏆 LENDA (ELITE)", 3
    elif pts >= 2200: return "✅ PRO (PROFISS.)", 1
    return "❌ BASE (BRONZE)", 0

# --- 4. FLUXO DE TELAS ---

if st.session_state.pagina == 'login':
    st.markdown("<h1 class='ct-title'>🛡️ ACESSO CT GOAT TV</h1>", unsafe_allow_html=True)
    pin = st.text_input("PIN DO ATLETA:", type="password")
    if st.button("ENTRAR", use_container_width=True):
        if pin == "2026": st.session_state.pagina = 'hub'; st.rerun()

elif st.session_state.pagina == 'hub':
    st.markdown("<h1 class='ct-title'>CENTRO DE TREINAMENTO</h1>", unsafe_allow_html=True)
    st.markdown("<style>div.stButton > button[key='btn_d'] { background: linear-gradient(135deg, #4A90E2, #357ABD) !important; }</style>", unsafe_allow_html=True)
    if st.button("⚽ DRIBLE: BRASILEIRO GAUNTLET", key="btn_d"):
        st.session_state.pagina = 'treino_drible'; st.rerun()

# SALA: DRIBLE (VERTICAL EXPANDIDO + ANALÓGICO + CIRCUITO COMPLEXO BRASILEIRO)
elif st.session_state.pagina == 'treino_drible':
    st.markdown("<h2 style='text-align:center;'>⚽ BRASILEIRO GAUNTLET</h2>", unsafe_allow_html=True)
    
    # Campo vertical com 800px para caber todo o circuito
    game_html = """
    <div id="f" style="height:800px; width:100%; background-color:#0D47A1; border-radius:30px; position:relative; overflow:hidden; border:4px solid #08306B; touch-action:none;">
        <div id="p" style="width:34px; height:34px; background:white; border-radius:50%; position:absolute; left:45%; bottom:60px; z-index:30; border:2px solid #333; display:flex; justify-content:center; align-items:center;">⚽</div>
        
        <div id="goal_line" style="width:120px; height:15px; background:yellow; position:absolute; bottom:0; right:0; z-index:10; box-shadow: 0 -5px 15px yellow;"></div>
        
        <div class="cone pivot" style="left: 47%; top: 400px; width: 30px; height: 30px;"></div>

        <div class="c" style="left: 10%; top: 650px;"></div> <div class="c" style="left: 30%; top: 650px;"></div> <div class="gate" id="gA" style="left: 11%; top: 650px; width:19%"></div>
        
        <div class="c" style="left: 70%; top: 100px;"></div> <div class="c" style="left: 90%; top: 100px;"></div> <div class="gate" id="gB" style="left: 71%; top: 100px; width:19%"></div>
        
        <div class="c" style="left: 10%; top: 100px;"></div> <div class="c" style="left: 30%; top: 100px;"></div> <div class="gate" id="gC" style="left: 11%; top: 100px; width:19%"></div>
        
        <div class="c" style="left: 70%; top: 250px;"></div> <div class="c" style="left: 90%; top: 250px;"></div> <div class="gate" id="gE" style="left: 71%; top: 250px; width:19%"></div>
        
        <div class="c" style="left: 70%; top: 650px;"></div> <div class="c" style="left: 90%; top: 650px;"></div> <div class="gate" id="gF" style="left: 71%; top: 650px; width:19%"></div>

        <svg id="arrow" style="position:absolute; width:45px; height:45px; left:46%; top:500px; z-index:5; opacity:0.8; transform:rotate(-90deg); transition:transform 0.1s;" viewBox="0 0 24 24">
            <path fill="#FFD700" d="M12 2L4.5 10H8v12h8V10h3.5L12 2z"/>
        </svg>

        <div id="joy_base" style="position:absolute; bottom:20px; left:20px; width:100px; height:100px; background:rgba(255,255,255,0.1); border-radius:50%; z-index:100; border:2px solid rgba(255,255,255,0.2);">
            <div id="joy_stick" style="position:absolute; top:25px; left:25px; width:50px; height:50px; background:rgba(255,255,255,0.4); border-radius:50%;"></div>
        </div>
        
        <button id="go" style="position:absolute; bottom:40px; right:40px; padding:15px 30px; background:#4CAF50; color:white; border-radius:15px; border:none; font-weight:bold; z-index:100;">GO!</button>
        <div style="position:absolute; top:10px; width:100%; display:flex; justify-content:space-around; color:white; font-weight:bold; z-index:40;">
            <span id="s_ui">PONTOS: 0</span> <span id="t_ui">15.0s</span>
        </div>
    </div>
    
    <style>
        .c {width:24px;height:24px;background:orange;border-radius:50%;position:absolute;border:2px solid #CC5500; z-index:20;}
        .pivot {background:red; border:3px solid white;}
        .gate{width:10px;background:rgba(255,255,255,0.03);position:absolute;border-left:2px dashed rgba(255,255,255,0.1); height:24px; z-index:15;}
    </style>
    
    <script>
        const p=document.getElementById('p'), f=document.getElementById('f'), go=document.getElementById('go'), jB=document.getElementById('joy_base'), jS=document.getElementById('joy_stick'), arrow=document.getElementById('arrow');
        let x=f.offsetWidth/2-17, y=700, score=0, time=15.0, run=false, gates=new Set(), jX=0, jY=0, drag=false;
        
        // Coordenadas táticas dos portões (x, y centro de cada portão p/ Seta Dinâmica)
        const checkpoints = [
            {id: 'gA', x: f.offsetWidth*0.2, y: 650}, // A: Inferior Esq
            {id: 'gB', x: f.offsetWidth*0.8, y: 100}, // B: Superior Dir
            {id: 'gC', x: f.offsetWidth*0.2, y: 100}, // C: Superior Esq
            {id: 'pivot', x: f.offsetWidth/2, y: 400}, // D: Pivô Central
            {id: 'gE', x: f.offsetWidth*0.8, y: 250}, // E: Sup Dir Baixo
            {id: 'gF', x: f.offsetWidth*0.8, y: 650}, // F: Inferior Dir
            {id: 'goal', x: f.offsetWidth*0.8, y: 790} // G: Linha de Chegada
        ];

        jB.ontouchstart=(e)=>{drag=true; e.preventDefault();};
        window.ontouchmove=(e)=>{ 
            if(!drag)return; 
            let t=e.touches[0], r=jB.getBoundingClientRect(), dx=t.clientX-(r.left+50), dy=t.clientY-(r.top+50), d=Math.min(Math.sqrt(dx*dx+dy*dy), 50), a=Math.atan2(dy,dx); 
            jX=Math.cos(a)*(d/50); jY=Math.sin(a)*(d/50); jS.style.transform=`translate(${jX*40}px, ${jY*40}px)`; 
        };
        window.ontouchend=()=>{drag=false; jX=0; jY=0; jS.style.transform='translate(0,0)';};
        go.onclick=()=>{if(!run){run=true; go.style.display='none';}};

        function checkConeCollision(nx, ny) {
            const cones = document.querySelectorAll('.c, .pivot');
            for(let c of cones) {
                const cx=c.offsetLeft+c.offsetWidth/2, cy=c.offsetTop+c.offsetHeight/2, cr=c.offsetWidth/2;
                const dist = Math.sqrt(Math.pow(nx+17-cx,2) + Math.pow(ny+17-cy,2));
                if(dist < 17+cr) return true;
            }
            return false;
        }

        function rotateArrow() {
            let target = checkpoints[gates.size];
            if(!target) target = checkpoints[6]; // Linha de Chegada
            let dx = target.x - (x+17);
            let dy = target.y - (y+17);
            let angle = Math.atan2(dy, dx);
            arrow.style.transform = `rotate(${angle}rad)`;
            arrow.style.left = (x+17-22.5) + 'px'; // Move a seta junto com a bola
            arrow.style.top = (y-50) + 'px';
        }

        function loop(){
            if(run && time>0){
                time-=0.016; 
                let nx=x+jX*5.5, ny=y+jY*5.5; // Velocidade tática PES Mobile
                
                if(!checkConeCollision(nx, y)) x=nx;
                if(!checkConeCollision(x, ny)) y=ny;
                
                x=Math.max(0,Math.min(x,f.offsetWidth-34)); y=Math.max(0,Math.min(y,f.offsetHeight-34));
                p.style.left=x+'px'; p.style.top=y+'px';
                
                rotateArrow(); // Seta dinâmica 360° guiando o percurso

                // Check Gates (Somente se passar pelo portão correto na ordem)
                if(gates.size < checkpoints.length - 1) {
                   const nextGate = document.getElementById(checkpoints[gates.size].id);
                   if(nextGate && gates.size !== 3) { // Pula o Pivô na detecção de portão
                       const gr=nextGate.getBoundingClientRect(), pr=p.getBoundingClientRect();
                       if(!(pr.right<gr.left||pr.left>gr.right||pr.bottom<gr.top||pr.top>gr.bottom)){
                           gates.add(gates.size); score+=500; nextGate.style.background='rgba(0,255,0,0.2)'; nextGate.style.border='none';
                       }
                   } else if (gates.size === 3) { // Lógica especial p/ o Pivô Central (volta 360°)
                       const pivot = document.querySelector('.pivot');
                       const cx=pivot.offsetLeft+15, cy=pivot.offsetTop+15;
                       const dist = Math.sqrt(Math.pow(x+17-cx,2) + Math.pow(y+17-cy,2));
                       if(dist < 50 && dist > 32) { // Está contornando o cone
                           gates.add(gates.size); score+=500;
                       }
                   }
                }

                // Linha de Chegada (Base Direita)
                const goal=document.getElementById('goal_line');
                const glr=goal.getBoundingClientRect(), pr=p.getBoundingClientRect();
                if(!(pr.right<glr.left||pr.left>glr.right||pr.bottom<glr.top||pr.top>glr.bottom)){
                    if(gates.size >= 6) { // Passou por todo o percurso
                        window.parent.location.href=window.parent.location.href.split('?')[0]+"?score="+(score+1000+Math.round(time*150)); run=false;
                    }
                }
                document.getElementById('s_ui').innerHTML="PONTOS: "+score; document.getElementById('t_ui').innerHTML=time.toFixed(1)+"s";
            }
            requestAnimationFrame(loop);
        }
        loop();
    </script>
    """
    components.html(game_html, height=850)
    st.write("Siga a Seta Dinâmica! O percurso começa na base esquerda e termina na base direita.")
    if st.button("⬅️ VOLTAR AO HUB"): st.session_state.pagina='hub'; st.rerun()

# Relatórios mantidos para processar os dados do Analógico
elif st.session_state.pagina == 'relatorio_drible':
    pts = st.session_state.get('pontos_drible', 0)
    n, v = calc_drible(pts)
    st.markdown(f"<div class='stats-box'><h3>SISTEMA GOAT TV: {n}</h3>✔️ Slalom Tático Analógico 360°<br><b>+ {v} Pontos</b><br><br>❌ Defesa / Físico<br><b>- {v} Pontos</b></div>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align:center;'>{pts} PTS</h1>", unsafe_allow_html=True)
    if st.button("CONCLUIR"): st.query_params.clear(); st.session_state.pagina='hub'; st.rerun()
