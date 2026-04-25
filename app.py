# --- app.py ---
import streamlit as st
import os, sys, pandas as pd
from PIL import Image
from datetime import date

# Injeção de dependências
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# --- INTEGRAÇÃO COM SUPABASE ---
from database.db_handler import (
    carregar_todos_jogadores, 
    buscar_atleta, 
    salvar_evolucao_treino, 
    registrar_novo_atleta
)
from engine.regras import STATS_BASE_PES, STATS_NIVEL, REGRAS_TREINO, REQUISITOS_ESTILOS, REQUISITOS_SKILLS
from engine.calculos import calcular_ovr_supremo, distribuir_stats_iniciais, calcular_idade
from interface.visual import gerar_radar, desenhar_personalidade, exibir_laboratorio_skills, definir_arquetipo_master

# Configurações Globais
st.set_page_config(page_title="GOAT TV - CT SUPREMO 2021", layout="wide", initial_sidebar_state="expanded")

# Tática da Federação (Com PTD e PTE)
LISTA_POSICOES_SUPREMAS = ["CA", "SA", "PTD", "PTE", "MAT", "VOL", "ZC", "LD", "LE", "GOL"]

# Inicialização de Variáveis de Sessão
if 'auth' not in st.session_state: st.session_state.auth = False
if 'portal' not in st.session_state: st.session_state.portal = None
if 'id_logado' not in st.session_state: st.session_state.id_logado = None

# --- NÚCLEO DE ACESSO ---
if not st.session_state.auth:
    st.markdown("<h1 style='text-align: center; color: #ffd700;'>🏟️ CT GOAT TV - VERSÃO PES 2021</h1>", unsafe_allow_html=True)
    col_log, col_reg = st.columns([1, 1.5])
    
    with col_log:
        st.subheader("🔍 Acessar Registro")
        id_user = st.text_input("ID ATLETA (Ex: GOAT-01):").upper().strip()
        if st.button("ENTRAR NO CT", use_container_width=True):
            atleta = buscar_atleta(id_user)
            if atleta:
                st.session_state.id_logado = id_user
                st.session_state.auth = True
                st.rerun()
            else: st.error("ID não localizado.")

    with col_reg:
        if id_user and not buscar_atleta(id_user):
            with st.form("registro_goat_supremo"):
                st.subheader("📝 Contrato de Estreia (Flat 75)")
                c1, c2 = st.columns(2)
                with c1:
                    nome_atleta = st.text_input("NOME COMPLETO:")
                    nasc = st.date_input("NASCIMENTO:", value=date(2005, 1, 1))
                    pos = st.selectbox("POSIÇÃO:", LISTA_POSICOES_SUPREMAS)
                with c2:
                    dna_ini = st.selectbox("DNA:", list(REGRAS_TREINO.keys()))
                    alt = st.number_input("ALTURA:", 1.50, 2.20, 1.76)
                    peso = st.number_input("PESO:", 50, 130, 74)
                
                ft = st.file_uploader("FOTO:")
                
                if st.form_submit_button("🚀 INICIAR CARREIRA"):
                    path = f"fotos_atletas/{id_user}.png" if ft else "fotos_atletas/default.png"
                    if ft: Image.open(ft).save(path)
                    
                    idade_c = calcular_idade(nasc)
                    atleta_payload = {
                        "nome": id_user, 
                        "nome_completo": nome_atleta, 
                        "nascimento": nasc.strftime("%Y-%m-%d"),
                        "idade": idade_c, "altura": alt, "peso": peso, 
                        "posicao": pos, "dna": dna_ini, "dna_origem": dna_ini,
                        "foto": path, "status": "Saudável", "overall": 75.0,
                        "stats": distribuir_stats_iniciais(dna_ini), 
                        "habilidades": [],
                        "maestria": {m: 0.0 for m in REQUISITOS_SKILLS.keys()},
                        "personalidade": {"Raça": 50, "Técnica": 50, "Altruísmo": 50, "Compostura": 50},
                        "stats_fixos": {"Forma física": 4, "Resistência a lesão": 2, "Pior pé frequência": 2, "Pior pé precisão": 2},
                        "historico_ovr": [{"idade": idade_c, "ovr": 75}]
                    }
                    atleta_payload["overall"] = calcular_ovr_supremo(atleta_payload)
                    if registrar_novo_atleta(atleta_payload):
                        st.success("Contrato assinado! Clique em Entrar.")
                        st.rerun()

