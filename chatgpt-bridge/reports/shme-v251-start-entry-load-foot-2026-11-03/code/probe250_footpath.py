"""probe250_footpath.py (measure job, read-only): authored world path of the feet (component space WITH the animated root bone) for the
turning-start crops and their correct-retarget sources, frames 0..14: ball / ankle position and height. Prints FOOTPATH250 {...}."""
import unreal as u, json, math
ar = u.AssetRegistryHelpers.get_asset_registry(); A = {}
for a in ar.get_assets_by_class(u.TopLevelAssetPath('/Script/Engine', 'AnimSequence'), True): A.setdefault(str(a.package_name), 1)
P = ['/Game/GraceRanger/SHME/Animations/V248/SHM248_Jog_Start_TurnL135_crop', '/Game/CoreMotion_Retargeted/AAMS/Walk/af_Loco_Jog_Start_TurnL135_Lfoot',
     '/Game/GraceRanger/SHME/Animations/V248/SHM248_Jog_Start_TurnR180_crop', '/Game/CoreMotion_Retargeted/AAMS/Walk/af_Loco_Jog_Start_TurnR180_Rfoot']
out = {}
for p in P:
    seq = u.load_asset(p); o = u.AnimPoseEvaluationOptions(); o.set_editor_property('evaluation_type', u.AnimDataEvalType.RAW)
    try: o.set_editor_property('extract_root_motion', False)
    except Exception: pass
    rows = []
    for f in range(0, 15):
        t = f / 30.0; po = u.AnimPoseExtensions.get_anim_pose_at_time(seq, t, o); r = [f]
        for b in ('root', 'ball_l', 'foot_l', 'ball_r', 'foot_r'):
            v = u.AnimPoseExtensions.get_bone_pose(po, b, u.AnimPoseSpaces.WORLD).translation; r.append([round(v.x, 1), round(v.y, 1), round(v.z, 1)])
        rows.append(r)
    out[p.split('/')[-1]] = rows
print('FOOTPATH250 ' + json.dumps(out))
