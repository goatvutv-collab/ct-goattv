# --- app.py ---
import streamlit as st
import sys, os, pandas as pd
from PIL import Image

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.db_handler import carregar_db, salvar_db
from engine.regras import REGRAS_TREINO, REQUISITOS_SKILLS, STATS_BASE_PES, STATS_NIVEL, REQUISITOS_ESTILOS
from engine.calculos import calcular_ovr_supremo, processar_treino_master
from interface.visual import gerar_radar, desenhar_personalidade, exibir_laboratorio_skills, definir_arquetipo_master

st.set_page_config(page_title="GOAT TV - CT SUPREMO 2021", layout="wide", initial_sidebar_state="expanded")

if 'auth' not in st.session_state: st.session_state.auth = False
if 'portal' not in st.session_state: st.session_state.portal = None

# --- LISTA DE 13 ARQUÉTIPOS (ESTILOS DE JOGO PES 2021) ---
ARQUETIPOS_PES = [
    "Nenhum", "Artilheiro", "Puxa-marcação", "Homem de Área", "Pivô", 
    "Armador Criativo", "Ponta Prolífico", "Ala Produtivo", "Clássico № 10", 
    "Infiltrado", "Área a Área", "Primeiro Volante", "Destruidor", "Lateral Ofensivo"
]

# --- ACESSO / REGISTRO ---
if not st.session_state.auth:
    st.markdown("<h1 style='text-align: center; color: #ffd700;'>🏟️ CT GOAT TV - VERSÃO PES 2021</h1>", unsafe_allow_html=True)
    id_user = st.text_input("ID ATLETA (Ex: GOAT-01):").upper().strip()

    if st.button("🔍 ACESSAR REGISTROS", use_container_width=True):
        db = carregar_db()
        if id_user in db: 
            st.session_state.perfil, st.session_state.id_logado, st.session_state.auth = db[id_user], id_user, True
            st.rerun()
        else:
            st.error("ID não encontrado. Preencha o contrato abaixo para estrear.")

    if id_user and id_user not in carregar_db():
        with st.form("registro"):
            st.subheader("📝 CONTRATO DE ESTREIA (NASCIMENTO FLAT 75)")
            col1, col2 = st.columns(2)
            with col1:
                n = st.text_input("NOME COMPLETO:")
                i = st.number_input("IDADE:", 15, 45, 17)
                pos = st.selectbox("POSIÇÃO PRINCIPAL:", ["CA", "SA", "MAT", "MLD", "MLE", "VOL", "ZC", "LD", "LE", "GOL"])
            with col2:
                dna_escolhido = st.selectbox("DNA / ESTILO DE JOGO INICIAL:", ARQUETIPOS_PES)
                alt = st.number_input("ALTURA (m):", 1.5, 2.2, 1.80)
                peso = st.number_input("PESO (kg):", 50, 130, 75)
            
            ft = st.file_uploader("FOTO DO ATLETA (Opcional):")
            
            if st.form_submit_button("🚀 INICIAR CARREIRA"):
                db = carregar_db()
                path = f"fotos_atletas/{id_user}.png"
                if ft: Image.open(ft).save(path)
                else: path = "fotos_atletas/default.png"
                
                # IMPLEMENTAÇÃO NASCIMENTO FLAT 75
                novo_atleta = {
                    "nome": n, "idade": i, "altura": alt, "peso": peso, "posicao": pos, 
                    "overall": 75, "foto": path, "status": "Saudável", 
                    "dna": dna_escolhido,       
                    "dna_origem": dna_escolhido, 
                    "habilidades": [],
                    "maestria": {m: 0.0 for m in REGRAS_TREINO.keys()},
                    "stats": {k: 75.0 for k in STATS_BASE_PES}, 
                    "stats_fixos": {k: 2 for k in STATS_NIVEL.keys()},
                    "personalidade": {"Raça": 50, "Técnica": 50, "Altruísmo": 50, "Compostura": 50},
                    "historico_ovr": [{"idade": i, "ovr": 75}], "posicoes": {pos: "A"}
                }
                
                novo_atleta["overall"] = calcular_ovr_supremo(novo_atleta)
                db[id_user] = novo_atleta
                
                salvar_db(db)
                st.success("Atleta registrado com sucesso! Clique em ACESSAR REGISTROS.")

