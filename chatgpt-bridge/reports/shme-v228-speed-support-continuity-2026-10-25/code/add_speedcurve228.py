"""add_speedcurve228.py (editor job): designed capsule speed curve on the authored V2.26 reversal clips. The clips carry the designed
capsule path as their root track (root y = D(ct) in the clip frame, +y = character forward; ABP root motion mode = montages only, so the
capsule never consumed it). Writes two float curves into every SHM226_JogRev_* clip:
  SHM226_V  = d/dt root y (cm/s, signed along the character forward axis; central difference at the 30 Hz root keys; linear keys)
  SHM226_W  = 1.0 constant (blend-weight witness: a curve blends with the clip weight, so V / W = the clip's own value during blends)
Consumers: ABP_GR_MotionMatchingBase (install_v228_clipspeed.py) -> component ClipSpeed / ClipSpeedOn -> BP_GR_Player velocity.
Candidate assets only. builtins.V228_CURVE_DRY prints only; otherwise saves each clip. Prints SPEEDCURVE228 {...}."""
import unreal as u, json, builtins
AL = u.AnimationLibrary; EAL = u.EditorAssetLibrary; DRY = bool(getattr(builtins, 'V228_CURVE_DRY', False))
V = '/Game/GraceRanger/SHME/Animations/V226/'
CLIPS = [V + 'SHM226_JogRev_%s_P%d' % (f, k) for f in ('B_F', 'F_B') for k in range(32)]
out = {'dry': DRY, 'n': 0, 'saved': 0, 'err': {}, 'sample': {}}
DT = 1.0 / 30.0
for path in CLIPS:
    seq = u.load_asset(path); nm = path.rsplit('/', 1)[-1]
    if not seq: out['err'][nm] = 'missing'; continue
    T = float(seq.get_play_length()); n = int(round(T / DT))
    ys = []
    for k in range(n + 1):
        t = min(T, k * DT); ys.append(float(AL.get_bone_pose_for_time(seq, 'root', t, False).translation.y))
    vs = []
    for k in range(n + 1):
        if k == 0: vs.append((ys[1] - ys[0]) / DT)
        elif k == n: vs.append((ys[n] - ys[n - 1]) / DT)
        else: vs.append((ys[k + 1] - ys[k - 1]) / (2 * DT))
    ts = [min(T, k * DT) for k in range(n + 1)]
    if nm.endswith('_P0') or nm.endswith('_P4'): out['sample'][nm] = {'len': round(T, 3), 'v0..5': [round(v) for v in vs[:6]], 'v_mid': round(vs[n // 2]), 'v_end': round(vs[-1])}
    if DRY: continue
    try:
        for name, keys in (('SHM226_V', vs), ('SHM226_W', [1.0] * len(ts))):
            if AL.does_curve_exist(seq, name, u.RawCurveTrackTypes.RCT_FLOAT): AL.remove_curve(seq, name, False)
            AL.add_curve(seq, name, u.RawCurveTrackTypes.RCT_FLOAT); AL.add_float_curve_keys(seq, name, ts, keys)
        out['n'] += 1
        if EAL.save_asset(path, False): out['saved'] += 1
    except Exception as e: out['err'][nm] = str(e)[:160]
if not DRY:
    s0 = u.load_asset(CLIPS[0]); out['curves_P0'] = [str(c) for c in AL.get_animation_curve_names(s0, u.RawCurveTrackTypes.RCT_FLOAT)]
out['dirty'] = [q.get_name() for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('SPEEDCURVE228 ' + json.dumps(out, default=str))
