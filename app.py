import streamlit as st
import json
import os
from PIL import Image

# --- 1. MÓDULOS E BANCO DE DADOS ---
import defesa, meio_campo, ataque
DB_DIR = "/app/fotos_atletas" if os.path.exists("/app/fotos_atletas") else "fotos_atletas"
DB_FILE = os.path.join(DB_DIR, "jogadores_goat.json")
if not os.path.exists(DB_DIR): os.makedirs(DB_DIR)

# --- 2. TABELAS TÉCNICAS (LÓGICA PES & RPG) ---
PESOS = {
    "ATA": {"Drible": 5, "Passe": 3, "Defesa": 1, "Físico": 4, "Finalização": 5, "Velocidade": 4},
    "MEI": {"Drible": 4, "Passe": 5, "Defesa": 2, "Físico": 3, "Finalização": 3, "Velocidade": 3},
    "DEF": {"Drible": 1, "Passe": 3, "Defesa": 5, "Físico": 5, "Finalização": 1, "Velocidade": 3}
}

# REGRAS DOS 12 ARQUÉTIPOS (+3 SOBE / -3 DESCE)
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

# --- 3. FUNÇÕES DE CÁLCULO ---
def carregar_db():
    if not os.path.exists(DB_FILE): return {}
    try:
        with open(DB_FILE, "r") as f: return json.load(f)
    except: return {}

def salvar_db(dados):
    with open(DB_FILE, "w") as f: json.dump(dados, f, indent=4)

def calcular_overall(atleta):
    stats, pos, alt = atleta["stats"], atleta["posicao"], atleta["altura"]
    pesos_pos = PESOS.get(pos, PESOS["MEI"])
    ovr_base = sum(stats[s] * pesos_pos[s] for s in pesos_pos) / sum(pesos_pos.values())
    bonus = 1 if (pos == "DEF" and alt >= 1.85) or (pos == "ATA" and alt >= 1.88) else 0
    return int(ovr_base + bonus + 0.5)

def processar_treino(id_atleta, arquetipo_alvo, score):
    db = carregar_db()
    atleta = db[id_atleta]
    regra = REGRAS_TREINO.get(arquetipo_alvo)
    rendimento = (score / 2500)
    
    # 1. Ajuste de Atributos
    for s in regra["sobe"]: atleta["stats"][s] = round(atleta["stats"][s] + rendimento, 1)
    for d in regra["desce"]: atleta["stats"][d] = round(atleta["stats"][d] - (rendimento * 0.4), 1)
    
    # 2. Maestria
    atleta["maestria"][arquetipo_alvo] = min(100.0, atleta["maestria"][arquetipo_alvo] + (score / 350))
    
    # 3. DNA Especialista
    if atleta["maestria"][arquetipo_alvo] >= 90:
        atleta["dna"] = f"ESPECIALISTA: {arquetipo_alvo.upper()}"
    
    atleta["overall"] = calcular_overall(atleta)
    db[id_atleta] = atleta
    salvar_db(db)
    return atleta

# --- 4. INTERFACE ---
st.set_page_config(page_title="GOAT TV - CT", layout="wide")
if 'auth' not in st.session_state: st.session_state.auth = False
if 'check_id' not in st.session_state: st.session_state.check_id = False

