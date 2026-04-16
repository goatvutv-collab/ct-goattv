import streamlit as st
import sys
import os
import pandas as pd
import plotly.express as px
from PIL import Image

# 1. FIX DO RENDER (Essencial da Versão 11)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 2. IMPORTAÇÕES MODULARES
from database.db_handler import carregar_db, salvar_db
from engine.regras import REGRAS_TREINO, REQUISITOS_SKILLS, STATS_BASE_PES
from engine.calculos import calcular_ovr_supremo, processar_treino_master
from interface.visual import gerar_radar, desenhar_personalidade

# 3. IMPORTAÇÃO DOS SETORES (Como está no seu GitHub)
import setores.defesa.portal as defesa
import setores.meio_campo.portal as meio_campo
import setores.ataque.portal as ataque

st.set_page_config(page_title="GOAT TV - CT SUPREMO", layout="wide", initial_sidebar_state="expanded")

if 'auth' not in st.session_state: st.session_state.auth = False

# --- LÓGICA DE LOGIN E ACESSO ---
if not st.session_state.auth:
    st.markdown("<h1 style='text-align: center; color: #ffd700;'>🏟️ CT GOAT TV - VERSÃO ÔMEGA</h1>", unsafe_allow_html=True)
    id_user = st.text_input("ID ATLETA:").upper().strip()
    
    if st.button("🔍 ACESSAR REGISTROS", use_container_width=True):
        db = carregar_db()
        if id_user in db: 
            st.session_state.perfil, st.session_state.id_logado, st.session_state.auth = db[id_user], id_user, True
            st.rerun()

    if id_user and id_user not in carregar_db():
        with st.form("registro_supremo"):
            st.subheader("📝 Novo Registro de Atleta")
            n = st.text_input("NOME COMPLETO:")
            i = st.number_input("IDADE:", 15, 45, 17)
            pos = st.selectbox("POSIÇÃO:", ["ATA", "MEI", "DEF"])
            c1, c2 = st.columns(2)
            alt = c1.number_input("ALTURA (m):", 1.5, 2.2, 1.78)
            peso = c2.number_input("PESO (kg):", 50, 130, 75)
            ft = st.file_uploader("FOTO OFICIAL:", type=['jpg', 'png', 'jpeg'])
            
            if st.form_submit_button("🚀 INICIAR CARREIRA"):
                base_ovr = 75.0
                path = f"fotos_atletas/{id_user}.png"
                if ft: Image.open(ft).save(path)
                
                db = carregar_db()
                # AQUI A MÁGICA: Registrando com os 23 Atributos do PES
                db[id_user] = {
                    "nome": n, "idade": i, "altura": alt, "peso": peso, "posicao": pos, 
                    "overall": base_ovr, "foto": path, "status": "Saudável", 
                    "habilidades": [], "maestria": {m: 0.0 for m in REGRAS_TREINO.keys()},
                    "stats": {k: base_ovr for k in STATS_BASE_PES}, # Usa a lista de 23 stats
                    "personalidade": {"Altruísmo": 50, "Raça": 50, "Técnica": 50, "Compostura": 50},
                    "historico_ovr": [{"idade": i, "ovr": base_ovr}]
                }
                salvar_db(db)
                st.rerun()

else:
    p = st.session_state.perfil
    
    # --- SIDEBAR (SCOUT CARD) ---
    with st.sidebar:
        if os.path.exists(p.get("foto", "")): st.image(p["foto"], use_container_width=True)
        st.metric("OVERALL", p["overall"])
        st.write(f"**STATUS:** {p['status']}")
        if st.button("SAIR"): st.session_state.auth = False; st.rerun()

    # --- DASHBOARD TÁTICO ---
    st.title(f"Bem-vindo, {p['nome'].split()[0]}")
    tabs = st.tabs(["🎮 Campo de Treino", "🧠 Atleta", "📈 Evolução"])

    with tabs[0]: # CAMPO DE TREINO
        col_radar, col_menu = st.columns([1.5, 1])
        with col_radar: st.plotly_chart(gerar_radar(p["stats"]), use_container_width=True)
        with col_menu:
            st.subheader("Setores")
            if st.button("🛡️ DEFESA", use_container_width=True): st.session_state.portal = "DEF"
            if st.button("⚙️ MEIO", use_container_width=True): st.session_state.portal = "MEI"
            if st.button("🎯 ATAQUE", use_container_width=True): st.session_state.portal = "ATQ"

        # CHAMADA DOS PORTAIS MODULARES
        portal = st.session_state.get('portal')
        if portal == "DEF": defesa.mostrar_sala_defesa()
        elif portal == "MEI": meio_campo.mostrar_sala_meio()
        elif portal == "ATQ": ataque.mostrar_sala_ataque()

    with tabs[1]: # ATLETA
        desenhar_personalidade(p["personalidade"])

    with tabs[2]: # EVOLUÇÃO
        df = pd.DataFrame(p["historico_ovr"])
        fig_evol = px.line(df, x="idade", y="ovr", title="Crescimento de Overall")
        st.plotly_chart(fig_evol, use_container_width=True)
