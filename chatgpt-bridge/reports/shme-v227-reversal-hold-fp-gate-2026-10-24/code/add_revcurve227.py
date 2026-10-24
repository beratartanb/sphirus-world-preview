"""add_revcurve227.py (editor job): marker / clock curve on the authored V2.26 reversal clips. Writes the float curve SHM226_Rev = REMAINING clip
seconds (keys t=0 -> T, t=T -> 0; linear) into every SHM226_JogRev_* clip. Consumers (ABP_GR_MotionMatchingBase, install_v227_revhold.py):
value > 0 = an authored reversal clip is in the pose (blends to 0 with the clip weight, the loops carry no such curve), value = time to the clip
end (the DB hold releases SHM227_HoldExit s before it). Candidate assets only (the clips are not in production). builtins.V227_CURVE_DRY prints
only; otherwise saves each clip. Prints REVCURVE227 {...}."""
import unreal as u, json, builtins
AL = u.AnimationLibrary; EAL = u.EditorAssetLibrary; DRY = bool(getattr(builtins, 'V227_CURVE_DRY', False))
V = '/Game/GraceRanger/SHME/Animations/V226/'; NAME = 'SHM226_Rev'
CLIPS = [V + 'SHM226_JogRev_%s_P%d' % (f, k) for f in ('B_F', 'F_B') for k in range(32)]
out = {'dry': DRY, 'n': 0, 'saved': 0, 'lens': {}, 'err': {}}
for path in CLIPS:
    seq = u.load_asset(path); nm = path.rsplit('/', 1)[-1]
    if not seq: out['err'][nm] = 'missing'; continue
    T = float(seq.get_play_length()); out['lens'][nm] = round(T, 3)
    if DRY: continue
    try:
        if AL.does_curve_exist(seq, NAME, u.RawCurveTrackTypes.RCT_FLOAT): AL.remove_curve(seq, NAME, False)
        AL.add_curve(seq, NAME, u.RawCurveTrackTypes.RCT_FLOAT); AL.add_float_curve_keys(seq, NAME, [0.0, T], [T, 0.0])
        out['n'] += 1
        if EAL.save_asset(path, False): out['saved'] += 1
    except Exception as e: out['err'][nm] = str(e)[:160]
if not DRY and CLIPS:
    s0 = u.load_asset(CLIPS[0]); out['curves_P0'] = [str(c) for c in AL.get_animation_curve_names(s0, u.RawCurveTrackTypes.RCT_FLOAT)]
    try: out['value_P0_mid'] = round(float(AL.evaluate_float_curve(s0, NAME, 0.5 * out['lens'][CLIPS[0].rsplit('/', 1)[-1]])), 3) if hasattr(AL, 'evaluate_float_curve') else 'n/a'
    except Exception as e: out['value_P0_mid'] = str(e)[:80]
out['dirty'] = [q.get_name() for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('REVCURVE227 ' + json.dumps(out, default=str))
