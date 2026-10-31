"""probe241_start.py (measure): entries of the V2.37 jog start DBs + resume DB, per clip: length, root yaw change (deg) and root
displacement over the clip, curve names. Prints START241 {...}."""
import unreal as u, json, math
AL = u.AnimationLibrary
out = {}
for p in ('/Game/GraceRanger/SHME/Animations/V237/PSD_SHM237_JogStartS_L', '/Game/GraceRanger/SHME/Animations/V237/PSD_SHM237_JogStartS_R'):
    db = u.load_asset(p); rows = []
    for i in range(db.get_num_animation_assets()):
        a = db.get_animation_asset(i)
        try:
            ln = float(a.get_play_length())
            t0 = AL.get_bone_pose_for_time(a, 'root', 0.0, False); t1 = AL.get_bone_pose_for_time(a, 'root', ln, False)
            y0 = t0.rotation.rotator().yaw; y1 = t1.rotation.rotator().yaw; d = t1.translation - t0.translation
            curves = [str(c) for c in AL.get_animation_curve_names(a, u.RawCurveTrackTypes.RCT_FLOAT)][:12]
            rows.append([a.get_name(), round(ln, 2), round(((y1 - y0) + 180) % 360 - 180, 1), [round(d.x), round(d.y)], curves])
        except Exception as e: rows.append([a.get_name(), 'err ' + str(e)[:80]])
    out[p.split('/')[-1]] = rows
print('START241 ' + json.dumps(out))
