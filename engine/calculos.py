from .regras import REQUISITOS_SKILLS, REGRAS_TREINO
import streamlit as st

def processar_treino_master(atleta, arq_alvo, score):
    # Física de Momentum
    # $$Momentum = peso \times \frac{Velocidade}{100}$$
    vel = atleta["stats"].get("Velocidade", 70)
    momentum = atleta["peso"] * (vel / 100)

    if score < 1200:
        # Lógica de Lesão baseada na Resistência (1-3)
        res_lesao = atleta["stats_fixos"].get("Resistência a lesão", 2)
        chance_lesao = (1200 - score) / (res_lesao * 100)
        if chance_lesao > 0.5: atleta["status"] = "Lesionado"
        
        # Regra 3 Desce
        for s in REGRAS_TREINO[arq_alvo]["desce"]:
            atleta["stats"][s] = max(40, round(atleta["stats"][s] - 0.5, 1))
    else:
        # Regra 3 Sobe
        ganho = (score / 3000) * (max(0.1, 1 - (atleta["overall"] / 105)))
        for s in REGRAS_TREINO[arq_alvo]["sobe"]:
            atleta["stats"][s] = min(99, round(atleta["stats"][s] + ganho, 1))
        
        # Evolução da Personalidade
        atleta["personalidade"]["Técnica"] += 0.2 if score > 2000 else 0.1
        atleta["status"] = "Saudável"

        # DESBLOQUEIO DE SKILLS (Limite de 10)
        if len(atleta.get("habilidades", [])) < 10:
            for sk, reqs in REQUISITOS_SKILLS.items():
                if sk not in atleta["habilidades"]:
                    if all(atleta["stats"].get(sr, 0) >= v for sr, v in reqs.items()):
                        atleta["habilidades"].append(sk)
                        st.success(f"🔥 APRENDEU: {sk}!")

    # Maestria de Estilo
    atleta["maestria"][arq_alvo] = min(100.0, atleta["maestria"].get(arq_alvo, 0) + (score / 400))
    return atleta
