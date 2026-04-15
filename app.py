import streamlit as st
import os
from PIL import Image

# --- 1. CONEXÃO COM AS CASINHAS (MÓDULOS) ---
from database.db_handler import carregar_db, salvar_db
from engine.regras import REQUISITOS_SKILLS, REGRAS_TREINO
from engine.calculos import processar_treino_master, calcular_ovr_supremo
from interface.visual import gerar_radar, gerar_evolucao

# Import dos Setores (Netos)
import setores.defesa, setores.meio_campo, setores.ataque

# --- 2. CONFIGURAÇÃO INICIAL ---
st.set_page_config(page_title="GOAT TV - CT SUPREMO", layout="wide", initial_sidebar_state="expanded")

if 'auth' not in st.session_state: st.session_state.auth = False
if 'portal' not in st.session_state: st.session_state.portal = None

# --- 3. RECEPTOR SENSORIAL (Sincronização com Mini-games) ---
if st.session_state.get('score_pendente') is not None:
    db = carregar_db()
    id_log = st.session_state.id_logado
    # O Cérebro Master processa o resultado vindo do setor
    db[id_log] = processar_treino_master(db[id_log], st.session_state.arquetipo_pendente, st.session_state.score_pendente)
    salvar_db(db)
    st.session_state.perfil = db[id_log] # Atualiza o perfil em standby
    st.session_state.score_pendente = None # Limpa o sinal
    st.success("🧠 Desempenho processado e Scout Card atualizado!")
    st.rerun()

# --- 4. TELA DE ACESSO (LOGIN / REGISTRO) ---
if not st.session_state.auth:
    st.markdown("<h1 style='text-align: center; color: #ffd700;'>🏟️ CT GOAT TV</h1>", unsafe_allow_html=True)
    id_user = st.text_input("DIGITE SEU ID DE ATLETA (Ex: GOAT01):").upper().strip()
    
    if st.button("🔍 ACESSAR CARREIRA", use_container_width=True):
        db = carregar_db()
        if id_user in db: 
            st.session_state.perfil, st.session_state.id_logado, st.session_state.auth = db[id_user], id_user, True
            st.rerun()
        elif id_user: st.error("ID não cadastrado. Preencha a ficha técnica abaixo.")

    if id_user and id_user not in carregar_db():
        with st.form("registro_supremo"):
            st.subheader("📝 REGISTRO DE NOVA PROMESSA")
            n = st.text_input("NOME COMPLETO:")
            idade = st.number_input("IDADE:", 15, 45, 17)
            t = st.radio("JÁ FOI JOGADOR?", ["Veterano (Já Jogo)", "Iniciante (Promessa)"])
            c1, c2 = st.columns(2)
            alt = c1.number_input("ALTURA (m):", 1.5, 2.2, 1.78)
            pso = c2.number_input("PESO (kg):", 50, 130, 75)
            pos = st.selectbox("POSIÇÃO PRINCIPAL:", ["ATA", "MEI", "DEF"])
            arq_ini = st.selectbox("ARQUÉTIPO DE INÍCIO:", list(REGRAS_TREINO.keys()))
            ft = st.file_uploader("FOTO OFICIAL:", type=['jpg', 'png', 'jpeg'])
            
            if st.form_submit_button("🚀 INICIAR CARREIRA"):
                if n and ft:
                    # Lógica de Piso por Idade + Bônus Veterano
                    base = 75.0 if idade <= 18 else (80.0 if idade <= 22 else 85.0)
                    if t == "Veterano (Já Jogo)": base += 2.0
                    
                    path = f"fotos_atletas/{id_user}.png"; Image.open(ft).save(path)
                    db = carregar_db()
                    db[id_user] = {
                        "nome": n, "idade": idade, "altura": alt, "peso": pso, "posicao": pos, "overall": base,
                        "foto": path, "dna": t, "status": "Saudável", "habilidades": [],
                        "stats": {k: base for k in ["Habilid. ofensiva", "Controle de bola", "Drible", "Passe rasteiro", "Passe alto", "Finalização", "Velocidade", "Resistência", "Desarme", "Resistência a lesão", "Força do chute", "Raça"]},
                        "personalidade": {"Altruísmo": 50, "Raça": 50, "Técnica": 50, "Compostura": 50},
                        "maestria": {m: (40.0 if m == arq_ini else 0.0) for m in REGRAS_TREINO.keys()},
                        "historico_ovr": [{"idade": idade, "ovr": base}],
                        "posicoes": {"CA": "B", "MEI": "A", "ZC": "C"} # Grades PES
                    }
                    salvar_db(db); st.rerun()

