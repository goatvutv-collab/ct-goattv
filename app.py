import streamlit as st
import json
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
from datetime import datetime

# --- 1. INFRAESTRUTURA E BANCO DE DADOS ---
st.set_page_config(page_title="GOAT TV - CT SUPREMO", layout="wide", initial_sidebar_state="expanded")

DB_DIR = "fotos_atletas" 
DB_FILE = os.path.join(DB_DIR, "jogadores_goat.json")
if not os.path.exists(DB_DIR): os.makedirs(DB_DIR)

# --- 2. BÍBLIA TÉCNICA INTEGRADA (PES 2019 + GOAT) ---
PESOS_OVR = {
    "ATA": {"Finalização": 5, "Habilid. Ofensiva": 5, "Velocidade": 4, "Drible": 4, "Força do Chute": 3},
    "MEI": {"Passe Rasteiro": 5, "Passe Alto": 5, "Controle de Bola": 4, "Visão": 4, "Resistência": 3},
    "DEF": {"Desarme": 5, "Habilid. Defensiva": 5, "Contato Físico": 4, "Cabeçada": 3, "Velocidade": 3}
}

REGRAS_TREINO = {
    "O Xerife":          {"sobe": ["Desarme", "Habilid. Defensiva", "Contato Físico"], "desce": ["Drible", "Velocidade"]},
    "O Libero":          {"sobe": ["Passe Alto", "Habilid. Defensiva", "Controle de Bola"], "desce": ["Contato Físico", "Finalização"]},
    "O Carrapato":       {"sobe": ["Desarme", "Resistência", "Velocidade"], "desce": ["Finalização", "Passe Alto"]},
    "O Paredão":         {"sobe": ["Habilid. Defensiva", "Cabeçada", "Contato Físico"], "desce": ["Velocidade", "Drible"]},
    "O Maestro":         {"sobe": ["Passe Rasteiro", "Controle de Bola", "Visão"], "desce": ["Contato Físico", "Desarme"]},
    "O Motorzinho":      {"sobe": ["Resistência", "Velocidade", "Passe Rasteiro"], "desce": ["Finalização", "Drible"]},
    "O Garçom":          {"sobe": ["Passe Rasteiro", "Passe Alto", "Curva"], "desce": ["Contato Físico", "Velocidade"]},
    "O Coringa":         {"sobe": ["Drible", "Controle de Bola", "Equilíbrio"], "desce": ["Habilid. Defensiva", "Cabeçada"]},
    "O Ponta-Liso":      {"sobe": ["Velocidade", "Drible", "Explosão"], "desce": ["Contato Físico", "Habilid. Defensiva"]},
    "O Pivô":            {"sobe": ["Contato Físico", "Finalização", "Cabeçada"], "desce": ["Velocidade", "Explosão"]},
    "O Matador":         {"sobe": ["Finalização", "Habilid. Ofensiva", "Força do Chute"], "desce": ["Resistência", "Habilid. Defensiva"]},
    "O Segundo Atacante": {"sobe": ["Drible", "Passe Rasteiro", "Habilid. Ofensiva"], "desce": ["Contato Físico", "Cabeçada"]}
}

REQUISITOS_ESTILOS = {
    "Artilheiro": ["O Matador", "O Pivô"], "Infiltrador": ["O Segundo Atacante", "O Coringa"],
    "Ponta Incisivo": ["O Ponta-Liso", "O Motorzinho"], "Orquestrador": ["O Maestro", "O Garçom"],
    "Destruidor": ["O Xerife", "O Carrapato"], "Líbero (Build Up)": ["O Libero", "O Paredão"]
}

REQUISITOS_SKILLS = {
    "Pedalada Simples": {"Drible": 75, "Velocidade": 70}, "Toque Duplo": {"Drible": 80, "Controle de Bola": 75},
    "Elástico": {"Drible": 85, "Equilíbrio": 70}, "360 Graus": {"Drible": 78, "Controle de Bola": 82},
    "Chute de Longe": {"Finalização": 82, "Força do Chute": 80}, "Folha Seca": {"Finalização": 85, "Curva": 75},
    "Cabeceio": {"Cabeçada": 80, "Contato Físico": 75}, "Interceptação": {"Desarme": 80, "Habilid. Defensiva": 75},
    "Espírito de Luta": {"Resistência": 85, "Raça": 70}, "Malícia": {"Equilíbrio": 70, "Drible": 75}
}

