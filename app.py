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

def processar_treino(id_atleta, modulo, score):
    db = carregar_db()
    atleta = db[id_atleta]
    regra = REGRAS_TREINO.get(modulo)
    rendimento = (score / 2500)
    
    for s in regra["sobe"]: atleta["stats"][s] = round(atleta["stats"][s] + rendimento, 1)
    for d in regra["desce"]: atleta["stats"][d] = round(atleta["stats"][d] - (rendimento * 0.4), 1)
    
    atleta["maestria"][modulo] = min(100.0, atleta["maestria"][modulo] + (score / 350))
    if atleta["maestria"][modulo] >= 90: atleta["dna"] = f"ESPECIALISTA: {modulo.upper()}"
    
    atleta["overall"] = calcular_overall(atleta)
    db[id_atleta] = atleta
    salvar_db(db)
    return atleta

# --- 4. INTERFACE ---
st.set_page_config(page_title="GOAT TV - CT", layout="wide")

if 'auth' not in st.session_state: st.session_state.auth = False
if 'check_id' not in st.session_state: st.session_state.check_id = False

# --- 5. TELA DE ACESSO ---
if not st.session_state.auth:
    st.markdown("<h1 style='text-align: center; color: #ffd700;'>🏟️ CT GOAT TV</h1>", unsafe_allow_html=True)
    id_user = st.text_input("DIGITE SEU ID DE ATLETA (Ex: GOAT01):").upper().strip()
    
    btn_check = st.button("🔍 VERIFICAR STATUS DO ATLETA", use_container_width=True)
    
    if id_user and (btn_check or st.session_state.check_id):
        st.session_state.check_id = True
        db = carregar_db()
        
        if id_user in db:
            st.success(f"Atleta {id_user} localizado!")
            if st.button(f"ENTRAR NO CT", use_container_width=True):
                st.session_state.perfil, st.session_state.id_logado, st.session_state.auth = db[id_user], id_user, True
                st.rerun()
        else:
            # --- CADASTRO COMPLETO ---
            st.warning("ID não encontrado. Crie sua ficha abaixo:")
            nome = st.text_input("NOME COMPLETO:")
            idade = st.number_input("IDADE:", 14, 45, 17)
            tipo = st.radio("SITUAÇÃO NO FUTEBOL:", ["Iniciante (Promessa)", "Já jogo (Veterano)"])
            
            c1, c2 = st.columns(2)
            with c1: alt = st.number_input("ALTURA (m):", 1.50, 2.15, 1.75)
            with c2: pos = st.selectbox("POSIÇÃO:", ["ATA", "MEI", "DEF"])
            
            arq_ini = st.selectbox("ARQUÉTIPO INICIAL (Sua Especialidade):", list(REGRAS_TREINO.keys()))
            
            ovr_base = 75.0 # Padrão
            if tipo == "Já jogo (Veterano)":
                ovr_base = st.slider("Qual seu Overall base atual?", 80, 95, 85)
            else:
                if 18 <= idade <= 21: ovr_base = 80.0
                elif 22 <= idade <= 25: ovr_base = 83.0
                elif idade >= 26: ovr_base = 85.0

            foto = st.file_uploader("SUA MELHOR FOTO:")

            if st.button("FINALIZAR REGISTRO E SINCRONIZAR"):
                if nome and foto:
                    stats_ini = {k: ovr_base for k in ["Drible", "Passe", "Defesa", "Físico", "Finalização", "Velocidade"]}
                    # Maestria inicial de 40% no estilo escolhido
                    maestria_ini = {m: (40.0 if m == arq_ini else 0.0) for m in REGRAS_TREINO.keys()}
                    
                    foto_path = os.path.join(DB_DIR, f"{id_user}.png")
                    Image.open(foto).save(foto_path)
                    
                    atleta_obj = {
                        "nome": nome, "idade": idade, "altura": alt, "posicao": pos,
                        "overall": ovr_base, "dna": f"{tipo} ({arq_ini})", "foto": foto_path,
                        "stats": stats_ini, "maestria": maestria_ini
                    }
                    atleta_obj["overall"] = calcular_overall(atleta_obj)
                    
                    db[id_user] = atleta_obj
                    salvar_db(db); st.success("✅ Registro concluído! Clique em Verificar novamente."); st.session_state.check_id = False

# --- 6. LOBBY (STANDBY) ---
else:
    perfil = st.session_state.perfil
    with st.sidebar:
        st.markdown("<h2 style='text-align: center;'>📄 SCOUT CARD</h2>", unsafe_allow_html=True)
        if os.path.exists(perfil["foto"]): st.image(perfil["foto"], use_container_width=True)
        st.metric("OVERALL", f"{perfil['overall']}")
        st.write(f"**DNA:** {perfil['dna']}")
        if st.button("SAIR"): st.session_state.auth = False; st.rerun()

    st.title(f"Bem-vindo ao CT, {perfil['nome'].split()[0]}!")
    
    # --- AS 12 BARRAS (SISTEMA DE RPG) ---
    st.subheader("📊 Maestria de Estilos de Jogo")
    c_def, c_mei, c_atq = st.columns(3)
    setores = {
        "🛡️ DEFESA": ["Muralha Fixa", "Perseguidor", "Back de Saída", "Antena Tática"],
        "⚙️ MEIO": ["Maestro", "Infiltrador", "Motor de Arque", "Organizador"],
        "🎯 ATAQUE": ["Pivô de Ferro", "Homem-Gol", "Segundo Atacante", "Tanque de Explosão"]
    }
    
    for i, (setor, modulos) in enumerate(setores.items()):
        with [c_def, c_mei, c_atq][i]:
            st.markdown(f"**{setor}**")
            for m in modulos:
                prog = perfil["maestria"].get(m, 0)
                st.caption(f"{m}: {prog:.1f}%")
                st.progress(prog / 100)

    st.divider()
    # Botões de Setores e Treinos (Mantenha a lógica de chamada dos arquivos .py aqui)
