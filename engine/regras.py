# --- engine/regras.py ---

# LISTA PRINCIPAL DE ATRIBUTOS (40-99)
STATS_BASE_PES = [
    "Habil. ofensiva", "Controle de bola", "Drible", "Passe rasteiro", "Passe alto",
    "Finalização", "Chute colocado", "Efeito", "Cabeçada", "Habil. defensiva",
    "Desarme", "Força do chute", "Velocidade", "Explosão", "Equilíbrio implacável",
    "Contato físico", "Impulsão", "Habil. como goleiro", "Firmeza do goleiro",
    "Chutão", "Reflexos", "Cobertura", "Resistência"
]

# STATS DE NÍVEL ESPECÍFICO (Barrinhas de 1-4, 1-8, etc)
STATS_NIVEL = {
    "Pior pé frequência": 4, "Pior pé precisão": 4, 
    "Condição física": 8, "Resistência a lesão": 3
}

# --- REGRAS DE TREINO (3 SOBE / 3 DESCE) ---
REGRAS_TREINO = {
    "O Matador": {"sobe": ["Finalização", "Habil. ofensiva", "Força do chute"], "desce": ["Habil. defensiva", "Resistência", "Desarme"]},
    "O Xerife": {"sobe": ["Desarme", "Habil. defensiva", "Contato físico"], "desce": ["Drible", "Velocidade", "Passe alto"]},
    "Goleiro Fixo": {"sobe": ["Reflexos", "Firmeza do goleiro", "Cobertura"], "desce": ["Velocidade", "Drible", "Finalização"]},
    "Goleiro Linha": {"sobe": ["Reflexos", "Passe rasteiro", "Habil. como goleiro"], "desce": ["Contato físico", "Cabeçada", "Habil. defensiva"]},
    "O Maestro": {"sobe": ["Passe rasteiro", "Controle de bola", "Efeito"], "desce": ["Contato físico", "Desarme", "Explosão"]},
    "O Pivô": {"sobe": ["Contato físico", "Finalização", "Cabeçada"], "desce": ["Velocidade", "Explosão", "Drible"]},
    "O Ponta-Liso": {"sobe": ["Velocidade", "Drible", "Explosão"], "desce": ["Contato físico", "Habil. defensiva", "Cabeçada"]}
}

# --- ARQUÉTIPOS E COMPATIBILIDADE ---
REQUISITOS_ESTILOS = {
    "Artilheiro": ["O Matador", "O Pivô"],
    "Orquestrador": ["O Maestro"],
    "Destruidor": ["O Xerife"],
    "Ponta Incisivo": ["O Ponta-Liso"]
}

# --- LABORATÓRIO DE SKILLS (Requisitos exatos para desbloqueio) ---
REQUISITOS_SKILLS = {
    "Pedalada Simples": {"Drible": 75, "Velocidade": 70},
    "Toque Duplo": {"Drible": 80, "Controle de bola": 75},
    "Chute de Longe": {"Finalização": 82, "Força do chute": 80},
    "Espírito Guerreiro": {"Resistência": 85, "Raça": 75},
    "Super Sub": {"Habil. ofensiva": 80, "Compostura": 80},
    "Interceptação": {"Desarme": 80, "Habil. defensiva": 75}
}
