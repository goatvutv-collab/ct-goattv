import plotly.graph_objects as go
import streamlit as st

def gerar_radar(stats):
    labels = ["Habil. ofensiva", "Drible", "Passe rasteiro", "Finalização", "Velocidade", "Contato físico", "Habil. defensiva", "Resistência"]
    values = [stats.get(l, 70) for l in labels]
    fig = go.Figure(data=go.Scatterpolar(r=values, theta=labels, fill='toself', line_color='#ffd700', fillcolor='rgba(255, 215, 0, 0.3)'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=False)), paper_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
    return fig

def desenhar_personalidade(pers):
    st.write("### 🧠 Matriz de Personalidade")
    c1, c2 = st.columns(2)
    with c1:
        st.write("**Raça**")
        st.progress(pers.get("Raça", 50) / 100)
        st.write("**Técnica**")
        st.progress(pers.get("Técnica", 50) / 100)
    with c2:
        st.write("**Altruísmo**")
        st.progress(pers.get("Altruísmo", 50) / 100)
        st.write("**Compostura**")
        st.progress(pers.get("Compostura", 50) / 100)
