"""add251_exitcurve.py (dry = measure job, write = manifest of the 6 crops): V2.51 crop EXIT marker. Measured (all v250/v251 runs, 129 crop
exits): Motion Matching leaves every SHM248 turn crop exactly 0.30 s before its end (1.000 -> 0.70, 1.133 -> 0.83, 0.933 -> 0.63): the last
0.30 s of a crop is not a candidate, while the turn itself ends 0.25 s before the end. With the T2 database still held, the search then hops
through the OTHER crops for single frames (R135 @0.83, R090 @0.63) before a run start -> shoulder 77-79 m/s2 at 60 FPS.
Curve SHM251_Exit = 0 until len - SHM251_TAIL (0.32 s), 1 after (step), on the 6 crops; install251_exitdone.py releases the V2.49 owner
on it so the hand-over is ONE transition. builtins.V251_EX = {'dry': bool, 'tail': 0.32}. Prints EXITCURVE251 {...}."""
import unreal as u, json, builtins
AL = u.AnimationLibrary; EAL = u.EditorAssetLibrary
cfg = dict(getattr(builtins, 'V251_EX', {})); DRY = bool(cfg.get('dry', True)); TAIL = float(cfg.get('tail', 0.32))
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
V = '/Game/GraceRanger/SHME/Animations/V248/'; DT = 1.0 / 30.0; NAME = 'SHM251_Exit'
out = {'dry': DRY, 'tail': TAIL, 'clips': {}, 'saved': 0}
for s in 'LR':
    for d in ('090', '135', '180'):
        p = V + 'SHM248_Jog_Start_Turn%s%s_crop' % (s, d); seq = u.load_asset(p); T = float(seq.get_play_length()); te = max(0.0, T - TAIL)
        ts = [0.0, max(0.0, te - DT), te, T]; ks = [0.0, 0.0, 1.0, 1.0]
        before = [str(x) for x in AL.get_animation_curve_names(seq, u.RawCurveTrackTypes.RCT_FLOAT)]
        rec = {'len': round(T, 3), 'exit_at': round(te, 3), 'curves_before': len(before)}
        if not DRY:
            if AL.does_curve_exist(seq, NAME, u.RawCurveTrackTypes.RCT_FLOAT): AL.remove_curve(seq, NAME, False)
            AL.add_curve(seq, NAME, u.RawCurveTrackTypes.RCT_FLOAT); AL.add_float_curve_keys(seq, NAME, ts, ks)
            after = [str(x) for x in AL.get_animation_curve_names(seq, u.RawCurveTrackTypes.RCT_FLOAT)]
            rec['curves_after'] = len(after); rec['renamed'] = sorted(set(after) - set(before) - {NAME})
            assert EAL.save_asset(p, False), p; out['saved'] += 1
        out['clips'][p.split('/')[-1]] = rec
out['dirty'] = [q.get_name().split('/')[-1] for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('EXITCURVE251 ' + json.dumps(out, default=str))
