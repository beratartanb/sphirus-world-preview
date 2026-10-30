import builtins, json, glob, re
VP9 = '/Game/GraceRanger/SHME/Animations/V239/'
J = {}
for f in sorted(glob.glob(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Saved/Codex/SHME_V239_20261030/gen239_tk_write_part*.json')): J.update({n: c for n, c in json.load(open(f))['clips'].items() if c.get('saved')})
groups = {}
for n, c in J.items():
    m = re.match(r'SHM239_Tk_([RL])_P(\d\d)_K(\d+)_(Back|Opp)$', n); sd, p, k, tg = m.group(1), int(m.group(2)), int(m.group(3)), m.group(4)
    e = 2 * ((0 if sd == 'R' else 24) + p) + (1 if tg == 'Opp' else 0)
    groups.setdefault(e, []).append((n, c['contacts'][k - 1]['t'], c['tK'] + 0.05))
for e in range(96):
    g = groups.get(e, [])
    builtins.V240_EDB = {'dry': False, 'name': 'PSD_SHM240_E%02d' % e, 'bias': -25.0, 'clips': [VP9 + n for n, _, _ in g],
                         'wstart': {VP9 + n: a for n, a, _ in g}, 'wins': {VP9 + n: b for n, _, b in g}}
    exec(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V240_20261030/build240_edb.py', encoding='utf8').read())
