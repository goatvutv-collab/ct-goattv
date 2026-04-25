import streamlit as st
import os
from supabase import create_client

# --- CONEXÃO BLINDADA (MULTI-AMBIENTE) ---
URL = os.environ.get("SUPABASE_URL") or (st.secrets.get("SUPABASE_URL") if "SUPABASE_URL" in st.secrets else None)
KEY = os.environ.get("SUPABASE_KEY") or (st.secrets.get("SUPABASE_KEY") if "SUPABASE_KEY" in st.secrets else None)

if not URL or not KEY:
    st.error("⚠️ FALHA CRÍTICA: Chaves de autenticação não detectadas.")
    st.stop()

supabase = create_client(URL, KEY)

# --- NÚCLEO DE TRADUÇÃO (CURA DA RODINHA MURCHA) ---
def mapear_stats_para_radar(row):
    """Traduz colunas do SQL para os nomes que a Interface (Radar/Fisiologia) exige."""
    return {
        "Finalização":      row.get("finalizacao", 70.0),
        "Talento ofensivo": row.get("talento_ofensivo", 70.0),
        "Drible":           row.get("drible", 70.0),
        "Velocidade":       row.get("velocidade", 70.0),
        "Aceleração":       row.get("aceleracao", 70.0),
        "Passe rasteiro":   row.get("passe_rasteiro", 70.0),
        "Resistência":      row.get("resistencia", 70.0),
        "Talento defensivo": row.get("talento_defensivo", 70.0),
        "Contato físico":   row.get("contato_fisico", 70.0),
        "Reflexo GK":       row.get("reflexo_gk", 70.0),
        "Firmeza GK":       row.get("firmeza_gk", 70.0),
        "Alcance GK":       row.get("alcance_gk", 70.0)
    }

# --- FUNÇÕES DE MEMÓRIA SUPREMA ---

def carregar_todos_jogadores():
    """Busca a federação inteira para rankings ou listagens."""
    try:
        res = supabase.table("jogadores").select("*").execute()
        jogadores_formatados = {}
        for atleta in res.data:
            atleta["stats"] = mapear_stats_para_radar(atleta)
            jogadores_formatados[atleta['nome']] = atleta
        return jogadores_formatados
    except Exception as e:
        st.error(f"❌ Erro ao carregar federação: {e}")
        return {}

def buscar_atleta(nome_id):
    """Localiza o atleta e reconstrói o objeto complexo para o App."""
    try:
        id_limpo = nome_id.upper().strip()
        res = supabase.table("jogadores").select("*").eq("nome", id_limpo).execute()
        if res.data:
            atleta = res.data[0]
            atleta["stats"] = mapear_stats_para_radar(atleta)
            return atleta
        return None
    except Exception as e:
        print(f"Erro na busca: {e}")
        return None

def registrar_novo_atleta(atleta_dict):
    """Transforma o dicionário do App em colunas SQL com preservação de DNA."""
    try:
        # Copiamos para não destruir o dicionário original do App
        dados = atleta_dict.copy()
        s = dados.pop("stats", {})
        
        payload = {
            "nome":           dados.get("nome").upper().strip(),
            "nome_completo":  dados.get("nome_completo"),
            "nascimento":     dados.get("nascimento"),
            "idade":          dados.get("idade"),
            "altura":         dados.get("altura"),
            "peso":           dados.get("peso"),
            "posicao":        dados.get("posicao"),
            "dna":            dados.get("dna"),
            "dna_origem":     dados.get("dna_origem", dados.get("dna")), # Preserva o berço
            "foto":           dados.get("foto"),
            "status":         dados.get("status", "Saudável"),
            "overall":        dados.get("overall", 75.0),
            
            # Espalhando stats (Case-insensitive e Acento-safe)
            "finalizacao":      s.get("Finalização", s.get("finalizacao", 70.0)),
            "talento_ofensivo": s.get("Talento ofensivo", s.get("talento_ofensivo", 70.0)),
            "drible":           s.get("Drible", s.get("drible", 70.0)),
            "velocidade":       s.get("Velocidade", s.get("velocidade", 70.0)),
            "aceleracao":       s.get("Aceleração", s.get("aceleracao", 70.0)),
            "passe_rasteiro":   s.get("Passe rasteiro", s.get("passe_rasteiro", 70.0)),
            "resistencia":      s.get("Resistência", s.get("resistencia", 70.0)),
            "talento_defensivo": s.get("Talento defensivo", s.get("talento_defensivo", 70.0)),
            "contato_fisico":   s.get("Contato físico", s.get("contato_fisico", 70.0)),
            "reflexo_gk":       s.get("Reflexo GK", 70.0),
            "firmeza_gk":       s.get("Firmeza GK", 70.0),
            "alcance_gk":       s.get("Alcance GK", 70.0),
            
            # Campos JSONB (Metadados)
            "habilidades":    dados.get("habilidades", []),
            "maestria":       dados.get("maestria", {}),
            "personalidade":  dados.get("personalidade", {}),
            "stats_fixos":    dados.get("stats_fixos", {}),
            "historico_ovr":  dados.get("historico_ovr", []),
            "posicoes":       dados.get("posicoes", {})
        }
        
        supabase.table("jogadores").insert(payload).execute()
        return True
    except Exception as e:
        st.error(f"❌ Erro ao registrar contrato: {e}")
        return False

def salvar_evolucao_treino(nome_id, atributos_novos):
    """Atualização cirúrgica: stats, maestria ou bag de habilidades."""
    try:
        id_atleta = nome_id.upper().strip()
        supabase.table("jogadores").update(atributos_novos).eq("nome", id_atleta).execute()
        return True
    except Exception as e:
        st.error(f"❌ Erro na sincronização: {e}")
        return False
