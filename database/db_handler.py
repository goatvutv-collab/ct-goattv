import json
import os

DB_DIR = "fotos_atletas"
DB_FILE = os.path.join(DB_DIR, "jogadores_goat.json")

def carregar_db():
    if not os.path.exists(DB_FILE): return {}
    try:
        with open(DB_FILE, "r") as f: return json.load(f)
    except: return {}

def salvar_db(dados):
    if not os.path.exists(DB_DIR): os.makedirs(DB_DIR)
    with open(DB_FILE, "w") as f:
        json.dump(dados, f, indent=4)