# --- 5. LOBBY CENTRAL (SESSÃO ATIVA) ---
else:
    p = st.session_state.perfil
    status = p.get("status", "Saudável")

    # --- SIDEBAR (STANDBY): O CORAÇÃO VISUAL ---
    with st.sidebar:
        st.markdown("<h2 style='text-align: center;'>📄 SCOUT CARD</h2>", unsafe_allow_html=True)
        if os.path.exists(p["foto"]): st.image(p["foto"], use_container_width=True)
        
        st.metric("OVERALL", p["overall"])
        st.write(f"**DNA:** {p['dna']}")
        st.write(f"**STATUS:** {status}")
        st.write(f"**BIOMETRIA:** {p['peso']}kg | {p['altura']}m")
        
        st.divider()
        st.subheader("🔭 Lab de Skills")
        for sk, reqs in REQUISITOS_SKILLS.items():
            if sk not in p["habilidades"]:
                # Mostra o progresso baseado no atributo principal da skill
                at_nome = list(reqs.keys())[0]
                meta = reqs[at_nome]
                atual = p["stats"].get(at_nome, 70)
                if (meta - atual) <= 12:
                    st.caption(f"{sk} ({atual}/{meta})")
                    st.progress(min(atual/meta, 1.0))
        
        st.divider()
        st.subheader("📊 Maestrias")
        for m, val in p["maestria"].items():
            if val > 0:
                st.caption(f"{m}: {val:.1f}%")
                st.progress(min(val/100, 1.0))
        
        if st.button("SAIR DO SISTEMA"): st.session_state.auth = False; st.rerun()

    # --- ÁREA DE ABAS (ORGANIZAÇÃO PES) ---
    st.title(f"Centro de Excelência - {p['nome'].split()[0]}")
    tab_ct, tab_atleta, tab_evol, tab_edit = st.tabs(["🎮 Campo de Treino", "🧠 Atleta", "📈 Evolução", "⚙️ Configurações"])

    with tab_ct:
        if status == "Incapacitado":
            st.error("🚑 DEPARTAMENTO MÉDICO: Você está impossibilitado de treinar hoje.")
            if st.button("🧊 TRATAMENTO INTENSIVO"):
                db = carregar_db(); db[st.session_state.id_logado]["status"] = "Saudável"
                salvar_db(db); st.rerun()
        else:
            c1, c2 = st.columns([1.5, 1])
            with c1:
                st.plotly_chart(gerar_radar(p["stats"]), use_container_width=True)
            with c2:
                st.subheader("Acessar Portais")
                if st.button("🛡️ SETOR DE DEFESA", use_container_width=True): st.session_state.portal = "DEF"
                if st.button("⚙️ SETOR DE MEIO", use_container_width=True): st.session_state.portal = "MEI"
                if st.button("🎯 SETOR DE ATAQUE", use_container_width=True): st.session_state.portal = "ATQ"
            
            # Chamada dos Portais
            if st.session_state.portal == "DEF": setores.defesa.mostrar_sala_defesa()
            elif st.session_state.portal == "MEI": setores.meio_campo.mostrar_sala_meio()
            elif st.session_state.portal == "ATQ": setores.ataque.mostrar_sala_ataque()

    with tab_atleta:
        st.subheader("🧠 Matriz de Personalidade")
        c1, c2 = st.columns(2)
        with c1:
            for k, v in p["personalidade"].items():
                st.write(f"**{k}:** {v}%")
                st.progress(v/100)
        with c2:
            st.subheader("📍 Domínio de Posição")
            for pos, grade in p["posicoes"].items():
                st.write(f"**{pos}:** {grade}")

    with tab_evol:
        st.subheader("📊 Folha de Evolução")
        st.plotly_chart(gerar_evolucao(p["historico_ovr"], p["idade"]), use_container_width=True)

    with tab_edit:
        st.subheader("🔧 Reedição de Perfil")
        with st.form("edicao_total"):
            new_n = st.text_input("Nome:", value=p["nome"])
            new_p = st.number_input("Peso:", value=p["peso"])
            new_a = st.number_input("Altura:", value=p["altura"])
            nova_ft = st.file_uploader("Trocar Foto:")
            if st.form_submit_button("💾 SALVAR ALTERAÇÕES"):
                db = carregar_db(); id_log = st.session_state.id_logado
                if nova_ft:
                    if os.path.exists(p["foto"]): os.remove(p["foto"])
                    nova_ft_path = f"fotos_atletas/{id_log}.png"; Image.open(nova_ft).save(nova_ft_path)
                    db[id_log]["foto"] = nova_ft_path
                db[id_log].update({"nome": new_n, "peso": new_p, "altura": new_a})
                db[id_log]["overall"] = calcular_ovr_supremo(db[id_log])
                salvar_db(db); st.session_state.perfil = db[id_log]; st.rerun()
