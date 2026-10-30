import builtins
VP9 = '/Game/GraceRanger/SHME/Animations/V239/'
for nm, tg in (('PSD_SHM239_TkP_Back', 'Back'), ('PSD_SHM239_TkP_Opp', 'Opp')):
    builtins.V239_TDB = {'dry': False, 'name': nm, 'bias': -25.0, 'clips': [VP9 + 'SHM239_Tk_%s_K%d_%s' % (s, k, tg) for s in ('R_P21', 'R_P10') for k in (1, 2, 3, 4)]}
    exec(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V239_20261030/build239_tkdb.py', encoding='utf8').read())
