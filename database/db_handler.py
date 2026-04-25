import streamlit as st
import os
from supabase import create_client

# --- CONEXÃO BLINDADA (MULTI-AMBIENTE) ---
URL = os.environ.get("SUPABASE_URL") or (st.secrets.get("SUPABASE_URL") if "SUPABASE_URL" in st.secrets else None)
KEY = os.environ.get("SUPABASE_KEY") or (st.secrets.get("SUPABASE_KEY") if "SUPABASE_KEY" in st.secrets else None)

if not URL or not KEY:
    st.error("⚠️ FALHA CRÍTICA DE INFRAESTRUTURA: Chaves de autenticação não detectadas.")
    st.stop()

supabase = create_client(URL, KEY)

# --- NÚCLEO DE TRADUÇÃO (CURA DA RODINHA MURCHA) ---
def mapear_stats_para_radar(row):
    """
    SINCRONIA TOTAL: Traduz as colunas do SQL para os nomes EXATOS que o 
    gráfico do Radar espera na interface. Se o Radar usar 'Talento ofensivo', 
    o banco 'talento_ofensivo' vira a chave certa aqui.
    """
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
    """Busca a federação inteira e reconstrói os objetos complexos."""
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
    """Localiza o atleta e garante que o Radar e os Metadados estejam íntegros."""
    try:
        id_limpo = nome_id.upper().strip()
        res = supabase.table("jogadores").select("*").eq("nome", id_limpo).execute()
        if res.data:
            atleta = res.data[0]
            # Reconstrução do dicionário de stats para o Plotly
            atleta["stats"] = mapear_stats_para_radar(atleta)
            return atleta
        return None
    except Exception as e:
        print(f"Erro na busca: {e}")
        return None

def registrar_novo_atleta(atleta_dict):
    """
    FUSÃO TOTAL: Transforma o dicionário do App nas colunas planas do SQL.
    Aplica lógica robusta para aceitar chaves com ou sem acentos no dicionário de origem.
    """
    try:
        # Extraímos o dicionário 'stats' para espalhar nas colunas SQL
        s = atleta_dict.pop("stats", {})
        
        payload = {
            "nome":          atleta_dict.get("nome").upper().strip(),
            "nome_completo": atleta_dict.get("nome_completo"),
            "nascimento":    atleta_dict.get("nascimento"),
            "idade":         atleta_dict.get("idade"),
            "altura":        atleta_dict.get("altura"),
            "peso":          atleta_dict.get("peso"),
            "posicao":       atleta_dict.get("posicao"),
            "dna":           atleta_dict.get("dna"),
            "dna_origem":    atleta_dict.get("dna_origem"), # Preservação histórica
            "foto":          atleta_dict.get("foto"),
            "status":        atleta_dict.get("status", "Saudável"),
            "overall":       atleta_dict.get("overall", 75.0),
            
            # --- MAPEAMENTO CASE-INSENSITIVE PARA SQL SUPREMO ---
            # Busca 'Finalização' ou 'finalizacao' para garantir que nunca venha vazio
            "finalizacao":      s.get("Finalização", s.get("finalizacao", 70.0)),
            "talento_ofensivo": s.get("Talento ofensivo", s.get("Talento Ofensivo", 70.0)),
            "drible":           s.get("Drible", s.get("drible", 70.0)),
            "velocidade":       s.get("Velocidade", s.get("velocidade", 70.0)),
            "aceleracao":       s.get("Aceleração", s.get("aceleracao", 70.0)),
            "passe_rasteiro":   s.get("Passe rasteiro", s.get("Passe Rasteiro", 70.0)),
            "resistencia":      s.get("Resistência", s.get("resistencia", 70.0)),
            "talento_defensivo": s.get("Talento defensivo", s.get("Talento Defensivo", 70.0)),
            "contato_fisico":   s.get("Contato físico", s.get("Contato Físico", 70.0)),
            "reflexo_gk":       s.get("Reflexo GK", 70.0),
            "firmeza_gk":       s.get("Firmeza GK", 70.0),
            "alcance_gk":       s.get("Alcance GK", 70.0),
            
            # --- CAMPOS JSONB (METADADOS) ---
            "habilidades":   atleta_dict.get("habilidades", []),
            "maestria":      atleta_dict.get("maestria", {}), # Vital para o Laboratório persistente
            "personalidade": atleta_dict.get("personalidade", {}),
            "stats_fixos":   atleta_dict.get("stats_fixos", {}),
            "historico_ovr": atleta_dict.get("historico_ovr", [])
        }
        
        supabase.table("jogadores").insert(payload).execute()
        return True
    except Exception as e:
        st.error(f"❌ Erro Crítico no Registro de Contrato: {e}")
        return False

def salvar_evolucao_treino(nome_id, atributos_novos):
    """Atualização atômica para stats, progresso de maestria ou novas skills."""
    try:
        id_atleta = nome_id.upper().strip()
        supabase.table("jogadores").update(atributos_novos).eq("nome", id_atleta).execute()
        return True
    except Exception as e:
        st.error(f"❌ Erro na Sincronização de Evolução: {e}")
        return False
