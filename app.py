# --- app.py ---
import streamlit as st
import os, sys, pandas as pd
from PIL import Image
from datetime import date, datetime
import plotly.express as px
import plotly.graph_objects as go

# Infraestrutura de Mídia e Dependências
os.makedirs("fotos_atletas", exist_ok=True)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# --- INTEGRAÇÃO COM O MOTOR DE DADOS SUPREMO (SUPABASE) ---
from database.db_handler import (
    buscar_atleta, 
    salvar_evolucao_treino, 
    registrar_novo_atleta
)
from engine.regras import REGRAS_TREINO, REQUISITOS_ESTILOS, REQUISITOS_SKILLS
from engine.calculos import calcular_ovr_supremo, distribuir_stats_iniciais, calcular_idade
from interface.visual import gerar_radar, definir_arquetipo_master, desenhar_personalidade

# Configurações de Elite
st.set_page_config(page_title="GOAT TV - CT SUPREMO 2021", layout="wide", initial_sidebar_state="expanded")

# BÍBLIA TÉCNICA (RESTURADA DO MACARRÃO)
PESOS_OVR_SETOR = {
    "ATA": {"Finalização": 5, "Talento ofensivo": 5, "Velocidade": 4, "Drible": 4, "Aceleração": 3},
    "MEI": {"Passe rasteiro": 5, "Controle de bola": 4, "Drible": 4, "Resistência": 3},
    "DEF": {"Talento defensivo": 5, "Contato físico": 4, "Resistência": 3, "Velocidade": 3}
}

LISTA_POSICOES_SUPREMAS = ["CA", "SA", "PTD", "PTE", "MAT", "VOL", "ZC", "LD", "LE", "GOL"]
IMG_DEFAULT = "https://raw.githubusercontent.com/streamlit/documentation/main/public/images/avatars/avatar_1.png"

if 'auth' not in st.session_state: st.session_state.auth = False
if 'portal' not in st.session_state: st.session_state.portal = None
if 'id_logado' not in st.session_state: st.session_state.id_logado = None

# --- 1. NÚCLEO DE ACESSO (LOGIN E REGISTRO COMPLEXO) ---
if not st.session_state.auth:
    st.markdown("<h1 style='text-align: center; color: #ffd700;'>🏟️ CT GOAT TV - ALPHA UNIFICADO</h1>", unsafe_allow_html=True)
    col_log, col_reg = st.columns([1, 1.5])
    
    with col_log:
        st.subheader("🔍 Acessar Registros")
        id_user = st.text_input("ID ATLETA:").upper().strip()
        if st.button("ENTRAR NO CT", use_container_width=True):
            atleta = buscar_atleta(id_user)
            if atleta:
                st.session_state.id_logado, st.session_state.auth = id_user, True
                st.rerun()
            else: st.error("ID não localizado.")

    with col_reg:
        if id_user and not buscar_atleta(id_user):
            with st.form("registro_supremo"):
                st.subheader("📝 Contrato de Estreia")
                n_completo = st.text_input("NOME COMPLETO:")
                i_reg = st.number_input("IDADE:", 15, 45, 17)
                t_origem = st.radio("JÁ FOI JOGADOR?", ["Veterano (Já Jogo)", "Iniciante (Promessa)"])
                
                c1, c2, c3 = st.columns(3)
                alt = c1.number_input("ALTURA (m):", 1.5, 2.2, 1.80)
                peso = c2.number_input("PESO (kg):", 50, 130, 75)
                pos = c3.selectbox("POSIÇÃO:", LISTA_POSICOES_SUPREMAS)
                
                ft = st.file_uploader("FOTO OFICIAL:", type=['jpg', 'png', 'jpeg'])
                
                if st.form_submit_button("🚀 INICIAR CARREIRA"):
                    # Lógica de Piso por Idade (Bônus Veterano)
                    base_ovr = 75.0 if i_reg <= 18 else (80.0 if i_reg <= 22 else 85.0)
                    if t_origem == "Veterano (Já Jogo)": base_ovr += 2.0
                    
                    path = f"fotos_atletas/{id_user}.png" if ft else "fotos_atletas/default.png"
                    if ft: Image.open(ft).save(path)
                    
                    atleta_payload = {
                        "nome": id_user, "nome_completo": n_completo, "idade": i_reg,
                        "nascimento": date(2026-i_reg, 1, 1).strftime("%Y-%m-%d"),
                        "altura": alt, "peso": peso, "posicao": pos, "overall": base_ovr,
                        "foto": path, "dna": t_origem, "status": "Saudável", "habilidades": [],
                        "stats": distribuir_stats_iniciais("O Coringa"), 
                        "personalidade": {"Altruísmo": 50, "Raça": 50, "Técnica": 50, "Compostura": 50, "Individualismo": 50},
                        "maestria": {m: 0.0 for m in REGRAS_TREINO.keys()},
                        "historico_ovr": [{"idade": i_reg, "ovr": base_ovr}],
                        "posicoes": {"CA": "B", "SA": "C", "PTD": "C", "PTE": "C", "GK": "C"},
                        "stats_fixos": {"Forma física": 4, "Resistência a lesão": 2, "Pior pé frequência": 2, "Pior pé precisão": 2}
                    }
                    atleta_payload["overall"] = calcular_ovr_supremo(atleta_payload)
                    if registrar_novo_atleta(atleta_payload):
                        st.success("Contrato assinado! Entre com seu ID.")

