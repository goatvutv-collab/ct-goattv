# --- app.py ---
import streamlit as st
import os, sys
from PIL import Image
from database.db_handler import carregar_db, salvar_db, gerenciar_foto_antiga
from engine.regras import STATS_BASE_PES, STATS_NIVEL, REGRAS_TREINO, REQUISITOS_ESTILOS, REQUISITOS_SKILLS
from engine.calculos import calcular_ovr_supremo

st.set_page_config(page_title="GOAT TV - CT SUPREMO", layout="wide")

if 'auth' not in st.session_state: st.session_state.auth = False

# REGISTRO COM FLAT 75 PONDERADO
if not st.session_state.auth:
    st.title("🏟️ REGISTRO GOAT TV")
    id_user = st.text_input("ID:").upper()
    
    if st.button("ACESSAR"):
        db = carregar_db()
        if id_user in db:
            st.session_state.perfil, st.session_state.id_logado, st.session_state.auth = db[id_user], id_user, True
            st.rerun()

    if id_user and id_user not in carregar_db():
        with st.form("registro"):
            col1, col2 = st.columns(2)
            with col1:
                n = st.text_input("NOME:")
                i = st.number_input("IDADE:", 15, 45, 17)
                pos = st.selectbox("POSIÇÃO:", ["CA", "SA", "MAT", "VOL", "ZC", "LD", "LE", "GOL"])
            with col2:
                dna = st.selectbox("DNA (ARQUÉTIPO):", ["Nenhum"] + list(REGRAS_TREINO.keys()))
                alt = st.number_input("ALTURA:", 1.5, 2.2, 1.80)
                peso = st.number_input("PESO:", 50, 120, 75)
            
            ft = st.file_uploader("FOTO:")
            if st.form_submit_button("CRIAR ATLETA"):
                db = carregar_db()
                path = f"fotos_atletas/{id_user}.png" if ft else "fotos_atletas/default.png"
                if ft: Image.open(ft).save(path)
                
                # O Atleta nasce 75, mas a distribuição depende do Arquétipo e Posição
                atleta = {
                    "nome": n, "idade": i, "altura": alt, "peso": peso, "posicao": pos,
                    "dna": dna, "foto": path, "status": "Saudável",
                    "stats": {s: 75.0 for s in STATS_BASE_PES},
                    "stats_fixos": {"Forma física": 4, "Resistência a lesão": 2, "Pior pé frequência": 2, "Pior pé precisão": 2}
                }
                atleta["overall"] = calcular_ovr_supremo(atleta)
                db[id_user] = atleta
                salvar_db(db); st.rerun()

else:
    p = st.session_state.perfil
    tabs = st.tabs(["🎮 Treino", "🧠 Atleta", "⚙️ Configurações"])

    with tabs[2]: # CONFIGURAÇÕES COM TROCA DE FOTO E DELETE
        st.subheader("⚙️ AJUSTES DE PERFIL")
        with st.form("edit"):
            new_nome = st.text_input("Nome:", value=p["nome"])
            nova_ft = st.file_uploader("Trocar Foto (Deleta a anterior):")
            if st.form_submit_button("SALVAR"):
                db = carregar_db()
                if nova_ft:
                    gerenciar_foto_antiga(p["foto"]) # LIMPEZA DE MEMÓRIA
                    path = f"fotos_atletas/{st.session_state.id_logado}.png"
                    Image.open(nova_ft).save(path)
                    db[st.session_state.id_logado]["foto"] = path
                db[st.session_state.id_logado]["nome"] = new_nome
                salvar_db(db); st.session_state.perfil = db[st.session_state.id_logado]; st.rerun()
