# --- app.py ---
import streamlit as st
import sys, os
import pandas as pd
import plotly.express as px
from PIL import Image

# Garante que o Python ache as pastas do projeto
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.db_handler import carregar_db, salvar_db
from engine.regras import REGRAS_TREINO, REQUISITOS_SKILLS, STATS_BASE_PES
from engine.calculos import calcular_ovr_supremo, processar_treino_master
from interface.visual import gerar_radar, desenhar_personalidade, exibir_laboratorio_skills

st.set_page_config(page_title="GOAT TV - CT SUPREMO", layout="wide", initial_sidebar_state="expanded")

if 'auth' not in st.session_state: st.session_state.auth = False

# --- TELA DE ACESSO ---
if not st.session_state.auth:
    st.markdown("<h1 style='text-align: center; color: #ffd700;'>🏟️ CT GOAT TV - VERSÃO ÔMEGA</h1>", unsafe_allow_html=True)
    id_user = st.text_input("ID ATLETA:").upper().strip()

    if st.button("🔍 ACESSAR REGISTROS", use_container_width=True):
        db = carregar_db()
        if id_user in db: 
            st.session_state.perfil, st.session_state.id_logado, st.session_state.auth = db[id_user], id_user, True
            st.rerun()
    
    # Lógica de Registro (Se ID não existir)
    if id_user and id_user not in carregar_db():
        with st.form("registro_atleta"):
            st.subheader("📝 Criar Novo Perfil")
            n = st.text_input("NOME COMPLETO:")
            i = st.number_input("IDADE:", 15, 45, 17)
            pos = st.selectbox("POSIÇÃO:", ["ATA", "MEI", "DEF", "GOL"])
            alt = st.number_input("ALTURA (m):", 1.5, 2.2, 1.78)
            peso = st.number_input("PESO (kg):", 50, 130, 75)
            ft = st.file_uploader("FOTO OFICIAL:", type=['jpg', 'png', 'jpeg'])

            if st.form_submit_button("🚀 INICIAR CARREIRA"):
                db = carregar_db()
                path = f"fotos_atletas/{id_user}.png"
                if ft: Image.open(ft).save(path)
                db[id_user] = {
                    "nome": n, "idade": i, "altura": alt, "peso": peso, "posicao": pos, 
                    "overall": 75, "foto": path, "status": "Saudável", "dna": "Iniciante",
                    "habilidades": [], "maestria": {m: 0.0 for m in REGRAS_TREINO.keys()},
                    "stats": {k: 75.0 for k in STATS_BASE_PES},
                    "personalidade": {"Altruísmo": 50, "Raça": 50, "Técnica": 50, "Compostura": 50},
                    "historico_ovr": [{"idade": i, "ovr": 75}]
                }
                salvar_db(db); st.rerun()

# --- ÁREA INTERNA ---
else:
    p = st.session_state.perfil

    # SIDEBAR
    with st.sidebar:
        st.markdown("<h2 style='text-align: center;'>📄 SCOUT CARD</h2>", unsafe_allow_html=True)
        if os.path.exists(p.get("foto", "")): st.image(p["foto"], use_container_width=True)
        st.metric("OVERALL", p["overall"])
        st.write(f"**DNA:** {p.get('dna', 'Padrão')}")
        st.write(f"**STATUS:** {p['status']}")
        if st.button("SAIR"): st.session_state.auth = False; st.rerun()

    # CORREÇÃO DO NOME NO TÍTULO
    nome_exibicao = p['nome'].split()[0] if p.get('nome') and p['nome'].strip() else "Atleta"
    st.title(f"Bem-vindo ao CT, {nome_exibicao}")

    tabs = st.tabs(["🎮 Campo de Treino", "🧠 Atleta", "📈 Evolução", "⚙️ Configurações"])

    with tabs[0]:
        st.subheader("Treinamento Tático")
        col_radar, col_menu = st.columns([1.5, 1])
        with col_radar: st.plotly_chart(gerar_radar(p["stats"]), use_container_width=True)
        with col_menu:
            if st.button("🛡️ DEFESA", use_container_width=True): st.session_state.portal = "DEF"
            if st.button("⚙️ MEIO", use_container_width=True): st.session_state.portal = "MEI"
            if st.button("🎯 ATAQUE", use_container_width=True): st.session_state.portal = "ATQ"

    with tabs[1]:
        desenhar_personalidade(p["personalidade"])

    with tabs[2]:
        df = pd.DataFrame(p.get("historico_ovr", []))
        if not df.empty:
            st.plotly_chart(px.line(df, x="idade", y="ovr"), use_container_width=True)

    with tabs[3]: # CONFIGURAÇÕES (REEDIÇÃO)
        st.subheader("⚙️ Central de Personalização")
        with st.form("edit_total"):
            new_n = st.text_input("Nome:", value=p["nome"])
            new_p = st.number_input("Peso:", value=p["peso"])
            new_a = st.number_input("Altura:", value=p["altura"])
            new_pos = st.selectbox("Posição:", ["ATA", "MEI", "DEF", "GOL"], index=["ATA", "MEI", "DEF", "GOL"].index(p["posicao"]))
            nova_ft = st.file_uploader("Trocar Foto:")

            if st.form_submit_button("💾 SALVAR ALTERAÇÕES"):
                db = carregar_db(); id_l = st.session_state.id_logado
                if nova_ft:
                    path = f"fotos_atletas/{id_l}.png"
                    Image.open(nova_ft).save(path)
                    db[id_l]["foto"] = path
                db[id_l].update({"nome": new_n, "peso": new_p, "altura": new_a, "posicao": new_pos})
                db[id_l]["overall"] = calcular_ovr_supremo(db[id_l])
                salvar_db(db); st.session_state.perfil = db[id_l]
                st.success("Perfil atualizado!")
                st.rerun()
