# --- engine/calculos.py ---
from .regras import REQUISITOS_SKILLS, REGRAS_TREINO, STATS_BASE_PES, PESOS_OVR
import streamlit as st

def calcular_ovr_supremo(atleta):
    stats, pos = atleta["stats"], atleta["posicao"]
    # Define qual peso usar baseado na categoria da posição
    cat = "ATA" if pos in ["CA", "SA"] else ("MEI" if pos in ["MAT", "MLD", "MLE", "VOL"] else ("GOL" if pos == "GOL" else "DEF"))
    pesos = PESOS_OVR.get(cat, PESOS_OVR["MEI"])
    
    ovr_base = sum(stats.get(s, 70) * w for s, w in pesos.items()) / sum(pesos.values())
    bonus = 1 if (cat == "DEF" and atleta["altura"] >= 1.85) or (cat == "ATA" and atleta["altura"] >= 1.88) else 0
    return int(ovr_base + bonus + 0.5)

def processar_treino_master(atleta, arq_alvo, score):
    vel = atleta["stats"].get("Velocidade", 70)
    momentum = atleta["peso"] * (vel / 100)

    if score < 1200:
        # LOGICA DE LESÃO (Baseada na Resistência a Lesão 1-3)
        res_lesao = atleta.get("stats_fixos", {}).get("Resistência a lesão", 2)
        if score < (900 / res_lesao):
            atleta["status"] = "Lesionado"
            st.warning("🚑 LESÃO NO TREINO! Cuidado com a carga.")

        # Regra 3 Desce
        for s in REGRAS_TREINO[arq_alvo]["desce"]:
            atleta["stats"][s] = max(40, round(atleta["stats"][s] - 0.7, 1))
        atleta["personalidade"]["Raça"] = max(0, atleta["personalidade"]["Raça"] - 3)
    
    else:
        # Regra 3 Sobe
        ganho = (score / 2800) * (max(0.1, 1 - (atleta["overall"] / 105)))
        for s in REGRAS_TREINO[arq_alvo]["sobe"]:
            atleta["stats"][s] = min(99, round(atleta["stats"][s] + ganho, 1))

        # Evolução Mental
        atleta["personalidade"]["Técnica"] += 0.2 if score > 2000 else 0.1
        atleta["personalidade"]["Compostura"] += 0.3 if score > 2500 else 0
        atleta["status"] = "Saudável"

        # DESBLOQUEIO DE SKILLS (Limite 10 - Não desaprende)
        if len(atleta.get("habilidades", [])) < 10:
            for sk, reqs in REQUISITOS_SKILLS.items():
                if sk not in atleta["habilidades"]:
                    if all(atleta["stats"].get(sr, 0) >= v for sr, v in reqs.items()):
                        atleta["habilidades"].append(sk)
                        st.balloons()
                        st.success(f"🔥 NOVO CONHECIMENTO: {sk}!")

    atleta["maestria"][arq_alvo] = min(100.0, atleta["maestria"].get(arq_alvo, 0) + (score / 400))
    if atleta["maestria"][arq_alvo] >= 90:
        atleta["dna"] = f"ESPECIALISTA: {arq_alvo.upper()}"

    atleta["overall"] = calcular_ovr_supremo(atleta)
    return atleta
