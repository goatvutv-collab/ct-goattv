# --- interface/visual.py ---
import plotly.graph_objects as go
import streamlit as st

def definir_arquetipo_master(atleta, requisitos_estilos):
    """Analisa as maestrias e define o Arquétipo Master baseado no DNA dominante."""
    maestrias = atleta.get("maestria", {})
    if not any(v > 0 for v in maestrias.values()):
        return "Iniciante (Promessa)"
    
    melhor_estilo = max(maestrias, key=maestrias.get)
    for arq, estilos in requisitos_estilos.items():
        if melhor_estilo in estilos:
            return arq
    return "Especialista"

def gerar_radar(stats):
    """Radar Chart Supremo com escala PES [40, 99]."""
    labels = [
        "Talento ofensivo", "Drible", "Passe rasteiro", "Finalização", 
        "Velocidade", "Contato físico", "Talento defensivo", "Resistência"
    ]
    values = [stats.get(l, 40) for l in labels]
    
    fig = go.Figure(data=go.Scatterpolar(
        r=values + [values[0]],
        theta=labels + [labels[0]],
        fill='toself',
        line_color='#ffd700',
        fillcolor='rgba(255, 215, 0, 0.3)',
        marker=dict(size=8, color="#ffffff")
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[40, 99], gridcolor="rgba(255,255,255,0.1)", showticklabels=False),
            angularaxis=dict(gridcolor="rgba(255,255,255,0.1)", linecolor="white", tickfont=dict(size=12, color="white")),
            bgcolor="rgba(0,0,0,0)"
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=50, r=50, t=30, b=30),
        showlegend=False
    )
    return fig

def desenhar_personalidade(pers):
    """Desenha a Matriz Mental com colunas e emojis restaurados."""
    st.markdown("### 🧠 Matriz de Personalidade")
    c1, c2 = st.columns(2)
    
    # Lógica de grid que você acha bonito
    matriz = [
        ("Raça", "💪", c1),
        ("Técnica", "🧠", c1),
        ("Altruísmo", "🤝", c2),
        ("Compostura", "🧘", c2)
    ]
    
    for label, emoji, col in matriz:
        val = pers.get(label, 50)
        col.write(f"{emoji} **{label}:** {val}%")
        col.progress(val / 100)

def exibir_laboratorio_skills(atleta, requisitos_skills):
    """
    O Laboratório Supremo: 
    1. Mostra 🏆 para o que já está na Bag.
    2. Mostra 🚀 para o que está sendo treinado (Maestria).
    3. Mostra 🔭 para o que você está perto de liberar (Proximidade por Stats).
    """
    st.markdown("### 🧪 Laboratório de Talentos")
    habs_atuais = atleta.get("habilidades", [])
    maestria = atleta.get("maestria", {})
    stats = atleta.get("stats", {})

    for sk, reqs in requisitos_skills.items():
        prog_treino = maestria.get(sk, 0.0)
        
        # 1. SE JÁ ESTÁ MASTERIZADO
        if sk in habs_atuais:
            st.caption(f"🏆 **{sk.upper()}** - MASTERIZADO")
            st.progress(1.0)
            
        # 2. SE ESTÁ EM TREINAMENTO ATIVO
        elif prog_treino > 0:
            st.caption(f"🚀 **{sk}** (Evolução: {prog_treino:.1f}%)")
            st.progress(min(prog_treino/100, 1.0))
            
        # 3. SE ESTÁ TRANCADO, MOSTRA A PROXIMIDADE (Lógica do Backup!)
        else:
            progs_fisicos = [min(stats.get(s, 40)/v, 1.0) for s, v in reqs.items()]
            proximidade = sum(progs_fisicos) / len(progs_fisicos)
            
            # Só mostra se tiver mais de 65% de chance de liberar
            if proximidade > 0.65:
                cor = "🟢" if proximidade > 0.9 else "🟡"
                st.caption(f"🔭 {cor} **{sk}** (Disponível p/ Treino: {int(proximidade*100)}%)")
                st.progress(proximidade)
