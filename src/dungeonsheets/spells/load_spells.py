import dungeonsheets.spells

def load_spell_file(code: str):
    exec(code, dungeonsheets.spells.__dict__, {})