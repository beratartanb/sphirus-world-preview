import builtins
VP9 = '/Game/GraceRanger/SHME/Animations/V239/'
for nm, tg in (('PSD_SHM239_Tk_Back', 'Back'), ('PSD_SHM239_Tk_Opp', 'Opp')):
    builtins.V239_TDB = {'dry': False, 'name': nm, 'bias': -25.0, 'clips': [VP9 + 'SHM239_Tk_R_P21_K%d_%s' % (k, tg) for k in (1, 2, 3)]}
    exec(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V239_20261030/build239_tkdb.py', encoding='utf8').read())
