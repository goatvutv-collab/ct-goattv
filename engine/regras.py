# --- engine/regras.py ---

# LISTA COMPLETA DE ATRIBUTOS (40-99)
STATS_BASE_PES = [
    "Habil. ofensiva", "Controle de bola", "Drible", "Passe rasteiro", "Passe alto",
    "Finalização", "Chute colocado", "Efeito", "Cabeçada", "Habil. defensiva",
    "Desarme", "Força do chute", "Velocidade", "Explosão", "Equilíbrio implacável",
    "Contato físico", "Impulsão", "Habil. como goleiro", "Firmeza do goleiro",
    "Chutão", "Reflexos", "Cobertura", "Resistência"
]

# ATRIBUTOS DE NÍVEL (Barrinhas específicas)
STATS_NIVEL = {
    "Pior pé frequência": 4,  # 1 a 4
    "Pior pé precisão": 4,    # 1 a 4
    "Condição física": 8,     # 1 a 8
    "Resistência a lesão": 3  # 1 a 3
}

# --- TODOS OS 14 ESTILOS DE TREINO (Regra 3 Sobe / 3 Desce) ---
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

# --- ARQUÉTIPOS MASTER ---
REQUISITOS_ESTILOS = {
    "Artilheiro": ["O Matador", "O Pivô"],
    "Infiltrador": ["O Segundo Atacante", "O Coringa"],
    "Ponta Incisivo": ["O Ponta-Liso", "O Motorzinho"],
    "Orquestrador": ["O Maestro", "O Garçom"],
    "Destruidor": ["O Xerife", "O Carrapato"],
    "Líbero (Build Up)": ["O Libero", "O Paredão"],
    "Guardião": ["Goleiro Fixo", "Goleiro Linha"]
}

# --- LABORATÓRIO DE SKILLS (Requisitos do seu Dossiê) ---
REQUISITOS_SKILLS = {
    "Pedalada Simples": {"Drible": 75, "Velocidade": 70},
    "Toque Duplo": {"Drible": 80, "Controle de bola": 75},
    "Elástico": {"Drible": 85, "Equilíbrio implacável": 70},
    "360 Graus": {"Drible": 78, "Controle de bola": 82},
    "Chute de Longe": {"Finalização": 82, "Força do chute": 80},
    "Folha Seca": {"Finalização": 85, "Efeito": 75},
    "Cabeceio": {"Cabeçada": 80, "Contato físico": 75},
    "Interceptação": {"Desarme": 80, "Habil. defensiva": 75},
    "Espírito Guerreiro": {"Resistência": 85, "Raça": 75},
    "Malícia": {"Equilíbrio implacável": 70, "Drible": 75},
    "Super Sub": {"Habil. ofensiva": 80, "Compostura": 80}
}