# --- 3. MOTORES DE CÁLCULO E GRÁFICOS ---
def carregar_db():
    if not os.path.exists(DB_FILE): return {}
    try:
        with open(DB_FILE, "r") as f: return json.load(f)
    except: return {}

def salvar_db(dados):
    with open(DB_FILE, "w") as f: json.dump(dados, f, indent=4)

def calcular_ovr_supremo(atleta):
    stats, pos = atleta["stats"], atleta["posicao"]
    pesos = PESOS_OVR.get(pos, PESOS_OVR["MEI"])
    ovr_base = sum(stats.get(s, 70) * w for s, w in pesos.items()) / sum(pesos.values())
    # Bônus PES: Altura estratégica
    bonus = 1 if (pos == "DEF" and atleta["altura"] >= 1.85) or (pos == "ATA" and atleta["altura"] >= 1.88) else 0
    return int(ovr_base + bonus + 0.5)

def gerar_radar(stats):
    # Seleciona os top 6 atributos para o radar
    labels = list(stats.keys())[:8]
    values = [stats[l] for l in labels]
    fig = go.Figure(data=go.Scatterpolar(r=values, theta=labels, fill='toself', line_color='#ffd700', fillcolor='rgba(255, 215, 0, 0.3)'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=False)), paper_bgcolor="rgba(0,0,0,0)", font=dict(color="white"), showlegend=False)
    return fig

# --- 4. ENGINE MASTER (EVOLUÇÃO E PERSONALIDADE) ---
def processar_treino_master(id_atleta, arq_alvo, score):
    db = carregar_db(); p = db[id_atleta]
    ovr_atual = p["overall"]; status_ini = p.get("status", "Saudável")
    
    # Física de Momentum
    momentum = p["peso"] * (p["stats"].get("Velocidade", 70) / 100)
    
    if score < 1200:
        p["status"] = "Lesionado" if status_ini == "Saudável" else "Incapacitado"
        p["personalidade"]["Raça"] = max(0, p["personalidade"]["Raça"] - 3)
        # Punição Tier
        punicao = 3.0 if ovr_atual >= 90 else (1.5 if ovr_atual >= 85 else 0.5)
        for s in p["stats"]: p["stats"][s] = round(max(40, p["stats"][s] - (punicao * (momentum/70))), 1)
    else:
        mult = 0.3 if status_ini == "Lesionado" else 1.0
        ganho = (score / 2500) * mult * (max(0.1, 1 - (ovr_atual / 105)))
        for s in REGRAS_TREINO[arq_alvo]["sobe"]: p["stats"][s] = round(p["stats"].get(s, 70) + ganho, 1)
        # Evolução Psicológica
        p["personalidade"]["Técnica"] = min(100, p["personalidade"]["Técnica"] + 0.5)
        if score > 2000: p["personalidade"]["Compostura"] = min(100, p["personalidade"]["Compostura"] + 1)

        if status_ini == "Saudável" and len(p.get("habilidades", [])) < 10:
            for sk, reqs in REQUISITOS_SKILLS.items():
                if sk not in p["habilidades"] and all(p["stats"].get(sr, 0) >= v for sr, v in reqs.items()):
                    p["habilidades"].append(sk); st.balloons()

    # Maestria e DNA
    p["maestria"][arq_alvo] = min(100.0, p["maestria"].get(arq_alvo, 0) + (score / 350))
    if p["maestria"][arq_alvo] >= 90: p["dna"] = f"ESPECIALISTA: {arq_alvo.upper()}"
    
    p["historico_ovr"].append({"idade": p["idade"], "ovr": p["overall"]})
    p["overall"] = calcular_ovr_supremo(p)
    db[id_atleta] = p; salvar_db(db); return p

