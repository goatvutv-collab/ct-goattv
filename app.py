# --- app.py ---
import streamlit as st
import os, sys, pandas as pd
from PIL import Image
from datetime import date

# Garante que o Python encontre os módulos locais
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# --- MUDANÇA AQUI: IMPORTANDO O NOVO HANDLER DO SUPABASE ---
from database.db_handler import (
    carregar_todos_jogadores, 
    buscar_atleta, 
    salvar_evolucao_treino, 
    registrar_novo_atleta
)
# Mantendo os outros motores intactos
from engine.regras import STATS_BASE_PES, STATS_NIVEL, REGRAS_TREINO, REQUISITOS_ESTILOS, REQUISITOS_SKILLS
from engine.calculos import calcular_ovr_supremo, distribuir_stats_iniciais, calcular_idade
from interface.visual import gerar_radar, desenhar_personalidade, exibir_laboratorio_skills, definir_arquetipo_master

# Configuração de Página Única
st.set_page_config(page_title="GOAT TV - CT SUPREMO 2021", layout="wide", initial_sidebar_state="expanded")

if 'auth' not in st.session_state: st.session_state.auth = False
if 'portal' not in st.session_state: st.session_state.portal = None
if 'jogadores' not in st.session_state: st.session_state.jogadores = {}

# --- FLUXO DE ACESSO E REGISTRO ---
if not st.session_state.auth:
    st.markdown("<h1 style='text-align: center; color: #ffd700;'>🏟️ CT GOAT TV - VERSÃO PES 2021</h1>", unsafe_allow_html=True)
    
    col_log, col_reg = st.columns([1, 1.5])
    
    with col_log:
        st.subheader("🔍 Acessar Registro")
        id_user = st.text_input("ID ATLETA (Ex: GOAT-01):").upper().strip()
        if st.button("ENTRAR NO CT", use_container_width=True):
            # BUSCA NO SUPABASE EM VEZ DO JSON
            atleta_encontrado = buscar_atleta(id_user)
            if atleta_encontrado:
                st.session_state.perfil = atleta_encontrado
                st.session_state.id_logado = id_user
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("ID não encontrado no banco de dados da Goat TV.")

    with col_reg:
        # Checa se o ID já existe no banco de dados global
        if id_user and not buscar_atleta(id_user):
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
                    path = f"fotos_atletas/{id_user}.png" if ft else "fotos_atletas/default.png"
                    if ft: Image.open(ft).save(path)
                    
                    idade_atleta = calcular_idade(nasc)
                    
                    # Construção do Atleta para o Supabase
                    atleta = {
                        "nome": id_user, # ID Único para o banco
                        "nome_completo": nome,
                        "nascimento": nasc.strftime("%Y-%m-%d"), 
                        "idade": idade_atleta,
                        "altura": alt, 
                        "peso": peso, 
                        "posicao": pos, 
                        "dna": dna_ini, 
                        "dna_origem": dna_ini,
                        "foto": path, 
                        "status": "Saudável", 
                        "habilidades": [],
                        "stats": distribuir_stats_iniciais(dna_ini),
                        "maestria": {m: 0.0 for m in REGRAS_TREINO.keys()},
                        "personalidade": {"Raça": 50, "Técnica": 50, "Altruísmo": 50, "Compostura": 50},
                        "stats_fixos": {"Forma física": 4, "Resistência a lesão": 2, "Pior pé frequência": 2, "Pior pé precisão": 2},
                        "historico_ovr": [{"idade": idade_atleta, "ovr": 75}],
                        "overall": 75.0
                    }
                    
                    # Cálculo de Overall antes de salvar
                    atleta["overall"] = calcular_ovr_supremo(atleta)
                    
                    # SALVA NO SUPABASE
                    if registrar_novo_atleta(atleta):
                        st.success("Contrato assinado e gravado na nuvem! Clique em ENTRAR.")
                        st.rerun()

