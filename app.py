# --- app.py ---
import streamlit as st
import os, sys
from PIL import Image
from datetime import date
from database.db_handler import carregar_db, salvar_db, gerenciar_foto_antiga
from engine.regras import STATS_BASE_PES, STATS_NIVEL, REGRAS_TREINO, REQUISITOS_ESTILOS, REQUISITOS_SKILLS
from engine.calculos import calcular_ovr_supremo, distribuir_stats_iniciais, calcular_idade
from interface.visual import gerar_radar, desenhar_personalidade, definir_estilo_exibicao

st.set_page_config(page_title="GOAT TV - CT SUPREMO", layout="wide", initial_sidebar_state="expanded")

if 'auth' not in st.session_state: st.session_state.auth = False
if 'portal' not in st.session_state: st.session_state.portal = None

# --- ACESSO / REGISTRO ---
if not st.session_state.auth:
    st.markdown("<h1 style='text-align: center; color: #ffd700;'>🏟️ CT GOAT TV 2021</h1>", unsafe_allow_html=True)
    id_user = st.text_input("ID ATLETA:").upper().strip()
    
    if st.button("🔍 ENTRAR NO CT", use_container_width=True):
        db = carregar_db()
        if id_user in db:
            st.session_state.perfil, st.session_state.id_logado, st.session_state.auth = db[id_user], id_user, True
            st.rerun()

    if id_user and id_user not in carregar_db():
        with st.form("registro"):
            st.subheader("📝 CONTRATO DE ESTREIA")
            c1, c2 = st.columns(2)
            with c1:
                n = st.text_input("NOME COMPLETO:")
                # DATA DE NASCIMENTO (CALENDÁRIO)
                nasc = st.date_input("DATA DE NASCIMENTO:", value=date(2000, 1, 1), min_value=date(1980, 1, 1), max_value=date(2012, 12, 31))
                pos = st.selectbox("POSIÇÃO:", ["CA", "SA", "MAT", "VOL", "ZC", "LD", "LE", "GOL"])
            with c2:
                dna_ini = st.selectbox("DNA (ARQUÉTIPO):", ["Nenhum"] + list(REGRAS_TREINO.keys()))
                alt = st.number_input("ALTURA (m):", 1.5, 2.2, 1.80); pes = st.number_input("PESO (kg):", 50, 120, 75)
            ft = st.file_uploader("FOTO DO PERFIL:")
            if st.form_submit_button("🚀 INICIAR CARREIRA"):
                db = carregar_db(); path = f"fotos_atletas/{id_user}.png" if ft else "fotos_atletas/default.png"
                if ft: Image.open(ft).save(path)
                idade_real = calcular_idade(nasc)
                
                atleta = {
                    "nome": n, "nascimento": nasc.strftime("%Y-%m-%d"), "idade": idade_real,
                    "altura": alt, "peso": pes, "posicao": pos, "dna": dna_ini, "dna_origem": dna_ini,
                    "foto": path, "status": "Saudável", "stats": distribuir_stats_iniciais(dna_ini),
                    "maestria": {m: 0.0 for m in REGRAS_TREINO.keys()}, "habilidades": [],
                    "personalidade": {"Raça": 50, "Técnica": 50, "Altruísmo": 50, "Compostura": 50},
                    "stats_fixos": {"Forma física": 4, "Resistência a lesão": 2, "Pior pé frequência": 2, "Pior pé precisão": 2}
                }
                atleta["overall"] = calcular_ovr_supremo(atleta); db[id_user] = atleta; salvar_db(db); st.rerun()

else:
    p = st.session_state.perfil
    with st.sidebar:
        st.markdown("<h2 style='text-align: center;'>📄 SCOUT CARD</h2>", unsafe_allow_html=True)
        st.image(p["foto"], use_container_width=True)
        st.metric("OVERALL", p["overall"])
        st.write(f"**🧬 DNA:** {p['dna']}")
        st.write(f"**🎂 IDADE:** {p['idade']} anos")
        if st.button("🚪 SAIR"): st.session_state.auth = False; st.rerun()

    tabs = st.tabs(["🎮 Campo de Treino", "🧠 Atleta", "⚙️ Ajustes"])

    with tabs[1]: # ABA ATLETA
        st.subheader(f"📊 Perfil de {p['nome']}")
        col_pers, col_fisi = st.columns(2)
        with col_pers: desenhar_personalidade(p["personalidade"])
        with col_fisi:
            st.markdown("### 🧬 Fisiologia")
            st.write(f"**Pior Pé Precisão:** {p['stats_fixos']['Pior pé precisão']}/4")
            st.write(f"**Forma Física:** {p['stats_fixos']['Forma física']}/8")
            st.write(f"**Resistência a Lesão:** {p['stats_fixos']['Resistência a lesão']}/3")
