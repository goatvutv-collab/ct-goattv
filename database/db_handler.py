import streamlit as st
import os  # Essencial para ler as chaves no Render
from supabase import create_client

# --- CONEXÃO BLINDADA (RENDER + SUPABASE) ---
# O código tenta primeiro o ambiente do Render, depois o segredo local do Streamlit
URL = os.environ.get("SUPABASE_URL") or (st.secrets.get("SUPABASE_URL") if "SUPABASE_URL" in st.secrets else None)
KEY = os.environ.get("SUPABASE_KEY") or (st.secrets.get("SUPABASE_KEY") if "SUPABASE_KEY" in st.secrets else None)

# Travão de Segurança: Se as chaves sumirem, o app avisa antes de dar erro vermelho
if not URL or not KEY:
    st.error("⚠️ Erro de Conexão: As chaves SUPABASE_URL ou SUPABASE_KEY não foram encontradas. Verifique o painel Environment no Render.")
    st.stop()

# Inicializa o cliente oficial do Supabase
supabase = create_client(URL, KEY)

# --- FUNÇÕES DE MEMÓRIA (BANCO DE DADOS) ---

def carregar_todos_jogadores():
    """
    Busca a lista completa de atletas no banco para o sistema de login/scout.
    """
    try:
        res = supabase.table("jogadores").select("*").execute()
        # Retorna um dicionário {nome_id: dados} para manter a lógica do App
        return {j['nome']: j for j in res.data}
    except Exception as e:
        st.error(f"⚠️ Erro ao carregar banco: {e}")
        return {}

def buscar_atleta(nome_id):
    """
    Busca um perfil específico (ex: LUCAS_01) sem sobrecarregar o sistema.
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
    A função mestre da evolução. Grava os novos stats permanentemente.
    Ex: salvar_evolucao_treino("LUCAS_01", {"finalizacao": 82.5})
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
    Cria a 'certidão de nascimento' do jogador no banco de dados.
    """
    try:
        supabase.table("jogadores").insert(dados_atleta).execute()
        return True
    except Exception as e:
        st.error(f"❌ Erro ao registrar atleta: {e}")
        return False
