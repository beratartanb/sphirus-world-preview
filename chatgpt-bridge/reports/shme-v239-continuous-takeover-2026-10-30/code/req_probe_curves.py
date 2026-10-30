import unreal as u
AL = u.AnimationLibrary
for n in ('SHM238_Cut_R_P00', 'SHM238_Cut_R_P21', 'SHM238_Cut_L_P10'):
    s = u.load_asset('/Game/GraceRanger/SHME/Animations/V238/' + n)
    cn = [str(c) for c in AL.get_animation_curve_names(s, u.RawCurveTrackTypes.RCT_FLOAT)]
    print('CURVES', n, len(cn), sorted(cn)[:20])
