import streamlit as st
import streamlit.components.v1 as components

# --- 1. ESTILO GOAT TV (CSS PERSONALIZADO) ---
st.set_page_config(page_title="GOAT TV - CT", page_icon="⚽", layout="centered")

st.markdown("""
    <style>
    /* Fundo e Texto Geral */
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    
    /* Customização dos Botões do Hub */
    div.stButton > button:first-child {
        height: 120px;
        background: linear-gradient(145deg, #1e1e1e, #111);
        border: 2px solid #FFD700;
        color: #FFD700;
        border-radius: 20px;
        font-size: 20px;
        font-weight: bold;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.5);
        transition: 0.3s;
    }
    div.stButton > button:hover {
        border-color: #4CAF50;
        color: #4CAF50;
        transform: scale(1.02);
    }
    
    /* Esconder menus do Streamlit para parecer App */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 2. MOTOR DE DADOS ---
if 'pagina' not in st.session_state: st.session_state.pagina = 'login'
if 'arquetipo' not in st.session_state: st.session_state.arquetipo = None

# Captura de Resultado (A API interna via URL)
params = st.query_params
if "ms" in params:
    st.session_state.resultado_ms = int(params["ms"])
    st.session_state.pagina = 'resultado'

def calcular_evolucao(ms):
    if ms < 420: return 3, 3 # Nível Elite
    elif ms < 620: return 1, 1 # Nível Padrão
    else: return 0, 0

# --- 3. TELAS ---

# LOGIN
if st.session_state.pagina == 'login':
    st.markdown("<h1 style='text-align: center; color: #FFD700;'>🛡️ GOAT TV</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>CENTRO DE TREINAMENTO</p>", unsafe_allow_html=True)
    pin = st.text_input("PIN DE ACESSO:", type="password")
    if st.button("ACESSAR SISTEMA", use_container_width=True):
        if pin == "2026": 
            st.session_state.pagina = 'hub'
            st.rerun()

# HUB (GRID DE ELITE)
elif st.session_state.pagina == 'hub':
    st.markdown("<h2 style='text-align: center;'>🏟️ HUB DE ARQUÉTIPOS</h2>", unsafe_allow_html=True)
    arqs = ["Pivô", "Finalizador", "Ponta", "2º Atacante", "Maestro", "Motorzinho", 
            "Pitbull", "Organizador", "Muralha", "Zagueiro Técnico", "Lateral Ala", "Goleiro"]
    
    col1, col2 = st.columns(2)
    for i, nome in enumerate(arqs):
        with [col1, col2][i % 2]:
            if st.button(f"{nome}", use_container_width=True):
                st.session_state.arquetipo = nome
                st.session_state.pagina = 'jogar'
                st.rerun()

# SALA DO JOGO (HTML/JS RUDEZÃO)
elif st.session_state.pagina == 'jogar':
    st.markdown(f"<h2 style='text-align: center; color: #4CAF50;'>🏠 SALA: {st.session_state.arquetipo}</h2>", unsafe_allow_html=True)
    
    game_html = """
    <div id="box" style="height:350px; width:100%; border:3px solid #FFD700; position:relative; background:#000; overflow:hidden; border-radius:15px; display:flex; justify-content:center; align-items:center;">
        <div id="ball" style="width:55px; height:55px; background:red; border-radius:50%; position:absolute; display:none; cursor:pointer; box-shadow: 0 0 20px red; border: 3px solid white;"></div>
        <div id="ui">
            <button id="start" style="padding:20px 40px; font-size:20px; background:#4CAF50; color:white; border:none; border-radius:12px; cursor:pointer; font-weight:bold; box-shadow: 0 5px 0 #2E7D32;">INICIAR TREINO</button>
            <p id="info" style="color:white; font-family:sans-serif; text-align:center; font-weight:bold;"></p>
        </div>
    </div>

    <script>
        const ball = document.getElementById('ball');
        const startBtn = document.getElementById('start');
        const info = document.getElementById('info');
        const box = document.getElementById('box');
        let times = [];
        let start;
        let count = 0;

        function play() {
            if (count >= 5) {
                const avg = Math.round(times.reduce((a, b) => a + b, 0) / 5);
                info.innerHTML = "<span style='color:#FFD700; font-size:24px;'>🏁 FIM!</span><br>Sincronizando Média: " + avg + "ms";
                ball.style.display = 'none';
                
                // REDIRECIONAMENTO COM TIMEOUT PARA O USUÁRIO VER O FIM
                setTimeout(() => {
                    const currentUrl = window.parent.location.href.split('?')[0];
                    window.parent.location.href = currentUrl + "?ms=" + avg;
                }, 1200);
                return;
            }
            ball.style.display = 'none';
            setTimeout(() => {
                const x = Math.random() * (box.offsetWidth - 70);
                const y = Math.random() * (box.offsetHeight - 70);
                ball.style.left = x + 'px';
                ball.style.top = y + 'px';
                ball.style.display = 'block';
                start = Date.now();
            }, 600 + Math.random() * 800);
        }

        startBtn.onclick = () => {
            count = 0; times = [];
            startBtn.style.display = 'none';
            info.innerHTML = "FOCO NA TELA...";
            play();
        };

        ball.onclick = () => {
            times.push(Date.now() - start);
            count++;
            ball.style.display = 'none';
            play();
        };
    </script>
    """
    components.html(game_html, height=450)
    
    if st.button("⬅️ SAIR DA SALA"):
        st.session_state.pagina = 'hub'
        st.rerun()

# TELA DE RESULTADO (ONDE O PONTO É COMPUTADO)
elif st.session_state.pagina == 'resultado':
    st.markdown("<h2 style='text-align: center; color: #FFD700;'>📊 RELATÓRIO TÉCNICO</h2>", unsafe_allow_html=True)
    media = st.session_state.resultado_ms
    s, d = calcular_evolucao(media)
    
    st.divider()
    st.metric(label="Média de Reflexo", value=f"{media} ms")
    
    if s > 0:
        st.balloons()
        st.success(f"📈 NÍVEL APROVADO! Ganhos: +{s} / Perdas: -{d}")
        st.write("A ficha do seu atleta no PES 2020 já pode ser atualizada.")
    else:
        st.error(f"❌ DESEMPENHO ABAIXO DA MÉDIA. O nível profissional exige mais agilidade.")
        
    if st.button("CONCLUIR E VOLTAR AO HUB", use_container_width=True):
        st.query_params.clear() 
        st.session_state.pagina = 'hub'
        st.rerun()
