import streamlit as st
import sys
import os
import pandas as pd
import plotly.express as px
from PIL import Image

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.db_handler import carregar_db, salvar_db
from engine.regras import REGRAS_TREINO, REQUISITOS_SKILLS, STATS_BASE_PES
from engine.calculos import calcular_ovr_supremo, processar_treino_master
from interface.visual import gerar_radar, desenhar_personalidade, exibir_laboratorio_skills

st.set_page_config(page_title="GOAT TV - CT SUPREMO", layout="wide", initial_sidebar_state="expanded")

if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    # --- TELA DE LOGIN / REGISTRO ---
    st.markdown("<h1 style='text-align: center; color: #ffd700;'>🏟️ CT GOAT TV - VERSÃO ÔMEGA</h1>", unsafe_allow_html=True)
    id_user = st.text_input("ID ATLETA:").upper().strip()

    if st.button("🔍 ACESSAR REGISTROS", use_container_width=True):
        db = carregar_db()
        if id_user in db: 
            st.session_state.perfil, st.session_state.id_logado, st.session_state.auth = db[id_user], id_user, True
            st.rerun()

    if id_user and id_user not in carregar_db():
        with st.form("registro_supremo"):
            st.subheader("📝 Novo Registro")
            n = st.text_input("NOME:"); i = st.number_input("IDADE:", 15, 45, 17)
            pos = st.selectbox("POSIÇÃO:", ["ATA", "MEI", "DEF"])
            c1, c2 = st.columns(2)
            alt = c1.number_input("ALTURA (m):", 1.5, 2.2, 1.78); peso = c2.number_input("PESO (kg):", 50, 130, 75)
            ft = st.file_uploader("FOTO:", type=['jpg', 'png', 'jpeg'])

            if st.form_submit_button("🚀 INICIAR CARREIRA"):
                base_ovr = 75.0
                path = f"fotos_atletas/{id_user}.png"
                if ft: Image.open(ft).save(path)
                db = carregar_db()
                db[id_user] = {
                    "nome": n, "idade": i, "altura": alt, "peso": peso, "posicao": pos, 
                    "overall": base_ovr, "foto": path, "status": "Saudável", "dna": "Iniciante",
                    "habilidades": [], "maestria": {m: 0.0 for m in REGRAS_TREINO.keys()},
                    "stats": {k: base_ovr for k in STATS_BASE_PES},
                    "personalidade": {"Altruísmo": 50, "Raça": 50, "Técnica": 50, "Compostura": 50},
                    "historico_ovr": [{"idade": i, "ovr": base_ovr}]
                }
                salvar_db(db); st.rerun()

else:
    p = st.session_state.perfil
    
    # --- SIDEBAR (SCOUT CARD COMPLETO) ---
    with st.sidebar:
        st.markdown("<h2 style='text-align: center;'>📄 SCOUT CARD</h2>", unsafe_allow_html=True)
        if os.path.exists(p.get("foto", "")): st.image(p["foto"], use_container_width=True)
        st.metric("OVERALL", p["overall"])
        st.write(f"**DNA:** {p.get('dna', 'Padrão')}")
        st.write(f"**STATUS:** {p['status']}")
        
        st.divider()
        st.subheader("🎒 Habilidades Ativas")
        st.write(", ".join(p.get("habilidades", ["Nenhuma"])))

        st.divider()
        exibir_laboratorio_skills(p, REQUISITOS_SKILLS)

        st.divider()
        st.subheader("📊 Maestria")
        for m, val in p.get("maestria", {}).items():
            if val > 0:
                st.caption(f"{m}: {val:.1f}%")
                st.progress(val/100)
        
        if st.button("SAIR"): st.session_state.auth = False; st.rerun()

    # --- DASHBOARD TÁTICO ---
    st.title(f"Bem-vindo ao CT, {p['nome'].split()[0]}")
    tabs = st.tabs(["🎮 Campo de Treino", "🧠 Atleta", "📈 Evolução"])

    with tabs[0]: 
        col_radar, col_menu = st.columns([1.5, 1])
        with col_radar: st.plotly_chart(gerar_radar(p["stats"]), use_container_width=True)
        with col_menu:
            st.subheader("Setores de Ação")
            if st.button("🛡️ DEFESA", use_container_width=True): st.session_state.portal = "DEF"
            if st.button("⚙️ MEIO", use_container_width=True): st.session_state.portal = "MEI"
            if st.button("🎯 ATAQUE", use_container_width=True): st.session_state.portal = "ATQ"

        import setores.defesa.portal as defesa
        import setores.meio_campo.portal as meio_campo
        import setores.ataque.portal as ataque
        portal = st.session_state.get('portal')
        if portal == "DEF": defesa.mostrar_sala_defesa()
        elif portal == "MEI": meio_campo.mostrar_sala_meio()
        elif portal == "ATQ": ataque.mostrar_sala_ataque()

    with tabs[1]:
        desenhar_personalidade(p["personalidade"])

    with tabs[2]:
        df = pd.DataFrame(p["historico_ovr"])
        st.plotly_chart(px.line(df, x="idade", y="ovr", title="Curva de Crescimento"), use_container_width=True)
