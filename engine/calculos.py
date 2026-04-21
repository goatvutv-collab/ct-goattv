# --- engine/calculos.py ---
from .regras import STATS_BASE_PES, PESOS_OVR, REGRAS_TREINO, REQUISITOS_SKILLS
import streamlit as st

def calcular_ovr_supremo(atleta):
    stats, pos = atleta["stats"], atleta["posicao"]
    cat = "ATA" if pos in ["CA", "SA"] else ("MEI" if pos in ["MAT", "MLD", "MLE", "VOL"] else ("GOL" if pos == "GOL" else "DEF"))
    
    pesos = PESOS_OVR.get(cat, PESOS_OVR["MEI"])
    # Cálculo Ponderado (A posição define a nota)
    total_pesos = sum(pesos.values())
    soma_ponderada = sum(stats.get(s, 40) * w for s, w in pesos.items())
    
    ovr = soma_ponderada / total_pesos
    # Bônus Biométrico
    if (cat == "DEF" and atleta["altura"] >= 1.88) or (cat == "ATA" and atleta["altura"] >= 1.90):
        ovr += 1
    return int(ovr)

def processar_treino_master(atleta, score):
    # Lógica de Idade: Novos aprendem 4x mais que Veteranos
    idade = atleta["idade"]
    fator_idade = 2.0 if idade <= 20 else (1.0 if idade <= 29 else 0.5)
    
    # Se lesionado e velho, ganho é quase nulo
    if atleta["status"] == "Lesionado":
        fator_idade *= 0.3
        if idade > 30: fator_idade *= 0.5

    # Evolução baseada no Arquétipo (DNA)
    arq = atleta.get("dna", "Nenhum")
    if arq != "Nenhum":
        regras = REGRAS_TREINO.get(arq)
        # Sobe os 3 pontos fortes
        for s in regras["sobe"]:
            atleta["stats"][s] = min(99, atleta["stats"][s] + (score/1000 * fator_idade))
        # Desce ou estagna os 3 pontos fracos
        for s in regras["desce"]:
            atleta["stats"][s] = max(40, atleta["stats"][s] - (0.5 if score < 1500 else 0))
    
    atleta["overall"] = calcular_ovr_supremo(atleta)
    return atleta
