# --- engine/regras.py ---

# Habilidades PES 2021 (40-99)
STATS_BASE_PES = [
    "Talento ofensivo", "Controle de bola", "Drible", "Condução firme", 
    "Passe rasteiro", "Passe alto", "Finalização", "Cabeceio", 
    "Chute colocado", "Curva", "Velocidade", "Aceleração", 
    "Força de chute", "Impulsão", "Contato físico", "Equilíbrio", 
    "Resistência", "Talento defensivo", "Agressividade", 
    "Talento de goleiro", "Firmeza de goleiro", "Afastamento de goleiro", 
    "Reflexo do goleiro", "Alcance do goleiro"
]

# Barrinhas de Nível
STATS_NIVEL = {
    "Pior pé frequência": 4, "Pior pé precisão": 4,
    "Forma física": 8, "Resistência a lesão": 3
}

# PESOS PARA OVERALL (Não é média! É relevância por posição)
PESOS_OVR = {
    "ATA": {"Finalização": 5, "Talento ofensivo": 5, "Velocidade": 3, "Aceleração": 3, "Drible": 2},
    "MEI": {"Passe rasteiro": 5, "Controle de bola": 5, "Passe alto": 4, "Curva": 3, "Resistência": 3},
    "DEF": {"Talento defensivo": 5, "Agressividade": 4, "Contato físico": 4, "Cabeceio": 3, "Impulsão": 3},
    "GOL": {"Reflexo do goleiro": 5, "Talento de goleiro": 5, "Alcance do goleiro": 4, "Firmeza de goleiro": 4, "Afastamento de goleiro": 2}
}

# ARQUÉTIPOS (DNA): 3 FORTES (Sobe mais) / 3 FRACOS (Sobe menos ou desce)
REGRAS_TREINO = {
    "O Matador": {
        "sobe": ["Finalização", "Talento ofensivo", "Chute colocado"], 
        "desce": ["Velocidade", "Aceleração", "Talento defensivo"]
    },
    "O Maestro": {
        "sobe": ["Passe rasteiro", "Controle de bola", "Curva"], 
        "desce": ["Contato físico", "Agressividade", "Velocidade"]
    },
    "O Xerife": {
        "sobe": ["Talento defensivo", "Agressividade", "Contato físico"], 
        "desce": ["Drible", "Velocidade", "Finalização"]
    },
    # Adicione os demais 10 arquétipos seguindo esta lógica 3x3...
}

REQUISITOS_ESTILOS = {
    "Artilheiro": ["O Matador"], "Orquestrador": ["O Maestro"], "Destruidor": ["O Xerife"]
}

# Mesma lista de 37 habilidades (Skills) anterior para o Laboratório...
REQUISITOS_SKILLS = { 
    "Folha Seca": {"Finalização": 85, "Curva": 80},
    "Interceptação": {"Talento defensivo": 80, "Aceleração": 75}
}
