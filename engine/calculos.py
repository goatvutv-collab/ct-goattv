# --- engine/calculos.py ---
from .regras import STATS_BASE_PES, PESOS_OVR, REGRAS_TREINO, REQUISITOS_SKILLS
import streamlit as st
from datetime import date

def calcular_idade(data_nascimento):
    """Calcula idade exata baseada na data do calendário para evitar burlas."""
    if isinstance(data_nascimento, str):
        data_nascimento = date.fromisoformat(data_nascimento)
    today = date.today()
    return today.year - data_nascimento.year - ((today.month, today.day) < (data_nascimento.month, data_nascimento.day))

def distribuir_stats_iniciais(dna):
    """
    IMPLEMENTAÇÃO NASCIMENTO FLAT 75 PONDERADO.
    O Atleta nasce com média 75, mas a distribuição foca nos pontos fortes do DNA escolhido.
    """
    stats = {s: 75.0 for s in STATS_BASE_PES}
    if dna in REGRAS_TREINO:
        for s in REGRAS_TREINO[dna]["sobe"]: 
            stats[s] = 82.0  # Atributos dominantes começam acima da média
        for s in REGRAS_TREINO[dna]["desce"]: 
            stats[s] = 68.0  # Atributos de dificuldade começam abaixo
    return stats

def calcular_ovr_supremo(atleta):
    """
    Cálculo Ponderado de Overall (Nota Geral).
    A posição define quais atributos pesam mais. Inclui bônus biométrico PES 2021.
    """
    stats, pos, alt = atleta["stats"], atleta["posicao"], atleta["altura"]
    
    # Mapeamento de Categoria Tática
    cat = "ATA" if pos in ["CA", "SA"] else (
        "MEI" if pos in ["MAT", "MLD", "MLE", "VOL"] else (
            "GOL" if pos == "GOL" else "DEF"
        )
    )

    pesos = PESOS_OVR.get(cat, PESOS_OVR["MEI"])
    
    # Cálculo Ponderado
    total_pesos = sum(pesos.values())
    soma_ponderada = sum(stats.get(s, 40) * w for s, w in pesos.items())
    ovr_base = soma_ponderada / total_pesos
    
    # Bônus Biométrico Estratégico (Zagueiros >= 1.88m ou Atacantes >= 1.90m ganham +1)
    bonus = 1 if (cat == "DEF" and alt >= 1.88) or (cat == "ATA" and alt >= 1.90) else 0
    
    return int(ovr_base + bonus + 0.5)

def processar_treino_master(atleta, estilo_treino, score):
    """
    MOTOR PRINCIPAL DE EVOLUÇÃO (VERSÃO SUPREMA).
    Processa: Momentum Físico, Idade Real, Regra 3x3, Mutação de DNA e Unlock de Skills.
    """
    ovr_atual = atleta["overall"]
    status_ini = atleta.get("status", "Saudável")
    vel_atleta = atleta["stats"].get("Velocidade", 70)
    idade = atleta["idade"]

    # 1. FATOR BIOLÓGICO (IDADE)
    # Jovens (até 20) aprendem 2x. Veteranos (30+) têm aprendizado reduzido para 0.4x.
    fator_idade = 2.0 if idade <= 20 else (1.0 if idade <= 29 else 0.4)
    
    # 2. FÍSICA DE MOMENTUM (Impacto do Peso vs Velocidade no esforço)
    momentum = atleta["peso"] * (vel_atleta / 100)

    # --- CENÁRIO A: FALHA NO TREINO (Score < 1200) ---
    if score < 1200:
        # Lógica de Lesão baseada na Resistência (1 a 3)
        res_lesao = atleta.get("stats_fixos", {}).get("Resistência a lesão", 2)
        if score < (900 / res_lesao):
            atleta["status"] = "Lesionado" if status_ini == "Saudável" else "Incapacitado"
            st.error(f"🚑 DP MÉDICO: Lesão detectada! Momentum de impacto: {momentum:.1f}")

        # Atrofia Psicológica (Perda de Raça por baixo desempenho)
        atleta["personalidade"]["Raça"] = max(0, atleta["personalidade"]["Raça"] - 3)
        
        # PUNIÇÃO TIER (Jogadores de elite perdem mais se treinarem mal)
        punicao = 3.0 if ovr_atual >= 90 else (1.5 if ovr_atual >= 85 else 0.5)
        
        # Regra 3 Desce (Atrofia técnica por negligência)
        for s in REGRAS_TREINO[estilo_treino]["desce"]:
            atleta["stats"][s] = round(max(40, atleta["stats"][s] - (punicao * (momentum/70))), 1)

    # --- CENÁRIO B: SUCESSO NO TREINO (Score >= 1200) ---
    else:
        # Multiplicador de Rendimento (Lesionados evoluem apenas 30%)
        mult = 0.3 if status_ini == "Lesionado" else 1.0
        
        # FÓRMULA DE GANHO SUPREMO (A curva fica flat conforme chega em 105)
        # $$Ganho = (\frac{Score}{2800}) \times FatorIdade \times Multiplicador \times \max(0.1, 1 - \frac{OVR}{105})$$
        ganho = (score / 2800) * fator_idade * mult * (max(0.1, 1 - (ovr_atual / 105)))
        
        # Regra 3 Sobe
        for s in REGRAS_TREINO[estilo_treino]["sobe"]:
            atleta["stats"][s] = round(min(99, atleta["stats"][s] + ganho), 1)
        
        # EVOLUÇÃO PSICOLÓGICA
        atleta["personalidade"]["Técnica"] = min(100, atleta["personalidade"]["Técnica"] + 0.5)
        if score > 2000:
            atleta["personalidade"]["Compostura"] = min(100, atleta["personalidade"]["Compostura"] + 1)
            atleta["status"] = "Saudável" # Treino de elite acelera recuperação

        # DESBLOQUEIO DE SKILLS (Limite 10 simultâneas)
        if status_ini == "Saudável" and len(atleta.get("habilidades", [])) < 10:
            for sk, reqs in REQUISITOS_SKILLS.items():
                if sk not in atleta["habilidades"]:
                    if all(atleta["stats"].get(sr, 0) >= v for sr, v in reqs.items()):
                        atleta["habilidades"].append(sk)
                        st.balloons()
                        st.success(f"🔥 NOVO CONHECIMENTO ADQUIRIDO: {sk}!")

    # 3. MAESTRIA E MUTAÇÃO DE DNA
    if "maestria" not in atleta: atleta["maestria"] = {}
    atleta["maestria"][estilo_treino] = min(100.0, atleta["maestria"].get(estilo_treino, 0) + (score / 350))
    
    # Gatilho de Mutação: O estilo com maior maestria acumulada define o novo DNA
    novo_dna = max(atleta["maestria"], key=atleta["maestria"].get)
    if novo_dna != atleta["dna"]:
        atleta["dna"] = novo_dna
        st.toast(f"🧬 MUTAÇÃO TÁTICA: Agora você é {novo_dna}!", icon="🧪")

    # 4. ATUALIZAÇÃO FINAL
    atleta["overall"] = calcular_ovr_supremo(atleta)
    
    # Histórico para gráfico de evolução
    if "historico_ovr" not in atleta: atleta["historico_ovr"] = []
    atleta["historico_ovr"].append({"idade": atleta["idade"], "ovr": atleta["overall"]})
    
    return atleta
