# --- engine/regras.py ---

# 1. LISTA MESTRA DE ATRIBUTOS (Escala PES 2021: 40-99)
STATS_BASE_PES = [
    "Talento ofensivo", "Controle de bola", "Drible", "Condução firme", 
    "Passe rasteiro", "Passe alto", "Finalização", "Cabeceio", 
    "Chute colocado", "Curva", "Velocidade", "Aceleração", 
    "Força de chute", "Impulsão", "Contato físico", "Equilíbrio", 
    "Resistência", "Talento defensivo", "Agressividade", 
    "Talento de goleiro", "Firmeza de goleiro", "Afastamento de goleiro", 
    "Reflexo do goleiro", "Alcance do goleiro"
]

# 2. ATRIBUTOS DE NÍVEL (Barrinhas Fixas)
STATS_NIVEL = {
    "Pior pé frequência": 4, 
    "Pior pé precisão": 4,
    "Forma física": 8, 
    "Resistência a lesão": 3
}

# 3. PESOS PARA CÁLCULO DE OVERALL (Não é média! É relevância por posição)
PESOS_OVR = {
    "ATA": {"Finalização": 5, "Talento ofensivo": 5, "Velocidade": 3, "Aceleração": 3, "Força de chute": 3},
    "MEI": {"Passe rasteiro": 5, "Controle de bola": 5, "Passe alto": 4, "Curva": 3, "Resistência": 3},
    "DEF": {"Talento defensivo": 5, "Agressividade": 4, "Contato físico": 4, "Cabeceio": 3, "Impulsão": 3},
    "GOL": {"Reflexo do goleiro": 5, "Talento de goleiro": 5, "Alcance do goleiro": 4, "Firmeza de goleiro": 4, "Afastamento de goleiro": 2}
}

# 4. REGRAS DE TREINO (DNA MUTÁVEL) - Regra 3 Sobe / 3 Desce
REGRAS_TREINO = {
    "O Xerife":          {"sobe": ["Talento defensivo", "Agressividade", "Contato físico"], "desce": ["Drible", "Velocidade", "Passe alto"]},
    "O Libero":          {"sobe": ["Passe alto", "Talento defensivo", "Controle de bola"], "desce": ["Contato físico", "Finalização", "Drible"]},
    "O Carrapato":       {"sobe": ["Talento defensivo", "Resistência", "Velocidade"], "desce": ["Finalização", "Passe alto", "Cabeceio"]},
    "O Paredão":         {"sobe": ["Talento defensivo", "Cabeceio", "Contato físico"], "desce": ["Velocidade", "Drible", "Aceleração"]},
    "O Maestro":         {"sobe": ["Passe rasteiro", "Controle de bola", "Curva"], "desce": ["Contato físico", "Agressividade", "Aceleração"]},
    "O Motorzinho":      {"sobe": ["Resistência", "Velocidade", "Passe rasteiro"], "desce": ["Finalização", "Drible", "Talento defensivo"]},
    "O Garçom":          {"sobe": ["Passe rasteiro", "Passe alto", "Curva"], "desce": ["Contato físico", "Velocidade", "Talento defensivo"]},
    "O Coringa":         {"sobe": ["Drible", "Controle de bola", "Equilíbrio"], "desce": ["Talento defensivo", "Cabeceio", "Agressividade"]},
    "O Ponta-Liso":      {"sobe": ["Velocidade", "Drible", "Aceleração"], "desce": ["Contato físico", "Talento defensivo", "Cabeceio"]},
    "O Pivô":            {"sobe": ["Contato físico", "Finalização", "Cabeceio"], "desce": ["Velocidade", "Aceleração", "Passe rasteiro"]},
    "O Matador":         {"sobe": ["Finalização", "Talento ofensivo", "Chute colocado"], "desce": ["Talento defensivo", "Resistência", "Agressividade"]},
    "O Segundo Atacante": {"sobe": ["Drible", "Passe rasteiro", "Talento ofensivo"], "desce": ["Contato físico", "Cabeceio", "Talento defensivo"]},
    "Goleiro Fixo":      {"sobe": ["Reflexo do goleiro", "Firmeza de goleiro", "Alcance do goleiro"], "desce": ["Velocidade", "Drible", "Finalização"]},
    "Goleiro Linha":     {"sobe": ["Reflexo do goleiro", "Passe rasteiro", "Talento de goleiro"], "desce": ["Contato físico", "Cabeceio", "Talento defensivo"]}
}

