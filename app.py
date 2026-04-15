import streamlit as st
from PIL import Image
import os
import sys

# Garante que o Python ache as pastas locais no deploy
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.db_handler import carregar_db, salvar_db
from engine.calculos import processar_treino_master, calcular_ovr_supremo
from engine.regras import STATS_BASE_PES, REGRAS_TREINO
from interface.visual import gerar_radar, desenhar_personalidade

st.set_page_config(page_title="GOAT TV", layout="wide")

# --- LOGIN E RECEPTOR SENSORIAL ---
if 'auth' not in st.session_state: st.session_state.auth = False

# [Lógica de receptor sensorial e Login/Registro aqui - use a do turno anterior]
# Importante: No registro, inicialize os 28 stats da lista STATS_BASE_PES
