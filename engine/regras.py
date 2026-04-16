# --- ATRIBUTOS TÉCNICOS ---
STATS_PES_PADRAO = [
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

# --- REGRAS DE TREINO (3 SOBE / 3 DESCE) ---
REGRAS_TREINO = {
    "O Matador": {"sobe": ["Finalização", "Habil. ofensiva", "Força do chute"], "desce": ["Habil. defensiva", "Resistência", "Desarme"]},
    "O Xerife": {"sobe": ["Desarme", "Habil. defensiva", "Contato físico"], "desce": ["Drible", "Velocidade", "Passe alto"]},
    "Goleiro Fixo": {"sobe": ["Reflexos", "Firmeza do goleiro", "Cobertura"], "desce": ["Velocidade", "Drible", "Finalização"]},
    "Goleiro Linha": {"sobe": ["Reflexos", "Passe rasteiro", "Habil. como goleiro"], "desce": ["Contato físico", "Cabeçada", "Habil. defensiva"]},
    "O Maestro": {"sobe": ["Passe rasteiro", "Controle de bola", "Efeito"], "desce": ["Contato físico", "Desarme", "Explosão"]},
    # ... Adicionar os outros 8 conforme a sua lista (Pivô, Ponta-Liso, etc)
}

# --- ARQUÉTIPOS E COMPATIBILIDADE ---
ARQUETIPOS_COMPATIBILIDADE = {
    "Artilheiro": ["CA", "SA"],
    "Pivô": ["CA"],
    "Armador Criativo": ["PE", "PD", "SA", "MAT", "MLD", "MLE"],
    "O Destruidor": ["MAT", "VOL", "ZC"],
    "Goleiro Ofensivo": ["GOL"],
    "Goleiro Defensivo": ["GOL"]
}

# --- LABORATÓRIO DE SKILLS (Requisitos exatos) ---
REQUISITOS_SKILLS = {
    "Pedalada Simples": {"Drible": 75, "Velocidade": 70},
    "Toque Duplo": {"Drible": 80, "Controle de bola": 75},
    "Chute de Longe": {"Finalização": 82, "Força do chute": 80},
    "Espírito Guerreiro": {"Resistência": 85, "Raça": 75},
    "Super Sub": {"Habil. ofensiva": 80, "Compostura": 80}
}