# 5. REQUISITOS DE ARQUÉTIPOS MASTER (Exibição no Scout Card)
REQUISITOS_ESTILOS = {
    "Artilheiro": ["O Matador", "O Pivô"],
    "Infiltrador": ["O Segundo Atacante", "O Coringa"],
    "Ponta Incisivo": ["O Ponta-Liso", "O Motorzinho"],
    "Orquestrador": ["O Maestro", "O Garçom"],
    "Destruidor": ["O Xerife", "O Carrapato"],
    "Líbero (Build Up)": ["O Libero", "O Paredão"],
    "Guardião Supremo": ["Goleiro Fixo", "Goleiro Linha"]
}

# 6. LABORATÓRIO DE SKILLS (Dossiê Completo de 37 Habilidades)
REQUISITOS_SKILLS = {
    # DRIBLE E AGILIDADE
    "Pedalada Simples": {"Drible": 75, "Velocidade": 70},
    "Toque Duplo": {"Drible": 80, "Controle de bola": 75},
    "Elástico": {"Drible": 85, "Equilíbrio": 75},
    "360 Graus": {"Drible": 78, "Controle de bola": 82},
    "Lençol": {"Controle de bola": 85, "Drible": 80},
    "Corte de Calcanhar": {"Drible": 80, "Curva": 70},
    "Puxada de Letra": {"Drible": 82, "Controle de bola": 80},
    "Finta de Letra": {"Drible": 85, "Talento ofensivo": 75},
    "Habilidade de Domínio": {"Controle de bola": 88, "Equilíbrio": 80},

    # FINALIZAÇÃO
    "Cabeceio": {"Cabeceio": 80, "Impulsão": 75},
    "Chute de Longe": {"Finalização": 82, "Força de chute": 80},
    "Controle de Cavadinha": {"Finalização": 80, "Curva": 85},
    "Chute com Peito do Pé": {"Finalização": 85, "Força de chute": 85},
    "Folha Seca": {"Finalização": 88, "Curva": 90},
    "Chute com Decolagem": {"Finalização": 80, "Força de chute": 90},
    "Finalização Acrobática": {"Finalização": 85, "Impulsão": 85},
    "Toque de Calcanhar": {"Passe rasteiro": 75, "Controle de bola": 80},
    "Chute de Primeira": {"Finalização": 82, "Talento ofensivo": 80},

    # PASSES E CRUZAMENTOS
    "Passe de Primeira": {"Passe rasteiro": 82, "Controle de bola": 80},
    "Passe na Medida": {"Passe rasteiro": 85, "Passe alto": 80},
    "Cruzamento Preciso": {"Passe alto": 85, "Curva": 80},
    "Curva para Fora": {"Curva": 88, "Chute colocado": 80},
    "Passe Aero Baixo": {"Passe alto": 82, "Curva": 75},
    "Passe sem Olhar": {"Passe rasteiro": 80, "Controle de bola": 85},

    # DEFESA E GOLEIRO
    "Reposição Baixa de Goleiro": {"Talento de goleiro": 80, "Passe rasteiro": 70},
    "Reposição Alta de Goleiro": {"Talento de goleiro": 80, "Passe alto": 75},
    "Arremesso Longo": {"Contato físico": 80, "Força de chute": 75},
    "Interceptação": {"Agressividade": 80, "Talento defensivo": 75},
    "Marcação Individual": {"Agressividade": 82, "Talento defensivo": 85},
    "Volta para Marcar": {"Resistência": 85, "Talento defensivo": 75},
    "Afastamento Acrobático": {"Talento defensivo": 80, "Impulsão": 85},
    "Pegador de Pênalti": {"Reflexo do goleiro": 85, "Alcance do goleiro": 80},

    # MENTAL E ESPECIAL
    "Malícia": {"Drible": 75, "Equilíbrio": 85},
    "Espírito Guerreiro": {"Resistência": 88, "Agressividade": 85},
    "Super Sub": {"Talento ofensivo": 80, "Finalização": 80}
}
