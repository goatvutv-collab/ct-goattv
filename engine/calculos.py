# --- engine/calculos.py ---
from .regras import STATS_BASE_PES, PESOS_OVR, REGRAS_TREINO
import streamlit as st

def calcular_ovr_supremo(atleta):
    """Cálculo de Overall Ponderado baseado na posição."""
    stats, pos, alt = atleta["stats"], atleta["posicao"], atleta["altura"]
    cat = "ATA" if pos in ["CA", "SA"] else ("MEI" if pos in ["MAT", "MLD", "MLE", "VOL"] else ("GOL" if pos == "GOL" else "DEF"))
    
    pesos = PESOS_OVR.get(cat, PESOS_OVR["MEI"])
    soma_ponderada = sum(stats.get(s, 40) * w for s, w in pesos.items())
    ovr = soma_ponderada / sum(pesos.values())
    
    # Bônus Biométrico
    if (cat == "DEF" and alt >= 1.88) or (cat == "ATA" and alt >= 1.90): ovr += 1
    return int(ovr + 0.5)

def reavaliar_dna(atleta):
    """O DNA (Arquétipo) muda conforme a especialização do treino."""
    maestrias = atleta.get("maestria", {})
    if not any(v > 0 for v in maestrias.values()): return atleta["dna"]
    
    novo_dna = max(maestrias, key=maestrias.get)
    if novo_dna != atleta["dna"]:
        atleta["dna"] = novo_dna
        st.toast(f"🧬 MUTAÇÃO TÁTICA: Você agora é {novo_dna}!")
    return novo_dna

def processar_treino_master(atleta, estilo_treino, score):
    idade = atleta["idade"]
    # Curva de Aprendizado: Jovens voam, Veteranos lutam
    fator_idade = 2.0 if idade <= 20 else (1.0 if idade <= 29 else 0.4)
    
    # Penalidade de Lesão Crítica
    if atleta["status"] == "Lesionado":
        fator_idade *= 0.3
        if idade > 30: fator_idade = 0.05 # Quase impossível evoluir

    # REGRA SAGRADA 3x3
    regras = REGRAS_TREINO.get(estilo_treino)
    ganho = (score / 2200) * fator_idade * (max(0.1, 1 - (atleta["overall"] / 105)))

    for s in regras["sobe"]:
        atleta["stats"][s] = round(min(99, atleta["stats"][s] + ganho), 1)
    for s in regras["desce"]:
        perda = 0.3 if score > 1800 else 0.1
        atleta["stats"][s] = round(max(40, atleta["stats"][s] - perda), 1)

    # Evolução de Maestria e Mutação de DNA
    atleta["maestria"][estilo_treino] += (score / 400)
    atleta["dna"] = reavaliar_dna(atleta)
    atleta["overall"] = calcular_ovr_supremo(atleta)
    
    return atleta
