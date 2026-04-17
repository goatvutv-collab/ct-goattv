# --- app.py ---
import streamlit as st
import sys, os, pd, plotly.express as px
from PIL import Image

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.db_handler import carregar_db, salvar_db
from engine.regras import REGRAS_TREINO, REQUISITOS_SKILLS, STATS_BASE_PES, STATS_NIVEL
from engine.calculos import calcular_ovr_supremo, processar_treino_master
from interface.visual import gerar_radar, desenhar_personalidade, exibir_laboratorio_skills

st.set_page_config(page_title="GOAT TV - CT SUPREMO", layout="wide", initial_sidebar_state="expanded")

if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    # --- TELA DE ACESSO ---
    st.markdown("<h1 style='text-align: center; color: #ffd700;'>🏟️ CT GOAT TV - VERSÃO ÔMEGA</h1>", unsafe_allow_html=True)
    id_user = st.text_input("ID ATLETA:").upper().strip()

    if st.button("🔍 ACESSAR REGISTROS", use_container_width=True):
        db = carregar_db()
        if id_user in db: 
            st.session_state.perfil, st.session_state.id_logado, st.session_state.auth = db[id_user], id_user, True
            st.rerun()

    if id_user and id_user not in carregar_db():
        with st.form("registro_atleta"):
            st.subheader("📝 CONTRATO DE ESTREIA")
            nome = st.text_input("NOME COMPLETO:")
            idade = st.number_input("IDADE:", 15, 45, 17)
            pos = st.selectbox("POSIÇÃO:", ["CA", "SA", "MAT", "MLD", "MLE", "VOL", "ZC", "LD", "LE", "GOL"])
            alt = st.number_input("ALTURA (m):", 1.5, 2.2, 1.80)
            peso = st.number_input("PESO (kg):", 50, 130, 75)
            ft = st.file_uploader("FOTO:", type=['jpg', 'png', 'jpeg'])

            if st.form_submit_button("🚀 INICIAR CARREIRA"):
                db = carregar_db()
                path = f"fotos_atletas/{id_user}.png"
                if ft: Image.open(ft).save(path)
                db[id_user] = {
                    "nome": nome, "idade": idade, "altura": alt, "peso": peso, "posicao": pos, 
                    "overall": 75, "foto": path, "status": "Saudável", "dna": "Iniciante",
                    "habilidades": [], "maestria": {m: 0.0 for m in REGRAS_TREINO.keys()},
                    "stats": {k: 75.0 for k in STATS_BASE_PES},
                    "stats_fixos": {k: 2 for k in STATS_NIVEL.keys()},
                    "personalidade": {"Altruísmo": 50, "Raça": 50, "Técnica": 50, "Compostura": 50},
                    "historico_ovr": [{"idade": idade, "ovr": 75}]
                }
                salvar_db(db); st.rerun()

else:
    p = st.session_state.perfil
    # --- SIDEBAR COMPLETA ---
    with st.sidebar:
        st.markdown("<h2 style='text-align: center;'>📄 SCOUT CARD</h2>", unsafe_allow_html=True)
        if os.path.exists(p.get("foto", "")): st.image(p["foto"], use_container_width=True)
        st.metric("OVERALL", p["overall"])
        st.write(f"**DNA:** {p.get('dna', 'Padrão')}")
        st.write(f"**STATUS:** {p['status']}")
        
        st.divider()
        st.subheader("🎒 Habilidades (Max 10)")
        st.write(" • " + "\n • ".join(p["habilidades"]) if p["habilidades"] else "Nenhuma")

        st.divider()
        st.subheader("📊 Maestrias")
        for m, val in p["maestria"].items():
            if val > 0:
                st.caption(f"{m}: {val:.1f}%"); st.progress(val/100)
        
        if st.button("SAIR"): st.session_state.auth = False; st.rerun()

    # --- ÁREA CENTRAL ---
    nome_exibicao = p['nome'].split()[0] if p.get('nome') and p['nome'].strip() else "Atleta"
    st.title(f"Bem-vindo ao CT, {nome_exibicao}")

    tabs = st.tabs(["🎮 Campo de Treino", "🧠 Atleta", "📈 Evolução", "⚙️ Configurações"])

    with tabs[0]:
        col_radar, col_menu = st.columns([1.5, 1])
        with col_radar: st.plotly_chart(gerar_radar(p["stats"]), use_container_width=True)
        with col_menu:
            if st.button("🛡️ DEFESA", use_container_width=True): st.session_state.portal = "DEF"
            if st.button("⚙️ MEIO", use_container_width=True): st.session_state.portal = "MEI"
            if st.button("🎯 ATAQUE", use_container_width=True): st.session_state.portal = "ATQ"
            st.divider()
            exibir_laboratorio_skills(p, REQUISITOS_SKILLS)

    with tabs[1]:
        desenhar_personalidade(p["personalidade"])
        st.divider()
        st.subheader("📉 Condição PES")
        c1, c2, c3, c4 = st.columns(4)
        fixos = p.get("stats_fixos", {})
        c1.metric("Pior Pé (F)", fixos.get("Pior pé frequência", 2))
        c2.metric("Pior Pé (P)", fixos.get("Pior pé precisão", 2))
        c3.metric("Condição", fixos.get("Condição física", 4))
        c4.metric("Res. Lesão", fixos.get("Resistência a lesão", 2))

    with tabs[2]:
        df = pd.DataFrame(p.get("historico_ovr", []))
        if not df.empty: st.plotly_chart(px.line(df, x="idade", y="ovr"), use_container_width=True)

    with tabs[3]: # CONFIGURAÇÕES
        st.subheader("⚙️ Editar Perfil")
        with st.form("edit_total"):
            new_n = st.text_input("Nome:", value=p["nome"])
            new_pos = st.selectbox("Posição:", ["CA", "SA", "MAT", "MLD", "MLE", "VOL", "ZC", "LD", "LE", "GOL"], 
                                   index=["CA", "SA", "MAT", "MLD", "MLE", "VOL", "ZC", "LD", "LE", "GOL"].index(p["posicao"]))
            new_a = st.number_input("Altura:", value=p["altura"])
            new_p = st.number_input("Peso:", value=p["peso"])
            nova_ft = st.file_uploader("Trocar Foto:")

            if st.form_submit_button("💾 SALVAR"):
                db = carregar_db(); id_l = st.session_state.id_logado
                if nova_ft:
                    path = f"fotos_atletas/{id_l}.png"
                    Image.open(nova_ft).save(path); db[id_l]["foto"] = path
                db[id_l].update({"nome": new_n, "posicao": new_pos, "altura": new_a, "peso": new_p})
                db[id_l]["overall"] = calcular_ovr_supremo(db[id_l])
                salvar_db(db); st.session_state.perfil = db[id_l]; st.rerun()
