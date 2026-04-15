from .regras import PESOS_OVR, REGRAS_TREINO
import streamlit as st

def calcular_ovr_supremo(atleta):
    stats, pos = atleta["stats"], atleta["posicao"]
    pesos = PESOS_OVR.get(pos, PESOS_OVR["MEI"])
    ovr_base = sum(stats.get(s, 70) * w for s, w in pesos.items()) / sum(pesos.values())
    # Bônus PES: Altura estratégica
    bonus = 1 if (pos == "DEF" and atleta["altura"] >= 1.85) or (pos == "ATA" and atleta["altura"] >= 1.88) else 0
    return int(ovr_base + bonus + 0.5)

def processar_treino_master(atleta, arq_alvo, score):
    ovr_atual = atleta["overall"]
    status_ini = atleta.get("status", "Saudável")
    
    # Cálculo de Momentum via LaTeX: 
    # $$M = peso \times \frac{velocidade}{100}$$
    momentum = atleta["peso"] * (atleta["stats"].get("Velocidade", 70) / 100)

    if score < 1200:
        atleta["status"] = "Lesionado" if status_ini == "Saudável" else "Incapacitado"
        punicao = 3.0 if ovr_atual >= 90 else 1.5
        for s in atleta["stats"]:
            if isinstance(atleta["stats"][s], (int, float)):
                atleta["stats"][s] = round(max(40, atleta["stats"][s] - punicao), 1)
        atleta["personalidade"]["Raça"] = max(0, atleta["personalidade"]["Raça"] - 5)
    else:
        mult = 0.3 if status_ini == "Lesionado" else 1.0
        ganho = (score / 2500) * mult * (max(0.1, 1 - (ovr_atual / 105)))
        for s in REGRAS_TREINO[arq_alvo]["sobe"]:
            atleta["stats"][s] = round(atleta["stats"].get(s, 70) + ganho, 1)
        atleta["status"] = "Saudável"

    atleta["historico_ovr"].append({"idade": atleta["idade"], "ovr": atleta["overall"]})
    atleta["overall"] = calcular_ovr_supremo(atleta)
    return atleta
