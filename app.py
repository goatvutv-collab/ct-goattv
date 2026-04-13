import streamlit as st
import json
import os
from PIL import Image

# --- 1. MÓDULOS E BANCO DE DADOS ---
import defesa, meio_campo, ataque
DB_DIR = "/app/fotos_atletas" if os.path.exists("/app/fotos_atletas") else "fotos_atletas"
DB_FILE = os.path.join(DB_DIR, "jogadores_goat.json")
if not os.path.exists(DB_DIR): os.makedirs(DB_DIR)

# --- 2. TABELA DE PESOS (PES) E REGRAS DE TREINO (+3/-3) ---
PESOS = {
    "ATA": {"Drible": 5, "Passe": 3, "Defesa": 1, "Físico": 4, "Finalização": 5, "Velocidade": 4},
    "MEI": {"Drible": 4, "Passe": 5, "Defesa": 2, "Físico": 3, "Finalização": 3, "Velocidade": 3},
    "DEF": {"Drible": 1, "Passe": 3, "Defesa": 5, "Físico": 5, "Finalização": 1, "Velocidade": 3}
}

REGRAS_TREINO = {
    "Muralha Fixa":        {"sobe": ["Defesa", "Físico", "Passe"], "desce": ["Drible", "Velocidade", "Finalização"]},
    "Perseguidor":         {"sobe": ["Velocidade", "Defesa", "Físico"], "desce": ["Passe", "Finalização", "Drible"]},
    "Back de Saída":       {"sobe": ["Passe", "Defesa", "Velocidade"], "desce": ["Finalização", "Drible", "Físico"]},
    "Antena Tática":       {"sobe": ["Defesa", "Passe", "Drible"], "desce": ["Físico", "Velocidade", "Finalização"]},
    "Maestro":             {"sobe": ["Passe", "Drible", "Velocidade"], "desce": ["Físico", "Defesa", "Finalização"]},
    "Infiltrador":         {"sobe": ["Finalização", "Drible", "Velocidade"], "desce": ["Defesa", "Passe", "Físico"]},
    "Motor de Arque":      {"sobe": ["Físico", "Passe", "Velocidade"], "desce": ["Drible", "Finalização", "Defesa"]},
    "Organizador":         {"sobe": ["Passe", "Defesa", "Físico"], "desce": ["Velocidade", "Drible", "Finalização"]},
    "Pivô de Ferro":       {"sobe": ["Físico", "Finalização", "Passe"], "desce": ["Velocidade", "Drible", "Defesa"]},
    "Homem-Gol":           {"sobe": ["Finalização", "Velocidade", "Drible"], "desce": ["Defesa", "Passe", "Físico"]},
    "Segundo Atacante":    {"sobe": ["Drible", "Finalização", "Passe"], "desce": ["Físico", "Defesa", "Velocidade"]},
    "Tanque de Explosão":  {"sobe": ["Velocidade", "Físico", "Finalização"], "desce": ["Defesa", "Passe", "Drible"]}
}

# --- 3. FUNÇÕES TÉCNICAS ---
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

def processar_treino(id_atleta, modulo, score):
    db = carregar_db()
    atleta = db[id_atleta]
    regra = REGRAS_TREINO.get(modulo)
    rendimento = (score / 2500)
    
    # 1. Atualiza Atributos (+3/-3)
    for s in regra["sobe"]: atleta["stats"][s] = round(atleta["stats"][s] + rendimento, 1)
    for d in regra["desce"]: atleta["stats"][d] = round(atleta["stats"][d] - (rendimento * 0.4), 1)
    
    # 2. Atualiza Maestria (A Barrinha do Arquétipo)
    atleta["maestria"][modulo] = min(100.0, atleta["maestria"][modulo] + (score / 350))
    
    # 3. Se bater 90%, vira Especialista
    if atleta["maestria"][modulo] >= 90: atleta["dna"] = f"ESPECIALISTA: {modulo.upper()}"
    
    atleta["overall"] = calcular_overall(atleta)
    db[id_atleta] = atleta
    salvar_db(db)
    return atleta

