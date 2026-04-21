# --- app.py ---
import streamlit as st
import os, sys
from PIL import Image
from database.db_handler import carregar_db, salvar_db, gerenciar_foto_antiga
from engine.regras import STATS_BASE_PES, STATS_NIVEL, REGRAS_TREINO, REQUISITOS_ESTILOS, REQUISITOS_SKILLS
from engine.calculos import calcular_ovr_supremo
from interface.visual import gerar_radar, desenhar_personalidade, definir_estilo_exibicao

st.set_page_config(page_title="GOAT TV - CT SUPREMO", layout="wide")

if 'auth' not in st.session_state: st.session_state.auth = False
if 'portal' not in st.session_state: st.session_state.portal = None

# SISTEMA DE LOGIN E REGISTRO
if not st.session_state.auth:
    st.title("🏟️ CT GOAT TV 2021")
    id_user = st.text_input("ID ATLETA:").upper().strip()
    
    if st.button("ENTRAR"):
        db = carregar_db()
        if id_user in db:
            st.session_state.perfil, st.session_state.id_logado, st.session_state.auth = db[id_user], id_user, True
            st.rerun()

    if id_user and id_user not in carregar_db():
        with st.form("registro"):
            st.subheader("📝 CONTRATO DE ESTREIA (FLAT 75 PONDERADO)")
            col1, col2 = st.columns(2)
            with col1:
                n = st.text_input("NOME:"); i = st.number_input("IDADE:", 15, 45, 17)
                pos = st.selectbox("POSIÇÃO:", ["CA", "SA", "MAT", "VOL", "ZC", "LD", "LE", "GOL"])
            with col2:
                dna = st.selectbox("DNA (ARQUÉTIPO INICIAL):", ["Nenhum"] + list(REGRAS_TREINO.keys()))
                alt = st.number_input("ALTURA:", 1.5, 2.2, 1.80)
                peso = st.number_input("PESO:", 50, 120, 75)
            
            ft = st.file_uploader("FOTO:")
            if st.form_submit_button("INICIAR CARREIRA"):
                db = carregar_db()
                path = f"fotos_atletas/{id_user}.png" if ft else "fotos_atletas/default.png"
                if ft: Image.open(ft).save(path)
                
                # NASCIMENTO: Atributos 75, mas a nota geral depende da posição
                atleta = {
                    "nome": n, "idade": i, "altura": alt, "peso": peso, "posicao": pos,
                    "dna": dna, "foto": path, "status": "Saudável",
                    "stats": {s: 75.0 for s in STATS_BASE_PES},
                    "maestria": {m: 0.0 for m in REGRAS_TREINO.keys()},
                    "personalidade": {"Raça": 50, "Técnica": 50, "Altruísmo": 50, "Compostura": 50},
                    "stats_fixos": {"Forma física": 4, "Resistência a lesão": 2}
                }
                atleta["overall"] = calcular_ovr_supremo(atleta)
                db[id_user] = atleta; salvar_db(db); st.rerun()

else:
    p = st.session_state.perfil
    with st.sidebar:
        st.image(p["foto"])
        st.metric("OVERALL", p["overall"])
        st.write(f"**ESTILO:** {definir_estilo_exibicao(p, REQUISITOS_ESTILOS)}")
        st.write(f"**DNA (ARQUÉTIPO):** {p['dna']}")
        if st.button("SAIR"): st.session_state.auth = False; st.rerun()

    tabs = st.tabs(["🎮 Campo de Treino", "🧠 Atleta", "⚙️ Ajustes de Perfil"])

    with tabs[0]: # PORTAIS MODULARES
        c1, c2 = st.columns([1.5, 1])
        with c1: st.plotly_chart(gerar_radar(p["stats"]))
        with c2:
            if st.button("🛡️ DEFESA", use_container_width=True): st.session_state.portal = "DEF"
            if st.button("⚙️ MEIO-CAMPO", use_container_width=True): st.session_state.portal = "MEI"
            if st.button("🎯 ATAQUE", use_container_width=True): st.session_state.portal = "ATQ"
        
        st.divider()
        portal = st.session_state.portal
        if portal == "DEF":
            from setores.defesa.portal import mostrar_sala_defesa
            mostrar_sala_defesa()
        elif portal == "MEI":
            from setores.meio_campo.portal import mostrar_sala_meio
            mostrar_sala_meio()
        elif portal == "ATQ":
            from setores.ataque.portal import mostrar_sala_ataque
            mostrar_sala_ataque()

    with tabs[2]: # AJUSTES E TROCA DE FOTO
        with st.form("ajustes"):
            new_nome = st.text_input("Novo Nome:", value=p["nome"])
            nova_ft = st.file_uploader("Trocar Foto (A anterior será deletada):")
            if st.form_submit_button("SALVAR ALTERAÇÕES"):
                db = carregar_db()
                if nova_ft:
                    gerenciar_foto_antiga(p["foto"]) # Lógica de deleção
                    path = f"fotos_atletas/{st.session_state.id_logado}.png"
                    Image.open(nova_ft).save(path); db[st.session_state.id_logado]["foto"] = path
                db[st.session_state.id_logado]["nome"] = new_nome
                salvar_db(db); st.rerun()