# --- 5. INTERFACE (O LOBBY INTEGRAL) ---
import defesa, meio_campo, ataque
if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("<h1 style='text-align: center; color: #ffd700;'>🏟️ CT GOAT TV - ALPHA UNIFICADO</h1>", unsafe_allow_html=True)
    id_user = st.text_input("ID ATLETA:").upper().strip()
    if st.button("🔍 ACESSAR REGISTROS", use_container_width=True):
        db = carregar_db()
        if id_user in db: st.session_state.perfil, st.session_state.id_logado, st.session_state.auth = db[id_user], id_user, True; st.rerun()

    if id_user and id_user not in carregar_db():
        with st.form("registro_supremo"):
            n = st.text_input("NOME COMPLETO:"); i = st.number_input("IDADE:", 15, 45, 17)
            t = st.radio("JÁ FOI JOGADOR?", ["Veterano (Já Jogo)", "Iniciante (Promessa)"])
            c1, c2, c3 = st.columns(3)
            alt = c1.number_input("ALTURA (m):", 1.5, 2.2, 1.78); peso = c2.number_input("PESO (kg):", 50, 130, 75); pos = c3.selectbox("POSIÇÃO:", ["ATA", "MEI", "DEF"])
            ft = st.file_uploader("FOTO OFICIAL:", type=['jpg', 'png', 'jpeg'])
            if st.form_submit_button("🚀 INICIAR CARREIRA"):
                # PISO POR IDADE
                base = 75.0 if i <= 18 else (80.0 if i <= 22 else 85.0)
                if t == "Veterano (Já Jogo)": base += 2.0
                path = f"{DB_DIR}/{id_user}.png"
                if ft: Image.open(ft).save(path)
                db = carregar_db()
                db[id_user] = {
                    "nome": n, "idade": i, "altura": alt, "peso": peso, "posicao": pos, "overall": base, "foto": path,
                    "dna": t, "status": "Saudável", "habilidades": [], "estilo_jogo": "Nenhum",
                    "stats": {k: base for k in ["Habilid. Ofensiva", "Controle de Bola", "Drivel", "Passe Rasteiro", "Passe Alto", "Finalização", "Velocidade", "Explosão", "Resistência", "Desarme", "Habilid. Defensiva", "Curva", "Equilíbrio", "Contato Físico"]},
                    "personalidade": {"Altruísmo": 50, "Raça": 50, "Técnica": 50, "Compostura": 50, "Individualismo": 50},
                    "maestria": {m: 0.0 for m in REGRAS_TREINO.keys()}, "historico_ovr": [{"idade": i, "ovr": base}],
                    "posicoes": {"CA": "B", "SA": "C", "MEI": "B", "VOL": "C", "ZC": "C"}
                }
                salvar_db(db); st.rerun()

