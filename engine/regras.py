PESOS_OVR = {
    "ATA": {"Finalização": 5, "Habilid. Ofensiva": 5, "Velocidade": 4, "Drible": 4, "Força do Chute": 3},
    "MEI": {"Passe Rasteiro": 5, "Passe Alto": 5, "Controle de Bola": 4, "Visão": 4, "Resistência": 3},
    "DEF": {"Desarme": 5, "Habilid. Defensiva": 5, "Contato Físico": 4, "Cabeçada": 3, "Velocidade": 3}
}

REGRAS_TREINO = {
    "O Xerife": {"sobe": ["Desarme", "Habilid. Defensiva", "Contato Físico"], "desce": ["Drible", "Velocidade"]},
    "O Libero": {"sobe": ["Passe Alto", "Habilid. Defensiva", "Controle de Bola"], "desce": ["Contato Físico", "Finalização"]},
    "O Carrapato": {"sobe": ["Desarme", "Resistência", "Velocidade"], "desce": ["Finalização", "Passe Alto"]},
    "O Paredão": {"sobe": ["Habilid. Defensiva", "Cabeçada", "Contato Físico"], "desce": ["Velocidade", "Drible"]},
    "O Maestro": {"sobe": ["Passe Rasteiro", "Controle de Bola", "Visão"], "desce": ["Contato Físico", "Desarme"]},
    "O Motorzinho": {"sobe": ["Resistência", "Velocidade", "Passe Rasteiro"], "desce": ["Finalização", "Drible"]},
    "O Garçom": {"sobe": ["Passe Rasteiro", "Passe Alto", "Curva"], "desce": ["Contato Físico", "Velocidade"]},
    "O Coringa": {"sobe": ["Drible", "Controle de Bola", "Equilíbrio"], "desce": ["Habilid. Defensiva", "Cabeçada"]},
    "O Ponta-Liso": {"sobe": ["Velocidade", "Drible", "Explosão"], "desce": ["Contato Físico", "Habilid. Defensiva"]},
    "O Pivô": {"sobe": ["Contato Físico", "Finalização", "Cabeçada"], "desce": ["Velocidade", "Explosão"]},
    "O Matador": {"sobe": ["Finalização", "Habilid. Ofensiva", "Força do Chute"], "desce": ["Resistência", "Habilid. Defensiva"]},
    "O Segundo Atacante": {"sobe": ["Drible", "Passe Rasteiro", "Habilid. Ofensiva"], "desce": ["Contato Físico", "Cabeçada"]}
}

REQUISITOS_SKILLS = {
    "Pedalada Simples": {"Drible": 75, "Velocidade": 70},
    "Toque Duplo": {"Drible": 80, "Controle de Bola": 75},
    "Elástico": {"Drible": 85, "Equilíbrio": 70},
    "360 Graus": {"Drible": 78, "Controle de Bola": 82},
    "Chute de Longe": {"Finalização": 82, "Força do Chute": 80},
    "Folha Seca": {"Finalização": 85, "Curva": 75},
    "Cabeceio": {"Cabeçada": 80, "Contato Físico": 75},
    "Interceptação": {"Desarme": 80, "Habilid. Defensiva": 75},
    "Espírito de Luta": {"Resistência": 85, "Raça": 70},
    "Malícia": {"Equilíbrio": 70, "Drible": 75}
}
