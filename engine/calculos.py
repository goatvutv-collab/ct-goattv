from .regras import PESOS_OVR, REGRAS_TREINO, REQUISITOS_SKILLS
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
    momentum = atleta["peso"] * (atleta["stats"].get("Velocidade", 70) / 100)

    if score < 1200:
        atleta["status"] = "Lesionado" if status_ini == "Saudável" else "Incapacitado"
        atleta["personalidade"]["Raça"] = max(0, atleta["personalidade"]["Raça"] - 3)
        punicao = 3.0 if ovr_atual >= 90 else (1.5 if ovr_atual >= 85 else 0.5)
        for s in atleta["stats"]: atleta["stats"][s] = round(max(40, atleta["stats"][s] - (punicao * (momentum/70))), 1)
    else:
        mult = 0.3 if status_ini == "Lesionado" else 1.0
        ganho = (score / 2500) * mult * (max(0.1, 1 - (ovr_atual / 105)))
        for s in REGRAS_TREINO[arq_alvo]["sobe"]: atleta["stats"][s] = round(atleta["stats"].get(s, 70) + ganho, 1)
        atleta["personalidade"]["Técnica"] = min(100, atleta["personalidade"]["Técnica"] + 0.5)
        if score > 2000: atleta["personalidade"]["Compostura"] = min(100, atleta["personalidade"]["Compostura"] + 1)
        
        if status_ini == "Saudável" and len(atleta.get("habilidades", [])) < 10:
            for sk, reqs in REQUISITOS_SKILLS.items():
                if sk not in atleta["habilidades"] and all(atleta["stats"].get(sr, 0) >= v for sr, v in reqs.items()):
                    atleta["habilidades"].append(sk); st.balloons()

    atleta["maestria"][arq_alvo] = min(100.0, atleta["maestria"].get(arq_alvo, 0) + (score / 350))
    if atleta["maestria"][arq_alvo] >= 90: atleta["dna"] = f"ESPECIALISTA: {arq_alvo.upper()}"
    atleta["overall"] = calcular_ovr_supremo(atleta)
    return atleta
