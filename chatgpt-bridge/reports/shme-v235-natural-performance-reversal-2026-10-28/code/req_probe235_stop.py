import unreal as u, json
AL = u.AnimationLibrary; R = u.AssetRegistryHelpers.get_asset_registry()
out = {}
ad = R.get_assets_by_package_name('/Game/GraceRanger/SHME/Animations/Stops/SHM_A_CP2_Jog_Fwd_Stop') if False else None
f = u.ARFilter(class_paths=[u.TopLevelAssetPath('/Script/Engine', 'AnimSequence')], package_paths=['/Game'], recursive_paths=True)
hits = [a for a in R.get_assets(f) if 'CP2_Jog_Fwd_Stop' in str(a.asset_name)]
out['hits'] = [str(a.package_name) for a in hits]
for a in hits[:3]:
    seq = u.load_asset(str(a.package_name)); T = float(seq.get_play_length())
    curves = [str(c) for c in AL.get_animation_curve_names(seq, u.RawCurveTrackTypes.RCT_FLOAT)]
    root = [round(float(AL.get_bone_pose_for_time(seq, 'root', min(T, k / 15.0), False).translation.y), 1) for k in range(int(T * 15) + 1)]
    cv = {}
    for c in curves:
        if 'istance' in c or 'Speed' in c or 'SHM' in c:
            try: cv[c] = [round(float(x), 1) for x in [AL.get_float_value_at_time(seq, c, min(T, k / 15.0)) if hasattr(AL, 'get_float_value_at_time') else 0 for k in range(0, int(T * 15) + 1, 2)]]
            except Exception as e: cv[c] = str(e)[:60]
    refs = [str(x) for x in R.get_referencers(a.package_name, u.AssetRegistryDependencyOptions())] if hasattr(R, 'get_referencers') else []
    out[str(a.asset_name)] = {'len': round(T, 3), 'rootmotion': bool(seq.get_editor_property('enable_root_motion')), 'curves': curves, 'root_y_15hz': root, 'cv': cv, 'refs': refs}
print('PSTOP ' + json.dumps(out, default=str))