else:
    p = st.session_state.perfil; status = p.get("status", "Saudável")

    # --- SIDEBAR: STANDBY (O PROTOCOLO DE STATUS) ---
    with st.sidebar:
        st.markdown("<h2 style='text-align: center;'>📄 SCOUT CARD</h2>", unsafe_allow_html=True)
        if os.path.exists(p.get("foto", "")): st.image(p["foto"], use_container_width=True)
        
        st.metric("OVERALL", p["overall"])
        st.write(f"**DNA:** {p['dna']}")
        st.write(f"**STATUS:** {status}")
        st.write(f"**BIOMETRIA:** {p['peso']}kg | {p['altura']}m")
        
        st.divider()
        st.subheader("🔭 Laboratório de Skills")
        for sk, reqs in REQUISITOS_SKILLS.items():
            if sk not in p["habilidades"]:
                dif = sum(max(0, v - p["stats"].get(sr, 70)) for sr, v in reqs.items())
                if dif <= 12:
                    st.caption(f"**{sk}**")
                    for sr, v in reqs.items():
                        at = p["stats"].get(sr, 70)
                        st.caption(f"{sr}: {at}/{v}"); st.progress(min(at/v, 1.0))
        
        st.divider()
        st.subheader("📊 Maestrias")
        for m, val in p["maestria"].items():
            if val > 0:
                st.caption(f"{m}: {val:.1f}%"); st.progress(min(val/100, 1.0))
        
        if st.button("SAIR"): st.session_state.auth = False; st.rerun()

    # --- ÁREA CENTRAL: DASHBOARD TÁTICO ---
    st.title(f"CT GOAT TV - Bem-vindo, {p['nome'].split()[0]}")
    
    tabs = st.tabs(["🎮 Campo de Treino", "🧠 Atleta", "📈 Evolução", "⚙️ Configurações"])

    with tabs[0]: # CAMPO DE TREINO
        if status == "Incapacitado":
            st.error("🚑 DEPARTAMENTO MÉDICO: Você está impossibilitado de treinar hoje.")
            if st.button("🧊 REALIZAR TRATAMENTO"):
                db = carregar_db(); db[st.session_state.id_logado]["status"] = "Saudável"; salvar_db(db); st.rerun()
        else:
            if status == "Lesionado": st.warning("⚠️ VOCÊ ESTÁ LESIONADO! Rendimento reduzido em 70%.")
            col_radar, col_menu = st.columns([1.5, 1])
            with col_radar: st.plotly_chart(gerar_radar(p["stats"]), use_container_width=True)
            with col_menu:
                st.subheader("Setores de Ação")
                if st.button("🛡️ DEFESA", use_container_width=True): st.session_state.portal = "DEF"
                if st.button("⚙️ MEIO", use_container_width=True): st.session_state.portal = "MEI"
                if st.button("🎯 ATAQUE", use_container_width=True): st.session_state.portal = "ATQ"
            
            portal = st.session_state.get('portal')
            if portal == "DEF": defesa.mostrar_sala_defesa()
            elif portal == "MEI": meio_campo.mostrar_sala_meio()
            elif portal == "ATQ": ataque.mostrar_sala_ataque()

    with tabs[1]: # CÉREBRO E PERSONALIDADE
        st.subheader("🧠 Matriz de Personalidade")
        c1, c2 = st.columns(2)
        with c1:
            for k, v in p["personalidade"].items():
                st.write(f"**{k}:** {v}%")
                st.progress(v/100)
        with c2:
            st.subheader("📍 Domínio de Posição")
            for pos, nivel in p["posicoes"].items():
                st.write(f"**{pos}:** {nivel}")

    with tabs[2]: # FOLHA DE EVOLUÇÃO
        st.subheader("📊 Folha de Evolução (Real vs Esperado)")
        df = pd.DataFrame(p["historico_ovr"])
        df["esperado"] = df["ovr"].iloc[0] + (df["idade"] - p["idade"]) * 1.2 # Curva esperada
        fig_evol = px.line(df, x="idade", y=["ovr", "esperado"], color_discrete_sequence=["#ffd700", "#ff00ff"])
        st.plotly_chart(fig_evol, use_container_width=True)

    with tabs[3]: # CONFIGURAÇÕES (REEDIÇÃO)
        st.subheader("⚙️ Reedição de Perfil")
        with st.form("edit_total"):
            new_n = st.text_input("Nome:", value=p["nome"])
            new_p = st.number_input("Peso:", value=p["peso"])
            new_a = st.number_input("Altura:", value=p["altura"])
            new_pos = st.selectbox("Posição:", ["ATA", "MEI", "DEF"], index=["ATA", "MEI", "DEF"].index(p["posicao"]))
            nova_ft = st.file_uploader("Trocar Foto:")
            if st.form_submit_button("💾 SALVAR ALTERAÇÕES"):
                db = carregar_db(); id_l = st.session_state.id_logado
                if nova_ft:
                    if os.path.exists(p["foto"]): os.remove(p["foto"])
                    path = f"{DB_DIR}/{id_l}.png"; Image.open(nova_ft).save(path); db[id_l]["foto"] = path
                db[id_l].update({"nome": new_n, "peso": new_p, "altura": new_a, "posicao": new_pos})
                db[id_l]["overall"] = calcular_ovr_supremo(db[id_l]); salvar_db(db)
                st.session_state.perfil = db[id_l]; st.rerun()
