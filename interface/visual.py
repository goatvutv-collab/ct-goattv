# --- interface/visual.py ---
import plotly.graph_objects as go
import streamlit as st

def definir_arquetipo_master(atleta, requisitos_estilos):
    """
    Analisa as maestrias e define a 'Peça de Xadrez' no tabuleiro.
    Fiel à lógica de que o esforço do dono molda a alma do avatar.
    """
    maestrias = atleta.get("maestria", {})
    
    # Se nunca treinou, é uma promessa
    if not any(v > 0 for v in maestrias.values()):
        return "Iniciante (Promessa)"
    
    # Identifica o estilo com maior progresso (DNA dominante no momento)
    melhor_estilo = max(maestrias, key=maestrias.get)
    
    # Mapeia para o Arquétipo Master (Artilheiro, Orquestrador, etc.)
    for arq, estilos in requisitos_estilos.items():
        if melhor_estilo in estilos:
            return arq
            
    return "Especialista"

def gerar_radar(stats):
    """
    Radar Chart Supremo. 
    A escala fixa em [40, 99] garante que a evolução visual seja real e perceptível.
    """
    # Atributos chave para o mapeamento visual do Radar PES
    labels = [
        "Talento ofensivo", "Drible", "Passe rasteiro", "Finalização", 
        "Velocidade", "Contato físico", "Talento defensivo", "Resistência"
    ]
    
    # Fallback para 40 (piso técnico) caso o stat não exista
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
                range=[40, 99], # Escala fixa para mostrar o crescimento real
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
        margin=dict(l=50, r=50, t=30, b=30),
        showlegend=False
    )
    return fig

def desenhar_personalidade(pers):
    """
    A Matriz Mental: Traduz os valores psicológicos (Raça, Técnica, etc.)
    em barras de progresso visuais com emojis.
    """
    st.markdown("### 🧠 Matriz de Personalidade")
    c1, c2 = st.columns(2)
    
    matriz = [
        ("Raça", "🔥", c1),
        ("Técnica", "🎨", c1),
        ("Altruísmo", "🤝", c2),
        ("Compostura", "🧊", c2)
    ]
    
    for label, emoji, col in matriz:
        val = pers.get(label, 50)
        col.write(f"{emoji} **{label}:** {val}%")
        col.progress(val / 100)

def exibir_laboratorio_skills(atleta, requisitos_skills):
    """
    Radar de Proximidade Técnica.
    Filtra as 37 habilidades para mostrar apenas o que o atleta está perto de desbloquear.
    """
    st.markdown("### 🔭 Laboratório de Skills")
    habs_atuais = atleta.get("habilidades", [])
    
    # Lista de habilidades que ainda não foram conquistadas
    for sk, reqs in requisitos_skills.items():
        if sk not in habs_atuais:
            # Calcula o progresso médio baseado nos requisitos da skill
            progs = [min(atleta["stats"].get(s, 40)/v, 1.0) for s, v in reqs.items()]
            media = sum(progs) / len(progs)
            
            # Só mostra no radar se o jogador tiver mais de 65% de proximidade
            if media > 0.65:
                # Cor indicativa: Verde (quase lá) ou Dourado (no caminho)
                cor = "🟢" if media > 0.9 else "🟡"
                st.caption(f"{cor} **{sk}** ({int(media*100)}%)")
                st.progress(media)
