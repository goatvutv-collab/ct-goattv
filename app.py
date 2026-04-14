import streamlit as st
import json
import os
import pandas as pd
import plotly.express as px
from PIL import Image
from datetime import datetime

# --- 1. CONFIGURAÇÃO E INFRAESTRUTURA ---
st.set_page_config(page_title="GOAT TV - CT", layout="wide", initial_sidebar_state="expanded")

DB_DIR = "fotos_atletas" 
DB_FILE = os.path.join(DB_DIR, "jogadores_goat.json")
if not os.path.exists(DB_DIR): os.makedirs(DB_DIR)

# --- 2. TABELAS TÉCNICAS (A BÍBLIA DA FEDERAÇÃO) ---
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
    "Artilheiro": ["O Matador", "O Pivô"], "Infiltrador": ["O Segundo Atacante", "O Coringa"],
    "Ponta Incisivo": ["O Ponta-Liso", "O Motorzinho"], "Orquestrador": ["O Maestro", "O Garçom"],
    "Destruidor": ["O Xerife", "O Carrapato"], "Líbero (Build Up)": ["O Libero", "O Paredão"]
}

REQUISITOS_SKILLS = {
    "Pedalada Simples": {"Drible": 75, "Velocidade": 70}, "Passe de Primeira": {"Passe": 80, "Drible": 70},
    "Chute de Longe": {"Finalização": 82, "Físico": 75}, "Interceptação": {"Defesa": 80, "Velocidade": 75},
    "Espírito de Luta": {"Físico": 85, "Defesa": 70}, "Folha Seca": {"Finalização": 85, "Físico": 70},
    "Finalização Acrobática": {"Finalização": 80, "Velocidade": 75}, "Cabeceio": {"Finalização": 75, "Físico": 82},
    "Giro 360": {"Drible": 85, "Passe": 70}, "Elástico": {"Drible": 88, "Velocidade": 80},
    "Malícia": {"Drible": 70, "Físico": 60}, "Carrinho Técnico": {"Defesa": 82, "Velocidade": 78},
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

def calcular_overall_ponderado(atleta):
    stats, pos, alt = atleta["stats"], atleta["posicao"], atleta["altura"]
    pesos_pos = PESOS_OVR.get(pos, PESOS_OVR["MEI"])
    ovr_base = sum(stats.get(s, 80) * pesos_pos[s] for s in pesos_pos) / sum(pesos_pos.values())
    # Bônus de Altura PES:
    bonus = 1 if (pos == "DEF" and alt >= 1.85) or (pos == "ATA" and alt >= 1.88) else 0
    return int(ovr_base + bonus + 0.5)

def gerar_grafico_radar(stats):
    df_radar = pd.DataFrame(dict(r=list(stats.values()), theta=list(stats.keys())))
    fig = px.line_polar(df_radar, r='r', theta='theta', line_close=True, range_r=[40, 100])
    fig.update_traces(fill='toself', line_color='#ffd700', fillcolor='rgba(255, 215, 0, 0.3)')
    fig.update_layout(polar=dict(bgcolor="rgba(0,0,0,0)", radialaxis=dict(visible=False)), paper_bgcolor="rgba(0,0,0,0)", font=dict(color="white"), showlegend=False)
    return fig

# --- 4. ENGINE MASTER (EVOLUÇÃO, BIOMETRIA E PRESSÃO) ---
def processar_treino_master(id_atleta, arquetipo_alvo, score):
    db = carregar_db(); atleta = db[id_atleta]
    ovr_atual = atleta["overall"]; status_ini = atleta.get("status", "Saudável")
    peso, altura = atleta.get("peso", 75), atleta.get("altura", 1.75)
    
    # 4.1 Razão Biométrica: Distribuição proporcional (Fator Bio)
    razao_massa = peso / altura
    delta = razao_massa - 42.0
    f_vel = 1.0 - (delta / 40); f_fis = 1.0 + (delta / 40)
    momentum = peso * (atleta["stats"]["Velocidade"] / 100)

    # 4.2 A - LÓGICA DE FALHA E LESÃO (Dúvida do Atleta)
    if score < 1200:
        atleta["status"] = "Lesionado" if status_ini == "Saudável" else "Incapacitado"
        # Pressão 4 Níveis
        p_base = 3.0 if ovr_atual >= 90 else (1.5 if ovr_atual >= 85 else (1.0 if ovr_atual >= 80 else 0.5))
        grav_física = momentum / 70 
        
        for s in atleta["stats"]:
            perda = (p_base * grav_física) if s in REGRAS_TREINO[arquetipo_alvo]["sobe"] else p_base/2
            atleta["stats"][s] = round(max(40, atleta["stats"][s] - perda), 1)
        st.error(f"⚠️ FALHA SOB PRESSÃO! Impacto: {momentum:.1f}. Perda Tier: -{p_base}")

    # 4.3 B - LÓGICA DE SUCESSO E DESBLOQUEIO
    else:
        mult_ovr = max(0.1, 1 - (ovr_atual / 105))
        if status_ini == "Lesionado": mult_ovr *= 0.3 # Debuff 70%
        else: atleta["status"] = "Saudável"

        ganho_base = (score / 2500) * mult_ovr
        regra = REGRAS_TREINO[arquetipo_alvo]
        for s in regra["sobe"]:
            f_aj = f_vel if s == "Velocidade" else (f_fis if s == "Físico" else 1.0)
            atleta["stats"][s] = round(atleta["stats"][s] + (ganho_base * f_aj), 1)
        for d in regra["desce"]:
            atleta["stats"][d] = round(max(40, atleta["stats"][d] - (ganho_base * 0.4)), 1)

        # SKILLS: Só libera se 100% Saudável
        if atleta["status"] == "Saudável" and len(atleta.get("habilidades", [])) < 10:
            for sk, reqs in REQUISITOS_SKILLS.items():
                if sk not in atleta["habilidades"] and all(atleta["stats"].get(sr, 0) >= v for sr, v in reqs.items()):
                    atleta["habilidades"].append(sk); st.balloons(); st.success(f"✨ SKILL: {sk}!")

    # 4.4 C - ACÚMULO PARA ESTILO E DNA ESPECIALISTA
    atleta["maestria"][arquetipo_alvo] = min(100.0, atleta["maestria"].get(arquetipo_alvo, 0) + (score / 350))
    if atleta["maestria"].get(arquetipo_alvo, 0) >= 90:
        atleta["dna"] = f"ESPECIALISTA: {arquetipo_alvo.upper()}"

    if atleta.get("estilo_jogo", "Nenhum") == "Nenhum":
        for est, arqs in REQUISITOS_ESTILOS.items():
            if sum(atleta["maestria"].get(a, 0) for a in arqs) >= 120:
                if est not in atleta.setdefault("estilos_disponiveis", []): atleta["estilos_disponiveis"].append(est)

    atleta["overall"] = calcular_overall_ponderado(atleta)
    db[id_atleta] = atleta; salvar_db(db); return atleta

# --- 5. INTERFACE DO SISTEMA ---
import defesa, meio_campo, ataque
if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("<h1 style='text-align: center; color: #ffd700;'>🏟️ CT GOAT TV</h1>", unsafe_allow_html=True)
    id_user = st.text_input("DIGITE SEU ID DE ATLETA:").upper().strip()
    
    if st.button("🔍 ACESSAR REGISTROS", use_container_width=True):
        db = carregar_db()
        if id_user in db: st.session_state.perfil, st.session_state.id_logado, st.session_state.auth = db[id_user], id_user, True; st.rerun()
        elif id_user: st.error("ID não encontrado. Cadastre-se abaixo.")

    if id_user and id_user not in carregar_db():
        with st.form("registro_goat_elite"):
            n = st.text_input("NOME COMPLETO:"); i = st.number_input("IDADE:", 14, 45, 17)
            t = st.radio("SITUAÇÃO:", ["Iniciante (Promessa)", "Já jogo (Veterano)"])
            c1, c2, c3 = st.columns(3)
            alt = c1.number_input("ALTURA (m):", 1.5, 2.15, 1.78); pso = c2.number_input("PESO (kg):", 50, 130, 75); pos = c3.selectbox("POSIÇÃO:", ["ATA", "MEI", "DEF"])
            arq = st.selectbox("ARQUÉTIPO INICIAL:", list(REGRAS_TREINO.keys()))
            ft = st.file_uploader("FOTO (Obrigatória):", type=['jpg', 'png', 'jpeg'])
            if st.form_submit_button("🚀 FINALIZAR REGISTRO E ENTRAR"):
                if n and ft:
                    base = 75.0 if i <= 17 else (80.0 if i <= 21 else 85.0)
                    if t == "Já jogo (Veterano)": base += 2.0
                    path = f"{DB_DIR}/{id_user}.png"; Image.open(ft).save(path)
                    db = carregar_db()
                    db[id_user] = {"nome": n, "idade": i, "altura": alt, "peso": pso, "posicao": pos, "overall": base, "dna": f"{t} ({arq})", "foto": path, "stats": {k: base for k in ["Drible", "Passe", "Defesa", "Físico", "Finalização", "Velocidade"]}, "maestria": {m: (40.0 if m == arq else 0.0) for m in REGRAS_TREINO.keys()}, "habilidades": [], "estilo_jogo": "Nenhum", "status": "Saudável"}
                    db[id_user]["overall"] = calcular_overall_ponderado(db[id_user]); salvar_db(db)
                    st.session_state.perfil, st.session_state.id_logado, st.session_state.auth = db[id_user], id_user, True; st.rerun()

else:
    perfil = st.session_state.perfil; status = perfil.get("status", "Saudável")

    # --- SIDEBAR: STANDBY (O PROTOCOLO DE STATUS) ---
    with st.sidebar:
        st.markdown("<h2 style='text-align: center;'>📄 SCOUT CARD</h2>", unsafe_allow_html=True)
        if os.path.exists(perfil.get("foto", "")): st.image(perfil["foto"], use_container_width=True)
        
        st.metric("OVERALL", perfil["overall"])
        st.write(f"**NOME:** {perfil['nome']}")
        st.write(f"**DNA:** {perfil['dna']}")
        st.write(f"**BIOMETRIA:** {perfil['peso']}kg | {perfil['altura']}m")
        st.write(f"**STATUS:** {status}")
        
        st.divider()
        st.markdown("### 🔭 LABORATÓRIO DE SKILLS")
        for sk, reqs in REQUISITOS_SKILLS.items():
            if sk not in perfil["habilidades"]:
                dif = sum(max(0, v - perfil["stats"].get(sr, 0)) for sr, v in reqs.items())
                if dif <= 12:
                    st.caption(f"**{sk}**")
                    for sr, v in reqs.items():
                        at = perfil["stats"].get(sr, 0)
                        st.caption(f"{sr}: {at}/{v}")
                        st.progress(min(at/v, 1.0))
        
        st.divider()
        st.markdown("### 📊 MAESTRIA")
        for m, val in perfil["maestria"].items():
            if val > 0:
                st.caption(f"{m}: {val:.1f}%")
                st.progress(min(val/100, 1.0))
        
        if st.button("SAIR"): st.session_state.auth = False; st.rerun()

    # --- LOBBY CENTRAL (RUDY) ---
    st.title(f"Centro de Treinamento - {perfil['nome'].split()[0]}")
    
    if status == "Incapacitado":
        st.error("🚑 DEPARTAMENTO MÉDICO: Você está fora de combate hoje.")
        if st.button("🧊 REALIZAR TRATAMENTO"):
            db = carregar_db(); db[st.session_state.id_logado]["status"] = "Saudável"; salvar_db(db); st.rerun()
    elif status == "Lesionado":
        st.warning("⚠️ VOCÊ ESTÁ LESIONADO! Treinar agora trará 70% de debuff.")
        if st.button("🩹 TRATAR AGORA", use_container_width=True):
            db = carregar_db(); db[st.session_state.id_logado]["status"] = "Saudável"; salvar_db(db); st.rerun()

    if perfil.get("estilo_jogo") == "Nenhum" and perfil.get("estilos_disponiveis"):
        with st.expander("✨ NOVA IDENTIDADE DISPONÍVEL!", expanded=True):
            for est in perfil["estilos_disponiveis"]:
                if st.button(f"Assumir DNA: {est}"):
                    db = carregar_db(); db[st.session_state.id_logado]["estilo_jogo"] = est
                    db[st.session_state.id_logado]["dna"] = f"ESPECIALISTA: {est.upper()}"; salvar_db(db); st.rerun()

    if status != "Incapacitado":
        col_radar, col_menu = st.columns([1.5, 1])
        with col_radar: st.plotly_chart(gerar_grafico_radar(perfil["stats"]), use_container_width=True)
        with col_menu:
            st.subheader("Painel de Treino")
            if st.button("🛡️ DEFESA", use_container_width=True): st.session_state.portal = "DEF"
            if st.button("⚙️ MEIO", use_container_width=True): st.session_state.portal = "MEI"
            if st.button("🎯 ATAQUE", use_container_width=True): st.session_state.portal = "ATQ"
            if st.button("👤 CONFIGURAÇÕES / EDITAR", use_container_width=True): st.session_state.portal = "SETTINGS"

    portal = st.session_state.get('portal')
    if portal == "SETTINGS":
        with st.form("edicao"):
            ed_n = st.text_input("NOME:", value=perfil["nome"])
            ed_p = st.number_input("PESO (kg):", value=perfil["peso"])
            ed_a = st.number_input("ALTURA (m):", value=perfil["altura"])
            if st.form_submit_button("💾 SALVAR"):
                db = carregar_db(); db[st.session_state.id_logado].update({"nome": ed_n, "peso": ed_p, "altura": ed_a})
                db[st.session_state.id_logado]["overall"] = calcular_overall_ponderado(db[st.session_state.id_logado])
                salvar_db(db); st.session_state.perfil = db[st.session_state.id_logado]; st.success("Atualizado!"); st.rerun()
        if st.button("🔙 VOLTAR"): st.session_state.portal = None; st.rerun()
    
    elif portal == "DEF": defesa.mostrar_sala_defesa()
    elif portal == "MEI": meio_campo.mostrar_sala_meio()
    elif portal == "ATQ": ataque.mostrar_sala_ataque()
