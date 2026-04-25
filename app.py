# --- app.py ---
import streamlit as st
import os, sys, pandas as pd
from PIL import Image
from datetime import date

# Injeção de dependências e proteção de diretórios
os.makedirs("fotos_atletas", exist_ok=True)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# --- INTEGRAÇÃO COM O MOTOR DE DADOS (SUPABASE) ---
from database.db_handler import (
    buscar_atleta, 
    salvar_evolucao_treino, 
    registrar_novo_atleta
)
from engine.regras import REGRAS_TREINO, REQUISITOS_ESTILOS, REQUISITOS_SKILLS
from engine.calculos import calcular_ovr_supremo, distribuir_stats_iniciais, calcular_idade
from interface.visual import gerar_radar, desenhar_personalidade, exibir_laboratorio_skills, definir_arquetipo_master

# Configurações de Interface de Elite
st.set_page_config(page_title="GOAT TV - CT SUPREMO 2021", layout="wide", initial_sidebar_state="expanded")

# Constantes Táticas e Visuais
LISTA_POSICOES_SUPREMAS = ["CA", "SA", "PTD", "PTE", "MAT", "VOL", "ZC", "LD", "LE", "GOL"]
IMG_DEFAULT = "https://raw.githubusercontent.com/streamlit/documentation/main/public/images/avatars/avatar_1.png"

# Inicialização de Estado de Sessão
if 'auth' not in st.session_state: st.session_state.auth = False
if 'portal' not in st.session_state: st.session_state.portal = None
if 'id_logado' not in st.session_state: st.session_state.id_logado = None