# --- ÁREA INTERNA ---
else:
    p = st.session_state.perfil

    with st.sidebar:
        st.markdown(f"<h2 style='text-align: center;'>📄 SCOUT CARD</h2>", unsafe_allow_html=True)
        if os.path.exists(p.get("foto", "")): st.image(p["foto"], use_container_width=True)
        st.metric("OVERALL", p["overall"])

        arq_atual = definir_arquetipo_master(p, REQUISITOS_ESTILOS)
        st.write(f"**ARQUÉTIPO ATUAL:** {arq_atual}")
        st.write(f"**DNA ORIGEM:** {p.get('dna_origem', 'Nenhum')}")
        st.write(f"**STATUS:** {p['status']}")

        if p["status"] == "Lesionado":
            if st.button("🧊 TRATAMENTO MÉDICO"):
                p["status"] = "Saudável"; db = carregar_db(); db[st.session_state.id_logado] = p
                salvar_db(db); st.rerun()

        st.divider()
        st.subheader("🎒 Skills Ativas (PES 2021)")
        if p["habilidades"]:
            for s in p["habilidades"]: st.caption(f"✅ {s}")
        else: st.caption("Nenhuma")

        st.divider()
        if st.button("🚪 SAIR DO CT"): st.session_state.auth = False; st.rerun()

    nome_exibicao = p['nome'].split()[0] if p.get('nome') else "Atleta"
    st.title(f"Centro de Treinamento - {nome_exibicao}")
    tabs = st.tabs(["🎮 Campo de Treino", "🧠 Fisiologia", "📈 Evolução", "⚙️ Configurações"])

    with tabs[0]:
        if p["status"] == "Lesionado": 
            st.error("🚑 BLOQUEADO: Você está no Departamento Médico.")
        else:
            col_radar, col_menu = st.columns([1.5, 1])
            with col_radar: 
                st.plotly_chart(gerar_radar(p["stats"]), use_container_width=True)
            with col_menu:
                st.markdown("### Selecione o Setor")
                if st.button("🛡️ PORTAL DE DEFESA", use_container_width=True): st.session_state.portal = "DEF"
                if st.button("⚙️ PORTAL DE MEIO-CAMPO", use_container_width=True): st.session_state.portal = "MEI"
                if st.button("🎯 PORTAL DE ATAQUE", use_container_width=True): st.session_state.portal = "ATQ"
                st.divider()
                exibir_laboratorio_skills(p, REQUISITOS_SKILLS)

            # --- LÓGICA DE NAVEGAÇÃO DOS PORTAIS (FIXED PATHS) ---
            portal = st.session_state.get('portal')
            st.divider()
            
            if portal == "DEF": 
                from setores.defesa.portal import mostrar_sala_defesa
                mostrar_sala_defesa()
            elif portal == "MEI":
                from setores.meio_campo.portal import mostrar_sala_meio
                mostrar_sala_meio()
            elif portal == "ATQ":
                from setores.ataque.portal import mostrar_sala_ataque
                mostrar_sala_ataque()

    with tabs[1]:
        col_p, col_f = st.columns(2)
        with col_p:
            desenhar_personalidade(p["personalidade"])
        with col_f:
            st.subheader("📊 Índices Físicos PES")
            fixos = p.get("stats_fixos", {})
            st.write(f"**Pior Pé (Frequência):** {fixos.get('Pior pé frequência', 2)}")
            st.write(f"**Pior Pé (Precisão):** {fixos.get('Pior pé precisão', 2)}")
            st.write(f"**Condição Física:** {fixos.get('Condição física', 4)}")
            st.write(f"**Resistência a Lesão:** {fixos.get('Resistência a lesão', 2)}")

    with tabs[2]:
        st.subheader("Crescimento Profissional")
        df = pd.DataFrame(p.get("historico_ovr", []))
        if not df.empty:
            import plotly.express as px
            fig = px.line(df, x="idade", y="ovr", title="Curva de Evolução")
            st.plotly_chart(fig, use_container_width=True)

    with tabs[3]:
        st.subheader("⚙️ Gerenciar Contrato")
        with st.form("edit"):
            new_n = st.text_input("Nome:", value=p["nome"])
            new_pos = st.selectbox("Posição Principal:", ["CA", "SA", "MAT", "MLD", "MLE", "VOL", "ZC", "LD", "LE", "GOL"])
            new_a = st.number_input("Altura:", value=p["altura"])
            new_p = st.number_input("Peso:", value=p["peso"])
            if st.form_submit_button("💾 SALVAR ALTERAÇÕES"):
                db = carregar_db(); id_l = st.session_state.id_logado
                db[id_l].update({"nome": new_n, "posicao": new_pos, "altura": new_a, "peso": new_p})
                db[id_l]["overall"] = calcular_ovr_supremo(db[id_l])
                salvar_db(db); st.session_state.perfil = db[id_l]; st.rerun()
