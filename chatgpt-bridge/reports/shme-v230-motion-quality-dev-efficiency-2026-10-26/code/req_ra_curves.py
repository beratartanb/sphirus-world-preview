import builtins
C = '/Game/GraceRanger/SHME/Animations/Curves/A_SHM_Sprint_Curve_'
SP = {'pelvis': 0.6, 'chest': 0.5, 'head': 0.45, 'arm': 0.75}
builtins.RA230 = {'mode': 'inplace', 'clips': [dict(path=C + n, stride=1.0, **SP) for n in ('L12', 'R12', 'L25', 'R25', 'L40', 'R40')]}
exec(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V230_20261026/reauthor230.py', encoding='utf8').read())
