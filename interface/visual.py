# --- interface/visual.py ---
import plotly.graph_objects as go
import streamlit as st

def definir_estilo_exibicao(atleta, requisitos_estilos):
    maestrias = atleta.get("maestria", {})
    if not any(v > 0 for v in maestrias.values()): return "Promessa"
    dominante = max(maestrias, key=maestrias.get)
    for estilo, dnas in requisitos_estilos.items():
        if dominante in dnas: return estilo
    return "Especialista"

def gerar_radar(stats):
    labels = ["Talento ofensivo", "Drible", "Passe rasteiro", "Finalização", "Velocidade", "Contato físico", "Talento defensivo", "Resistência"]
    values = [stats.get(l, 40) for l in labels]
    fig = go.Figure(data=go.Scatterpolar(r=values, theta=labels, fill='toself', line_color='#ffd700', fillcolor='rgba(255, 215, 0, 0.3)'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[40, 99])), paper_bgcolor="rgba(0,0,0,0)", showlegend=False)
    return fig

def desenhar_personalidade(pers):
    st.markdown("### 🧠 Mentalidade")
    c1, c2 = st.columns(2)
    with c1:
        st.write(f"🔥 **Raça:** {pers.get('Raça', 50)}%"); st.progress(pers.get('Raça', 50)/100)
        st.write(f"🎨 **Técnica:** {pers.get('Técnica', 50)}%"); st.progress(pers.get('Técnica', 50)/100)
    with c2:
        st.write(f"🤝 **Altruísmo:** {pers.get('Altruísmo', 50)}%"); st.progress(pers.get('Altruísmo', 50)/100)
        st.write(f"🧊 **Compostura:** {pers.get('Compostura', 50)}%"); st.progress(pers.get('Compostura', 50)/100)
