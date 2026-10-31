"""bake241_syaw.py (editor job, write manifest = the turning start copies) - V2.41 start heading contract content: the only start clips
whose root TURNS (V2.37 start databases: SHM_JogQ_af_Loco_Jog_Start_TurnL045_Lfoot_AAMS -45 deg, ..._TurnR045_Rfoot_AAMS +45 deg) get
  SHM241_SYaw = root yaw (deg) relative to frame 0, unwrapped, per frame;  SHM241_SW = 1 over the clip.
Poses / existing curves untouched (curves are not schema features). builtins.V241_SY = {'clips': [...]}. Prints SY241 {...}."""
import unreal as u, json, builtins
AL = u.AnimationLibrary; EAL = u.EditorAssetLibrary
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
c = dict(getattr(builtins, 'V241_SY', {})); out = {'clips': []}
for p in c['clips']:
    a = u.load_asset(p); ln = float(a.get_play_length()); n = int(round(ln * 30.0)) + 1
    ts = [min(ln, i / 30.0) for i in range(n)]; ys = []; prev = None; acc = 0.0; y0 = None
    for t in ts:
        y = AL.get_bone_pose_for_time(a, 'root', t, False).rotation.rotator().yaw
        if prev is not None: acc += ((y - prev) + 180.0) % 360.0 - 180.0
        prev = y; ys.append(acc)
    for nm, vals in (('SHM241_SYaw', ys), ('SHM241_SW', [1.0] * len(ts))):
        if AL.does_curve_exist(a, nm, u.RawCurveTrackTypes.RCT_FLOAT): AL.remove_curve(a, nm, False)
        AL.add_curve(a, nm, u.RawCurveTrackTypes.RCT_FLOAT, False); AL.add_float_curve_keys(a, nm, ts, vals)
    assert EAL.save_asset(p, False)
    out['clips'].append([p.split('/')[-1], round(ln, 2), [round(ys[i], 1) for i in range(0, len(ys), 6)]])
out['dirty'] = [q.get_name() for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('SY241 ' + json.dumps(out))
