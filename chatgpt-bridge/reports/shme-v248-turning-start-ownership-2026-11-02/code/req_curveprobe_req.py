import unreal as u, json
AL = u.AnimationLibrary; out = {}
for s in ('L090_Lfoot', 'L135_Lfoot', 'L180_Lfoot', 'R090_Rfoot', 'R135_Rfoot', 'R180_Rfoot', 'L045_Lfoot'):
    a = u.load_asset('/Game/GraceRanger/SHME/Animations/Starts/Jog/SHM_JogQ_af_Loco_Jog_Start_Turn%s_AAMS' % s)
    out[s] = [str(c) for c in AL.get_animation_curve_names(a, u.RawCurveTrackTypes.RCT_FLOAT)]
print('CURVEPROBE248 ' + json.dumps(out))
