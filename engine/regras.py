# --- engine/regras.py ---

# 1. LISTA MESTRA DE ATRIBUTOS (Escala PES 40-99)
# Unificação total: nomes exatos que o PES usa e o motor de cálculo buscará.
STATS_BASE_PES = [
    "Habil. ofensiva", "Controle de bola", "Drible", "Passe rasteiro", "Passe alto",
    "Finalização", "Chute colocado", "Efeito", "Cabeçada", "Habil. defensiva",
    "Desarme", "Força do chute", "Velocidade", "Explosão", "Equilíbrio implacável",
    "Contato físico", "Impulsão", "Habil. como goleiro", "Firmeza do goleiro",
    "Chutão", "Reflexos", "Cobertura", "Resistência"
]

# 2. ATRIBUTOS DE NÍVEL (Barrinhas Fixas)
# Define o teto máximo de cada atributo especial.
STATS_NIVEL = {
    "Pior pé frequência": 4,  # Escala 1-4
    "Pior pé precisão": 4,    # Escala 1-4
    "Condição física": 8,     # Escala 1-8
    "Resistência a lesão": 3  # Escala 1-3
}

# 3. PESOS PARA CÁLCULO DE OVERALL (OVR SUPREMO)
# Recuperado do macarrão original e corrigido para os nomes da STATS_BASE_PES.
# Adicionado setor GOL (Goleiro) que não existia no macarrão.
PESOS_OVR = {
    "ATA": {"Finalização": 5, "Habil. ofensiva": 5, "Velocidade": 4, "Drible": 4, "Força do chute": 3},
    "MEI": {"Passe rasteiro": 5, "Passe alto": 5, "Controle de bola": 4, "Efeito": 4, "Resistência": 3},
    "DEF": {"Desarme": 5, "Habil. defensiva": 5, "Contato físico": 4, "Cabeçada": 3, "Velocidade": 3},
    "GOL": {"Reflexos": 5, "Firmeza do goleiro": 5, "Cobertura": 4, "Chutão": 3, "Impulsão": 3}
}

# 4. REGRAS DE TREINO (Regra 3 Sobe / 3 Desce)
# Aqui estão todos os 14 estilos do Dossiê. 
# Completei a regra de 3 atributos descendo para os que estavam incompletos no macarrão.
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

# 5. REQUISITOS DE ARQUÉTIPOS MASTER
# Determina o nome de exibição no Scout Card baseado nos estilos treinados.
REQUISITOS_ESTILOS = {
    "Artilheiro": ["O Matador", "O Pivô"],
    "Infiltrador": ["O Segundo Atacante", "O Coringa"],
    "Ponta Incisivo": ["O Ponta-Liso", "O Motorzinho"],
    "Orquestrador": ["O Maestro", "O Garçom"],
    "Destruidor": ["O Xerife", "O Carrapato"],
    "Líbero (Build Up)": ["O Libero", "O Paredão"],
    "Guardião Supremo": ["Goleiro Fixo", "Goleiro Linha"]
}

# 6. LABORATÓRIO DE SKILLS (Dossiê de 37 Habilidades)
# Unifica as 10 skills do macarrão com as 27 novas.
# Requisitos ajustados para bater com a lista STATS_BASE_PES.
REQUISITOS_SKILLS = {
    # GRUPO: DRIBLE E AGILIDADE
    "Pedalada Simples": {"Drible": 75, "Velocidade": 70},
    "Toque Duplo": {"Drible": 80, "Controle de bola": 75},
    "Elástico": {"Drible": 85, "Equilíbrio implacável": 75},
    "360 Graus": {"Drible": 78, "Controle de bola": 82},
    "Lençol": {"Controle de bola": 85, "Drible": 80},
    "Corte de Calcanhar": {"Drible": 80, "Efeito": 70},
    "Puxada de Letra": {"Drible": 82, "Controle de bola": 80},
    "Finta de Letra": {"Drible": 85, "Habil. ofensiva": 75},
    "Habilidade de Domínio": {"Controle de bola": 88, "Equilíbrio implacável": 80},
    
    # GRUPO: FINALIZAÇÃO
    "Cabeçada": {"Cabeçada": 80, "Impulsão": 75},
    "Chute de Longe": {"Finalização": 82, "Força do chute": 80},
    "Controle de Cavadinha": {"Finalização": 80, "Efeito": 85},
    "Chute com Peito do Pé": {"Finalização": 85, "Força do chute": 85},
    "Folha Seca": {"Finalização": 88, "Efeito": 90},
    "Chute com Decolagem": {"Finalização": 80, "Força do chute": 90},
    "Finalização Acrobática": {"Finalização": 85, "Impulsão": 85},
    "Toque de Calcanhar": {"Passe rasteiro": 75, "Controle de bola": 80},
    "Chute de Primeira": {"Finalização": 82, "Habil. ofensiva": 80},
    
    # GRUPO: PASSES E CRUZAMENTOS
    "Passe de Primeira": {"Passe rasteiro": 82, "Controle de bola": 80},
    "Passe na Medida": {"Passe rasteiro": 85, "Passe alto": 80},
    "Cruzamento Preciso": {"Passe alto": 85, "Efeito": 80},
    "Curva para Fora": {"Efeito": 88, "Chute colocado": 80},
    "Passe Aero Baixo": {"Passe alto": 82, "Efeito": 75},
    "Passe sem Olhar": {"Passe rasteiro": 80, "Controle de bola": 85},
    
    # GRUPO: DEFESA E GOLEIRO
    "Reposição Baixa de Goleiro": {"Habil. como goleiro": 80, "Passe rasteiro": 70},
    "Reposição Alta de Goleiro": {"Habil. como goleiro": 80, "Passe alto": 75},
    "Arremesso Longo": {"Contato físico": 80, "Força do chute": 75},
    "Especialista em Pênalti": {"Finalização": 85, "Compostura": 85},
    "Pegador de Pênalti": {"Reflexos": 85, "Cobertura": 80},
    "Interceptação": {"Desarme": 80, "Habil. defensiva": 75},
    "Marcação Individual": {"Desarme": 82, "Habil. defensiva": 85},
    "Volta para Marcar": {"Resistência": 85, "Habil. defensiva": 75},
    "Afastamento Acrobático": {"Habil. defensiva": 80, "Impulsão": 85},
    
    # GRUPO: MENTAL E ESPECIAL (RAÇA)
    "Malícia": {"Drible": 75, "Equilíbrio implacável": 85},
    "Liderança": {"Compostura": 90, "Raça": 85},
    "Super Sub": {"Habil. ofensiva": 80, "Finalização": 80},
    "Espírito Guerreiro": {"Resistência": 88, "Raça": 90}
}