# --- ÁREA LOGADA ---
else:
    # Sincronização obrigatória com o banco
    p = buscar_atleta(st.session_state.id_logado)
    id_log = st.session_state.id_logado

    with st.sidebar:
        # 1. PROTEÇÃO DA IMAGEM
        foto_path = p.get("foto", "fotos_atletas/default.png")
        if os.path.exists(foto_path):
            st.image(foto_path, use_container_width=True)
        else:
            st.image("fotos_atletas/default.png", use_container_width=True)
        
        st.metric("OVERALL", f"{p['overall']:.1f}")
        st.divider()
        st.write(f"**DNA:** {p['dna']}")
        st.write(f"**IDADE:** {p['idade']} anos")
        
        # 2. SKILLS ATIVAS (BADGES DOURADOS)
        st.subheader("🎒 Skills Ativas")
        if p.get("habilidades"):
            for sk in p["habilidades"]:
                st.markdown(f"""<div style='background-color:#ffd700;color:black;padding:5px;border-radius:5px;
                margin-bottom:5px;font-weight:bold;text-align:center;border:1px solid #b8860b;'>{sk.upper()}</div>""", unsafe_allow_html=True)
        else: st.caption("Aguardando evolução técnica...")
        
        if st.button("🚪 SAIR DO CT", use_container_width=True):
            st.session_state.auth = False
            st.rerun()

    st.title(f"CT Goat TV - {p.get('nome_completo', p['nome'])}")
    tabs = st.tabs(["🎮 Treino", "🧠 Atleta", "📈 Evolução", "⚙️ Ajustes"])

    with tabs[0]:
        col_radar, col_menu = st.columns([1.5, 1])
        with col_radar:
            # Radar utiliza o mapeamento do Handler (Cura da Rodinha)
            st.plotly_chart(gerar_radar(p["stats"]), use_container_width=True)
        
        with col_menu:
            st.markdown("### Portais")
            c1, c2 = st.columns(2)
            if c1.button("🛡️ DEFESA", use_container_width=True): st.session_state.portal = "DEF"
            if c1.button("🎯 ATAQUE", use_container_width=True): st.session_state.portal = "ATQ"
            if c2.button("⚙️ MEIO", use_container_width=True): st.session_state.portal = "MEI"
            if c2.button("🧤 GOLEIRO", use_container_width=True): st.session_state.portal = "GK"
            
            st.divider()
            
            # 3. LABORATÓRIO (LÓGICA FOTO 2)
            st.subheader("🧪 Laboratório")
            prog_m = p.get("maestria", {})
            sk_ativas = p.get("habilidades", [])
            for skill, score in prog_m.items():
                if score > 0:
                    label = f"**{skill}** (OK)" if score >= 100 else f"**{skill}** ({score}%)"
                    st.caption(label)
                    st.progress(min(score/100, 1.0))
                    
                    # Graduação automática
                    if score >= 100 and skill not in sk_ativas:
                        sk_ativas.append(skill)
                        if salvar_evolucao_treino(id_log, {"habilidades": sk_ativas}):
                            st.toast(f"✅ SKILL MASTERIZADA: {skill}!", icon="⭐")
                            st.rerun()

        st.divider()
        portal = st.session_state.get('portal')
        if portal == "ATQ":
            from setores.ataque.portal import mostrar_sala_ataque
            mostrar_sala_ataque()
        elif portal == "GK":
            try:
                from setores.goleiro.portal import mostrar_sala_goleiro
                mostrar_sala_goleiro()
            except ImportError: st.warning("Setor de Goleiros em obras.")

    with tabs[3]:
        with st.form("edicao"):
            new_n = st.text_input("Nome:", value=p.get("nome_completo", p["nome"]))
            new_p = st.selectbox("Posição:", LISTA_POSICOES_SUPREMAS, index=LISTA_POSICOES_SUPREMAS.index(p["posicao"]))
            if st.form_submit_button("💾 SALVAR ALTERAÇÕES"):
                mudancas = {"nome_completo": new_n, "posicao": new_p}
                p_copy = p.copy(); p_copy.update(mudancas)
                mudancas["overall"] = calcular_ovr_supremo(p_copy)
                if salvar_evolucao_treino(id_log, mudancas):
                    st.success("Sincronizado!")
                    st.rerun()
