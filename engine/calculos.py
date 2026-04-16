from .regras import PESOS_OVR, REGRAS_TREINO
import streamlit as st

def calcular_ovr_supremo(atleta):
    stats, pos = atleta["stats"], atleta["posicao"]
    pesos = PESOS_OVR.get(pos, PESOS_OVR["MEI"])
    ovr_base = sum(stats.get(s, 70) * w for s, w in pesos.items()) / sum(pesos.values())
    bonus = 1 if (pos == "DEF" and atleta["altura"] >= 1.85) or (pos == "ATA" and atleta["altura"] >= 1.88) else 0
    return int(ovr_base + bonus + 0.5)

def processar_treino_master(atleta, arq_alvo, score):
    ovr_atual = atleta["overall"]
    status_ini = atleta.get("status", "Saudável")
    
    # Impacto Físico (Momentum)
    # $$Momentum = peso \times \frac{Velocidade}{100}$$
    momentum = atleta["peso"] * (atleta["stats"].get("Velocidade", 70) / 100)

    if score < 1200:
        atleta["status"] = "Lesionado" if status_ini == "Saudável" else "Incapacitado"
        punicao = 2.8 if ovr_atual >= 90 else 1.4
        for s in atleta["stats"]:
            atleta["stats"][s] = round(max(40, atleta["stats"][s] - (punicao * (momentum/72))), 1)
    else:
        mult = 0.3 if status_ini == "Lesionado" else 1.0
        ganho = (score / 2500) * mult * (max(0.1, 1 - (ovr_atual / 105)))
        for s in REGRAS_TREINO[arq_alvo]["sobe"]:
            atleta["stats"][s] = round(atleta["stats"].get(s, 70) + ganho, 1)
        atleta["status"] = "Saudável"

    atleta["overall"] = calcular_ovr_supremo(atleta)
    return atleta
