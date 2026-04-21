# --- engine/calculos.py ---
from .regras import STATS_BASE_PES, PESOS_OVR, REGRAS_TREINO, REQUISITOS_SKILLS
import streamlit as st

def calcular_ovr_supremo(atleta):
    """
    Cálculo Ponderado de Nota Geral (OVR).
    Não é média simples! Atributos chave da posição pesam 5x mais.
    """
    stats, pos, alt = atleta["stats"], atleta["posicao"], atleta["altura"]

    # Definição de Categoria Tática
    if pos in ["CA", "SA"]: cat = "ATA"
    elif pos in ["MAT", "MLD", "MLE", "VOL"]: cat = "MEI"
    elif pos == "GOL": cat = "GOL"
    else: cat = "DEF"

    pesos = PESOS_OVR.get(cat, PESOS_OVR["MEI"])
    
    # Cálculo Ponderado: Soma(Atributo * Peso) / Soma(Pesos)
    total_pesos = sum(pesos.values())
    soma_ponderada = sum(stats.get(s, 40) * w for s, w in pesos.items())
    
    ovr_final = soma_ponderada / total_pesos

    # Bônus Biométrico PES 2021 (Altura Estratégica)
    # Zagueiros/Laterais >= 1.88m ou Atacantes >= 1.90m ganham +1 de bônus real no OVR
    if (cat == "DEF" and alt >= 1.88) or (cat == "ATA" and alt >= 1.90):
        ovr_final += 1

    return int(ovr_final + 0.5) # Arredondamento clássico

def reavaliar_dna_atleta(atleta):
    """
    O Motor de Mutação: O DNA não é fixo.
    O arquétipo com maior maestria acumulada define a identidade atual do jogador.
    """
    maestrias = atleta.get("maestria", {})
    
    # Se nunca treinou de verdade, mantém o DNA de nascimento (Origem)
    if not any(v > 0 for v in maestrias.values()):
        return atleta.get("dna_origem", "Nenhum")

    # Identifica qual arquétipo o jogador mais 'gastou tempo' treinando
    novo_dna = max(maestrias, key=maestrias.get)
    
    # Se o DNA mudou, avisamos o sistema
    if novo_dna != atleta["dna"]:
        atleta["dna"] = novo_dna
        st.toast(f"🧬 DNA MUTADO: Agora você é reconhecido como {novo_dna}!", icon="🧪")
    
    return novo_dna

def processar_treino_master(atleta, arq_treinado, score):
    """
    Motor de Evolução Bio-Técnica.
    Processa: Idade, Lesão, Regra 3x3 e Mutação de DNA.
    """
    idade = atleta["idade"]
    ovr_atual = atleta["overall"]
    status = atleta.get("status", "Saudável")

    # 1. FATOR BIOLÓGICO (IDADE)
    # Novos (até 20) aprendem 2x mais. Veteranos (30+) aprendem metade.
    fator_idade = 2.0 if idade <= 20 else (1.0 if idade <= 29 else 0.5)
    
    # Penalidade por Lesão (Evolução cai para 30%)
    if status == "Lesionado":
        fator_idade *= 0.3
        # Veterano lesionado praticamente estagna (Regra do 0.15x)
        if idade >= 30: fator_idade *= 0.5

    # 2. A REGRA SAGRADA: 3 SOBE / 3 DESCE
    # O jogador é um sistema de vasos comunicantes.
    regras = REGRAS_TREINO.get(arq_treinado)
    
    if regras:
        # GANHO TÉCNICO: Baseado no Score e na Facilidade Biológica (Idade)
        # Fórmula: (Pontos / 2000) * Multiplicador de Idade * (Dificuldade de Elite)
        ganho_base = (score / 2000) * fator_idade * (max(0.1, 1 - (ovr_atual / 105)))
        
        for s in regras["sobe"]:
            atleta["stats"][s] = round(min(99, atleta["stats"][s] + ganho_base), 1)
            
        for s in regras["desce"]:
            # Perda Técnica: Quanto melhor o treino, mais você 'esquece' o que não foca
            perda = 0.3 if score > 1500 else 0.1
            atleta["stats"][s] = round(max(40, atleta["stats"][s] - perda), 1)

    # 3. ATUALIZAÇÃO DE MAESTRIA E DNA
    # A maestria sobe sempre, consolidando o novo caminho do jogador
    if "maestria" not in atleta: 
        atleta["maestria"] = {m: 0.0 for m in REGRAS_TREINO.keys()}
    
    atleta["maestria"][arq_treinado] += (score / 500)
    
    # Chama a Mutação
    atleta["dna"] = reavaliar_dna_atleta(atleta)

    # 4. FINALIZAÇÃO E HISTÓRICO
    atleta["overall"] = calcular_ovr_supremo(atleta)
    
    if "historico_ovr" not in atleta: atleta["historico_ovr"] = []
    atleta["historico_ovr"].append({"idade": idade, "ovr": atleta["overall"]})

    return atleta
