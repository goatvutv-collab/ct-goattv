import streamlit as st
import json
import os
from PIL import Image

# --- CONFIGURAÇÃO DE DIRETÓRIOS ---
DB_DIR = "/app/fotos_atletas" if os.path.exists("/app/fotos_atletas") else "fotos_atletas"
DB_FILE = os.path.join(DB_DIR, "jogadores_goat.json")

if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)

# --- FUNÇÕES DE INTELIGÊNCIA DE DADOS ---
def carregar_db():
    if not os.path.exists(DB_FILE): return {}
    with open(DB_FILE, "r") as f: return json.load(f)

def salvar_db(dados):
    with open(DB_FILE, "w") as f: json.dump(dados, f, indent=4)

def processar_resultado_treino(id_atleta, modulo, score):
    """
    Esta é a função que o Lobby usa para calcular o desempenho.
    Ela aplica a Lei da Compensação (3x3) do Dossiê.
    """
    db = carregar_db()
    atleta = db[id_atleta]
    
    # Exemplo: Se for o Módulo 11 (Drible)
    if modulo == "DRIBLE":
        ganho = (score / 1000) * 2.5  # Max +2.5
        perda = (score / 1000) * 1.5  # Max -1.5
        
        # Sobe DNA
        atleta["stats"]["Drible"] += ganho
        atleta["stats"]["Controle"] += ganho
        # Desce Trava
        atleta["stats"]["Defesa"] -= perda
        
    # Atualiza o Overall Geral (Média simples para exemplo)
    atleta["overall"] = sum(atleta["stats"].values()) / len(atleta["stats"])
    
    db[id_atleta] = atleta
    salvar_db(db)
    return atleta

# --- INTERFACE DO LOBBY ---
st.set_page_config(page_title="GOAT TV - CENTRAL DE INTELIGÊNCIA", layout="centered")

if 'auth' not in st.session_state: st.session_state.auth = False

# TELA DE ACESSO
if not st.session_state.auth:
    st.markdown("<h1 style='text-align: center; color: #ffd700;'>🏟️ CT GOAT TV</h1>", unsafe_allow_html=True)
    id_user = st.text_input("ID DO ATLETA:").upper().strip()
    
    if id_user:
        db = carregar_db()
        if id_user in db:
            if st.button(f"ACESSAR PERFIL DE {id_user}", use_container_width=True):
                st.session_state.perfil = db[id_user]
                st.session_state.id_logado = id_user
                st.session_state.auth = True
                st.rerun()
        else:
            # CADASTRO NOVO (Regra de Idade)
            nome = st.text_input("NOME COMPLETO:")
            idade = st.number_input("IDADE:", min_value=14, max_value=45, value=18)
            foto = st.file_uploader("FOTO DE PERFIL:", type=['jpg', 'png', 'jpeg'])
            
            if st.button("GERAR FICHA CADASTRAL"):
                if nome and foto:
                    base = 85 if idade > 22 else (80 if 20 <= idade <= 22 else 75)
                    foto_path = os.path.join(DB_DIR, f"{id_user}.png")
                    Image.open(foto).save(foto_path)
                    
                    db[id_user] = {
                        "nome": nome, "idade": idade, "overall": base, "dna": "Recruta", "foto": foto_path,
                        "stats": {"Drible": base, "Controle": base, "Defesa": base, "Físico": base}
                    }
                    salvar_db(db)
                    st.success("Ficha Criada! Acesse agora.")
                    st.rerun()

# LOBBY ATIVO (CENTRAL DE DADOS)
else:
    perfil = st.session_state.perfil
    
    # Scout Card Lateral
    with st.sidebar:
        st.image(perfil["foto"], use_container_width=True)
        st.markdown(f"<h3 style='text-align: center;'>{perfil['nome']}</h3>", unsafe_allow_html=True)
        st.metric("OVERALL", f"{perfil['overall']:.1f}")
        st.write(f"**DNA:** {perfil['dna']}")
        if st.button("LOGOUT"):
            st.session_state.auth = False
            st.rerun()

    st.title("Painel de Desempenho")
    
    # Portais de acesso às salas
    col1, col2, col3 = st.columns(3)
    with col1: st.button("🛡️ SALA DEFESA", use_container_width=True)
    with col2: st.button("⚙️ SALA MEIO", use_container_width=True)
    with col3: 
        if st.button("🎯 SALA ATAQUE", use_container_width=True):
            st.session_state.sala = "ATAQUE"

    # Dentro da Sala de Ataque
    if st.session_state.get('sala') == "ATAQUE":
        st.markdown("---")
        st.subheader("Módulos Disponíveis: ATAQUE")
        if st.button("INICIAR TREINO: SLALOM EM U (Drible)"):
            if os.path.exists("drible_engine.py"):
                import drible_engine
                # O Lobby envia o tipo, e o drible_engine devolve o score para o Lobby calcular
                score_final = drible_engine.executar_treino("DRIBLE")
                
                # O LOBBY CALCULA E VINCULA AO PERFIL
                novo_perfil = processar_resultado_treino(st.session_state.id_logado, "DRIBLE", score_final)
                st.session_state.perfil = novo_perfil
                st.success(f"Treino Finalizado! Score: {score_final}. Dados vinculados ao seu Scout.")
            else:
                st.error("Módulo de treino não encontrado no servidor.")
                        "nome": nome, "idade": idade, "overall": base,
                        "dna": "Recruta", "foto": foto_path,
                        "stats": {"Drible": base, "Físico": base, "Passe": base, "Defesa": base}
                    }
                    salvar_db(db)
                    st.success("✅ Atleta Registrado! Clique no botão de Acessar.")
                    st.rerun()

# --- LOBBY (PERFIL DO ATLETA) ---
else:
    perfil = st.session_state.perfil
    
    with st.sidebar:
        st.markdown("<h2 style='text-align: center;'>📄 SCOUT CARD</h2>", unsafe_allow_html=True)
        if os.path.exists(perfil["foto"]):
            st.image(perfil["foto"], use_container_width=True)
        
        st.markdown(f"<h3 style='text-align: center;'>{perfil['nome']}</h3>", unsafe_allow_html=True)
        st.divider()
        st.metric("OVERALL", f"{perfil['overall']}")
        st.write(f"**DNA:** {perfil['dna']}")
        
        if st.button("DESLOGAR"):
            st.session_state.auth = False
            st.rerun()

    st.markdown(f"## Bem-vindo, {perfil['nome'].split()[0]}!")
    st.write("Selecione o setor do campo para treinar:")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🛡️ DEF", use_container_width=True): st.session_state.portal = "DEF"
    with col2:
        if st.button("⚙️ MEI", use_container_width=True): st.session_state.portal = "MEI"
    with col3:
        if st.button("🎯 ATQ", use_container_width=True): st.session_state.portal = "ATQ"

    if 'portal' in st.session_state:
        st.write("---")
        st.subheader(f"📍 Setor: {st.session_state.portal}")
        
        if st.session_state.portal == "ATQ":
            if st.button("🎮 INICIAR MÓDULO 11 (Slalom em U)", use_container_width=True):
                # TENTA CHAMAR O TREINO SÓ SE O ARQUIVO EXISTIR
                if os.path.exists("drible_engine.py"):
                    import drible_engine
                    drible_engine.executar_treino("DRIBLE")
                else:
                    st.error("🚧 Módulo em manutenção técnica. Aguarde o Comissário.")
        else:
            st.info("🚧 Este setor está em preparação tática.")

st.sidebar.caption("GOAT TV FEDERATION © 2026")
