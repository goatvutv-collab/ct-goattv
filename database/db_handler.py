import json
import os

# Caminho absoluto para evitar erros no deploy
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, "fotos_atletas")
DB_FILE = os.path.join(DB_DIR, "jogadores_goat.json")

def carregar_db():
    if not os.path.exists(DB_FILE): return {}
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f: return json.load(f)
    except: return {}

def salvar_db(dados):
    if not os.path.exists(DB_DIR): os.makedirs(DB_DIR)
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)
