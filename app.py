import streamlit as st
import json
import os
import pandas as pd
import plotly.express as px
from PIL import Image
from datetime import datetime

# --- 1. MÓDULOS EXTERNOS E BANCO DE DADOS ---
import defesa, meio_campo, ataque

DB_DIR = "fotos_atletas" 
DB_FILE = os.path.join(DB_DIR, "jogadores_goat.json")
if not os.path.exists(DB_DIR): os.makedirs(DB_DIR)

# --- 2. TABELAS TÉCNICAS E REGRAS DE NEGÓCIO (A BÍBLIA) ---
PESOS_OVR = {
    "ATA": {"Drible": 5, "Passe": 3, "Defesa": 1, "Físico": 4, "Finalização": 5, "Velocidade": 4},
    "MEI": {"Drible": 4, "Passe": 5, "Defesa": 2, "Físico": 3, "Finalização": 3, "Velocidade": 3},
    "DEF": {"Drible": 1, "Passe": 3, "Defesa": 5, "Físico": 5, "Finalização": 1, "Velocidade": 3}
}

REGRAS_TREINO = {
    "O Xerife":          {"sobe": ["Defesa", "Físico", "Passe"], "desce": ["Velocidade", "Drible", "Finalização"]},
    "O Libero":          {"sobe": ["Passe", "Defesa", "Drible"], "desce": ["Físico", "Finalização", "Velocidade"]},
    "O Carrapato":       {"sobe": ["Defesa", "Físico", "Velocidade"], "desce": ["Passe", "Drible", "Finalização"]},
    "O Paredão":         {"sobe": ["Defesa", "Físico", "Velocidade"], "desce": ["Passe", "Drible", "Finalização"]},
    "O Maestro":         {"sobe": ["Passe", "Drible", "Velocidade"], "desce": ["Defesa", "Físico", "Finalização"]},
    "O Motorzinho":      {"sobe": ["Físico", "Velocidade", "Passe"], "desce": ["Drible", "Finalização", "Defesa"]},
    "O Garçom":          {"sobe": ["Passe", "Drible", "Defesa"], "desce": ["Finalização", "Físico", "Velocidade"]},
    "O Coringa":         {"sobe": ["Drible", "Passe", "Físico"], "desce": ["Defesa", "Finalização", "Velocidade"]},
    "O Ponta-Liso":      {"sobe": ["Drible", "Velocidade", "Finalização"], "desce": ["Físico", "Defesa", "Passe"]},
    "O Pivô":            {"sobe": ["Físico", "Finalização", "Passe"], "desce": ["Velocidade", "Drible", "Defesa"]},
    "O Matador":         {"sobe": ["Finalização", "Físico", "Drible"], "desce": ["Passe", "Velocidade", "Defesa"]},
    "O Segundo Atacante": {"sobe": ["Drible", "Finalização", "Passe"], "desce": ["Defesa", "Físico", "Velocidade"]}
}

REQUISITOS_ESTILOS = {
    "Artilheiro": ["O Matador", "O Pivô"],
    "Infiltrador": ["O Segundo Atacante", "O Coringa"],
    "Ponta Incisivo": ["O Ponta-Liso", "O Motorzinho"],
    "Orquestrador": ["O Maestro", "O Garçom"],
    "Destruidor": ["O Xerife", "O Carrapato"],
    "Líbero (Build Up)": ["O Libero", "O Paredão"]
}

REQUISITOS_SKILLS = {
    "Pedalada Simples": {"Drible": 75, "Velocidade": 70},
    "Passe de Primeira": {"Passe": 80, "Drible": 70},
    "Chute de Longe": {"Finalização": 82, "Físico": 75},
    "Interceptação": {"Defesa": 80, "Velocidade": 75},
    "Espírito de Luta": {"Físico": 85, "Defesa": 70},
    "Folha Seca": {"Finalização": 85, "Físico": 70},
    "Finalização Acrobática": {"Finalização": 80, "Velocidade": 75},
    "Cabeceio": {"Finalização": 75, "Físico": 82},
    "Giro 360": {"Drible": 85, "Passe": 70},
    "Elástico": {"Drible": 88, "Velocidade": 80},
    "Malícia": {"Drible": 70, "Físico": 60},
    "Carrinho Técnico": {"Defesa": 82, "Velocidade": 78},
    "Passe em Profundidade": {"Passe": 85, "Drible": 75}
}

