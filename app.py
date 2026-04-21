# --- app.py ---
import streamlit as st
import os, sys, pandas as pd
from PIL import Image
from datetime import date

# Garante que o Python encontre os módulos locais
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.db_handler import carregar_db, salvar_db, gerenciar_foto_antiga
from engine.regras import STATS_BASE_PES, STATS_NIVEL, REGRAS_TREINO, REQUISITOS_ESTILOS, REQUISITOS_SKILLS
from engine.calculos import calcular_ovr_supremo, distribuir_stats_iniciais, calcular_idade
from interface.visual import gerar_radar, desenhar_personalidade, exibir_laboratorio_skills, definir_arquetipo_master

# Configuração de Página Única
st.set_page_config(page_title="GOAT TV - CT SUPREMO 2021", layout="wide", initial_sidebar_state="expanded")

if 'auth' not in st.session_state: st.session_state.auth = False
if 'portal' not in st.session_state: st.session_state.portal = None

# --- FLUXO DE ACESSO E REGISTRO ---
if not st.session_state.auth:
    st.markdown("<h1 style='text-align: center; color: #ffd700;'>🏟️ CT GOAT TV - VERSÃO PES 2021</h1>", unsafe_allow_html=True)
    
    col_log, col_reg = st.columns([1, 1.5])
    
    with col_log:
        st.subheader("🔍 Acessar Registro")
        id_user = st.text_input("ID ATLETA (Ex: GOAT-01):").upper().strip()
        if st.button("ENTRAR NO CT", use_container_width=True):
            db = carregar_db()
            if id_user in db:
                st.session_state.perfil, st.session_state.id_logado, st.session_state.auth = db[id_user], id_user, True
                st.rerun()
            else:
                st.error("ID não encontrado no banco de dados.")

    with col_reg:
        if id_user and id_user not in carregar_db():
            with st.form("registro_goat"):
                st.subheader("📝 Contrato de Estreia (Nascimento Flat 75)")
                c1, c2 = st.columns(2)
                with c1:
                    nome = st.text_input("NOME COMPLETO:")
                    nasc = st.date_input("DATA DE NASCIMENTO:", value=date(2005, 1, 1), min_value=date(1980, 1, 1), max_value=date(2012, 12, 31))
                    pos = st.selectbox("POSIÇÃO:", ["CA", "SA", "MAT", "VOL", "ZC", "LD", "LE", "GOL"])
                with c2:
                    dna_ini = st.selectbox("DNA (ARQUÉTIPO INICIAL):", list(REGRAS_TREINO.keys()))
                    alt = st.number_input("ALTURA (m):", 1.50, 2.20, 1.80)
                    peso = st.number_input("PESO (kg):", 50, 130, 75)
                
                ft = st.file_uploader("FOTO DO PERFIL:")
                
                if st.form_submit_button("🚀 INICIAR CARREIRA"):
                    db = carregar_db()
                    path = f"fotos_atletas/{id_user}.png" if ft else "fotos_atletas/default.png"
                    if ft: Image.open(ft).save(path)
                    
                    # Cálculo de Idade Real via Calendário
                    idade_atleta = calcular_idade(nasc)
                    
                    # Construção do Atleta (Nascimento Ponderado)
                    atleta = {
                        "nome": nome, "nascimento": nasc.strftime("%Y-%m-%d"), "idade": idade_atleta,
                        "altura": alt, "peso": peso, "posicao": pos, "dna": dna_ini, "dna_origem": dna_ini,
                        "foto": path, "status": "Saudável", "habilidades": [],
                        "stats": distribuir_stats_iniciais(dna_ini),
                        "maestria": {m: 0.0 for m in REGRAS_TREINO.keys()},
                        "personalidade": {"Raça": 50, "Técnica": 50, "Altruísmo": 50, "Compostura": 50},
                        "stats_fixos": {"Forma física": 4, "Resistência a lesão": 2, "Pior pé frequência": 2, "Pior pé precisão": 2},
                        "historico_ovr": [{"idade": idade_atleta, "ovr": 75}]
                    }
                    
                    atleta["overall"] = calcular_ovr_supremo(atleta)
                    db[id_user] = atleta
                    salvar_db(db)
                    st.success("Contrato assinado! Clique em ENTRAR.")
                    st.rerun()

