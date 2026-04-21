# --- database/db_handler.py ---
import json
import os

DB_DIR = "fotos_atletas"
DB_FILE = os.path.join(DB_DIR, "jogadores_goat.json")

def garantir_infraestrutura():
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)

def carregar_db():
    garantir_infraestrutura()
    if not os.path.exists(DB_FILE): return {}
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except: return {}

def salvar_db(dados):
    garantir_infraestrutura()
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
            return True
    except: return False

def gerenciar_foto_antiga(caminho_antigo):
    """Deleta a foto anterior para economizar espaço no sistema."""
    if caminho_antigo and os.path.exists(caminho_antigo) and "default.png" not in caminho_antigo:
        try:
            os.remove(caminho_antigo)
        except:
            pass
