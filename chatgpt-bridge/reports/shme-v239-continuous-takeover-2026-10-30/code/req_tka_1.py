import builtins, json
S = json.load(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Saved/Codex/SHME_V239_20261030/tk_all_specs.json'))
builtins.G239TK = {'dry_run': False, 'clips': S[1::4]}
exec(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V239_20261030/gen239_tk.py', encoding='utf8').read())
