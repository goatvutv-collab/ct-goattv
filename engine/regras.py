# --- engine/regras.py ---

# 1. Habilidades PES 2021 (Escala 40-99)
STATS_BASE_PES = [
    "Talento ofensivo", "Controle de bola", "Drible", "Condução firme", 
    "Passe rasteiro", "Passe alto", "Finalização", "Cabeceio", 
    "Chute colocado", "Curva", "Velocidade", "Aceleração", 
    "Força de chute", "Impulsão", "Contato físico", "Equilíbrio", 
    "Resistência", "Talento defensivo", "Agressividade", 
    "Talento de goleiro", "Firmeza de goleiro", "Afastamento de goleiro", 
    "Reflexo do goleiro", "Alcance do goleiro"
]

# 2. Atributos de Nível
STATS_NIVEL = {
    "Pior pé frequência": 4, "Pior pé precisão": 4,
    "Forma física": 8, "Resistência a lesão": 3
}

# 3. Pesos para Overall (Não é média!)
PESOS_OVR = {
    "ATA": {"Finalização": 5, "Talento ofensivo": 5, "Velocidade": 3, "Aceleração": 3, "Drible": 2},
    "MEI": {"Passe rasteiro": 5, "Controle de bola": 5, "Passe alto": 4, "Curva": 3, "Resistência": 3},
    "DEF": {"Talento defensivo": 5, "Agressividade": 4, "Contato físico": 4, "Cabeceio": 3, "Impulsão": 3},
    "GOL": {"Reflexo do goleiro": 5, "Talento de goleiro": 5, "Alcance do goleiro": 4, "Firmeza de goleiro": 4, "Afastamento de goleiro": 2}
}

# 4. Os 13 Arquétipos (DNA Mutável) - 3 Sobe / 3 Desce
REGRAS_TREINO = {
    "O Matador": {"sobe": ["Finalização", "Talento ofensivo", "Força de chute"], "desce": ["Talento defensivo", "Resistência", "Agressividade"]},
    "O Maestro": {"sobe": ["Passe rasteiro", "Controle de bola", "Curva"], "desce": ["Contato físico", "Agressividade", "Velocidade"]},
    "O Xerife": {"sobe": ["Talento defensivo", "Agressividade", "Contato físico"], "desce": ["Drible", "Velocidade", "Finalização"]},
    "O Libero": {"sobe": ["Passe alto", "Talento defensivo", "Controle de bola"], "desce": ["Contato físico", "Finalização", "Drible"]},
    "O Carrapato": {"sobe": ["Talento defensivo", "Resistência", "Aceleração"], "desce": ["Finalização", "Passe alto", "Cabeceio"]},
    "O Paredão": {"sobe": ["Talento defensivo", "Cabeceio", "Contato físico"], "desce": ["Velocidade", "Drible", "Aceleração"]},
    "O Motorzinho": {"sobe": ["Resistência", "Velocidade", "Passe rasteiro"], "desce": ["Finalização", "Drible", "Talento defensivo"]},
    "O Garçom": {"sobe": ["Passe rasteiro", "Passe alto", "Curva"], "desce": ["Contato físico", "Velocidade", "Talento defensivo"]},
    "O Coringa": {"sobe": ["Drible", "Controle de bola", "Equilíbrio"], "desce": ["Talento defensivo", "Cabeceio", "Agressividade"]},
    "O Ponta-Liso": {"sobe": ["Velocidade", "Drible", "Aceleração"], "desce": ["Contato físico", "Talento defensivo", "Cabeceio"]},
    "O Pivô": {"sobe": ["Contato físico", "Finalização", "Cabeceio"], "desce": ["Velocidade", "Aceleração", "Passe rasteiro"]},
    "O Segundo Atacante": {"sobe": ["Drible", "Passe rasteiro", "Talento ofensivo"], "desce": ["Contato físico", "Cabeceio", "Talento defensivo"]},
    "Goleiro Supremo": {"sobe": ["Reflexo do goleiro", "Firmeza de goleiro", "Alcance do goleiro"], "desce": ["Velocidade", "Drible", "Finalização"]}
}

REQUISITOS_ESTILOS = {
    "Artilheiro": ["O Matador", "O Pivô"], "Infiltrador": ["O Segundo Atacante", "O Coringa"],
    "Orquestrador": ["O Maestro", "O Garçom"], "Destruidor": ["O Xerife", "O Carrapato"]
}

REQUISITOS_SKILLS = {
    "Folha Seca": {"Finalização": 85, "Curva": 82},
    "Interceptação": {"Talento defensivo": 80, "Aceleração": 75},
    "Espírito Guerreiro": {"Resistência": 88}
}
