# --- engine/calculos.py ---
from .regras import REQUISITOS_SKILLS, REGRAS_TREINO, STATS_BASE_PES, PESOS_OVR
import streamlit as st

def calcular_ovr_supremo(atleta):
    stats, pos, alt = atleta["stats"], atleta["posicao"], atleta["altura"]
    cat = "ATA" if pos in ["CA", "SA"] else ("MEI" if pos in ["MAT", "MLD", "MLE", "VOL"] else ("GOL" if pos == "GOL" else "DEF"))
    pesos = PESOS_OVR.get(cat, PESOS_OVR["MEI"])
    
    ovr_base = sum(stats.get(s, 70) * w for s, w in pesos.items()) / sum(pesos.values())
    # Bônus PES por altura estratégica
    bonus = 1 if (cat == "DEF" and alt >= 1.85) or (cat == "ATA" and alt >= 1.88) else 0
    return int(ovr_base + bonus + 0.5)

def processar_treino_master(atleta, arq_alvo, score):
    vel = atleta["stats"].get("Velocidade", 70)
    momentum = atleta["peso"] * (vel / 100)

    if score < 1200:
        res_lesao = atleta.get("stats_fixos", {}).get("Resistência a lesão", 2)
        if score < (900 / res_lesao):
            atleta["status"] = "Lesionado"
            st.error("🚑 DEPARTAMENTO MÉDICO: Lesão detectada!")

        for s in REGRAS_TREINO[arq_alvo]["desce"]:
            atleta["stats"][s] = max(40, round(atleta["stats"][s] - 0.7, 1))
        atleta["personalidade"]["Raça"] = max(0, atleta["personalidade"]["Raça"] - 3)
    else:
        ganho = (score / 2800) * (max(0.1, 1 - (atleta["overall"] / 105)))
        for s in REGRAS_TREINO[arq_alvo]["sobe"]:
            atleta["stats"][s] = min(99, round(atleta["stats"][s] + ganho, 1))
        
        atleta["personalidade"]["Técnica"] += 0.2 if score > 2000 else 0.1
        atleta["status"] = "Saudável"

        if len(atleta.get("habilidades", [])) < 10:
            for sk, reqs in REQUISITOS_SKILLS.items():
                if sk not in atleta["habilidades"]:
                    if all(atleta["stats"].get(sr, 0) >= v for sr, v in reqs.items()):
                        atleta["habilidades"].append(sk)
                        st.balloons()

    atleta["maestria"][arq_alvo] = min(100.0, atleta["maestria"].get(arq_alvo, 0) + (score / 400))
    atleta["overall"] = calcular_ovr_supremo(atleta)
    return atleta
