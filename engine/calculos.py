# --- engine/calculos.py ---
from .regras import REQUISITOS_SKILLS, REGRAS_TREINO, STATS_BASE_PES, PESOS_OVR
import streamlit as st

def calcular_ovr_supremo(atleta):
    """
    Calcula a nota geral (Overall) baseada na posição e atributos técnicos.
    Inclui bônus de altura estratégica do PES original.
    """
    stats, pos, alt = atleta["stats"], atleta["posicao"], atleta["altura"]
    
    # Mapeia a posição para a categoria de peso correta
    cat = "ATA" if pos in ["CA", "SA"] else (
        "MEI" if pos in ["MAT", "MLD", "MLE", "VOL"] else (
            "GOL" if pos == "GOL" else "DEF"
        )
    )
    
    pesos = PESOS_OVR.get(cat, PESOS_OVR["MEI"])
    
    # Cálculo ponderado: Atributos chave valem mais para o OVR
    # Se o stat não existir por algum motivo, assume 70 (padrão base)
    ovr_base = sum(stats.get(s, 70) * w for s, w in pesos.items()) / sum(pesos.values())
    
    # Bônus PES: Altura estratégica (Zagueiros >= 1.85m ou Atacantes >= 1.88m ganham +1)
    bonus = 1 if (cat == "DEF" and alt >= 1.85) or (cat == "ATA" and alt >= 1.88) else 0
    
    return int(ovr_base + bonus + 0.5)

def processar_treino_master(atleta, arq_alvo, score):
    """
    Motor principal de evolução. Processa ganhos técnicos, mentais e riscos físicos.
    arq_alvo: O estilo de treino escolhido (Ex: 'O Matador')
    score: Pontuação obtida no mini-game
    """
    ovr_atual = atleta["overall"]
    status_ini = atleta.get("status", "Saudável")
    vel_atleta = atleta["stats"].get("Velocidade", 70)
    
    # 1. FÍSICA DE MOMENTUM (Impacto do Peso vs Velocidade)
    momentum = atleta["peso"] * (vel_atleta / 100)

    # --- CENÁRIO A: FALHA NO TREINO (Score < 1200) ---
    if score < 1200:
        # Lógica de Lesão baseada na Resistência (1 a 3)
        res_lesao = atleta.get("stats_fixos", {}).get("Resistência a lesão", 2)
        # Quanto menor a resistência, mais fácil lesionar com score baixo
        if score < (900 / res_lesao):
            atleta["status"] = "Lesionado" if status_ini == "Saudável" else "Incapacitado"
            st.error(f"🚑 DEPARTAMENTO MÉDICO: Lesão detectada! Momentum de impacto: {momentum:.1f}")

        # Atrofia Psicológica
        atleta["personalidade"]["Raça"] = max(0, atleta["personalidade"]["Raça"] - 3)
        
        # PUNIÇÃO TIER (Jogadores de elite perdem mais se treinarem mal)
        punicao = 3.0 if ovr_atual >= 90 else (1.5 if ovr_atual >= 85 else 0.5)
        
        # Regra 3 Desce (Atributos que sofrem com esse estilo de treino)
        for s in REGRAS_TREINO[arq_alvo]["desce"]:
            atleta["stats"][s] = round(max(40, atleta["stats"][s] - (punicao * (momentum/70))), 1)

    # --- CENÁRIO B: SUCESSO NO TREINO (Score >= 1200) ---
    else:
        # Multiplicador de Rendimento (Lesionados evoluem apenas 30%)
        mult = 0.3 if status_ini == "Lesionado" else 1.0
        
        # FÓRMULA DE GANHO SUPREMO (Fica mais difícil subir conforme chega no limite 105)
        ganho = (score / 2800) * mult * (max(0.1, 1 - (ovr_atual / 105)))
        
        # Regra 3 Sobe (Atributos focados no estilo)
        for s in REGRAS_TREINO[arq_alvo]["sobe"]:
            atleta["stats"][s] = round(min(99, atleta["stats"][s] + ganho), 1)
        
        # EVOLUÇÃO PSICOLÓGICA (Técnica e Compostura sobem com dedicação)
        atleta["personalidade"]["Técnica"] = min(100, atleta["personalidade"]["Técnica"] + 0.5)
        if score > 2000:
            atleta["personalidade"]["Compostura"] = min(100, atleta["personalidade"]["Compostura"] + 1)
            atleta["status"] = "Saudável" # Treino de elite ajuda na recuperação

        # DESBLOQUEIO DE CONHECIMENTO (SKILLS - Limite 10)
        if status_ini == "Saudável" and len(atleta.get("habilidades", [])) < 10:
            for sk, reqs in REQUISITOS_SKILLS.items():
                if sk not in atleta["habilidades"]:
                    # Verifica se o atleta atingiu todos os requisitos técnicos da skill
                    if all(atleta["stats"].get(sr, 0) >= v for sr, v in reqs.items()):
                        atleta["habilidades"].append(sk)
                        st.balloons()
                        st.success(f"🔥 NOVO CONHECIMENTO ADQUIRIDO: {sk}!")

    # 2. MAESTRIA E DNA (Especialização no Estilo)
    # Ganhos de maestria são independentes de ser Healthy ou Lesionado
    atleta["maestria"][arq_alvo] = min(100.0, atleta["maestria"].get(arq_alvo, 0) + (score / 350))
    
    # Se atingir 90% de maestria, o DNA do atleta muda para Especialista
    if atleta["maestria"][arq_alvo] >= 90:
        atleta["dna"] = f"ESPECIALISTA: {arq_alvo.upper()}"

    # 3. ATUALIZAÇÃO FINAL
    atleta["overall"] = calcular_ovr_supremo(atleta)
    
    # Registra no histórico para o gráfico de evolução
    if "historico_ovr" not in atleta: atleta["historico_ovr"] = []
    atleta["historico_ovr"].append({"idade": atleta["idade"], "ovr": atleta["overall"]})
    
    return atleta
