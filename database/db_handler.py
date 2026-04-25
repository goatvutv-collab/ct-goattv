import streamlit as st
import os
from supabase import create_client

# --- CONEXÃO BLINDADA (RENDER + LOCAL) ---
URL = os.environ.get("SUPABASE_URL") or (st.secrets.get("SUPABASE_URL") if "SUPABASE_URL" in st.secrets else None)
KEY = os.environ.get("SUPABASE_KEY") or (st.secrets.get("SUPABASE_KEY") if "SUPABASE_KEY" in st.secrets else None)

if not URL or not KEY:
    st.error("⚠️ FALHA DE CONEXÃO: Chaves do Supabase não encontradas.")
    st.stop()

supabase = create_client(URL, KEY)

# --- NÚCLEO DE TRADUÇÃO (CURA DA RODINHA MURCHA) ---
def mapear_stats_para_radar(row):
    """
    Traduz as colunas do SQL para os nomes EXATOS que o gráfico Radar espera.
    Atenção: 'Talento ofensivo' com 'o' minúsculo é o padrão que o radar costuma ler.
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

# --- FUNÇÕES DE MEMÓRIA ---
def carregar_todos_jogadores():
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
    """
    FUSÃO TOTAL: Mapeia o App para o SQL sem esquecer Maestria nem DNA Origem.
    """
    try:
        # Extraímos o dicionário de stats para espalhar nas colunas
        stats_app = atleta_dict.pop("stats", {})
        
        payload = {
            "nome":          atleta_dict.get("nome").upper().strip(),
            "nome_completo": atleta_dict.get("nome_completo"),
            "nascimento":    atleta_dict.get("nascimento"),
            "idade":         atleta_dict.get("idade"),
            "altura":        atleta_dict.get("altura"),
            "peso":          atleta_dict.get("peso"),
            "posicao":       atleta_dict.get("posicao"),
            "dna":           atleta_dict.get("dna"),
            "dna_origem":    atleta_dict.get("dna_origem"), # Preservado!
            "foto":          atleta_dict.get("foto"),
            "status":        atleta_dict.get("status", "Saudável"),
            "overall":       atleta_dict.get("overall", 75.0),
            
            # --- MAPEAMENTO FLAT (Lógica Case-Insensitive para evitar erros) ---
            "finalizacao":      stats_app.get("Finalização", 70.0),
            "talento_ofensivo": stats_app.get("Talento ofensivo", stats_app.get("Talento Ofensivo", 70.0)),
            "chute_colocado":   stats_app.get("Chute Colocado", 70.0),
            "drible":           stats_app.get("Drible", 70.0),
            "velocidade":       stats_app.get("Velocidade", 70.0),
            "aceleracao":       stats_app.get("Aceleração", 70.0),
            "passe_rasteiro":   stats_app.get("Passe rasteiro", stats_app.get("Passe Rasteiro", 70.0)),
            "resistencia":      stats_app.get("Resistência", 70.0),
            "talento_defensivo": stats_app.get("Talento defensivo", stats_app.get("Talento Defensivo", 70.0)),
            "contato_fisico":   stats_app.get("Contato físico", stats_app.get("Contato Físico", 70.0)),
            "reflexo_gk":       stats_app.get("Reflexo GK", 70.0),
            "firmeza_gk":       stats_app.get("Firmeza GK", 70.0),
            "alcance_gk":       stats_app.get("Alcance GK", 70.0),
            
            # --- CAMPOS DE MEMÓRIA (JSONB) ---
            "habilidades":   atleta_dict.get("habilidades", []),
            "maestria":      atleta_dict.get("maestria", {}), # VITAL PARA O LABORATÓRIO!
            "personalidade": atleta_dict.get("personalidade", {}),
            "stats_fixos":   atleta_dict.get("stats_fixos", {}),
            "historico_ovr": atleta_dict.get("historico_ovr", [])
        }
        
        supabase.table("jogadores").insert(payload).execute()
        return True
    except Exception as e:
        st.error(f"❌ Erro Crítico no Registro: {e}")
        return False

def salvar_evolucao_treino(nome_id, atributos_novos):
    try:
        id_atleta = nome_id.upper().strip()
        supabase.table("jogadores").update(atributos_novos).eq("nome", id_atleta).execute()
        return True
    except Exception as e:
        st.error(f"❌ Erro na Evolução: {e}")
        return False
