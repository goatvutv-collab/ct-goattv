# --- app.py ---
import streamlit as st
import os, sys, pandas as pd
from PIL import Image
from datetime import date

# Injeção de dependências do sistema para garantir caminhos relativos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# --- INTEGRAÇÃO COM O MOTOR DE DADOS SUPREMO (SUPABASE) ---
from database.db_handler import (
    carregar_todos_jogadores, 
    buscar_atleta, 
    salvar_evolucao_treino, 
    registrar_novo_atleta
)
from engine.regras import STATS_BASE_PES, STATS_NIVEL, REGRAS_TREINO, REQUISITOS_ESTILOS, REQUISITOS_SKILLS
from engine.calculos import calcular_ovr_supremo, distribuir_stats_iniciais, calcular_idade
from interface.visual import gerar_radar, desenhar_personalidade, exibir_laboratorio_skills, definir_arquetipo_master

# Configurações de Elite da Engine
st.set_page_config(
    page_title="GOAT TV - CT SUPREMO 2021", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Constantes de Tática da Federação
LISTA_POSICOES_SUPREMAS = ["CA", "SA", "PTD", "PTE", "MAT", "VOL", "ZC", "LD", "LE", "GOL"]

# Inicialização de Variáveis de Persistência em Sessão
if 'auth' not in st.session_state: st.session_state.auth = False
if 'portal' not in st.session_state: st.session_state.portal = None
if 'perfil' not in st.session_state: st.session_state.perfil = None

# --- NÚCLEO DE AUTENTICAÇÃO E REGISTRO DE CONTRATOS ---
if not st.session_state.auth:
    st.markdown("<h1 style='text-align: center; color: #ffd700;'>🏟️ CT GOAT TV - VERSÃO PES 2021</h1>", unsafe_allow_html=True)
    
    col_log, col_reg = st.columns([1, 1.5])
    
    with col_log:
        st.subheader("🔍 Acessar Registro")
        id_user = st.text_input("ID ATLETA (Ex: GOAT-01):").upper().strip()
        if st.button("ENTRAR NO CT", use_container_width=True):
            # Query Complexa no Supabase via Handler (Busca e Reconstrução de Stats)
            atleta_encontrado = buscar_atleta(id_user)
            if atleta_encontrado:
                st.session_state.perfil = atleta_encontrado
                st.session_state.id_logado = id_user
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("ID não localizado na Federação Goat TV. Verifique a grafia.")

    with col_reg:
        # Lógica de Verificação de Existência em Tempo Real no Banco
        if id_user and not buscar_atleta(id_user):
            with st.form("registro_goat_complexo"):
                st.subheader("📝 Contrato de Estreia (Nascimento Flat 75)")
                c1, c2 = st.columns(2)
                with c1:
                    nome_atleta = st.text_input("NOME COMPLETO:")
                    nasc = st.date_input("DATA DE NASCIMENTO:", value=date(2005, 1, 1), min_value=date(1980, 1, 1), max_value=date(2012, 12, 31))
                    pos = st.selectbox("POSIÇÃO DE ELITE:", LISTA_POSICOES_SUPREMAS)
                with c2:
                    dna_ini = st.selectbox("DNA (ARQUÉTIPO INICIAL):", list(REGRAS_TREINO.keys()))
                    alt = st.number_input("ALTURA (m):", 1.50, 2.20, 1.76)
                    peso = st.number_input("PESO (kg):", 50, 130, 74)
                
                ft = st.file_uploader("FOTO DO PERFIL (UPLOAD PNG/JPG):")
                
                if st.form_submit_button("🚀 INICIAR CARREIRA"):
                    path = f"fotos_atletas/{id_user}.png" if ft else "fotos_atletas/default.png"
                    if ft: Image.open(ft).save(path)
                    
                    idade_calc = calcular_idade(nasc)
                    
                    # --- CONSTRUÇÃO SUPREMA PARA O NOVO SQL (ESTRUTURA HÍBRIDA) ---
                    atleta_payload = {
                        "nome": id_user,
                        "nome_completo": nome_atleta,
                        "nascimento": nasc.strftime("%Y-%m-%d"), 
                        "idade": idade_calc,
                        "altura": alt, 
                        "peso": peso, 
                        "posicao": pos, 
                        "dna": dna_ini, 
                        "dna_origem": dna_ini,
                        "foto": path, 
                        "status": "Saudável",
                        "overall": 75.0,
                        "stats": distribuir_stats_iniciais(dna_ini),
                        "habilidades": [],
                        "maestria": {m: 0.0 for m in REQUISITOS_SKILLS.keys()},
                        "personalidade": {"Raça": 50, "Técnica": 50, "Altruísmo": 50, "Compostura": 50},
                        "stats_fixos": {"Forma física": 4, "Resistência a lesão": 2, "Pior pé frequência": 2, "Pior pé precisão": 2},
                        "historico_ovr": [{"idade": idade_calc, "ovr": 75}]
                    }
                    
                    # Cálculo de Overall Real (DNA Ponta-Liso + PTD/PTE = 77.0)
                    atleta_payload["overall"] = calcular_ovr_supremo(atleta_payload)
                    
                    if registrar_novo_atleta(atleta_payload):
                        st.success("Contrato Blindado! Sincronizando com a Nuvem...")
                        st.rerun()

# --- ÁREA LOGADA (CT SUPREMO) ---
else:
    # Sincronização Obrigatória com o Cloud (Evita Amnésia do Render)
    p = buscar_atleta(st.session_state.id_logado)
    id_log = st.session_state.id_logado

    # === SIDEBAR: SCOUT CARD (BIOMETRIA ANALÍTICA) ===
    with st.sidebar:
        nome_card = p.get("nome_completo", p["nome"]).split()[0]
        st.markdown(f"<h2 style='text-align: center; color: #ffd700;'>{nome_card}</h2>", unsafe_allow_html=True)
        
        if os.path.exists(p["foto"]): 
            st.image(p["foto"], use_container_width=True)
        
        st.metric("OVERALL SUPREMO", f"{p['overall']:.1f}")
        st.divider()
        
        st.write(f"**🧬 DNA:** {p['dna']}")
        st.write(f"**🏆 ESTILO:** {definir_arquetipo_master(p, REQUISITOS_ESTILOS)}")
        st.write(f"**🎂 IDADE:** {p['idade']} anos")
        
        status_emoji = "🟢" if p["status"] == "Saudável" else "🔴"
        st.write(f"**🏥 STATUS:** {status_emoji} {p['status']}")
        
        # --- SISTEMA DE SKILLS ATIVAS (DESIGN PES 2021) ---
        st.divider()
        st.subheader("🎒 Skills Ativas")
        if p.get("habilidades"):
            for sk in p["habilidades"]:
                st.markdown(f"""
                    <div style='background-color: #ffd700; color: black; padding: 6px; 
                    border-radius: 4px; margin-bottom: 6px; font-weight: bold; 
                    text-align: center; font-size: 0.8em; border: 1px solid #b8860b;'>
                        {sk.upper()}
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.caption("Aguardando evolução técnica...")
        
        st.divider()
        if st.button("🚪 SAIR DO CT", use_container_width=True):
            st.session_state.auth = False
            st.rerun()

    # --- PAINEL DE CONTROLE CENTRAL ---
    st.title(f"Centro de Treinamento - {p.get('nome_completo', p['nome'])}")
    tabs = st.tabs(["🎮 Campo de Treino", "🧠 Atleta", "📈 Evolução", "⚙️ Configurações"])

    with tabs[0]: # CAMPO DE TREINO
        if p["status"] == "Lesionado":
            st.error("🚑 BLOQUEADO: Atleta inapto para atividades de campo.")
        else:
            col_radar, col_menu = st.columns([1.5, 1])
            with col_radar:
                # O Radar utiliza o mapeamento reconstruído (Aumentando a Rodunha)
                st.plotly_chart(gerar_radar(p["stats"]), use_container_width=True)
            
            with col_menu:
                st.markdown("### Selecione o Portal")
                if st.button("🛡️ PORTAL DE DEFESA", use_container_width=True): st.session_state.portal = "DEF"
                if st.button("⚙️ PORTAL DE MEIO-CAMPO", use_container_width=True): st.session_state.portal = "MEI"
                if st.button("🎯 PORTAL DE ATAQUE", use_container_width=True): st.session_state.portal = "ATQ"
                if st.button("🧤 PORTAL DE GOLEIRO", use_container_width=True): st.session_state.portal = "GK"
                
                st.divider()
                
                # --- LABORATÓRIO DE SKILLS COM AUTO-GRADUAÇÃO ---
                st.subheader("🧪 Laboratório de Skills")
                prog_maestria = p.get("maestria", {})
                skills_unlock = p.get("habilidades", [])
                
                for skill, score in prog_maestria.items():
                    if score > 0:
                        st.caption(f"**{skill}** ({score}%)")
                        st.progress(min(score / 100, 1.0))
                        
                        # Lógica de Graduação 100% (O Pulo do Gato)
                        if score >= 100 and skill not in skills_unlock:
                            skills_unlock.append(skill)
                            # Persistência atômica no banco
                            if salvar_evolucao_treino(id_log, {"habilidades": skills_unlock}):
                                st.toast(f"✅ NOVO TALENTO: {skill} dominado!", icon="🔥")
                                st.rerun()

            st.divider()
            portal_ativo = st.session_state.get('portal')
            if portal_ativo == "DEF":
                from setores.defesa.portal import mostrar_sala_defesa
                mostrar_sala_defesa()
            elif portal_ativo == "MEI":
                from setores.meio_campo.portal import mostrar_sala_meio
                mostrar_sala_meio()
            elif portal_ativo == "ATQ":
                from setores.ataque.portal import mostrar_sala_ataque
                mostrar_sala_ataque()
            elif portal_ativo == "GK":
                try:
                    from setores.goleiro.portal import mostrar_sala_goleiro
                    mostrar_sala_goleiro()
                except ImportError:
                    st.warning("🚧 MURALHA EM CONSTRUÇÃO.")

    with tabs[1]: # BIOMETRIA
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

    with tabs[2]: # DATA VISUALIZATION
        st.subheader("📈 Curva de Performance")
        df_evol = pd.DataFrame(p.get("historico_ovr", []))
        if not df_evol.empty:
            import plotly.express as px
            fig = px.line(df_evol, x="idade", y="ovr", markers=True)
            fig.update_traces(line_color='#ffd700', line_width=4)
            st.plotly_chart(fig, use_container_width=True)

    with tabs[3]: # ADMINISTRAÇÃO (UPDATE SUPREMO)
        st.subheader("⚙️ Ajustes de Vínculo")
        with st.form("edicao_perfil_final"):
            new_nome_f = st.text_input("Alterar Nome Completo:", value=p.get("nome_completo", p["nome"]))
            new_pos_t = st.selectbox(
                "Alterar Posição Tática:", 
                LISTA_POSICOES_SUPREMAS, 
                index=LISTA_POSICOES_SUPREMAS.index(p["posicao"]) if p["posicao"] in LISTA_POSICOES_SUPREMAS else 0
            )
            nova_ft_bin = st.file_uploader("Trocar Identidade Visual:")
            
            if st.form_submit_button("💾 SINCRONIZAR COM A NUVEM"):
                update_payload = {
                    "nome_completo": new_nome_f,
                    "posicao": new_pos_t
                }
                
                if nova_ft_bin:
                    path_ft = f"fotos_atletas/{id_log}.png"
                    Image.open(nova_ft_bin).save(path_ft)
                    update_payload["foto"] = path_ft
                
                # Recálculo para o OVR não "murchar" na mudança
                p_copy = p.copy()
                p_copy.update(update_payload)
                update_payload["overall"] = calcular_ovr_supremo(p_copy)
                
                if salvar_evolucao_treino(id_log, update_payload):
                    st.success("Dados re-selados no Supabase!")
                    st.rerun()
