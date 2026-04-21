# --- engine/calculos.py ---
from .regras import STATS_BASE_PES, PESOS_OVR, REGRAS_TREINO
import streamlit as st
from datetime import date

def calcular_idade(data_nascimento):
    """Calcula idade exata para evitar burlas."""
    today = date.today()
    return today.year - data_nascimento.year - ((today.month, today.day) < (data_nascimento.month, data_nascimento.day))

def distribuir_stats_iniciais(dna):
    """Nascimento Flat 75 Ponderado pelo DNA."""
    stats = {s: 75.0 for s in STATS_BASE_PES}
    if dna in REGRAS_TREINO:
        for s in REGRAS_TREINO[dna]["sobe"]: stats[s] = 82.0
        for s in REGRAS_TREINO[dna]["desce"]: stats[s] = 68.0
    return stats

def calcular_ovr_supremo(atleta):
    stats, pos, alt = atleta["stats"], atleta["posicao"], atleta["altura"]
    cat = "ATA" if pos in ["CA", "SA"] else ("MEI" if pos in ["MAT", "MLD", "MLE", "VOL"] else ("GOL" if pos == "GOL" else "DEF"))
    
    pesos = PESOS_OVR.get(cat, PESOS_OVR["MEI"])
    soma_ponderada = sum(stats.get(s, 40) * w for s, w in pesos.items())
    ovr = soma_ponderada / sum(pesos.values())
    
    if (cat == "DEF" and alt >= 1.88) or (cat == "ATA" and alt >= 1.90): ovr += 1
    return int(ovr + 0.5)

def processar_treino_master(atleta, estilo_treino, score):
    idade = atleta["idade"]
    fator_idade = 2.0 if idade <= 20 else (1.0 if idade <= 29 else 0.4)
    if atleta["status"] == "Lesionado": fator_idade *= 0.3

    regras = REGRAS_TREINO.get(estilo_treino)
    # XP final baseada em Idade e Nível atual (Elite)
    ganho = (score / 2200) * fator_idade * (max(0.1, 1 - (atleta["overall"] / 105)))

    for s in regras["sobe"]:
        atleta["stats"][s] = round(min(99, atleta["stats"][s] + ganho), 1)
    for s in regras["desce"]:
        perda = 0.3 if score > 1800 else 0.1
        atleta["stats"][s] = round(max(40, atleta["stats"][s] - perda), 1)

    atleta["maestria"][estilo_treino] += (score / 400)
    # Mutação de DNA Dinâmica
    atleta["dna"] = max(atleta["maestria"], key=atleta["maestria"].get)
    atleta["overall"] = calcular_ovr_supremo(atleta)
    return atleta