# --- NÚCLEO DE ACESSO (LOGIN E REGISTRO) ---
if not st.session_state.auth:
    st.markdown("<h1 style='text-align: center; color: #ffd700;'>🏟️ CT GOAT TV - VERSÃO PES 2021</h1>", unsafe_allow_html=True)
    col_log, col_reg = st.columns([1, 1.5])
    
    with col_log:
        st.subheader("🔍 Acessar Registro")
        id_user = st.text_input("ID ATLETA (Ex: GOAT-01):").upper().strip()
        if st.button("ENTRAR NO CT", use_container_width=True):
            atleta_nuvem = buscar_atleta(id_user)
            if atleta_nuvem:
                st.session_state.id_logado = id_user
                st.session_state.auth = True
                st.rerun()
            else: st.error("ID não localizado na Federação Goat TV.")

    with col_reg:
        if id_user and not buscar_atleta(id_user):
            with st.form("registro_goat_supremo"):
                st.subheader("📝 Contrato de Estreia (Nascimento Flat 75)")
                c1, c2 = st.columns(2)
                with c1:
                    nome_f = st.text_input("NOME COMPLETO:")
                    nasc = st.date_input("DATA DE NASCIMENTO:", value=date(2005, 1, 1))
                    pos = st.selectbox("POSIÇÃO DE ELITE:", LISTA_POSICOES_SUPREMAS)
                with c2:
                    dna_ini = st.selectbox("DNA (ARQUÉTIPO):", list(REGRAS_TREINO.keys()))
                    alt = st.number_input("ALTURA (m):", 1.50, 2.20, 1.76)
                    peso = st.number_input("PESO (kg):", 50, 130, 74)
                
                ft = st.file_uploader("FOTO DO PERFIL:")
                
                if st.form_submit_button("🚀 INICIAR CARREIRA"):
                    path = f"fotos_atletas/{id_user}.png" if ft else "fotos_atletas/default.png"
                    if ft: Image.open(ft).save(path)
                    
                    idade_c = calcular_idade(nasc)
                    # Payload completo para o Supabase (Não perdemos nada da versão antiga!)
                    atleta_payload = {
                        "nome": id_user, # ID Único
                        "nome_completo": nome_f,
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
                        st.success("Contrato Blindado! Clique em Entrar.")

# --- ÁREA INTERNA (CENTRO DE TREINAMENTO) ---
else:
    # Sincronização em tempo real com a Nuvem
    p = buscar_atleta(st.session_state.id_logado)
    id_log = st.session_state.id_logado

    # === SIDEBAR: SCOUT CARD (VISUAL PES 2021) ===
    with st.sidebar:
        # Foto com fallback anti-crash
        if os.path.exists(p["foto"]): st.image(p["foto"], use_container_width=True)
        else: st.image(IMG_DEFAULT, use_container_width=True)
        
        st.markdown(f"<h2 style='text-align: center; color: #ffd700;'>{p.get('nome_completo', p['nome']).split()[0]}</h2>", unsafe_allow_html=True)
        st.metric("OVERALL", f"{p['overall']:.1f}")
        st.divider()
        
        st.write(f"**🧬 DNA:** {p['dna']}")
        st.write(f"**🏆 ESTILO:** {definir_arquetipo_master(p, REQUISITOS_ESTILOS)}")
        st.write(f"**🎂 IDADE:** {p['idade']} anos")
        
        # Skills Ativas (Design de Badges Dourados)
        st.subheader("🎒 Skills Ativas")
        if p.get("habilidades"):
            for sk in p["habilidades"]:
                st.markdown(f"""<div style='background-color:#ffd700; color:black; padding:5px; border-radius:5px; 
                margin-bottom:5px; font-weight:bold; text-align:center; border: 1px solid #b8860b;'>{sk.upper()}</div>""", unsafe_allow_html=True)
        else: st.caption("Nenhum talento masterizado.")
        
        if st.button("🚪 SAIR DO CT", use_container_width=True):
            st.session_state.auth = False; st.rerun()

    # === PAINEL CENTRAL ===
    st.title(f"CT Goat TV - {p.get('nome_completo', p['nome'])}")
    tabs = st.tabs(["🎮 Campo de Treino", "🧠 Atleta", "📈 Evolução", "⚙️ Configurações"])

    with tabs[0]: # TREINAMENTO
        if p["status"] == "Lesionado":
            st.error("🚑 BLOQUEADO: Você está no Departamento Médico.")
        else:
            col_radar, col_menu = st.columns([1.5, 1])
            with col_radar:
                st.plotly_chart(gerar_radar(p["stats"]), use_container_width=True)
            
            with col_menu:
                st.markdown("### Portais de Especialização")
                c1, c2 = st.columns(2)
                if c1.button("🛡️ DEFESA"): st.session_state.portal = "DEF"
                if c1.button("🎯 ATAQUE"): st.session_state.portal = "ATQ"
                if c2.button("⚙️ MEIO"): st.session_state.portal = "MEI"
                if c2.button("🧤 GOLEIRO"): st.session_state.portal = "GK"
                
                st.divider()
                # --- LABORATÓRIO DE SKILLS (VISUAL FOTO 2) ---
                st.subheader("🧪 Laboratório de Skills")
                prog_m = p.get("maestria", {})
                sk_ativas = p.get("habilidades", [])
                
                for skill, score in prog_m.items():
                    if score > 0:
                        status_lab = "🏆 CONCLUÍDO" if score >= 100 else f"{score:.1f}%"
                        st.caption(f"**{skill}** ({status_lab})")
                        st.progress(min(score/100, 1.0))
                        
                        # Graduação automática (Sobe para o Sidebar)
                        if score >= 100 and skill not in sk_ativas:
                            sk_ativas.append(skill)
                            salvar_evolucao_treino(id_log, {"habilidades": sk_ativas})
                            st.toast(f"✅ NOVO TALENTO: {skill}!", icon="🔥")
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

    with tabs[1]: # BIOMETRIA (O que você sentiu falta do antigo)
        col_m, col_f = st.columns(2)
        with col_m:
            desenhar_personalidade(p["personalidade"])
        with col_f:
            st.markdown("### 🧬 Fisiologia PES")
            fixos = p.get("stats_fixos", {})
            st.write(f"**Altura:** {p['altura']}m | **Peso:** {p['peso']}kg")
            st.write(f"**Pior Pé:** {fixos.get('Pior pé frequência', 2)}/4 (Freq) | {fixos.get('Pior pé precisão', 2)}/4 (Prec)")
            st.write(f"**Forma Física:** {fixos.get('Forma física', 4)}/8")

    with tabs[2]: # EVOLUÇÃO
        st.subheader("📈 Curva de Performance Profissional")
        df_evol = pd.DataFrame(p.get("historico_ovr", []))
        if not df_evol.empty:
            import plotly.express as px
            fig = px.line(df_evol, x="idade", y="ovr", markers=True)
            fig.update_traces(line_color='#ffd700', line_width=4)
            st.plotly_chart(fig, use_container_width=True)

    with tabs[3]: # AJUSTES (A função de edição do antigo voltando)
        st.subheader("⚙️ Gerenciar Vínculo")
        with st.form("edicao_final"):
            new_n = st.text_input("Alterar Nome:", value=p.get("nome_completo", p["nome"]))
            new_p = st.selectbox("Posição:", LISTA_POSICOES_SUPREMAS, index=LISTA_POSICOES_SUPREMAS.index(p["posicao"]))
            if st.form_submit_button("💾 SALVAR ALTERAÇÕES"):
                mudancas = {"nome_completo": new_n, "posicao": new_p}
                p_copy = p.copy(); p_copy.update(mudancas)
                mudancas["overall"] = calcular_ovr_supremo(p_copy)
                if salvar_evolucao_treino(id_log, mudancas):
                    st.success("Contrato atualizado na nuvem!")
                    st.rerun()
