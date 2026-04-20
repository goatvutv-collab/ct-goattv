# --- database/db_handler.py ---
import json
import os

# Definições de caminhos (Centralizadas para facilitar manutenção)
DB_DIR = "fotos_atletas"
DB_FILE = os.path.join(DB_DIR, "jogadores_goat.json")

def garantir_infraestrutura():
    """
    Verifica se a pasta de banco de dados e fotos existe.
    Caso contrário, cria a estrutura necessária.
    """
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)
        print(f"✅ Infraestrutura '{DB_DIR}' criada com sucesso.")

def carregar_db():
    """
    Lê o banco de dados JSON.
    Retorna um dicionário vazio se o arquivo não existir ou estiver corrompido.
    """
    garantir_infraestrutura()
    
    if not os.path.exists(DB_FILE):
        return {}
        
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        # Proteção contra arquivos corrompidos: retorna vazio para não travar o App
        return {}

def salvar_db(dados):
    """
    Grava os dados dos atletas no JSON.
    Usa indent=4 para ser legível por humanos e ensure_ascii=False para aceitar acentos.
    """
    garantir_infraestrutura()
    
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
            return True
    except IOError as e:
        print(f"❌ Erro ao salvar banco de dados: {e}")
        return False

def buscar_atleta(id_atleta):
    """
    Função auxiliar para recuperar um perfil específico sem carregar o DB inteiro toda hora.
    """
    db = carregar_db()
    return db.get(id_atleta.upper().strip())