# --- 2. ÁREA INTERNA (O RG DO ATLETA COMPLETO) ---
else:
    p = buscar_atleta(st.session_state.id_logado)
    id_log = st.session_state.id_logado

    with st.sidebar:
        st.markdown("<h2 style='text-align: center;'>📄 SCOUT CARD</h2>", unsafe_allow_html=True)
        if os.path.exists(p.get("foto", "")): st.image(p["foto"], use_container_width=True)
        else: st.image(IMG_DEFAULT, use_container_width=True)

        st.metric("OVERALL", f"{p['overall']:.1f}")
        st.write(f"**DNA:** {p['dna']}")
        st.write(f"**STATUS:** {p.get('status', 'Saudável')}")
        st.write(f"**BIOMETRIA:** {p['peso']}kg | {p['altura']}m")

        st.divider()
        st.subheader("🎒 Skills Ativas")
        if p.get("habilidades"):
            for sk in p["habilidades"]:
                st.markdown(f"<div style='background-color:#ffd700; color:black; padding:5px; border-radius:5px; margin-bottom:5px; font-weight:bold; text-align:center;'>{sk.upper()}</div>", unsafe_allow_html=True)
        
        st.divider()
        st.subheader("📊 Maestrias")
        for m, val in p.get("maestria", {}).items():
            if val > 0:
                st.caption(f"{m}: {val:.1f}%")
                st.progress(min(val/100, 1.0))

        if st.button("🚪 SAIR"):
            st.session_state.auth = False; st.rerun()

    # --- 3. DASHBOARD CENTRAL (RESTAURADO) ---
    st.title(f"CT GOAT TV - Bem-vindo, {p.get('nome_completo', p['nome']).split()[0]}")
    tabs = st.tabs(["🎮 Campo de Treino", "🧠 Atleta", "📈 Evolução", "⚙️ Configurações"])

    with tabs[0]: # TREINO E LAB (FOTO 2)
        col_radar, col_menu = st.columns([1.5, 1])
        with col_radar: st.plotly_chart(gerar_radar(p["stats"]), use_container_width=True)
        with col_menu:
            st.subheader("Setores de Ação")
            c1, c2 = st.columns(2)
            if c1.button("🛡️ DEFESA"): st.session_state.portal = "DEF"
            if c1.button("🎯 ATAQUE"): st.session_state.portal = "ATQ"
            if c2.button("⚙️ MEIO"): st.session_state.portal = "MEI"
            if c2.button("🧤 GOLEIRO"): st.session_state.portal = "GK"
            st.divider()
            st.subheader("🧪 Laboratório de Skills")
            prog_m = p.get("maestria", {})
            sk_at = p.get("habilidades", [])
            for sk, score in prog_m.items():
                if score > 0:
                    st.caption(f"**{sk}** ({'OK' if score >= 100 else f'{score:.1f}%'})")
                    st.progress(min(score/100, 1.0))
                    if score >= 100 and sk not in sk_at:
                        sk_at.append(sk); salvar_evolucao_treino(id_log, {"habilidades": sk_at}); st.rerun()

        st.divider()
        portal = st.session_state.get('portal')
        if portal == "DEF": from setores.defesa.portal import mostrar_sala_defesa; mostrar_sala_defesa()
        elif portal == "MEI": from setores.meio_campo.portal import mostrar_sala_meio; mostrar_sala_meio()
        elif portal == "ATQ": from setores.ataque.portal import mostrar_sala_ataque; mostrar_sala_ataque()
        elif portal == "GK": 
            try: from setores.goleiro.portal import mostrar_sala_goleiro; mostrar_sala_goleiro()
            except: st.warning("Setor de Goleiros em obras.")

    with tabs[1]: # CÉREBRO E FISIOLOGIA (RESTAURADO!)
        st.subheader("🧠 Matriz de Personalidade e Fisiologia")
        c1, c2 = st.columns(2)
        with c1:
            for k, v in p.get("personalidade", {}).items():
                st.write(f"**{k}:** {v}%")
                st.progress(v/100)
        with c2:
            st.subheader("📍 Domínio de Posição")
            for pos_n, nivel in p.get("posicoes", {}).items():
                st.write(f"**{pos_n}:** {nivel}")
            st.divider()
            fixos = p.get("stats_fixos", {})
            st.write(f"**Pior Pé:** {fixos.get('Pior pé frequência', 2)}/4 | **Forma Física:** {fixos.get('Forma física', 4)}/8")

    with tabs[2]: # EVOLUÇÃO REAL VS ESPERADA (RESTAURADO!)
        st.subheader("📊 Folha de Evolução")
        df = pd.DataFrame(p.get("historico_ovr", []))
        if not df.empty:
            df["esperado"] = df["ovr"].iloc[0] + (df["idade"] - df["idade"].iloc[0]) * 1.2
            fig = px.line(df, x="idade", y=["ovr", "esperado"], color_discrete_sequence=["#ffd700", "#ff00ff"])
            st.plotly_chart(fig, use_container_width=True)

    with tabs[3]: # REEDIÇÃO COMPLETA (RESTAURADO!)
        st.subheader("⚙️ Reedição de Perfil")
        with st.form("edit_total"):
            new_n = st.text_input("Nome Completo:", value=p.get("nome_completo", p["nome"]))
            c_e1, c_e2 = st.columns(2)
            new_p = c_e1.number_input("Peso (kg):", value=float(p["peso"]))
            new_a = c_e2.number_input("Altura (m):", value=float(p["altura"]))
            new_pos = st.selectbox("Posição:", LISTA_POSICOES_SUPREMAS, index=LISTA_POSICOES_SUPREMAS.index(p["posicao"]))
            nova_ft = st.file_uploader("Trocar Foto Oficial:")
            if st.form_submit_button("💾 SALVAR ALTERAÇÕES SUPREMAS"):
                mudancas = {"nome_completo": new_n, "peso": new_p, "altura": new_a, "posicao": new_pos}
                if nova_ft:
                    path = f"fotos_atletas/{id_log}.png"; Image.open(nova_ft).save(path); mudancas["foto"] = path
                p.update(mudancas); mudancas["overall"] = calcular_ovr_supremo(p)
                if salvar_evolucao_treino(id_log, mudancas): st.success("Perfil re-selado!"); st.rerun()
