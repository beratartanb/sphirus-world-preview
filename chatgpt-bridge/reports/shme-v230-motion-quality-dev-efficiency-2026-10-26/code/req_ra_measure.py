import builtins
G = '/Game/GraceRanger/'
UB = {'pelvis': 0.6, 'chest': 0.5, 'head': 0.45, 'arm': 0.75}
builtins.RA230 = {'mode': 'measure', 'clips': [
  dict(path=G + 'Animations/LocomotionBehavior/A_LB_Sprint_Fwd', stride=0.82, **UB),
  dict(path=G + 'SHME/Animations/V217/SHM217_J2S_Lfoot_b', stride=1.0, **UB),
  dict(path=G + 'SHME/Animations/V218/SHM218_W2S_Lfoot_a', stride=1.0, **UB),
  dict(path=G + 'Animations/Continuity/DirectionalSteady/A_CT_Walk_Rear', stride=0.74, pelvis=0.8, chest=0.8, head=0.7, arm=0.85),
  dict(path=G + 'Animations/Continuity/A_CT_Jog_Right', stride=0.82, pelvis=0.8, chest=0.7, head=0.6, arm=0.85),
  dict(path=G + 'SHME/Animations/Curves/A_SHM_Sprint_Curve_R12', stride=0.64, **UB)]}
exec(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V230_20261026/reauthor230.py', encoding='utf8').read())
