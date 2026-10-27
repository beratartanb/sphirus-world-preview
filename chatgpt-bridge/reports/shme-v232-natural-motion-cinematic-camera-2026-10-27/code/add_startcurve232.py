"""add_startcurve232.py (editor job) - V2.32 C: designed capsule speed on the OWNED backward start clip(s): the clip root stays still for
0.2 s (weight shift) and then accelerates backward (-35 / -98 / -154 cm/s) while the CMC moved the capsule from the first frame -> both
planted feet slid 35-38 cm (j30_slow, j30_rel_3200). Writes SHM226_V (root +y velocity, central difference at 30 Hz), SHM226_W = 1 and the
start witness SHM232_SW = 1 (the ABP start-bind term, install_v232_startbind.py). builtins.SC232 = {'dry': True, 'clips': [...]}."""
import unreal as u, json, builtins
AL = u.AnimationLibrary; EAL = u.EditorAssetLibrary
cfg = getattr(builtins, 'SC232', {}); DRY = bool(cfg.get('dry', True))
CLIPS = cfg.get('clips', ['/Game/GraceRanger/SHME/Animations/Starts/Jog/SHM_JogQ_af_Loco_Jog_Bwd_Start_AAMS'])
out = {'dry': DRY, 'clips': {}, 'saved': 0}; DT = 1.0 / 30.0
for path in CLIPS:
    seq = u.load_asset(path); nm = path.rsplit('/', 1)[-1]
    if not seq: out['clips'][nm] = 'missing'; continue
    T = float(seq.get_play_length()); n = int(round(T / DT))
    ys = [float(AL.get_bone_pose_for_time(seq, 'root', min(T, k * DT), False).translation.y) for k in range(n + 1)]
    vs = [((ys[1] - ys[0]) if k == 0 else (ys[n] - ys[n - 1]) if k == n else (ys[k + 1] - ys[k - 1]) / 2.0) / DT for k in range(n + 1)]
    ts = [min(T, k * DT) for k in range(n + 1)]
    out['clips'][nm] = {'len': round(T, 3), 'v': [round(v) for v in vs[::3]], 'curves_before': [str(c) for c in AL.get_animation_curve_names(seq, u.RawCurveTrackTypes.RCT_FLOAT)][:10]}
    if DRY: continue
    for name, keys in (('SHM226_V', vs), ('SHM226_W', [1.0] * len(ts)), ('SHM232_SW', [1.0] * len(ts))):
        if AL.does_curve_exist(seq, name, u.RawCurveTrackTypes.RCT_FLOAT): AL.remove_curve(seq, name, False)
        AL.add_curve(seq, name, u.RawCurveTrackTypes.RCT_FLOAT); AL.add_float_curve_keys(seq, name, ts, keys)
    if EAL.save_asset(path, False): out['saved'] += 1
out['dirty'] = [q.get_name() for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('SC232 ' + json.dumps(out, default=str))
