import streamlit as st
from supabase import create_client

# --- CONFIGURAÇÃO DE CONEXÃO ---
# O Streamlit busca esses valores no Render (Environment Variables) 
# ou no seu arquivo local .streamlit/secrets.toml
URL = st.secrets["SUPABASE_URL"]
KEY = st.secrets["SUPABASE_KEY"]

# Inicializa o cliente oficial do Supabase
supabase = create_client(URL, KEY)

def carregar_todos_jogadores():
    """
    Equivalente ao antigo carregar_db(). 
    Busca a lista completa de atletas no banco.
    """
    try:
        res = supabase.table("jogadores").select("*").execute()
        # Transforma a lista de jogadores em um dicionário para manter compatibilidade
        return {j['nome']: j for j in res.data}
    except Exception as e:
        st.error(f"⚠️ Erro ao carregar banco: {e}")
        return {}

def buscar_atleta(nome_id):
    """
    Busca um perfil específico (ex: LUCAS_01) sem carregar tudo.
    """
    try:
        nome_limpo = nome_id.upper().strip()
        res = supabase.table("jogadores").select("*").eq("nome", nome_limpo).execute()
        return res.data[0] if res.data else None
    except Exception as e:
        print(f"Erro ao buscar atleta: {e}")
        return None

def salvar_evolucao_treino(nome_id, atributos_novos):
    """
    A função principal para a 'Memória'.
    Recebe o nome do jogador e um dicionário com os stats que mudaram.
    Ex: salvar_evolucao_treino("LUCAS_01", {"finalizacao": 82, "resistencia": 68})
    """
    try:
        nome_limpo = nome_id.upper().strip()
        supabase.table("jogadores").update(atributos_novos).eq("nome", nome_limpo).execute()
        return True
    except Exception as e:
        st.error(f"❌ Erro ao salvar evolução no Supabase: {e}")
        return False

def registrar_novo_atleta(dados_atleta):
    """
    Cria um novo registro no banco de dados.
    """
    try:
        supabase.table("jogadores").insert(dados_atleta).execute()
        return True
    except Exception as e:
        st.error(f"❌ Erro ao registrar atleta: {e}")
        return False

# Nota sobre Fotos: 
# Como estamos usando Supabase, as fotos no futuro devem ser URLs 
# guardadas na coluna 'foto_url' da tabela, em vez de arquivos locais.
