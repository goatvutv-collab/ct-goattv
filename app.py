# --- app.py ---
import streamlit as st
import os, sys, pandas as pd
from PIL import Image
from datetime import date

# Injeção de dependências do sistema
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# --- INTEGRAÇÃO COM O MOTOR DE DADOS SUPREMO ---
from database.db_handler import (
    carregar_todos_jogadores, 
    buscar_atleta, 
    salvar_evolucao_treino, 
    registrar_novo_atleta
)
from engine.regras import STATS_BASE_PES, STATS_NIVEL, REGRAS_TREINO, REQUISITOS_ESTILOS, REQUISITOS_SKILLS
from engine.calculos import calcular_ovr_supremo, distribuir_stats_iniciais, calcular_idade
from interface.visual import gerar_radar, desenhar_personalidade, exibir_laboratorio_skills, definir_arquetipo_master

# Configuração de Engine de Interface
st.set_page_config(
    page_title="GOAT TV - CT SUPREMO 2021", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Inicialização de Variáveis de Estado de Sessão (Persistence Layer)
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
            # Query Complexa no Supabase via Handler
            atleta_encontrado = buscar_atleta(id_user)
            if atleta_encontrado:
                st.session_state.perfil = atleta_encontrado
                st.session_state.id_logado = id_user
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("ID não localizado na Federação Goat TV.")

    with col_reg:
        # Lógica de Verificação de Existência em Tempo Real
        if id_user and not buscar_atleta(id_user):
            with st.form("registro_goat"):
                st.subheader("📝 Contrato de Estreia (Nascimento Flat 75)")
                c1, c2 = st.columns(2)
                with c1:
                    nome_atleta = st.text_input("NOME COMPLETO:")
                    nasc = st.date_input("DATA DE NASCIMENTO:", value=date(2005, 1, 1), min_value=date(1980, 1, 1), max_value=date(2012, 12, 31))
                    pos = st.selectbox("POSIÇÃO:", ["CA", "SA", "MAT", "VOL", "ZC", "LD", "LE", "GOL"])
                with c2:
                    dna_ini = st.selectbox("DNA (ARQUÉTIPO INICIAL):", list(REGRAS_TREINO.keys()))
                    alt = st.number_input("ALTURA (m):", 1.50, 2.20, 1.80)
                    peso = st.number_input("PESO (kg):", 50, 130, 75)
                
                ft = st.file_uploader("FOTO DO PERFIL (UPLOAD PNG/JPG):")
                
                if st.form_submit_button("🚀 INICIAR CARREIRA"):
                    # Processamento de Mídia
                    path = f"fotos_atletas/{id_user}.png" if ft else "fotos_atletas/default.png"
                    if ft: Image.open(ft).save(path)
                    
                    idade_calc = calcular_idade(nasc)
                    
                    # --- CONSTRUÇÃO SUPREMA PARA O NOVO SQL (ESTRUTURA HÍBRIDA) ---
                    atleta = {
                        "nome": id_user,           # Coluna 'nome' (PK)
                        "nome_completo": nome_atleta, # Coluna 'nome_completo'
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
                        "stats": distribuir_stats_iniciais(dna_ini), # O Handler fará o flattening
                        "habilidades": [],
                        "personalidade": {"Raça": 50, "Técnica": 50, "Altruísmo": 50, "Compostura": 50},
                        "stats_fixos": {"Forma física": 4, "Resistência a lesão": 2, "Pior pé frequência": 2, "Pior pé precisão": 2},
                        "historico_ovr": [{"idade": idade_calc, "ovr": 75}]
                    }
                    
                    # Cálculo de Potencial Inicial
                    atleta["overall"] = calcular_ovr_supremo(atleta)
                    
                    # Persistência via Handler Complexo
                    if registrar_novo_atleta(atleta):
                        st.success("Contrato Blindado! Sincronizando com a Nuvem...")
                        st.rerun()

# --- ÁREA LOGADA (CT INTERNO) ---
else:
    # Sincronização de Estado com o Banco de Dados (Evita Desvios de Memória)
    p = buscar_atleta(st.session_state.id_logado)
    id_log = st.session_state.id_logado

    # === SIDEBAR: SCOUT CARD (O RG ANALÍTICO DO ATLETA) ===
    with st.sidebar:
        # Renderização Dinâmica de Identidade
        nome_curto = p.get("nome_completo", p["nome"]).split()[0]
        st.markdown(f"<h2 style='text-align: center; color: #ffd700;'>{nome_curto}</h2>", unsafe_allow_html=True)
        
        if os.path.exists(p["foto"]): 
            st.image(p["foto"], use_container_width=True)
        
        st.metric("OVERALL SUPREMO", f"{p['overall']:.1f}")
        st.divider()
        
        # Grid de Atributos Bio-Táticos
        st.write(f"**🧬 DNA ATUAL:** {p['dna']}")
        st.write(f"**🏆 ARQUÉTIPO:** {definir_arquetipo_master(p, REQUISITOS_ESTILOS)}")
        st.write(f"**🎂 IDADE:** {p['idade']} anos")
        
        status_emoji = "🟢" if p["status"] == "Saudável" else "🔴"
        st.write(f"**🏥 STATUS:** {status_emoji} {p['status']}")
        
        if p["status"] == "Lesionado":
            if st.button("🧊 TRATAMENTO MÉDICO (RECOVERY)"):
                salvar_evolucao_treino(id_log, {"status": "Saudável"})
                st.rerun()
        
        st.divider()
        st.subheader("🎒 Skills Ativas")
        if p.get("habilidades"):
            for sk in p["habilidades"]: st.caption(f"✅ {sk}")
        else: st.caption("Nenhuma skill desbloqueada via Laboratory.")
        
        st.divider()
        if st.button("🚪 SAIR DO COMPLEXO", use_container_width=True):
            st.session_state.auth = False
            st.rerun()

    # --- PAINEL DE CONTROLE CENTRAL ---
    st.title(f"Centro de Treinamento - {p.get('nome_completo', p['nome'])}")
    tabs = st.tabs(["🎮 Campo de Treino", "🧠 Atleta", "📈 Evolução", "⚙️ Configurações"])

    with tabs[0]: # CAMPO DE TREINO (INTEGRAÇÃO CANVAS)
        if p["status"] == "Lesionado":
            st.error("🚑 ACESSO NEGADO: Atleta em observação no Departamento Médico.")
        else:
            col_radar, col_menu = st.columns([1.5, 1])
            with col_radar:
                # O Radar consome o p["stats"] reconstruído pelo buscar_atleta (complexo)
                st.plotly_chart(gerar_radar(p["stats"]), use_container_width=True)
            
            with col_menu:
                st.markdown("### Selecione o Portal de Especialização")
                if st.button("🛡️ PORTAL DE DEFESA", use_container_width=True): st.session_state.portal = "DEF"
                if st.button("⚙️ PORTAL DE MEIO-CAMPO", use_container_width=True): st.session_state.portal = "MEI"
                if st.button("🎯 PORTAL DE ATAQUE", use_container_width=True): st.session_state.portal = "ATQ"
                if st.button("🧤 PORTAL DE GOLEIRO", use_container_width=True): st.session_state.portal = "GK"
                st.divider()
                exibir_laboratorio_skills(p, REQUISITOS_SKILLS)

            # Navegação Modular (Dynamic Injections)
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
                    st.warning("🚧 SETOR EM OBRAS: A Federação está finalizando a instalação da Muralha.")

    with tabs[1]: # BIOMETRIA E MENTALIDADE
        col_m, col_f = st.columns(2)
        with col_m:
            desenhar_personalidade(p["personalidade"])
        with col_f:
            st.markdown("### 🧬 Fisiologia Avançada PES")
            fixos = p.get("stats_fixos", {})
            st.write(f"**Pior Pé (Frequência):** {fixos.get('Pior pé frequência', 2)}/4")
            st.write(f"**Pior Pé (Precisão):** {fixos.get('Pior pé precisão', 2)}/4")
            st.write(f"**Forma Física:** {fixos.get('Forma física', 4)}/8")
            st.write(f"**Resistência a Lesão:** {fixos.get('Resistência a lesão', 2)}/3")

    with tabs[2]: # DATA ANALYSIS (EVOLUÇÃO)
        st.subheader("📈 Curva de Maturação Profissional")
        df_evolucao = pd.DataFrame(p.get("historico_ovr", []))
        if not df_evolucao.empty:
            import plotly.express as px
            fig = px.line(df_evolucao, x="idade", y="ovr", markers=True, title="Histórico de Overall")
            fig.update_traces(line_color='#ffd700', line_width=4)
            st.plotly_chart(fig, use_container_width=True)

    with tabs[3]: # GERENCIAMENTO DE CONTRATO (SUPABASE UPDATE)
        st.subheader("⚙️ Ajustes de Vínculo")
        with st.form("edicao_perfil_complexa"):
            new_nome_full = st.text_input("Alterar Nome Completo:", value=p.get("nome_completo", p["nome"]))
            new_posicao = st.selectbox("Alterar Posição Tática:", ["CA", "SA", "MAT", "VOL", "ZC", "LD", "LE", "GOL"], 
                                     index=["CA", "SA", "MAT", "VOL", "ZC", "LD", "LE", "GOL"].index(p["posicao"]))
            nova_foto_bin = st.file_uploader("Substituir Identidade Visual (Foto):")
            
            if st.form_submit_button("💾 SALVAR ALTERAÇÕES NO SUPABASE"):
                # Pacote de Mudanças (Metadados)
                mudancas_supabase = {
                    "nome_completo": new_nome_full,
                    "posicao": new_posicao
                }
                
                # Gestão de Mídia no Servidor
                if nova_foto_bin:
                    path_foto = f"fotos_atletas/{id_log}.png"
                    Image.open(nova_foto_bin).save(path_foto)
                    mudancas_supabase["foto"] = path_foto
                
                # Recálculo de OVR (Sync com Mudança de Posição)
                p_copy = p.copy()
                p_copy.update(mudancas_supabase)
                mudancas_supabase["overall"] = calcular_ovr_supremo(p_copy)
                
                # EXECUÇÃO NO NÚCLEO DE DADOS
                if salvar_evolucao_treino(id_log, mudancas_supabase):
                    st.success("Sincronização com Supabase concluída com sucesso!")
                    st.rerun()
