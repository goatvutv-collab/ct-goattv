import streamlit as st
import streamlit.components.v1 as components

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="GOAT TV - PORTAL CT", page_icon="⚽", layout="centered")

# --- 2. MEMÓRIA DO SISTEMA (PROVA DE ERROS) ---
if 'pagina' not in st.session_state:
    st.session_state.pagina = 'login'
if 'arquetipo' not in st.session_state:
    st.session_state.arquetipo = None

# Captura automática de resultados vindos do jogo (URL)
params = st.query_params
if "ms" in params:
    st.session_state.resultado_atual = int(params["ms"])
    st.session_state.pagina = 'treino' # Mantém na sala

# --- 3. LÓGICA DE EVOLUÇÃO PROPORCIONAL (PES 2020) ---
def calcular_evolucao(media_ms):
    # Regra: Só ganha ponto se média < 450ms. Só perde se ganhar.
    if media_ms < 450: return 3, 3   # Nível Elite
    elif media_ms < 650: return 1, 1 # Nível Padrão
    else: return 0, 0               # Insuficiente

# --- 4. TELA DE LOGIN ---
if st.session_state.pagina == 'login':
    st.title("🛡️ PORTAL GOAT TV")
    st.write("Bem-vindo ao Centro de Treinamento")
    
    pin = st.text_input("PIN de Atleta:", type="password")
    
    if st.button("ACESSAR CT", use_container_width=True):
        if pin == "2026": 
            st.session_state.pagina = 'hub'
            st.rerun()
        else:
            st.error("PIN incorreto!")

# --- 5. HUB DE ARQUÉTIPOS (O MENU EM GRADE) ---
elif st.session_state.pagina == 'hub':
    st.title("🏟️ HUB DE ARQUÉTIPOS")
    st.write("Selecione sua especialidade para treinar:")

    arqs = ["Pivô", "Finalizador", "Ponta", "2º Atacante", 
            "Maestro", "Motorzinho", "Pitbull", "Organizador", 
            "Muralha", "Zagueiro Técnico", "Lateral Ala", "Goleiro"]

    # Grade de 2 colunas para visual mobile
    col1, col2 = st.columns(2)
    for i, nome in enumerate(arqs):
        with [col1, col2][i % 2]:
            if st.button(f"➔ {nome}", use_container_width=True):
                st.session_state.arquetipo = nome
                st.session_state.pagina = 'treino'
                st.session_state.resultado_atual = None # Limpa treino anterior
                st.rerun()

# --- 6. SALA DE TREINO (O RETORNO DO QUADRADÃO RUDEZÃO) ---
elif st.session_state.pagina == 'treino':
    arq = st.session_state.arquetipo
    st.title(f"🏠 SALA: {arq}")

    if arq == "Goleiro":
        st.subheader("🎯 Teste de Reflexo Ninja (Visual Clássico)")
        
        # O JOGO EM JAVASCRIPT (RANDOMIZADO, ANTI-FRAUDE E COM SINCRONIZAÇÃO AUTOMÁTICA)
        # Este código gera o "Quadradão Rudezão" de image_1.png
        game_html = """
        <div id="box" style="height:350px; width:100%; border:3px solid #4CAF50; position:relative; background:#111; overflow:hidden; border-radius:15px; display:flex; justify-content:center; align-items:center;">
            <div id="ball" style="width:55px; height:55px; background:red; border-radius:50%; position:absolute; display:none; cursor:pointer; box-shadow: 0 0 15px red;"></div>
            <div id="ui">
                <button id="start" style="padding:15px 30px; font-size:18px; background:#4CAF50; color:white; border:none; border-radius:10px; cursor:pointer; font-weight:bold;">INICIAR TREINO</button>
                <p id="info" style="color:white; font-family:sans-serif; text-align:center; font-size:1.2em; font-weight:bold;"></p>
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
                    info.innerHTML = "🏁 Fim! Média: " + avg + "ms<br><br>Sincronizando com a Ficha PES...";
                    ball.style.display = 'none';
                    
                    // ENVIAR AUTOMÁTICO PARA O PYTHON (SEM BOTÃO DE CONFIRMAR)
                    setTimeout(() => {
                        const url = new URL(window.parent.location.href);
                        url.searchParams.set('ms', avg);
                        window.parent.location.href = url.href;
                    }, 800);
                    return;
                }
                ball.style.display = 'none';
                // Delay aleatório anti-spam
                setTimeout(() => {
                    // Randy Real: Posição aleatória dentro do Quadradão
                    const x = Math.random() * (box.offsetWidth - 60);
                    const y = Math.random() * (box.offsetHeight - 60);
                    
                    // Randy Real: Tamanho aleatório da bola (simula profundidade)
                    const size = 45 + Math.random() * 20;
                    ball.style.width = size + 'px';
                    ball.style.height = size + 'px';
                    
                    ball.style.left = x + 'px';
                    ball.style.top = y + 'px';
                    ball.style.display = 'block';
                    start = Date.now();
                }, 500 + Math.random() * 1000); // 0.5s a 1.5s de delay aleatório
            }

            startBtn.onclick = () => {
                count = 0; times = [];
                startBtn.style.display = 'none';
                info.innerHTML = "Prepare-se...";
                play();
            };

            ball.onclick = () => {
                const diff = Date.now() - start;
                times.push(diff);
                count++;
                ball.style.display = 'none';
                play();
            };
        </script>
        """
        # Renderiza o jogo
        components.html(game_html, height=450)

        # Processamento Automático do Resultado Sincronizado
        if "ms" in params:
            media = int(params["ms"])
            
            # Chama a função calcular_evolucao para definir quem é elite
            s, d = calcular_evolucao(media)
            
            st.divider()
            
            if s > 0:
                # Layout de Sucesso igual a image_1.png
                st.balloons()
                st.success(f"✅ TREINO FINALIZADO! Média Detectada: {media}ms")
                st.markdown(f"### 🔥 FICHA PES 2020 ATUALIZADA")
                st.write(f"📈 GANHOU: +{s} Reflexos / Alcance (Goleiro Defensivo)")
                st.write(f"📈 GANHOU: +{s} Velocidade de Ação (Goleiro Líbero)")
                st.warning(f"📉 PERDEU: -{d} Força de Chute / Força Física (Custo do especialista)")
                
                if st.button("SALVAR E SAIR"):
                    st.query_params.clear() # Limpa o resultado
                    st.session_state.pagina = 'hub'
                    st.rerun()
            else:
                # Layout de Falha igual a image_4.png
                st.error(f"❌ Média {media}ms muito lenta. O nível profissional exige menos de 650ms!")
                if st.button("REFAZER TESTE"):
                    st.query_params.clear()
                    st.rerun()
        else:
            st.info("Aguardando finalização do mini-game acima...")

    # --- SALAS EM CONSTRUÇÃO ---
    else:
        st.warning(f"A sala do {arq} está sendo calibrada pelo Comissário.")

    if st.button("⬅️ VOLTAR AO HUB", use_container_width=True):
        st.query_params.clear()
        st.session_state.pagina = 'hub'
        st.rerun()
