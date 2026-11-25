# probe_stopclip.py (read-only): foot (ball) and root trajectories of stop clips in animation space, plus movedata_speed, every 0.05 s
import unreal as u
X = u.AnimPoseExtensions; opt = u.AnimPoseEvaluationOptions(); opt.set_editor_property('extract_root_motion', False)
C = ['/Game/Characters/UEFN_Mannequin/Animations/Relaxed/Stops/M_Relaxed_Walk_Stop_F_Rfoot', '/Game/Characters/UEFN_Mannequin/Animations/Relaxed/Stops/M_Relaxed_Run_Stop_F_Lfoot']
AR = u.AssetRegistryHelpers.get_asset_registry()
f = u.ARFilter(class_paths=[u.TopLevelAssetPath('/Script/Engine', 'AnimSequence')], package_paths=['/Game/Characters/UEFN_Mannequin'], recursive_paths=True)
want = ('M_Relaxed_Walk_Stop_F_Rfoot', 'M_Relaxed_Run_Stop_F_Lfoot', 'M_Relaxed_Run_Stop_B_Rfoot')
for ad in AR.get_assets(f):
    n = str(ad.asset_name)
    if n not in want: continue
    s = u.load_asset(str(ad.package_name)); d = s.get_play_length(); print('P4STOP ==', ad.package_name, 'len %.2f' % d)
    k = 0.0
    while k <= d + 1e-4:
        p = X.get_anim_pose_at_time(s, min(k, d), opt)
        r = X.get_bone_pose(p, 'root', u.AnimPoseSpaces.WORLD).translation
        bl = X.get_bone_pose(p, 'ball_l', u.AnimPoseSpaces.WORLD).translation; br = X.get_bone_pose(p, 'ball_r', u.AnimPoseSpaces.WORLD).translation
        try: ms = X.get_curve_weight(p, 'movedata_speed')
        except Exception: ms = -1
        print('P4STOP %.2f root %6.1f %6.1f | L %6.1f %6.1f z%4.1f | R %6.1f %6.1f z%4.1f | ms %5.0f' % (k, r.x, r.y, bl.x, bl.y, bl.z, br.x, br.y, br.z, ms))
        k += 0.1
