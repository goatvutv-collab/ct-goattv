# --- app.py ---
import streamlit as st
import sys, os
from PIL import Image
import pandas as pd
import plotly.express as px

# Garante que os módulos locais sejam encontrados
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.db_handler import carregar_db, salvar_db
from engine.regras import REGRAS_TREINO, REQUISITOS_SKILLS, STATS_BASE_PES
from engine.calculos import calcular_ovr_supremo, processar_treino_master
from interface.visual import gerar_radar, desenhar_personalidade, exibir_laboratorio_skills

st.set_page_config(page_title="GOAT TV - CT SUPREMO", layout="wide")

if 'auth' not in st.session_state: st.session_state.auth = False

# ... (Lógica de Login e Registro aqui) ...

if st.session_state.auth:
    p = st.session_state.perfil
    
    # --- CORREÇÃO INDEXERROR NO TÍTULO ---
    primeiro_nome = p['nome'].split()[0] if p.get('nome') and p['nome'].strip() else "Atleta"
    st.title(f"Bem-vindo ao CT, {primeiro_nome}")

    # --- TABS PRINCIPAIS ---
    tabs = st.tabs(["🎮 Campo de Treino", "🧠 Atleta", "📈 Evolução", "⚙️ Configurações"])

    with tabs[0]:
        # (Seu código do Campo de Treino...)
        st.write("Área de Treinamento")

    with tabs[1]:
        desenhar_personalidade(p["personalidade"])

    with tabs[2]:
        # Gráfico de evolução
        df = pd.DataFrame(p.get("historico_ovr", []))
        if not df.empty:
            st.plotly_chart(px.line(df, x="idade", y="ovr", title="Crescimento"), use_container_width=True)

    with tabs[3]: # --- ABA DE CONFIGURAÇÕES (EDIÇÃO) ---
        st.subheader("⚙️ Central de Personalização")
        with st.form("edit_perfil_total"):
            col1, col2 = st.columns(2)
            new_n = col1.text_input("Nome de Guerra:", value=p["nome"])
            new_pos = col2.selectbox("Posição Principal:", ["ATA", "MEI", "DEF", "GOL"], index=["ATA", "MEI", "DEF", "GOL"].index(p["posicao"]))
            new_alt = col1.number_input("Altura (m):", value=p["altura"])
            new_peso = col2.number_input("Peso (kg):", value=p["peso"])
            nova_ft = st.file_uploader("Trocar Foto Oficial:")

            if st.form_submit_button("💾 SALVAR ALTERAÇÕES"):
                db = carregar_db()
                id_atleta = st.session_state.id_logado
                if nova_ft:
                    path = f"fotos_atletas/{id_atleta}.png"
                    Image.open(nova_ft).save(path)
                    db[id_atleta]["foto"] = path
                db[id_atleta].update({"nome": new_n, "posicao": new_pos, "altura": new_alt, "peso": new_peso})
                db[id_atleta]["overall"] = calcular_ovr_supremo(db[id_atleta])
                salvar_db(db)
                st.session_state.perfil = db[id_atleta]
                st.success("Perfil atualizado!")
                st.rerun()