# --- 3. FUNÇÕES TÉCNICAS CORE ---
def carregar_db():
    if not os.path.exists(DB_FILE): return {}
    try:
        with open(DB_FILE, "r") as f: return json.load(f)
    except: return {}

def salvar_db(dados):
    with open(DB_FILE, "w") as f:
        json.dump(dados, f, indent=4)
        f.flush()
        os.fsync(f.fileno())

def calcular_overall_ponderado(atleta):
    stats, pos, alt = atleta["stats"], atleta["posicao"], atleta["altura"]
    pesos_pos = PESOS_OVR.get(pos, PESOS_OVR["MEI"])
    ovr_base = sum(stats.get(s, 80) * pesos_pos[s] for s in pesos_pos) / sum(pesos_pos.values())
    bonus = 1 if (pos == "DEF" and alt >= 1.85) or (pos == "ATA" and alt >= 1.88) else 0
    return int(ovr_base + bonus + 0.5)

def gerar_grafico_radar(stats):
    df_radar = pd.DataFrame(dict(r=list(stats.values()), theta=list(stats.keys())))
    fig = px.line_polar(df_radar, r='r', theta='theta', line_close=True, range_r=[40, 100])
    fig.update_traces(fill='toself', line_color='#ffd700', fillcolor='rgba(255, 215, 0, 0.3)')
    fig.update_layout(polar=dict(bgcolor="rgba(0,0,0,0)", radialaxis=dict(visible=False)), paper_bgcolor="rgba(0,0,0,0)", font=dict(color="white"), showlegend=False)
    return fig

