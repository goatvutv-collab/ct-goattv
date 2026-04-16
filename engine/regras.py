# --- BÍBLIA TÉCNICA GOAT TV (VERSÃO ÔMEGA FINAL) ---

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

REGRAS_TREINO = {
    "O Xerife": {"sobe": ["Desarme", "Habil. defensiva", "Contato físico"], "desce": ["Drible", "Velocidade"]},
    "O Maestro": {"sobe": ["Passe rasteiro", "Controle de bola", "Efeito"], "desce": ["Contato físico", "Desarme"]},
    "O Matador": {"sobe": ["Finalização", "Habil. ofensiva", "Força do chute"], "desce": ["Habil. defensiva", "Resistência"]}
}

# A PEÇA QUE ESTAVA FALTANDO E CAUSOU O ERRO:
REQUISITOS_ESTILOS = {
    "Artilheiro": ["O Matador"], 
    "Orquestrador": ["O Maestro"],
    "Destruidor": ["O Xerife"]
}

REQUISITOS_SKILLS = {
    "Pedalada Simples": {"Drible": 75, "Velocidade": 70},
    "Toque Duplo": {"Drible": 80, "Controle de bola": 75},
    "Chute de Longe": {"Finalização": 82, "Força do chute": 80},
    "Interceptação": {"Desarme": 80, "Habil. defensiva": 75}
}