import streamlit as st
import json
import os
from PIL import Image

# --- CONFIGURAÇÃO DE DISCO (RENDER) ---
# Se estiver no Render, usa o disco. Se estiver local, usa a pasta do projeto.
DB_DIR = "/app/fotos_atletas" if os.path.exists("/app/fotos_atletas") else "fotos_atletas"
DB_FILE = os.path.join(DB_DIR, "jogadores_goat.json")

if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)

def carregar_db():
    if not os.path.exists(DB_FILE): return {}
    with open(DB_FILE, "r") as f: return json.load(f)

def salvar_db(dados):
    with open(DB_FILE, "w") as f: json.dump(dados, f, indent=4)

# --- CONFIGURAÇÃO VISUAL ---
st.set_page_config(page_title="GOAT TV - CT", layout="centered")

st.markdown("""
    <style>
    div.stButton > button:first-child { height: 3em; font-size: 18px; font-weight: bold; margin-bottom: 10px; border-radius: 12px; }
    [data-testid="stSidebar"] { background-color: #0e1117; border-right: 2px solid #ffd700; }
    </style>
    """, unsafe_allow_html=True)

if 'auth' not in st.session_state: st.session_state.auth = False

# --- TELA DE ACESSO ---
if not st.session_state.auth:
    st.markdown("<h1 style='text-align: center; color: #ffd700;'>🏟️ CT GOAT TV</h1>", unsafe_allow_html=True)
    id_user = st.text_input("DIGITE SEU ID (Ex: GOAT01):").upper().strip()
    
    if id_user:
        db = carregar_db()
        if id_user in db:
            if st.button(f"ACESSAR FICHA DE {id_user} 🚀", use_container_width=True):
                st.session_state.perfil = db[id_user]
                st.session_state.id_logado = id_user
                st.session_state.auth = True
                st.rerun()
        else:
            st.info("🆔 ID não encontrado. Crie sua ficha de atleta:")
            nome = st.text_input("NOME COMPLETO:")
            idade = st.number_input("IDADE:", min_value=14, max_value=45, value=18)
            foto = st.file_uploader("CARREGUE SEU ROSTO (Foto de Perfil):", type=['jpg', 'png', 'jpeg'])
            
            if st.button("ASSINAR CONTRATO ✍️", use_container_width=True):
                if nome and foto:
                    # REGRA DE OVERALL POR IDADE (DOSSIÊ)
                    base = 85 if idade > 22 else (80 if 20 <= idade <= 22 else 75)
                    
                    foto_path = os.path.join(DB_DIR, f"{id_user}.png")
                    img = Image.open(foto)
                    img.save(foto_path)
                    
                    db[id_user] = {
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
