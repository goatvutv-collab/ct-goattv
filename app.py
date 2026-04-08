import streamlit as st
import streamlit.components.v1 as components

# --- 1. ESTILO VISUAL GOAT TV PRO (CSS DARK & GOLD) ---
st.set_page_config(page_title="GOAT TV - CT", page_icon="⚽", layout="centered")

st.markdown("""
    <style>
    /* Fundo e Texto Dark Mode */
    .stApp { background-color: #0E1117; color: #FFFFFF; font-family: sans-serif; }
    
    /* Títulos e Headers */
    h1, h2, h3 { text-align: center; color: #FFD700; font-weight: bold; }
    h2 { color: #FFFFFF; } /* Header da Sala em Branco */

    /* Botões Grandes e Estilizados para Mobile */
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

    /* Estilização do Relatório de Ficha */
    .report-card {
        padding: 20px;
        border-radius: 20px;
        background-color: #161b22;
        border: 2px solid #30363d;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .gain-card { border-left: 5px solid #4CAF50; background-color: rgba(76, 175, 80, 0.1); }
    .loss-card { border-left: 5px solid #F44336; background-color: rgba(244, 67, 54, 0.1); }
    .report-card h3 { color: #FFFFFF; margin-top: 0; }
    .report-card ul { list-style-type: none; padding: 0; }
    .report-card li { font-size: 18px; margin-bottom: 8px; }
    
    /* Configuração do "Quadradão Rudezão" de Jogo */
    iframe {
        border-radius: 20px;
        border: 3px solid #FFD700;
        background-color: #000;
    }
    
    /* Limpeza de Interface Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 2. GERENCIAMENTO DE ESTADOS (DADOS) ---
if 'pagina' not in st.session_state:
    st.session_state.pagina = 'login'
if 'arquetipo' not in st.session_state:
    st.session_state.arquetipo = None
if 'resultado_ms' not in st.session_state:
    st.session_state.resultado_ms = None

# Sincronização Automática via URL (A Ponte de Dados Blindada)
params = st.query_params
if "ms" in params:
    st.session_state.resultado_ms = int(params["ms"])
    st.session_state.pagina = 'relatorio' # Pula direto para o relatório

# Função de Ganhos/Perdas Proporcional (PES 2020 Mapeado)
def calcular_evolucao_pes2020(ms):
    if ms < 450: # Nível Elite
        subir = {"Reflexos do GL": 3, "Alcance do GL": 3, "Consciência de GO": 1}
        descer = {"Chute Rasteiro": 3, "Força de Chute": 2}
        return subir, descer
    elif ms < 650: # Nível Padrão
        subir = {"Reflexos do GL": 1, "Alcance do GL": 1, "Consciência de GO": 1}
        descer = {"Chute Rasteiro": 1, "Força de Chute": 1}
        return subir, descer
    else: # Insuficiente
        return None, None

# --- 3. NAVEGAÇÃO ENTRE TELAS ---

# TELA DE LOGIN
if st.session_state.pagina == 'login':
    st.markdown("<h1>🛡️ PORTAL GOAT TV</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>CENTRO DE TREINAMENTO DIGITAL</p>", unsafe_allow_html=True)
    pin = st.text_input("PIN DE ACESSO:", type="password")
    if st.button("ACESSAR SISTEMA", use_container_width=True):
        if pin == "2026": 
            st.session_state.pagina = 'hub'
            st.rerun()
        else:
            st.error("PIN Incorreto.")

# HUB (GRADE DE ELITE)
elif st.session_state.pagina == 'hub':
    st.markdown("<h2>🏟️ HUB DE ARQUÉTIPOS</h2>", unsafe_allow_html=True)
    st.write("Selecione sua especialidade para treinar:")

    arqs = ["Pivô", "Finalizador", "Ponta", "2º Atacante", "Maestro", "Motorzinho", 
            "Pitbull", "Organizador", "Muralha", "Zagueiro Técnico", "Lateral Ala", "Goleiro"]
    
    col1, col2 = st.columns(2)
    for i, nome in enumerate(arqs):
        with [col1, col2][i % 2]:
            if st.button(f"{nome}", use_container_width=True):
                st.session_state.arquetipo = nome
                st.session_state.pagina = 'jogar'
                st.rerun()

# SALA DO JOGO (HTML/JS RUDEZÃO COM RANDY REAL)
elif st.session_state.pagina == 'jogar':
    st.markdown(f"<h2 style='text-align: center;'>🏠 SALA: {st.session_state.arquetipo}</h2>", unsafe_allow_html=True)
    st.subheader("⚽ Teste de Reflexo Ninja (Visual Clássico)")

    # O QUADRADÃO RUDEZÃO DE JOGO (Image_1.png)
    game_html = """
    <div id="box" style="height:350px; width:100%; position:relative; overflow:hidden; display:flex; justify-content:center; align-items:center;">
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
                info.innerHTML = "<span style='color:#FFD700; font-size:24px;'>🏁 FIM!</span><br>Sincronizando Ficha: " + avg + "ms";
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
            count = 0; times = []; startBtn.style.display = 'none'; info.innerHTML = "PREPARE-SE..."; play();
        };

        ball.onclick = () => { times.push(Date.now() - start); count++; ball.style.display = 'none'; play(); };
    </script>
    """
    components.html(game_html, height=450)
    
    if st.button("⬅️ VOLTAR AO HUB", use_container_width=True):
        st.query_params.clear() 
        st.session_state.pagina = 'hub'
        st.rerun()

# RELATÓRIO TÉCNICO (ONDE O PONTO É COMPUTADO E EXIBIDO)
elif st.session_state.pagina == 'relatorio':
    st.markdown("<h2>📊 RELATÓRIO TÉCNICO</h2>", unsafe_allow_html=True)
    media = st.session_state.resultado_ms
    s, d = calcular_evolucao_pes2020(media)
    
    # Exibição do Resultado Geral
    st.divider()
    st.metric(label="Média de Reflexo Detectada", value=f"{media} ms")
    st.divider()

    # O RELATÓRIO QUE VOCÊ SOLICITOU (SUBIR E DESCER VISÍVEL)
    if s:
        # Tabela de Ganhos
        st.markdown("<div class='report-card gain-card'>", unsafe_allow_html=True)
        st.markdown("<h3>📈 GANHOS (Subir na Ficha)</h3>", unsafe_allow_html=True)
        st.markdown("<ul>", unsafe_allow_html=True)
        for attr, value in s.items():
            st.markdown(f"<li style='color:#4CAF50;'>✅ <b>+ {value}</b> {attr}</li>", unsafe_allow_html=True)
        st.markdown("</ul>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Tabela de Perdas
        st.markdown("<div class='report-card loss-card'>", unsafe_allow_html=True)
        st.markdown("<h3>📉 PERDAS (Descer na Ficha)</h3>", unsafe_allow_html=True)
        st.markdown("<ul>", unsafe_allow_html=True)
        for attr, value in d.items():
            st.markdown(f"<li style='color:#F44336;'>❌ <b>- {value}</b> {attr}</li>", unsafe_allow_html=True)
        st.markdown("</ul>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.balloons()
        st.success("Ficha do PES 2020 Validada! Atualize os valores.")

    else:
        st.error(f"❌ TREINO INSUFICIENTE: {media}ms")
        st.write("O desempenho profissional do goleiro exige menos de 650ms. Nenhuma pontuação foi alterada.")
        
    if st.button("CONCLUIR E VOLTAR AO CT", use_container_width=True):
        st.query_params.clear() 
        st.session_state.pagina = 'hub'
        st.rerun()