if not st.session_state.auth:
    st.markdown("<h1 style='text-align: center; color: #ffd700;'>🏟️ CT GOAT TV</h1>", unsafe_allow_html=True)
    id_user = st.text_input("ID DE ATLETA (Ex: GOAT01):").upper().strip()
    
    # BOTÃO VERIFICAR STATUS
    if st.button("🔍 VERIFICAR STATUS DO ATLETA", use_container_width=True):
        st.session_state.check_id = True

    if id_user and st.session_state.check_id:
        db = carregar_db()
        if id_user in db:
            st.success(f"Atleta {id_user} localizado!")
            if st.button("ENTRAR NO CT", use_container_width=True):
                st.session_state.perfil, st.session_state.id_logado, st.session_state.auth = db[id_user], id_user, True
                st.rerun()
        else:
            st.warning("ID não encontrado. Crie sua ficha:")
            nome = st.text_input("NOME COMPLETO:")
            idade = st.number_input("IDADE:", 14, 45, 17)
            tipo = st.radio("SITUAÇÃO:", ["Iniciante (Promessa)", "Já jogo (Veterano)"])
            c1, c2 = st.columns(2)
            with c1: alt = st.number_input("ALTURA (m):", 1.50, 2.15, 1.75)
            with c2: pos = st.selectbox("POSIÇÃO:", ["ATA", "MEI", "DEF"])
            
            arq_ini = st.selectbox("QUAL ARQUÉTIPO VOCÊ QUER SER?", list(REGRAS_TREINO.keys()))
            
            if st.button("FINALIZAR REGISTRO"):
                # Lógica de Piso por Idade
                if idade <= 17: base = 75.0
                elif idade <= 21: base = 80.0
                elif idade <= 25: base = 83.0
                else: base = 85.0
                
                if tipo == "Já jogo (Veterano)": base = 85.0 # Pode ser ajustado com slider se quiser
                
                stats_ini = {k: base for k in ["Drible", "Passe", "Defesa", "Físico", "Finalização", "Velocidade"]}
                maestria_ini = {m: (40.0 if m == arq_ini else 0.0) for m in REGRAS_TREINO.keys()}
                
                db[id_user] = {
                    "nome": nome, "idade": idade, "altura": alt, "posicao": pos,
                    "overall": base, "dna": f"{tipo} ({arq_ini})", "foto": f"{DB_DIR}/{id_user}.png",
                    "stats": stats_ini, "maestria": maestria_ini
                }
                db[id_user]["overall"] = calcular_overall(db[id_user])
                salvar_db(db); st.success("✅ Ficha Criada! Clique em Verificar Status.")

else:
    # --- LOBBY STANDBY ---
    perfil = st.session_state.perfil
    with st.sidebar:
        st.markdown("### 📄 SCOUT CARD")
        if os.path.exists(perfil["foto"]): st.image(perfil["foto"], use_container_width=True)
        st.metric("OVERALL", f"{perfil['overall']}")
        st.write(f"**DNA:** {perfil['dna']}")
        if st.button("SAIR"): st.session_state.auth = False; st.rerun()

    st.title(f"Centro de Treinamento - Atleta {perfil['nome']}")
    
    # 12 BARRAS DE ARQUÉTIPOS
    st.subheader("📊 Maestria de Especialização")
    c_def, c_mei, c_atq = st.columns(3)
    setores = {
        "🛡️ DEFESA": ["O Xerife", "O Libero", "O Carrapato", "O Paredão"],
        "⚙️ MEIO": ["O Maestro", "O Motorzinho", "O Garçom", "O Coringa"],
        "🎯 ATAQUE": ["O Ponta-Liso", "O Pivô", "O Matador", "O Segundo Atacante"]
    }
    
    for i, (setor, arqs) in enumerate(setores.items()):
        with [c_def, c_mei, c_atq][i]:
            st.markdown(f"**{setor}**")
            for a in arqs:
                prog = perfil["maestria"].get(a, 0)
                st.caption(f"{a}: {prog:.1f}%")
                st.progress(prog / 100)

    st.divider()
    # Navegação entre salas...
    c1, c2, c3 = st.columns(3)
    with c1: 
        if st.button("🛡️ SETOR DE DEFESA", use_container_width=True): st.session_state.portal = "DEF"
    with c2: 
        if st.button("⚙️ SETOR DE MEIO", use_container_width=True): st.session_state.portal = "MEI"
    with c3: 
        if st.button("🎯 SETOR DE ATAQUE", use_container_width=True): st.session_state.portal = "ATQ"

    # Execução de Treino (Exemplo Ponta-Liso / Slalom U)
    if st.session_state.get('executando_treino') == "DRIBLE":
        score = 1500 # Simulação do seu engine de drible
        st.session_state.perfil = processar_treino(st.session_state.id_logado, "O Ponta-Liso", score)
        st.session_state.executando_treino = None
        st.rerun()
