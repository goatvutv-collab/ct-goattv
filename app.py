import streamlit as st
import streamlit.components.v1 as components

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="GOAT TV - CT", page_icon="⚽", layout="centered")

# --- 2. MEMÓRIA DO SISTEMA ---
if 'pagina' not in st.session_state:
    st.session_state.pagina = 'login'
if 'arquetipo' not in st.session_state:
    st.session_state.arquetipo = None

# Captura automática de resultados vindos da URL
params = st.query_params
if "ms" in params:
    st.session_state.resultado_atual = int(params["ms"])
    st.session_state.pagina = 'treino' # Garante que ele continue na sala

# --- 3. LÓGICA DE EVOLUÇÃO ---
def calcular_evolucao(media_ms):
    if media_ms < 400: return 3, 3   # Elite
    elif media_ms < 600: return 1, 1 # Padrão
    else: return 0, 0               # Lento

# --- 4. TELA DE LOGIN ---
if st.session_state.pagina == 'login':
    st.title("🛡️ PORTAL GOAT TV")
    pin = st.text_input("PIN de Atleta:", type="password")
    if st.button("ENTRAR NO CT", use_container_width=True):
        if pin == "2026": 
            st.session_state.pagina = 'hub'
            st.rerun()

# --- 5. HUB DE ARQUÉTIPOS ---
elif st.session_state.pagina == 'hub':
    st.title("🏟️ HUB DE ARQUÉTIPOS")
    arqs = ["Pivô", "Finalizador", "Ponta", "2º Atacante", "Maestro", "Motorzinho", 
            "Pitbull", "Organizador", "Muralha", "Zagueiro Técnico", "Lateral Ala", "Goleiro"]
    
    col1, col2 = st.columns(2)
    for i, nome in enumerate(arqs):
        with [col1, col2][i % 2]:
            if st.button(f"➔ {nome}", use_container_width=True):
                st.session_state.arquetipo = nome
                st.session_state.pagina = 'treino'
                st.session_state.resultado_atual = None # Limpa treino anterior
                st.rerun()

# --- 6. SALA DE TREINO (O RETORNO DA BOLINHA) ---
elif st.session_state.pagina == 'treino':
    st.title(f"🏠 SALA: {st.session_state.arquetipo}")

    if st.session_state.arquetipo == "Goleiro":
        st.subheader("🎯 Teste de Reflexo Ninja")
        
        # O JOGO EM JAVASCRIPT (RANDOMIZADO E ANTI-FRAUDE)
        game_html = """
        <div id="box" style="height:350px; width:100%; border:3px solid #4CAF50; position:relative; background:#111; overflow:hidden; border-radius:15px; display:flex; justify-content:center; align-items:center;">
            <div id="ball" style="width:55px; height:55px; background:red; border-radius:50%; position:absolute; display:none; cursor:pointer; box-shadow: 0 0 15px red;"></div>
            <div id="ui">
                <button id="start" style="padding:15px 30px; font-size:18px; background:#4CAF50; color:white; border:none; border-radius:10px; cursor:pointer; font-weight:bold;">INICIAR TESTE</button>
                <p id="info" style="color:white; font-family:sans-serif; text-align:center;"></p>
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
                    info.innerHTML = "Média: " + avg + "ms<br><br><button onclick='sync(" + avg + ")' style='padding:10px; background:#FFD700; border:none; border-radius:5px; font-weight:bold; cursor:pointer;'>CONFIRMAR E SINCRONIZAR</button>";
                    ball.style.display = 'none';
                    return;
                }
                ball.style.display = 'none';
                // Delay aleatório para não ter "spam"
                setTimeout(() => {
                    const x = Math.random() * (box.offsetWidth - 60);
                    const y = Math.random() * (box.offsetHeight - 60);
                    ball.style.left = x + 'px';
                    ball.style.top = y + 'px';
                    ball.style.display = 'block';
                    start = Date.now();
                }, 500 + Math.random() * 1000);
            }

            startBtn.onclick = () => {
                count = 0; times = [];
                startBtn.style.display = 'none';
                info.innerHTML = "Prepare-se...";
                play();
            };

            ball.onclick = () => {
                times.push(Date.now() - start);
                count++;
                play();
            };

            function sync(val) {
                const url = new URL(window.parent.location.href);
                url.searchParams.set('ms', val);
                window.parent.location.href = url.href;
            }
        </script>
        """
        components.html(game_html, height=450)

        # Processamento do Resultado Sincronizado
        if "ms" in params:
            media = int(params["ms"])
            s, d = calcular_evolucao(media)
            st.divider()
            if s > 0:
                st.success(f"✅ TREINO VALIDADO: {media}ms")
                st.write(f"📈 SUBIU: +{s} Reflexo | 📉 CAIU: -{d} Chute Rasteiro")
                if st.button("SALVAR E SAIR"):
                    st.query_params.clear()
                    st.session_state.pagina = 'hub'
                    st.rerun()
            else:
                st.error(f"❌ Média {media}ms muito lenta. Tente novamente!")
                if st.button("REFAZER TESTE"):
                    st.query_params.clear()
                    st.rerun()
        else:
            st.info("Aguardando sincronização do resultado...")

    if st.button("⬅️ VOLTAR AO HUB", use_container_width=True):
        st.query_params.clear()
        st.session_state.pagina = 'hub'
        st.rerun()
