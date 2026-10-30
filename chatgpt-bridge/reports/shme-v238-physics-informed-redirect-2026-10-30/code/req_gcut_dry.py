import builtins
builtins.G238CUT = {'dry_run': True, 'clips': [{'name': 'SHM238_Cut_R_P%02d' % k, 'tau0': k * 1.5 / 24, 'side': 'R'} for k in (1, 8, 10, 14, 19, 9)] + [{'name': 'SHM238_Cut_L_P02', 'tau0': 0.125, 'side': 'L'}]}
exec(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V238_20261030/gen238_cut.py', encoding='utf8').read())