# --- 4. ENGINE MASTER (EVOLUÇÃO, FÍSICA, LESÃO E PRESSÃO) ---
def processar_treino_master(id_atleta, arquetipo_alvo, score):
    db = carregar_db(); atleta = db[id_atleta]
    ovr_atual = atleta["overall"]
    status_inicial = atleta.get("status", "Saudável")
    peso, altura = atleta.get("peso", 75), atleta.get("altura", 1.75)
    
    # Razão Biométrica e Momentum
    momentum = peso * (atleta["stats"]["Velocidade"] / 100)
    razao_massa = peso / altura
    razao_ref = 42.0
    delta_massa = razao_massa - razao_ref
    
    fator_velocidade = 1.0 - (delta_massa / 40)
    fator_fisico = 1.0 + (delta_massa / 40)

    # A. SISTEMA DE FALHA E IMPACTO (LESÃO)
    if score < 1200:
        if ovr_atual >= 90: punicao_base = 3.0
        elif ovr_atual >= 85: punicao_base = 1.5
        elif ovr_atual >= 80: punicao_base = 1.0
        else: punicao_base = 0.5
        
        # Agravamento por Momentum (O Tombo do Pesado)
        gravidade_física = momentum / 70 
        
        if momentum >= 75.0 or status_inicial == "Lesionado":
            atleta["status"] = "Incapacitado"
            st.error(f"🚑 COLAPSO FÍSICO! Impacto de {momentum:.1f}. Você está fora de combate.")
        else:
            atleta["status"] = "Lesionado"
            st.warning(f"⚠️ LESÃO NO TREINO! Impacto de {momentum:.1f}. Procure o DM no Lobby.")

        for s in atleta["stats"]:
            perda = (punicao_base * gravidade_física) if s in REGRAS_TREINO[arquetipo_alvo]["sobe"] else punicao_base/2
            atleta["stats"][s] = round(max(40, atleta["stats"][s] - perda), 1)

    # B. SISTEMA DE SUCESSO (GANHO E DESENVOLVIMENTO)
    else:
        mult_ovr = max(0.1, 1 - (ovr_atual / 105))
        # DEBUFF DE LESÃO: Se treinar quebrado, ganha quase nada.
        if status_inicial == "Lesionado":
            mult_ovr *= 0.3
            st.error("📉 DEBUFF DE SACRIFÍCIO: Por estar lesionado, seu rendimento caiu 70%.")
        else:
            atleta["status"] = "Saudável"

        ganho_base = (score / 2500) * mult_ovr
        regra = REGRAS_TREINO[arquetipo_alvo]
        for s in regra["sobe"]:
            f_ajuste = fator_velocidade if s == "Velocidade" else (fator_fisico if s == "Físico" else 1.0)
            atleta["stats"][s] = round(atleta["stats"][s] + (ganho_base * f_ajuste), 1)
        for d in regra["desce"]:
            atleta["stats"][d] = round(max(40, atleta["stats"][d] - (ganho_base * 0.4)), 1)

        # DESBLOQUEIO DE SKILLS (Só se estiver Saudável)
        if status_inicial == "Saudável" and len(atleta.get("habilidades", [])) < 10:
            for skill, reqs in REQUISITOS_SKILLS.items():
                if skill not in atleta["habilidades"] and all(atleta["stats"].get(sr, 0) >= v for sr, v in reqs.items()):
                    atleta["habilidades"].append(skill)
                    st.balloons(); st.success(f"✨ INSIGHT TÉCNICO: Você dominou a skill {skill}!")

    # C. ACÚMULO DE ESTILO
    if atleta.get("estilo_jogo", "Nenhum") == "Nenhum":
        atleta["maestria"][arquetipo_alvo] = min(100.0, atleta["maestria"].get(arquetipo_alvo, 0) + (score / 350))
        for est, arqs in REQUISITOS_ESTILOS.items():
            if sum(atleta["maestria"].get(a, 0) for a in arqs) >= 120:
                atleta.setdefault("estilos_disponiveis", [])
                if est not in atleta["estilos_disponiveis"]: atleta["estilos_disponiveis"].append(est)

    atleta["overall"] = calcular_overall_ponderado(atleta)
    db[id_atleta] = atleta; salvar_db(db); return atleta

# --- 5. INTERFACE (O RUDY / LOBBY) ---
st.set_page_config(page_title="GOAT TV - CT", layout="wide")
if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("<h1 style='text-align: center; color: #ffd700;'>🏟️ CT GOAT TV</h1>", unsafe_allow_html=True)
    id_user = st.text_input("ID DE ATLETA (Ex: GOAT01):").upper().strip()
    if st.button("🔍 ACESSAR REGISTROS", use_container_width=True):
        db = carregar_db()
        if id_user in db: st.session_state.perfil, st.session_state.id_logado, st.session_state.auth = db[id_user], id_user, True; st.rerun()
        elif id_user: st.error("ID não cadastrado. Preencha a ficha técnica abaixo.")

    if id_user and id_user not in carregar_db():
        with st.form("registro_goat"):
            n = st.text_input("NOME COMPLETO:"); i = st.number_input("IDADE:", 14, 45, 17)
            c1, c2, c3 = st.columns(3)
            alt = c1.number_input("ALTURA (m):", 1.50, 2.15, 1.75); peso = c2.number_input("PESO (kg):", 50, 130, 75); pos = c3.selectbox("POSIÇÃO:", ["ATA", "MEI", "DEF"])
            if st.form_submit_button("🚀 FINALIZAR REGISTRO E ENTRAR"):
                db = carregar_db()
                db[id_user] = {"nome": n, "idade": i, "altura": alt, "peso": peso, "posicao": pos, "overall": 75, "stats": {k: 75.0 for k in ["Drible", "Passe", "Defesa", "Físico", "Finalização", "Velocidade"]}, "maestria": {m: 0.0 for m in REGRAS_TREINO.keys()}, "habilidades": [], "estilo_jogo": "Nenhum", "estilos_disponiveis": [], "foto": "sem_foto", "status": "Saudável"}
                db[id_user]["overall"] = calcular_overall_ponderado(db[id_user]); salvar_db(db)
                st.session_state.perfil, st.session_state.id_logado, st.session_state.auth = db[id_user], id_user, True; st.rerun()
