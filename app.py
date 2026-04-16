import streamlit as st
import os
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image

# Importando das casinhas modulares
from database.db_handler import carregar_db, salvar_db
from engine.regras import REGRAS_TREINO, REQUISITOS_SKILLS, REQUISITOS_ESTILOS
from engine.calculos import calcular_ovr_supremo, processar_treino_master
from interface.visual import gerar_radar

# Importando os setores
import setores.defesa.portal as defesa
import setores.meio_campo.portal as meio_campo
import setores.ataque.portal as ataque

st.set_page_config(page_title="GOAT TV - CT SUPREMO", layout="wide", initial_sidebar_state="expanded")

if 'auth' not in st.session_state: st.session_state.auth = False

# [Aqui entra toda a lógica de LOGIN, REGISTRO e TABS que você mandou, 
# mas usando as funções importadas acima para processar os dados]
