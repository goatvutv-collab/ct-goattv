# --- engine/regras.py ---

STATS_BASE_PES = [
    "Habil. ofensiva", "Controle de bola", "Drible", "Passe rasteiro", "Passe alto",
    "Finalização", "Chute colocado", "Efeito", "Cabeçada", "Habil. defensiva",
    "Desarme", "Força do chute", "Velocidade", "Explosão", "Equilíbrio implacável",
    "Contato físico", "Impulsão", "Habil. como goleiro", "Firmeza do goleiro",
    "Chutão", "Reflexos", "Cobertura", "Resistência"
]

STATS_NIVEL = {
    "Pior pé frequência": 4, "Pior pé precisão": 4, 
    "Condição física": 8, "Resistência a lesão": 3
}

PESOS_OVR = {
    "ATA": {"Finalização": 5, "Habil. ofensiva": 5, "Velocidade": 4, "Drible": 4, "Força do chute": 3},
    "MEI": {"Passe rasteiro": 5, "Passe alto": 5, "Controle de bola": 4, "Efeito": 4, "Resistência": 3},
    "DEF": {"Desarme": 5, "Habil. defensiva": 5, "Contato físico": 4, "Cabeçada": 3, "Velocidade": 3},
    "GOL": {"Reflexos": 5, "Firmeza do goleiro": 5, "Cobertura": 4, "Chutão": 3, "Impulsão": 3}
}

REGRAS_TREINO = {
    "O Xerife":          {"sobe": ["Desarme", "Habil. defensiva", "Contato físico"], "desce": ["Drible", "Velocidade", "Passe alto"]},
    "O Libero":          {"sobe": ["Passe alto", "Habil. defensiva", "Controle de bola"], "desce": ["Contato físico", "Finalização", "Drible"]},
    "O Carrapato":       {"sobe": ["Desarme", "Resistência", "Velocidade"], "desce": ["Finalização", "Passe alto", "Cabeçada"]},
    "O Paredão":         {"sobe": ["Habil. defensiva", "Cabeçada", "Contato físico"], "desce": ["Velocidade", "Drible", "Explosão"]},
    "O Maestro":         {"sobe": ["Passe rasteiro", "Controle de bola", "Efeito"], "desce": ["Contato físico", "Desarme", "Explosão"]},
    "O Motorzinho":      {"sobe": ["Resistência", "Velocidade", "Passe rasteiro"], "desce": ["Finalização", "Drible", "Habil. defensiva"]},
    "O Garçom":          {"sobe": ["Passe rasteiro", "Passe alto", "Efeito"], "desce": ["Contato físico", "Velocidade", "Desarme"]},
    "O Coringa":         {"sobe": ["Drible", "Controle de bola", "Equilíbrio implacável"], "desce": ["Habil. defensiva", "Cabeçada", "Desarme"]},
    "O Ponta-Liso":      {"sobe": ["Velocidade", "Drible", "Explosão"], "desce": ["Contato físico", "Habil. defensiva", "Cabeçada"]},
    "O Pivô":            {"sobe": ["Contato físico", "Finalização", "Cabeçada"], "desce": ["Velocidade", "Explosão", "Passe rasteiro"]},
    "O Matador":         {"sobe": ["Finalização", "Habil. ofensiva", "Força do chute"], "desce": ["Habil. defensiva", "Resistência", "Desarme"]},
    "O Segundo Atacante": {"sobe": ["Drible", "Passe rasteiro", "Habil. ofensiva"], "desce": ["Contato físico", "Cabeçada", "Desarme"]},
    "Goleiro Fixo":      {"sobe": ["Reflexos", "Firmeza do goleiro", "Cobertura"], "desce": ["Velocidade", "Drible", "Finalização"]},
    "Goleiro Linha":     {"sobe": ["Reflexos", "Passe rasteiro", "Habil. como goleiro"], "desce": ["Contato físico", "Cabeçada", "Habil. defensiva"]}
}

REQUISITOS_ESTILOS = {
    "Artilheiro": ["O Matador", "O Pivô"],
    "Infiltrador": ["O Segundo Atacante", "O Coringa"],
    "Ponta Incisivo": ["O Ponta-Liso", "O Motorzinho"],
    "Orquestrador": ["O Maestro", "O Garçom"],
    "Destruidor": ["O Xerife", "O Carrapato"],
    "Líbero (Build Up)": ["O Libero", "O Paredão"],
    "Guardião Supremo": ["Goleiro Fixo", "Goleiro Linha"]
}

REQUISITOS_SKILLS = {
    "Pedalada Simples": {"Drible": 75, "Velocidade": 70},
    "Toque Duplo": {"Drible": 80, "Controle de bola": 75},
    "Chute de Longe": {"Finalização": 82, "Força do chute": 80},
    "Folha Seca": {"Finalização": 85, "Efeito": 75},
    "Espírito Guerreiro": {"Resistência": 85, "Raça": 75}
}
