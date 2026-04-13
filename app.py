import streamlit as st
import json
import os
from PIL import Image

# --- 1. MÓDULOS E BANCO DE DADOS ---
import defesa, meio_campo, ataque
DB_DIR = "fotos_atletas" 
DB_FILE = os.path.join(DB_DIR, "jogadores_goat.json")

if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)

# --- 2. TABELAS TÉCNICAS (LÓGICA PES & REGRAS) ---
PESOS = {
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

# --- 3. FUNÇÕES TÉCNICAS ---
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
    pesos_pos = PESOS.get(pos, PESOS["MEI"])
    ovr_base = sum(stats[s] * pesos_pos[s] for s in pesos_pos) / sum(pesos_pos.values())
    bonus = 1 if (pos == "DEF" and alt >= 1.85) or (pos == "ATA" and alt >= 1.88) else 0
    return int(ovr_base + bonus + 0.5)

def processar_treino_master(id_atleta, arquetipo_alvo, score):
    db = carregar_db()
    if id_atleta not in db: return None
    atleta = db[id_atleta]
    regra = REGRAS_TREINO.get(arquetipo_alvo)
    rendimento = (score / 2500)

    for s in regra["sobe"]: atleta["stats"][s] = round(atleta["stats"].get(s, 80) + rendimento, 1)
    for d in regra["desce"]: atleta["stats"][d] = round(atleta["stats"].get(d, 80) - (rendimento * 0.4), 1)

    atleta["maestria"][arquetipo_alvo] = min(100.0, atleta["maestria"].get(arquetipo_alvo, 0) + (score / 350))
    if atleta["maestria"][arquetipo_alvo] >= 90: atleta["dna"] = f"ESPECIALISTA: {arquetipo_alvo.upper()}"

    atleta["overall"] = calcular_overall_ponderado(atleta)
    db[id_atleta] = atleta
    salvar_db(db)
    return atleta

# --- 4. INTERFACE ---
st.set_page_config(page_title="GOAT TV - CT", layout="wide")
if 'auth' not in st.session_state: st.session_state.auth = False

# --- 5. TELA DE ACESSO ---
if not st.session_state.auth:
    st.markdown("<h1 style='text-align: center; color: #ffd700;'>🏟️ CT GOAT TV</h1>", unsafe_allow_html=True)
    id_user = st.text_input("DIGITE SEU ID DE ATLETA:").upper().strip()
    
    if st.button("🔍 VERIFICAR STATUS", use_container_width=True):
        db = carregar_db()
        if id_user and id_user in db:
            st.session_state.perfil = db[id_user]
            st.session_state.id_logado = id_user
            st.session_state.auth = True
            st.rerun()
        elif id_user:
            st.error("ID não encontrado. Cadastre-se abaixo.")

    # Bloco de Cadastro
    if id_user and id_user not in carregar_db():
        st.divider()
        nome = st.text_input("NOME COMPLETO:")
        idade = st.number_input("IDADE:", 14, 45, 17)
        tipo = st.radio("SITUAÇÃO:", ["Iniciante (Promessa)", "Já jogo (Veterano)"])
        c1, c2 = st.columns(2)
        with c1: alt = st.number_input("ALTURA (m):", 1.50, 2.15, 1.75)
        with c2: pos = st.selectbox("POSIÇÃO:", ["ATA", "MEI", "DEF"])
        arq_ini = st.selectbox("ARQUÉTIPO DESEJADO:", list(REGRAS_TREINO.keys()))
        
        if st.button("🚀 FINALIZAR REGISTRO E ENTRAR"):
            base_ovr = 75.0 if idade <= 17 else 82.0
            stats_ini = {k: base_ovr for k in ["Drible", "Passe", "Defesa", "Físico", "Finalização", "Velocidade"]}
            maestria_ini = {m: (40.0 if m == arq_ini else 0.0) for m in REGRAS_TREINO.keys()}
            
            db = carregar_db()
            db[id_user] = {
                "nome": nome, "idade": idade, "altura": alt, "posicao": pos,
                "overall": base_ovr, "dna": f"{tipo} ({arq_ini})", "foto": f"fotos_atletas/{id_user}.png",
                "stats": stats_ini, "maestria": maestria_ini
            }
            db[id_user]["overall"] = calcular_overall_ponderado(db[id_user])
            salvar_db(db)
            st.session_state.perfil = db[id_user]
            st.session_state.id_logado = id_user
            st.session_state.auth = True
            st.rerun()

# --- 6. LOBBY (AGORA COM AS BARRAS NA LATERAL) ---
else:
    perfil = st.session_state.perfil
    
    with st.sidebar:
        st.markdown("<h2 style='text-align: center;'>📄 SCOUT CARD</h2>", unsafe_allow_html=True)
        if os.path.exists(perfil["foto"]): st.image(perfil["foto"], use_container_width=True)
        st.metric("OVERALL", f"{perfil['overall']}")
        st.write(f"**DNA:** {perfil['dna']}")
        
        st.divider()
        
        # --- AS 12 BARRINHAS NA LATERAL ---
        st.markdown("### 📊 MAESTRIA")
        setores_map = {
            "🛡️ DEFESA": ["O Xerife", "O Libero", "O Carrapato", "O Paredão"],
            "⚙️ MEIO": ["O Maestro", "O Motorzinho", "O Garçom", "O Coringa"],
            "🎯 ATAQUE": ["O Ponta-Liso", "O Pivô", "O Matador", "O Segundo Atacante"]
        }
        
        for setor, arqs in setores_map.items():
            st.markdown(f"**{setor}**")
            for a in arqs:
                prog = perfil["maestria"].get(a, 0)
                st.caption(f"{a}: {prog:.1f}%")
                st.progress(min(prog / 100, 1.0))
        
        st.divider()
        if st.button("SAIR"): st.session_state.auth = False; st.rerun()

    # --- ÁREA CENTRAL (LIMPA E FOCADA NAS PORTAS) ---
    st.title(f"Centro de Treinamento - {perfil['nome']}")
    st.write("Selecione o setor para treinar. Sua evolução é monitorada no Scout Card lateral.")
    
    c1, c2, c3 = st.columns(3)
    with c1: 
        if st.button("🛡️ SETOR DE DEFESA", use_container_width=True): st.session_state.portal = "DEF"
    with c2: 
        if st.button("⚙️ SETOR DE MEIO", use_container_width=True): st.session_state.portal = "MEI"
    with c3: 
        if st.button("🎯 SETOR DE ATAQUE", use_container_width=True): st.session_state.portal = "ATQ"

    st.divider()
    
    # Execução das Salas
    portal = st.session_state.get('portal')
    if portal == "DEF": defesa.mostrar_sala_defesa()
    elif portal == "MEI": meio_campo.mostrar_sala_meio()
    elif portal == "ATQ":
        ataque.mostrar_sala_ataque()
        if st.session_state.get('executando_treino') == "DRIBLE":
            st.session_state.perfil = processar_treino_master(st.session_state.id_logado, "O Ponta-Liso", 1500)
            st.session_state.executando_treino = None
            st.rerun()