# --- ÁREA LOGADA (INTERNA) ---
else:
    p = st.session_state.perfil
    id_log = st.session_state.id_logado

    # === SIDEBAR: SCOUT CARD (O RG DO ATLETA) ===
    with st.sidebar:
        st.markdown(f"<h2 style='text-align: center; color: #ffd700;'>{p['nome'].split()[0]}</h2>", unsafe_allow_html=True)
        if os.path.exists(p["foto"]): st.image(p["foto"], use_container_width=True)
        
        st.metric("OVERALL", p["overall"])
        st.divider()
        
        st.write(f"**🧬 DNA ATUAL:** {p['dna']}")
        st.write(f"**🏆 ARQUÉTIPO:** {definir_arquetipo_master(p, REQUISITOS_ESTILOS)}")
        st.write(f"**🎂 IDADE:** {p['idade']} anos")
        
        status_emoji = "🟢" if p["status"] == "Saudável" else "🔴"
        st.write(f"**🏥 STATUS:** {status_emoji} {p['status']}")
        
        if p["status"] == "Lesionado":
            if st.button("🧊 TRATAMENTO MÉDICO"):
                p["status"] = "Saudável"
                db = carregar_db(); db[id_log] = p; salvar_db(db); st.rerun()
        
        st.divider()
        st.subheader("🎒 Skills Ativas")
        if p["habilidades"]:
            for sk in p["habilidades"]: st.caption(f"✅ {sk}")
        else: st.caption("Nenhuma skill desbloqueada.")
        
        st.divider()
        if st.button("🚪 SAIR DO CT", use_container_width=True):
            st.session_state.auth = False; st.rerun()

    # --- PAINEL PRINCIPAL ---
    st.title(f"Centro de Treinamento - {p['nome']}")
    tabs = st.tabs(["🎮 Campo de Treino", "🧠 Atleta", "📈 Evolução", "⚙️ Configurações"])

    with tabs[0]: # TREINAMENTO E PORTAIS
        if p["status"] == "Lesionado":
            st.error("🚑 BLOQUEADO: Você está no Departamento Médico.")
        else:
            col_radar, col_menu = st.columns([1.5, 1])
            with col_radar:
                st.plotly_chart(gerar_radar(p["stats"]), use_container_width=True)
            with col_menu:
                st.markdown("### Selecione o Portal")
                if st.button("🛡️ DEFESA", use_container_width=True): st.session_state.portal = "DEF"
                if st.button("⚙️ MEIO-CAMPO", use_container_width=True): st.session_state.portal = "MEI"
                if st.button("🎯 ATAQUE", use_container_width=True): st.session_state.portal = "ATQ"
                st.divider()
                exibir_laboratorio_skills(p, REQUISITOS_SKILLS)

            # Lógica de Navegação Modular
            st.divider()
            portal = st.session_state.get('portal')
            if portal == "DEF":
                from setores.defesa.portal import mostrar_sala_defesa
                mostrar_sala_defesa()
            elif portal == "MEI":
                from setores.meio_campo.portal import mostrar_sala_meio
                mostrar_sala_meio()
            elif portal == "ATQ":
                from setores.ataque.portal import mostrar_sala_ataque
                mostrar_sala_ataque()

    with tabs[1]: # ABA ATLETA (FISIOLOGIA E MENTALIDADE)
        col_m, col_f = st.columns(2)
        with col_m:
            desenhar_personalidade(p["personalidade"])
        with col_f:
            st.markdown("### 🧬 Fisiologia PES")
            fixos = p.get("stats_fixos", {})
            st.write(f"**Pior Pé (Frequência):** {fixos.get('Pior pé frequência', 2)}/4")
            st.write(f"**Pior Pé (Precisão):** {fixos.get('Pior pé precisão', 2)}/4")
            st.write(f"**Forma Física:** {fixos.get('Forma física', 4)}/8")
            st.write(f"**Resistência a Lesão:** {fixos.get('Resistência a lesão', 2)}/3")

    with tabs[2]: # GRÁFICO DE CRESCIMENTO
        st.subheader("📈 Curva de Evolução Profissional")
        df = pd.DataFrame(p.get("historico_ovr", []))
        if not df.empty:
            import plotly.express as px
            fig = px.line(df, x="idade", y="ovr", markers=True, title="Desenvolvimento de Overall")
            fig.update_traces(line_color='#ffd700')
            st.plotly_chart(fig, use_container_width=True)

    with tabs[3]: # AJUSTES E TROCA DE FOTO
        st.subheader("⚙️ Gerenciar Contrato")
        with st.form("edicao_perfil"):
            new_nome = st.text_input("Alterar Nome:", value=p["nome"])
            new_pos = st.selectbox("Alterar Posição:", ["CA", "SA", "MAT", "VOL", "ZC", "LD", "LE", "GOL"], 
                                   index=["CA", "SA", "MAT", "VOL", "ZC", "LD", "LE", "GOL"].index(p["posicao"]))
            nova_ft = st.file_uploader("Trocar Foto (Deleta a anterior):")
            
            if st.form_submit_button("💾 SALVAR ALTERAÇÕES"):
                db = carregar_db()
                if nova_ft:
                    gerenciar_foto_antiga(p["foto"]) # Limpa o lixo
                    path = f"fotos_atletas/{id_log}.png"
                    Image.open(nova_ft).save(path)
                    db[id_log]["foto"] = path
                
                db[id_log]["nome"] = new_nome
                db[id_log]["posicao"] = new_pos
                db[id_log]["overall"] = calcular_ovr_supremo(db[id_log]) # Recalcula OVR se mudou a posição
                
                salvar_db(db)
                st.session_state.perfil = db[id_log]
                st.success("Perfil atualizado com sucesso!")
                st.rerun()
