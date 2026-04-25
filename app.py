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

# Configuração de Engine de Interface Streamlit
st.set_page_config(
    page_title="GOAT TV - CT SUPREMO 2021", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

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
                st.error("ID não localizado na Federação Goat TV. Verifique a grafia ou registre-se.")

    with col_reg:
        # Lógica de Verificação de Existência em Tempo Real no Banco
        if id_user and not buscar_atleta(id_user):
            with st.form("registro_goat_complexo"):
                st.subheader("📝 Contrato de Estreia (Nascimento Flat 75)")
                c1, c2 = st.columns(2)
                with c1:
                    nome_atleta = st.text_input("NOME COMPLETO:")
                    nasc = st.date_input("DATA DE NASCIMENTO:", value=date(2005, 1, 1), min_value=date(1980, 1, 1), max_value=date(2012, 12, 31))
                    pos = st.selectbox("POSIÇÃO:", ["CA", "SA", "MAT", "VOL", "ZC", "LD", "LE", "GOL"])
                with c2:
                    dna_ini = st.selectbox("DNA (ARQUÉTIPO INICIAL):", list(REGRAS_TREINO.keys()))
                    alt = st.number_input("ALTURA (m):", 1.50, 2.20, 1.76)
                    peso = st.number_input("PESO (kg):", 50, 130, 74)
                
                ft = st.file_uploader("FOTO DO PERFIL (UPLOAD PNG/JPG):")
                
                if st.form_submit_button("🚀 INICIAR CARREIRA"):
                    # Processamento de Mídia Local (Snapshot para Deploy)
                    path = f"fotos_atletas/{id_user}.png" if ft else "fotos_atletas/default.png"
                    if ft: Image.open(ft).save(path)
                    
                    idade_calc = calcular_idade(nasc)
                    
                    # --- CONSTRUÇÃO SUPREMA PARA O NOVO SQL (ESTRUTURA HÍBRIDA) ---
                    # Este dicionário será 'achatado' pelo Handler antes de entrar no Supabase
                    atleta_payload = {
                        "nome": id_user,           # Chave Primária SQL
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
                        "stats": distribuir_stats_iniciais(dna_ini), # Objeto complexo PES
                        "habilidades": [],
                        "personalidade": {"Raça": 50, "Técnica": 50, "Altruísmo": 50, "Compostura": 50},
                        "stats_fixos": {"Forma física": 4, "Resistência a lesão": 2, "Pior pé frequência": 2, "Pior pé precisão": 2},
                        "historico_ovr": [{"idade": idade_calc, "ovr": 75}]
                    }
                    
                    # Cálculo de Potencial Via Engine de Cálculo
                    atleta_payload["overall"] = calcular_ovr_supremo(atleta_payload)
                    
                    # Persistência via Handler Complexo (Mapeamento de 15+ colunas SQL)
                    if registrar_novo_atleta(atleta_payload):
                        st.success("Contrato Blindado! Sincronizando com a Nuvem...")
                        st.rerun()

# --- ÁREA LOGADA (COMPLEXO ESPORTIVO INTERNO) ---
else:
    # Sincronização Obrigatória com o Cloud State (Evita Amnésia do Render)
    p = buscar_atleta(st.session_state.id_logado)
    id_log = st.session_state.id_logado

    # === SIDEBAR: SCOUT CARD (BIOMETRIA ANALÍTICA) ===
    with st.sidebar:
        # Renderização de Identidade Visual
        nome_card = p.get("nome_completo", p["nome"]).split()[0]
        st.markdown(f"<h2 style='text-align: center; color: #ffd700;'>{nome_card}</h2>", unsafe_allow_html=True)
        
        if os.path.exists(p["foto"]): 
            st.image(p["foto"], use_container_width=True)
        
        st.metric("OVERALL SUPREMO", f"{p['overall']:.1f}")
        st.divider()
        
        # Grid de Dados Bio-Táticos
        st.write(f"**🧬 DNA ATUAL:** {p['dna']}")
        st.write(f"**🏆 ARQUÉTIPO:** {definir_arquetipo_master(p, REQUISITOS_ESTILOS)}")
        st.write(f"**🎂 IDADE:** {p['idade']} anos")
        
        status_emoji = "🟢" if p["status"] == "Saudável" else "🔴"
        st.write(f"**🏥 STATUS:** {status_emoji} {p['status']}")
        
        if p["status"] == "Lesionado":
            if st.button("🧊 INICIAR RECOVERY (FISIOTERAPIA)"):
                salvar_evolucao_treino(id_log, {"status": "Saudável"})
                st.rerun()
        
        st.divider()
        st.subheader("🎒 Skills Ativas")
        if p.get("habilidades"):
            for sk in p["habilidades"]: st.caption(f"✅ {sk}")
        else: st.caption("Nenhuma skill desbloqueada no Laboratory.")
        
        st.divider()
        if st.button("🚪 SAIR DO CT", use_container_width=True):
            st.session_state.auth = False
            st.rerun()

    # --- PAINEL DE CONTROLE CENTRAL (TABS) ---
    st.title(f"Centro de Treinamento - {p.get('nome_completo', p['nome'])}")
    tabs = st.tabs(["🎮 Campo de Treino", "🧠 Atleta", "📈 Evolução", "⚙️ Configurações"])

    with tabs[0]: # CAMPO DE TREINO (INTEGRAÇÃO CANVAS E PORTAIS)
        if p["status"] == "Lesionado":
            st.error("🚑 BLOQUEADO: Atleta inapto para atividades de campo.")
        else:
            col_radar, col_menu = st.columns([1.5, 1])
            with col_radar:
                # O Radar utiliza o objeto p['stats'] reconstruído dinamicamente pelo Handler
                st.plotly_chart(gerar_radar(p["stats"]), use_container_width=True)
            
            with col_menu:
                st.markdown("### Selecione o Portal de Especialização")
                if st.button("🛡️ PORTAL DE DEFESA", use_container_width=True): st.session_state.portal = "DEF"
                if st.button("⚙️ PORTAL DE MEIO-CAMPO", use_container_width=True): st.session_state.portal = "MEI"
                if st.button("🎯 PORTAL DE ATAQUE", use_container_width=True): st.session_state.portal = "ATQ"
                # A CURA PARA A DOR: Botão de Goleiro Ativado no Menu
                if st.button("🧤 PORTAL DE GOLEIRO", use_container_width=True): st.session_state.portal = "GK"
                st.divider()
                exibir_laboratorio_skills(p, REQUISITOS_SKILLS)

            # Injeção de Lógica de Portais Modulares
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
                    st.warning("🚧 MURALHA EM CONSTRUÇÃO: O setor de Goleiros está recebendo as redes e luvas oficiais.")

    with tabs[1]: # BIOMETRIA E MENTALIDADE PES
        col_m, col_f = st.columns(2)
        with col_m:
            desenhar_personalidade(p["personalidade"])
        with col_f:
            st.markdown("### 🧬 Fisiologia Avançada (PES Base)")
            fixos = p.get("stats_fixos", {})
            st.write(f"**Pior Pé (Frequência):** {fixos.get('Pior pé frequência', 2)}/4")
            st.write(f"**Pior Pé (Precisão):** {fixos.get('Pior pé precisão', 2)}/4")
            st.write(f"**Forma Física:** {fixos.get('Forma física', 4)}/8")
            st.write(f"**Resistência a Lesão:** {fixos.get('Resistência a lesão', 2)}/3")

    with tabs[2]: # DATA VISUALIZATION (CRESCIMENTO)
        st.subheader("📈 Curva de Maturação Profissional")
        df_evol = pd.DataFrame(p.get("historico_ovr", []))
        if not df_evol.empty:
            import plotly.express as px
            fig = px.line(df_evol, x="idade", y="ovr", markers=True, title="Desenvolvimento de Performance")
            fig.update_traces(line_color='#ffd700', line_width=4)
            st.plotly_chart(fig, use_container_width=True)

    with tabs[3]: # ADMINISTRAÇÃO DE CONTRATO (UPDATE SUPABASE)
        st.subheader("⚙️ Gerenciar Vínculo com a Goat TV")
        with st.form("edicao_perfil_suprema"):
            new_nome_f = st.text_input("Alterar Nome Completo:", value=p.get("nome_completo", p["nome"]))
            new_pos_t = st.selectbox("Alterar Posição Tática:", ["CA", "SA", "MAT", "VOL", "ZC", "LD", "LE", "GOL"], 
                                     index=["CA", "SA", "MAT", "VOL", "ZC", "LD", "LE", "GOL"].index(p["posicao"]))
            nova_ft_bin = st.file_uploader("Trocar Identidade Visual (Foto):")
            
            if st.form_submit_button("💾 SINCRONIZAR ALTERAÇÕES COM O BANCO"):
                # Pacote de Mudanças Flat para o Supabase
                update_payload = {
                    "nome_completo": new_nome_f,
                    "posicao": new_pos_t
                }
                
                # Persistência de Mídia no Filesystem Local (Temp)
                if nova_ft_bin:
                    path_ft = f"fotos_atletas/{id_log}.png"
                    Image.open(nova_ft_bin).save(path_ft)
                    update_payload["foto"] = path_ft
                
                # Recálculo de Overall (Sincronizado com Mudança de Posição)
                p_copy = p.copy()
                p_copy.update(update_payload)
                update_payload["overall"] = calcular_ovr_supremo(p_copy)
                
                # Execução via Camada de Dados Suprema
                if salvar_evolucao_treino(id_log, update_payload):
                    st.success("Dados re-selados na nuvem com sucesso!")
                    st.rerun()
