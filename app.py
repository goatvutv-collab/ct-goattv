import streamlit as st
import json
import os
from PIL import Image

# --- 1. IMPORTAÇÃO DOS MÓDULOS (SALAS) ---
import defesa
import meio_campo
import ataque

# --- 2. CONFIGURAÇÃO DE DIRETÓRIOS E BANCO DE DADOS ---
# No Render, usamos /app/ para pastas persistentes
DB_DIR = "/app/fotos_atletas" if os.path.exists("/app/fotos_atletas") else "fotos_atletas"
DB_FILE = os.path.join(DB_DIR, "jogadores_goat.json")

if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)

# --- 3. FUNÇÕES DE INTELIGÊNCIA ---
def carregar_db():
    if not os.path.exists(DB_FILE): return {}
    try:
        with open(DB_FILE, "r") as f: return json.load(f)
    except: return {}

def salvar_db(dados):
    with open(DB_FILE, "w") as f: json.dump(dados, f, indent=4)

def processar_resultado_treino(id_atleta, modulo, score):
    db = carregar_db()
    if id_atleta not in db: return None
    atleta = db[id_atleta]
    
    # Lógica de Evolução (Exemplo: Módulo de Drible)
    if modulo == "DRIBLE":
        ganho = (score / 1000) * 2.5
        perda = (score / 1000) * 1.5
        atleta["stats"]["Drible"] = round(atleta["stats"].get("Drible", 80) + ganho, 1)
        atleta["stats"]["Defesa"] = round(atleta["stats"].get("Defesa", 80) - perda, 1)
        
    # Recalcula o Overall Geral
    atleta["overall"] = round(sum(atleta["stats"].values()) / len(atleta["stats"]), 1)
    db[id_atleta] = atleta
    salvar_db(db)
    return atleta

# --- 4. CONFIGURAÇÃO DA INTERFACE ---
st.set_page_config(page_title="GOAT TV - CT", layout="centered")

if 'auth' not in st.session_state: 
    st.session_state.auth = False
if 'portal' not in st.session_state:
    st.session_state.portal = None

# --- 5. TELA DE LOGIN / REGISTRO ---
if not st.session_state.auth:
    st.markdown("<h1 style='text-align: center; color: #ffd700;'>🏟️ CT GOAT TV</h1>", unsafe_allow_html=True)
    id_user = st.text_input("DIGITE SEU ID DE ATLETA (Ex: GOAT01):").upper().strip()
    
    if id_user:
        db = carregar_db()
        if id_user in db:
            if st.button(f"ENTRAR NO CT: {id_user}", use_container_width=True):
                st.session_state.perfil = db[id_user]
                st.session_state.id_logado = id_user
                st.session_state.auth = True
                st.rerun()
        else:
            st.warning("ID não encontrado. Se você é novo, crie sua ficha abaixo:")
            nome = st.text_input("NOME COMPLETO:")
            idade = st.number_input("IDADE:", min_value=14, max_value=45, value=18)
            foto = st.file_uploader("SUA MELHOR FOTO (JPG/PNG):", type=['jpg', 'png', 'jpeg'])
            
            if st.button("FINALIZAR CADASTRO E GERAR FICHA"):
                if nome and foto:
                    # Regra de Overall inicial por idade
                    base = 85 if idade > 22 else (80 if 20 <= idade <= 22 else 75)
                    foto_path = os.path.join(DB_DIR, f"{id_user}.png")
                    Image.open(foto).save(foto_path)
                    
                    db[id_user] = {
                        "nome": nome, "idade": idade, "overall": base, "dna": "Recruta", "foto": foto_path,
                        "stats": {"Drible": base, "Passe": base, "Defesa": base, "Físico": base}
                    }
                    salvar_db(db)
                    st.success("✅ Tudo pronto! Agora é só digitar seu ID lá em cima para acessar.")

# --- 6. LOBBY DO JOGADOR (DENTRO DO CT) ---
else:
    perfil = st.session_state.perfil
    
    # BARRA LATERAL (MENU SANDUÍCHE NO CELULAR)
    with st.sidebar:
        st.markdown("<h2 style='text-align: center;'>📄 SCOUT CARD</h2>", unsafe_allow_html=True)
        if os.path.exists(perfil["foto"]):
            st.image(perfil["foto"], use_container_width=True)
        
        st.markdown(f"<h3 style='text-align: center;'>{perfil['nome']}</h3>", unsafe_allow_html=True)
        st.divider()
        st.metric("OVERALL", f"{perfil['overall']}")
        st.write(f"**DNA:** {perfil['dna']}")
        
        if st.button("SAIR DO SISTEMA"):
            st.session_state.auth = False
            st.session_state.portal = None
            st.rerun()
        st.caption("GOAT TV FEDERATION © 2026")

    # ÁREA PRINCIPAL
    st.title(f"Bem-vindo ao CT, {perfil['nome'].split()[0]}!")
    st.write("Selecione o setor para iniciar as atividades:")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🛡️ DEFESA", use_container_width=True): st.session_state.portal = "DEF"
    with col2:
        if st.button("⚙️ MEIO", use_container_width=True): st.session_state.portal = "MEI"
    with col3:
        if st.button("🎯 ATAQUE", use_container_width=True): st.session_state.portal = "ATQ"

    st.divider()

    # ACESSO ÀS SALAS TÉCNICAS
    portal = st.session_state.get('portal')
    
    if portal == "DEF":
        defesa.mostrar_sala_defesa()
    elif portal == "MEI":
        meio_campo.mostrar_sala_meio()
    elif portal == "ATQ":
        ataque.mostrar_sala_ataque()
        
        # LOGICA DO MINI-GAME (Só ativa se o botão de treino for clicado no arquivo ataque.py)
        if st.session_state.get('executando_treino') == "DRIBLE":
            if os.path.exists("drible_engine.py"):
                import drible_engine
                score = drible_engine.executar_treino("DRIBLE")
                
                # Atualiza os dados no JSON e no Perfil atual
                novo_perfil = processar_resultado_treino(st.session_state.id_logado, "DRIBLE", score)
                st.session_state.perfil = novo_perfil
                st.session_state.executando_treino = None # Limpa o estado
                st.success(f"Treino Finalizado! Score: {score}")
                st.rerun()
            else:
                st.error("Erro: Módulo drible_engine.py não encontrado no servidor.")
