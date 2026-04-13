import streamlit as st
import json
import os
from PIL import Image

# Configuração para o Disco Persistente do Render
DB_FILE = "/app/fotos_atletas/jogadores_goat.json" if os.path.exists("/app/fotos_atletas") else "jogadores_goat.json"
IMG_DIR = "/app/fotos_atletas" if os.path.exists("/app/fotos_atletas") else "fotos_atletas"

if not os.path.exists(IMG_DIR):
    os.makedirs(IMG_DIR)

def carregar_db():
    if not os.path.exists(DB_FILE): return {}
    with open(DB_FILE, "r") as f: return json.load(f)

def salvar_db(dados):
    with open(DB_FILE, "w") as f: json.dump(dados, f, indent=4)

st.set_page_config(page_title="GOAT TV - CT", layout="centered")

# Estilo para botões mobile
st.markdown("<style>div.stButton > button:first-child {height: 3em; font-size: 18px; font-weight: bold; margin-bottom: 10px;}</style>", unsafe_allow_html=True)

if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("<h1 style='text-align: center; color: #ffd700;'>🏟️ CT GOAT TV</h1>", unsafe_allow_html=True)
    id_user = st.text_input("ID DO ATLETA:").upper()
    
    if id_user:
        db = carregar_db()
        if id_user in db:
            if st.button(f"ENTRAR COMO {id_user} 🚀", use_container_width=True):
                st.session_state.perfil = db[id_user]
                st.session_state.id_logado = id_user
                st.session_state.auth = True
                st.rerun()
        else:
            st.info("Novo Recruta! Preencha sua ficha:")
            nome = st.text_input("NOME COMPLETO:")
            idade = st.number_input("IDADE:", min_value=14, max_value=45, value=18)
            foto = st.file_uploader("SUA FOTO:", type=['jpg', 'png', 'jpeg'])
            
            if st.button("CONTRATAR ATLETA 📝", use_container_width=True):
                if nome and foto:
                    # Regra de Overall por Idade
                    if idade > 22: base = 85
                    elif 20 <= idade <= 22: base = 80
                    else: base = 75
                    
                    foto_path = os.path.join(IMG_DIR, f"{id_user}.png")
                    Image.open(foto).save(foto_path)
                    
                    db[id_user] = {"nome": nome, "idade": idade, "overall": base, "dna": "Recruta", "foto": foto_path, "stats": {"Drible": base, "Velocidade": base, "Controle": base, "Defesa": base}}
                    salvar_db(db)
                    st.success("Registrado! Agora clique em Entrar.")
                    st.rerun()
else:
    perfil = st.session_state.perfil
    with st.sidebar:
        if os.path.exists(perfil["foto"]): st.image(perfil["foto"], use_container_width=True)
        st.markdown(f"### {perfil['nome']}")
        st.metric("OVERALL", perfil["overall"])
        st.write(f"**DNA:** {perfil['dna']}")
        if st.button("SAIR"): 
            st.session_state.auth = False
            st.rerun()

    st.markdown("## Central de Treinamento")
    c1, c2, c3 = st.columns(3)
    with c1: st.button("🛡️ DEF", use_container_width=True)
    with c2: st.button("⚙️ MEI", use_container_width=True)
    with c3: 
        if st.button("🎯 ATQ", use_container_width=True): st.session_state.portal = "ATQ"

    if st.session_state.get('portal') == "ATQ":
        st.write("---")
        if st.button("🎮 MÓDULO 11: SLALOM EM U", use_container_width=True):
            import drible_engine
            drible_engine.executar_treino("DRIBLE")

