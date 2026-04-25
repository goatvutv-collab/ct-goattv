import streamlit as st
import os
from supabase import create_client

# --- CONEXÃO BLINDADA ---
URL = os.environ.get("SUPABASE_URL") or (st.secrets.get("SUPABASE_URL") if "SUPABASE_URL" in st.secrets else None)
KEY = os.environ.get("SUPABASE_KEY") or (st.secrets.get("SUPABASE_KEY") if "SUPABASE_KEY" in st.secrets else None)

if not URL or not KEY:
    st.error("⚠️ Falha Crítica: Chaves de autenticação do CT não encontradas.")
    st.stop()

supabase = create_client(URL, KEY)

# --- NÚCLEO DE INTELIGÊNCIA ---

def registrar_novo_atleta(atleta_dict):
    """
    Mapeamento Complexo: Converte a estrutura de dicionário aninhado do App 
    para o esquema de colunas planas (flat) do SQL Supremo.
    """
    try:
        # 1. Extração e Limpeza de Dados Primários
        nome_id = atleta_dict.get("nome", "SEM_ID").upper().strip()
        
        # 2. Captura do Dicionário de Stats (Removendo para não duplicar no INSERT)
        # O App envia como "stats": {"Finalização": 75, ...}
        stats_origem = atleta_dict.pop("stats", {})

        # 3. MAPEAMENTO TOTAL (Stats PES -> Colunas SQL)
        # Aqui a gente faz o 'de-para' garantindo que o banco entenda os acentos do código
        mapa_stats = {
            # --- SETOR: ATAQUE ---
            "finalizacao":      stats_origem.get("Finalização", 70.0),
            "talento_ofensivo": stats_origem.get("Talento Ofensivo", 70.0),
            "chute_colocado":   stats_origem.get("Chute Colocado", 70.0),
            "drible":           stats_origem.get("Drible", 70.0),
            "velocidade":       stats_origem.get("Velocidade", 70.0),
            "aceleracao":       stats_origem.get("Aceleração", 70.0),
            
            # --- SETOR: MEIO-CAMPO ---
            "passe_rasteiro":   stats_origem.get("Passe Rasteiro", 70.0),
            "controle_bola":    stats_origem.get("Controle de Bola", 70.0),
            "resistencia":      stats_origem.get("Resistência", 70.0),
            
            # --- SETOR: DEFESA ---
            "talento_defensivo": stats_origem.get("Talento Defensivo", 70.0),
            "agressividade":    stats_origem.get("Agressividade", 70.0),
            "contato_fisico":   stats_origem.get("Contato Físico", 70.0),
            
            # --- SETOR: GOLEIRO (A Cura da Dor) ---
            "reflexo_gk":       stats_origem.get("Reflexo GK", 70.0),
            "firmeza_gk":       stats_origem.get("Firmeza GK", 70.0),
            "alcance_gk":       stats_origem.get("Alcance GK", 70.0)
        }

        # 4. Construção do Payload de Inserção Final
        # Unimos os dados básicos do atleta com os stats mapeados
        payload = {
            "nome": nome_id,
            "nome_completo": atleta_dict.get("nome_completo"),
            "nascimento":    atleta_dict.get("nascimento"),
            "idade":         atleta_dict.get("idade"),
            "altura":        atleta_dict.get("altura"),
            "peso":          atleta_dict.get("peso"),
            "posicao":       atleta_dict.get("posicao"),
            "status":        atleta_dict.get("status", "Saudável"),
            "foto":          atleta_dict.get("foto"),
            "dna":           atleta_dict.get("dna"),
            "dna_origem":    atleta_dict.get("dna_origem"),
            "overall":       atleta_dict.get("overall", 75.0),
            
            # Campos JSONB (Mantidos como objetos para flexibilidade)
            "habilidades":   atleta_dict.get("habilidades", []),
            "personalidade": atleta_dict.get("personalidade", {}),
            "stats_fixos":   atleta_dict.get("stats_fixos", {}),
            "historico_ovr": atleta_dict.get("historico_ovr", []),
            
            # Injeção dos Stats Mapeados
            **mapa_stats
        }

        # 5. Execução no Supabase
        res = supabase.table("jogadores").insert(payload).execute()
        
        if res.data:
            return True
        return False

    except Exception as e:
        st.error(f"❌ Erro de Sistema no Registro: {e}")
        return False

def buscar_atleta(nome_id):
    """Busca o perfil completo e reconstrói o dicionário para o padrão do App."""
    try:
        res = supabase.table("jogadores").select("*").eq("nome", nome_id.upper().strip()).execute()
        if res.data:
            atleta = res.data[0]
            # Aqui fazemos o inverso: pegamos as colunas e montamos o 'stats' para o radar
            atleta["stats"] = {
                "Finalização": atleta.pop("finalizacao"),
                "Talento Ofensivo": atleta.pop("talento_ofensivo"),
                "Velocidade": atleta.pop("velocidade"),
                "Resistência": atleta.pop("resistencia"),
                "Talento Defensivo": atleta.pop("talento_defensivo"),
                # ... o app lê esse dicionário para gerar o radar Plotly
            }
            return atleta
        return None
    except Exception as e:
        print(f"Erro ao recuperar: {e}")
        return None

def salvar_evolucao_treino(nome_id, atributos_novos):
    """Atualização dinâmica de colunas específicas (Regra 3x3)."""
    try:
        supabase.table("jogadores").update(atributos_novos).eq("nome", nome_id.upper().strip()).execute()
        return True
    except Exception as e:
        st.error(f"❌ Erro ao salvar evolução: {e}")
        return False