# --- ÁREA LOGADA (INTERNA) ---
else:
    # Sempre busca a versão mais recente do banco para evitar amnésia
    p = buscar_atleta(st.session_state.id_logado)
    id_log = st.session_state.id_logado

    # === SIDEBAR: SCOUT CARD ===
    with st.sidebar:
        # Pega o primeiro nome do nome completo gravado
        nome_exibicao = p.get("nome_completo", p["nome"]).split()[0]
        st.markdown(f"<h2 style='text-align: center; color: #ffd700;'>{nome_exibicao}</h2>", unsafe_allow_html=True)
        
        if os.path.exists(p["foto"]): 
            st.image(p["foto"], use_container_width=True)
        
        st.metric("OVERALL", p["overall"])
        st.divider()
        
        st.write(f"**🧬 DNA ATUAL:** {p['dna']}")
        st.write(f"**🏆 ARQUÉTIPO:** {definir_arquetipo_master(p, REQUISITOS_ESTILOS)}")
        st.write(f"**🎂 IDADE:** {p['idade']} anos")
        
        status_emoji = "🟢" if p["status"] == "Saudável" else "🔴"
        st.write(f"**🏥 STATUS:** {status_emoji} {p['status']}")
        
        if p["status"] == "Lesionado":
            if st.button("🧊 TRATAMENTO MÉDICO"):
                # Atualiza no banco
                salvar_evolucao_treino(id_log, {"status": "Saudável"})
                st.rerun()
        
        st.divider()
        st.subheader("🎒 Skills Ativas")
        if p["habilidades"]:
            for sk in p["habilidades"]: st.caption(f"✅ {sk}")
        else: st.caption("Nenhuma skill desbloqueada.")
        
        st.divider()
        if st.button("🚪 SAIR DO CT", use_container_width=True):
            st.session_state.auth = False
            st.rerun()

    # --- PAINEL PRINCIPAL ---
    st.title(f"Centro de Treinamento - {p.get('nome_completo', p['nome'])}")
    tabs = st.tabs(["🎮 Campo de Treino", "🧠 Atleta", "📈 Evolução", "⚙️ Configurações"])

    with tabs[0]: # TREINAMENTO
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

    with tabs[1]: # ABA ATLETA
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

    with tabs[2]: # CRESCIMENTO
        st.subheader("📈 Curva de Evolução Profissional")
        df = pd.DataFrame(p.get("historico_ovr", []))
        if not df.empty:
            import plotly.express as px
            fig = px.line(df, x="idade", y="ovr", markers=True, title="Desenvolvimento de Overall")
            fig.update_traces(line_color='#ffd700')
            st.plotly_chart(fig, use_container_width=True)

    with tabs[3]: # AJUSTES
        st.subheader("⚙️ Gerenciar Contrato")
        with st.form("edicao_perfil"):
            new_nome_c = st.text_input("Alterar Nome Completo:", value=p.get("nome_completo", p["nome"]))
            new_pos = st.selectbox("Alterar Posição:", ["CA", "SA", "MAT", "VOL", "ZC", "LD", "LE", "GOL"], 
                                   index=["CA", "SA", "MAT", "VOL", "ZC", "LD", "LE", "GOL"].index(p["posicao"]))
            nova_ft = st.file_uploader("Trocar Foto:")
            
            if st.form_submit_button("💾 SALVAR ALTERAÇÕES NO SUPABASE"):
                # Prepara dicionário de mudanças
                mudancas = {
                    "nome_completo": new_nome_c,
                    "posicao": new_pos
                }
                
                if nova_ft:
                    # Lógica de foto local mantida como você pediu
                    path = f"fotos_atletas/{id_log}.png"
                    Image.open(nova_ft).save(path)
                    mudancas["foto"] = path
                
                # Recalcula OVR baseado no estado atual para salvar no banco
                p_temp = p.copy()
                p_temp.update(mudancas)
                mudancas["overall"] = calcular_ovr_supremo(p_temp)
                
                # GRAVA NO SUPABASE
                if salvar_evolucao_treino(id_log, mudancas):
                    st.success("Dados sincronizados com a nuvem!")
                    st.rerun()
