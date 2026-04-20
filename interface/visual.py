# --- interface/visual.py ---
import plotly.graph_objects as go
import streamlit as st

def definir_arquetipo_master(atleta, requisitos_estilos):
    """
    Analisa as maestrias e define a 'Peça de Xadrez' no tabuleiro.
    Fiel à lógica de que o dono molda o comportamento do avatar.
    """
    maestrias = atleta.get("maestria", {})
    if not any(v > 0 for v in maestrias.values()): 
        return "Iniciante (Promessa)"
    
    # Identifica o estilo com maior progresso
    melhor_estilo = max(maestrias, key=maestrias.get)
    
    # Mapeia para o Arquétipo Master da Goat TV
    for arq, estilos in requisitos_estilos.items():
        if melhor_estilo in estilos:
            return arq
            
    return "Especialista"

def gerar_radar(stats):
    """
    Radar Chart Supremo. 
    A escala fixa em 40-99 garante que a evolução visual seja real.
    """
    labels = [
        "Habil. ofensiva", "Drible", "Passe rasteiro", "Finalização", 
        "Velocidade", "Contato físico", "Habil. defensiva", "Resistência"
    ]
    
    # Se o atributo não existir, assume 40 (piso técnico do PES)
    values = [stats.get(l, 40) for l in labels]
    
    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=labels,
        fill='toself',
        line_color='#ffd700',       # Dourado Goat TV
        fillcolor='rgba(255, 215, 0, 0.3)', 
        marker=dict(size=8, color="#ffffff")
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True, 
                range=[40, 99], # Mantém a proporção real de evolução
                gridcolor="rgba(255,255,255,0.1)",
                showticklabels=False
            ),
            angularaxis=dict(
                gridcolor="rgba(255,255,255,0.1)",
                linecolor="white",
                tickfont=dict(size=12, color="white")
            ),
            bgcolor="rgba(0,0,0,0)"
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=40, r=40, t=30, b=30),
        showlegend=False
    )
    return fig

def desenhar_personalidade(pers):
    """
    A Matriz Mental: Traduz os valores psicológicos do dono para o boneco.
    """
    st.markdown("### 🧠 Matriz de Personalidade")
    c1, c2 = st.columns(2)
    
    with c1:
        for k, emoji in [("Raça", "🔥"), ("Técnica", "🎨")]:
            val = pers.get(k, 50)
            st.write(f"{emoji} **{k}:** {val}%")
            st.progress(val / 100)
            
    with c2:
        for k, emoji in [("Altruísmo", "🤝"), ("Compostura", "🧊")]:
            val = pers.get(k, 50)
            st.write(f"{emoji} **{k}:** {val}%")
            st.progress(val / 100)

def exibir_laboratorio_skills(atleta, requisitos_skills):
    """
    Radar de Proximidade Técnica.
    Filtra as 37 habilidades para mostrar apenas o que o dono está perto de 'desbloquear'.
    """
    st.markdown("### 🔭 Laboratório de Skills")
    habs_atuais = atleta.get("habilidades", [])
    
    for sk, reqs in requisitos_skills.items():
        if sk not in habs_atuais:
            # Calcula a média de progresso entre todos os requisitos da skill
            progs = [min(atleta["stats"].get(s, 40)/v, 1.0) for s, v in reqs.items()]
            media = sum(progs) / len(progs)
            
            # Só mostra se estiver "no radar" (acima de 65%)
            if media > 0.65:
                # Cor do progresso: Verde se estiver quase lá (>90%), dourado se estiver no caminho
                cor = "🟢" if media > 0.9 else "🟡"
                st.caption(f"{cor} **{sk}** ({int(media*100)}%)")
                st.progress(media)
