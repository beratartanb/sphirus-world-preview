import builtins
# V2.31: the six curved sprint loops re-baked from the V2.30 re-authored A_LB_Sprint_Fwd (stride 0.82, plays at ~1.0) at RATE 1.0
# (V1.3.9 baked them from the long-stride loop for an MM play rate of 0.813 and set rate_scale 0.813 -> they still played at 0.82)
builtins.V139_CURVES = {'src': '/Game/GraceRanger/Animations/LocomotionBehavior/A_LB_Sprint_Fwd', 'dst_dir': '/Game/GraceRanger/SHME/Animations/Curves', 'rate': 1.0,
  'curves': [['A_SHM_Sprint_Curve_R12', 12.0], ['A_SHM_Sprint_Curve_L12', -12.0], ['A_SHM_Sprint_Curve_R25', 25.0], ['A_SHM_Sprint_Curve_L25', -25.0], ['A_SHM_Sprint_Curve_R40', 40.0], ['A_SHM_Sprint_Curve_L40', -40.0]],
  'db': '/Game/GraceRanger/Animations/LocomotionBehavior/PSD_LB_SprintLoops', 'dry_run': False}
exec(open(r"C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/v139_curve_bake.py", encoding="utf8").read())
