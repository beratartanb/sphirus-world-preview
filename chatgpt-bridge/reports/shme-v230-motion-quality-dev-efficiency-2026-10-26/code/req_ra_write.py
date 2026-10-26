import builtins
G = '/Game/GraceRanger/'
SP = {'pelvis': 0.6, 'chest': 0.5, 'head': 0.45, 'arm': 0.75}      # sprint / push upper body
WK = {'pelvis': 0.8, 'chest': 0.8, 'head': 0.7, 'arm': 0.85}       # walk / jog lateral
C = G + 'SHME/Animations/Curves/A_SHM_Sprint_Curve_'
clips = [dict(path=G + 'Animations/LocomotionBehavior/A_LB_Sprint_Fwd', stride=0.82, **SP)]
clips += [dict(path=C + n, stride=k, **SP) for n, k in (('L12', 0.62), ('R12', 0.64), ('L25', 0.53), ('R25', 0.57), ('L40', 0.55), ('R40', 0.55))]
clips += [dict(path=G + 'SHME/Animations/V217/SHM217_J2S_' + n, stride=k, **SP) for n, k in (('Lfoot_a', 0.92), ('Lfoot_b', 0.92), ('Rfoot_a', 1.0), ('Rfoot_b', 0.92))]
clips += [dict(path=G + 'SHME/Animations/V218/SHM218_W2S_' + n, stride=1.0, **SP) for n in ('Lfoot_a', 'Lfoot_b', 'Rfoot_a', 'Rfoot_b')]
clips += [dict(path=G + 'Animations/Continuity/DirectionalSteady/A_CT_Walk_' + n, stride=k, **WK) for n, k in (('Rear', 0.74), ('RearRight', 0.72), ('RearLeft', 0.72))]
clips += [dict(path=G + 'Animations/Continuity/A_CT_Jog_' + n, stride=k, **WK) for n, k in (('Right', 0.82), ('Left', 1.0))]
builtins.RA230 = {'mode': getattr(builtins, 'RA230_MODE', 'inplace'), 'clips': clips}
if hasattr(builtins, 'RA230_MODE'): del builtins.RA230_MODE   # one-shot (builtins persist across runner jobs)
exec(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V230_20261026/reauthor230.py', encoding='utf8').read())