# --- 4. INTERFACE ---
st.set_page_config(page_title="GOAT TV - CT", layout="wide")
if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    # TELA DE LOGIN / REGISTRO (Com a lógica de idade e veterano)
    st.markdown("<h1 style='text-align: center; color: #ffd700;'>🏟️ CT GOAT TV</h1>", unsafe_allow_html=True)
    id_user = st.text_input("ID DE ATLETA:").upper().strip()
    
    if id_user:
        db = carregar_db()
        if id_user in db:
            if st.button(f"ENTRAR: {id_user}", use_container_width=True):
                st.session_state.perfil, st.session_state.id_logado, st.session_state.auth = db[id_user], id_user, True
                st.rerun()
        else:
            st.warning("Novo Registro:")
            nome = st.text_input("NOME COMPLETO:")
            idade = st.number_input("IDADE:", 14, 45, 17)
            tipo = st.radio("TIPO:", ["Iniciante (Promessa)", "Já jogo (Veterano)"])
            c1, c2 = st.columns(2)
            with c1: alt = st.number_input("ALTURA (m):", 1.50, 2.10, 1.75)
            with c2: pos = st.selectbox("POSIÇÃO:", ["ATA", "MEI", "DEF"])
            arq_ini = st.selectbox("ARQUÉTIPO DE INÍCIO:", list(REGRAS_TREINO.keys()))
            foto = st.file_uploader("FOTO:")

            if st.button("GERAR FICHA COM BARRAS DE MAESTRIA"):
                # Define Base por Idade
                if idade <= 17: base = 75.0
                elif idade <= 21: base = 80.0
                elif idade <= 25: base = 83.0
                else: base = 85.0
                
                if tipo == "Já jogo (Veterano)": base = st.slider("Overall Base:", 80, 95, 85)
                
                stats_ini = {k: base for k in ["Drible", "Passe", "Defesa", "Físico", "Finalização", "Velocidade"]}
                maestria_ini = {m: (40.0 if m == arq_ini else 0.0) for m in REGRAS_TREINO.keys()}
                
                foto_path = os.path.join(DB_DIR, f"{id_user}.png")
                if foto: Image.open(foto).save(foto_path)
                
                db[id_user] = {
                    "nome": nome, "idade": idade, "altura": alt, "posicao": pos,
                    "overall": base, "dna": f"{tipo} ({arq_ini})", "foto": foto_path,
                    "stats": stats_ini, "maestria": maestria_ini
                }
                salvar_db(db); st.success("Ficha Sincronizada! Logue com seu ID.")

else:
    # --- LOBBY DO JOGADOR ---
    perfil = st.session_state.perfil
    with st.sidebar:
        st.markdown("### 📄 SCOUT CARD")
        if os.path.exists(perfil["foto"]): st.image(perfil["foto"], use_container_width=True)
        st.metric("OVERALL", f"{perfil['overall']}")
        st.write(f"**DNA:** {perfil['dna']}")
        if st.button("SAIR"): st.session_state.auth = False; st.rerun()

    st.title(f"Centro de Treinamento - Atleta {perfil['nome']}")
    
    # --- AS 12 BARRAS (ÁREA STANDBY) ---
    st.subheader("📊 Maestria de Estilo de Jogo")
    col_d, col_m, col_a = st.columns(3)
    setores = {
        "🛡️ DEFESA": ["Muralha Fixa", "Perseguidor", "Back de Saída", "Antena Tática"],
        "⚙️ MEIO": ["Maestro", "Infiltrador", "Motor de Arque", "Organizador"],
        "🎯 ATAQUE": ["Pivô de Ferro", "Homem-Gol", "Segundo Atacante", "Tanque de Explosão"]
    }
    
    for i, (setor, modulos) in enumerate(setores.items()):
        with [col_d, col_m, col_a][i]:
            st.markdown(f"**{setor}**")
            for m in modulos:
                prog = perfil["maestria"].get(m, 0)
                st.caption(f"{m}: {prog:.1f}%")
                st.progress(prog / 100)

    st.divider()
    # Botões para os setores...
    c1, c2, c3 = st.columns(3)
    with c1: 
        if st.button("🛡️ DEFESA", use_container_width=True): st.session_state.portal = "DEF"
    with c2: 
        if st.button("⚙️ MEIO", use_container_width=True): st.session_state.portal = "MEI"
    with c3: 
        if st.button("🎯 ATAQUE", use_container_width=True): st.session_state.portal = "ATQ"

    # Salas... (Seção de execução de treino igual à anterior)
    if st.session_state.get('executando_treino') == "DRIBLE":
        # Simulação: O treino de Drible alimenta o "Tanque de Explosão"
        st.session_state.perfil = processar_treino(st.session_state.id_logado, "Tanque de Explosão", 1500)
        st.session_state.executando_treino = None
        st.rerun()