else:
    perfil = st.session_state.perfil; status = perfil.get("status", "Saudável")

    with st.sidebar:
        st.header("📄 SCOUT CARD")
        if perfil.get("foto") != "sem_foto": st.image(perfil["foto"], use_container_width=True)
        st.metric("OVERALL", perfil["overall"])
        st.write(f"**BIOMETRIA:** {perfil['peso']}kg | {perfil['altura']}m")
        st.write(f"**STATUS:** {status}")
        st.divider()
        if st.button("ENCERRAR SESSÃO"): st.session_state.auth = False; st.rerun()

    st.title(f"Centro de Excelência - {perfil['nome']}")

    # --- BANNER DE AVISOS E GESTÃO DE SAÚDE ---
    if status != "Saudável":
        st.error(f"🚑 ALERTA MÉDICO: Você está {status}. Treinar agora causará debuff e impedirá o aprendizado de novas técnicas.")
        if st.button("🧊 TRATAR AGORA (Focar na Recuperação)", use_container_width=True):
            db = carregar_db(); db[st.session_state.id_logado]["status"] = "Saudável"
            salvar_db(db); st.success("Recuperado!"); st.rerun()

    if perfil["overall"] in [79, 84, 89]:
        st.warning("⚖️ FRONTEIRA DE PRESSÃO: Você está a 1 ponto de subir de Tier. O erro será mais punitivo no próximo nível!")

    # --- ESCOLHA DE IDENTIDADE ---
    if perfil.get("estilo_jogo") == "Nenhum" and perfil.get("estilos_disponiveis"):
        with st.warning("✨ NOVA IDENTIDADE DISPONÍVEL!"):
            for est in perfil["estilos_disponiveis"]:
                if st.button(f"Assumir DNA: {est}"):
                    db = carregar_db(); db[st.session_state.id_logado]["estilo_jogo"] = est
                    salvar_db(db); st.rerun()

    # --- LOBBY: RADAR E LABORATÓRIO ---
    col_radar, col_lab = st.columns([1.5, 1])
    with col_radar:
        st.plotly_chart(gerar_grafico_radar(perfil["stats"]), use_container_width=True)
    with col_lab:
        st.subheader("🔭 Laboratório de Skills")
        for skill, reqs in REQUISITOS_SKILLS.items():
            if skill not in perfil.get("habilidades", []):
                dif = sum(max(0, v - perfil["stats"].get(sr, 0)) for sr, v in reqs.items())
                if dif <= 10:
                    prog = [f"{sr}: {perfil['stats'].get(sr,0)}/{v}" for sr, v in reqs.items()]
                    st.info(f"**{skill}**\n\n" + " | ".join(prog))

    st.divider()
    # BLOCO DE NAVEGAÇÃO (Só se não estiver Incapacitado)
    if status != "Incapacitado":
        c1, c2, c3 = st.columns(3)
        if c1.button("🛡️ DEFESA", use_container_width=True): st.session_state.portal = "DEF"
        if c2.button("⚙️ MEIO", use_container_width=True): st.session_state.portal = "MEI"
        if c3.button("🎯 ATAQUE", use_container_width=True): st.session_state.portal = "ATQ"
    
    # Lógica de integração com arquivos externos
    p = st.session_state.get('portal')
    if p == "DEF": defesa.mostrar_sala_defesa()
    elif p == "MEI": meio_campo.mostrar_sala_meio()
    elif p == "ATQ": ataque.mostrar_sala_ataque()
