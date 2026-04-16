# --- BÍBLIA TÉCNICA GOAT TV (VERSÃO ÔMEGA DETALHADA) ---

STATS_BASE_PES = [
    "Habil. ofensiva", "Controle de bola", "Drible", "Passe rasteiro", "Passe alto",
    "Finalização", "Chute colocado", "Efeito", "Cabeçada", "Habil. defensiva",
    "Desarme", "Força do chute", "Velocidade", "Explosão", "Equilíbrio implacável",
    "Contato físico", "Impulsão", "Habil. como goleiro", "Firmeza do goleiro",
    "Chutão", "Reflexos", "Cobertura", "Resistência"
]

PESOS_OVR = {
    "ATA": {"Finalização": 5, "Habil. ofensiva": 5, "Velocidade": 4, "Drible": 4, "Força do chute": 3},
    "MEI": {"Passe rasteiro": 5, "Passe alto": 5, "Controle de bola": 4, "Visão": 4, "Resistência": 3},
    "DEF": {"Desarme": 5, "Habil. defensiva": 5, "Contato físico": 4, "Cabeçada": 3, "Velocidade": 3}
}

# SEUS 12 ESTILOS ORIGINAIS INTEGRADOS
REGRAS_TREINO = {
    "O Xerife":          {"sobe": ["Desarme", "Habil. defensiva", "Contato físico"], "desce": ["Drible", "Velocidade"]},
    "O Libero":          {"sobe": ["Passe alto", "Habil. defensiva", "Controle de bola"], "desce": ["Contato físico", "Finalização"]},
    "O Carrapato":       {"sobe": ["Desarme", "Resistência", "Velocidade"], "desce": ["Finalização", "Passe alto"]},
    "O Paredão":         {"sobe": ["Habil. defensiva", "Cabeçada", "Contato físico"], "desce": ["Velocidade", "Drible"]},
    "O Maestro":         {"sobe": ["Passe rasteiro", "Controle de bola", "Efeito"], "desce": ["Contato físico", "Desarme"]},
    "O Motorzinho":      {"sobe": ["Resistência", "Velocidade", "Passe rasteiro"], "desce": ["Finalização", "Drible"]},
    "O Garçom":          {"sobe": ["Passe rasteiro", "Passe alto", "Efeito"], "desce": ["Contato físico", "Velocidade"]},
    "O Coringa":         {"sobe": ["Drible", "Controle de bola", "Equilíbrio implacável"], "desce": ["Habil. defensiva", "Cabeçada"]},
    "O Ponta-Liso":      {"sobe": ["Velocidade", "Drible", "Explosão"], "desce": ["Contato físico", "Habil. defensiva"]},
    "O Pivô":            {"sobe": ["Contato físico", "Finalização", "Cabeçada"], "desce": ["Velocidade", "Explosão"]},
    "O Matador":         {"sobe": ["Finalização", "Habil. ofensiva", "Força do chute"], "desce": ["Resistência", "Habil. defensiva"]},
    "O Segundo Atacante": {"sobe": ["Drible", "Passe rasteiro", "Habil. ofensiva"], "desce": ["Contato físico", "Cabeçada"]}
}

REQUISITOS_ESTILOS = {
    "Artilheiro": ["O Matador", "O Pivô"], 
    "Infiltrador": ["O Segundo Atacante", "O Coringa"],
    "Ponta Incisivo": ["O Ponta-Liso", "O Motorzinho"], 
    "Orquestrador": ["O Maestro", "O Garçom"],
    "Destruidor": ["O Xerife", "O Carrapato"], 
    "Líbero (Build Up)": ["O Libero", "O Paredão"]
}

REQUISITOS_SKILLS = {
    "Pedalada Simples": {"Drible": 75, "Velocidade": 70},
    "Toque Duplo": {"Drible": 80, "Controle de bola": 75},
    "Elástico": {"Drible": 85, "Equilíbrio implacável": 70},
    "Chute de Longe": {"Finalização": 82, "Força do chute": 80},
    "Interceptação": {"Desarme": 80, "Habil. defensiva": 75},
    "Espírito de Luta": {"Resistência": 85, "Contato físico": 75}
}
