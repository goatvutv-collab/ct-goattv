import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import streamlit as st

def gerar_radar(stats):
    labels = ["Habil. ofensiva", "Drible", "Passe rasteiro", "Finalização", "Velocidade", "Contato físico"]
    values = [stats.get(l, 70) for l in labels]
    fig = go.Figure(data=go.Scatterpolar(r=values, theta=labels, fill='toself', line_color='#ffd700'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=False)), paper_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
    return fig

def desenhar_personalidade(pers):
    # Baseado na sua Foto 11
    col1, col2 = st.columns(2)
    with col1:
        st.write("Altruísta vs Individualista")
        st.progress(pers["Altruísmo"] / 100)
        st.write("Raça vs Compostura")
        st.progress(pers["Raça"] / 100)
    with col2:
        st.write("Técnica vs Físico")
        st.progress(pers["Técnica"] / 100)
        st.write("Intuição vs Instinto")
        st.progress(pers["Intuição"] / 100)
