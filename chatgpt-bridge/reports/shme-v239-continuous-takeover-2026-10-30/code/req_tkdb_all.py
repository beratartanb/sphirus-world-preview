import builtins, json, glob
VP9 = '/Game/GraceRanger/SHME/Animations/V239/'
J = {}
for f in sorted(glob.glob(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Saved/Codex/SHME_V239_20261030/gen239_tk_write_part*.json')): J.update({n: c for n, c in json.load(open(f))['clips'].items() if c.get('saved')})   # leg-guard rejections stay out
for tg in ('Back', 'Opp'):
    cl = sorted(VP9 + n for n in J if n.endswith('_' + tg))
    builtins.V239_TDB = {'dry': False, 'name': 'PSD_SHM239_Tk_' + tg, 'bias': -25.0, 'clips': cl, 'wins': {VP9 + n: J[n]['tK'] + 0.05 for n in J if n.endswith('_' + tg)}}
    exec(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V239_20261030/build239_tkdb.py', encoding='utf8').read())
    builtins.V239_TDB = {'dry': False, 'name': 'PSD_SHM239_TkP_' + tg, 'bias': -25.0, 'clips': cl}
    exec(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V239_20261030/build239_tkdb.py', encoding='utf8').read())
