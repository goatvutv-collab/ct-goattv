import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def gerar_radar(stats):
    labels = list(stats.keys())[:8]
    values = [stats[l] for l in labels]
    fig = go.Figure(data=go.Scatterpolar(r=values, theta=labels, fill='toself', line_color='#ffd700', fillcolor='rgba(255, 215, 0, 0.3)'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=False)), paper_bgcolor="rgba(0,0,0,0)", font=dict(color="white"), showlegend=False)
    return fig

def gerar_grafico_evolucao(historico, idade_atleta):
    df = pd.DataFrame(historico)
    df["esperado"] = df["ovr"].iloc[0] + (df["idade"] - idade_atleta) * 1.2
    fig = px.line(df, x="idade", y=["ovr", "esperado"], color_discrete_sequence=["#ffd700", "#ff00ff"])
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
    return fig
