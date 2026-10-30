import builtins
S = [('R_P21', 1.3125, 'R')]
SRC = [{'name': 'SRC_R_P21', 'tau0': 1.3125, 'side': 'R'}]
builtins.G239TK = {'dry_run': False, 'clips': [{'name': 'SHM239_Tk_%s_K%d_%s' % (n, k, tn), 'tau0': t0, 'side': sd, 'tk': {'k': k, 'tgt': tg}}
                   for n, t0, sd in S for k in (1, 2, 3) for tn, tg in (('Back', 0.0), ('Opp', -90.0))]}
exec(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V239_20261030/gen239_tk.py', encoding='utf8').read())
