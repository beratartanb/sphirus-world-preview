"""add_footspeed226.py (editor job): the animation DATA the runtime reads from a reversal clip - FootPlacement reads the float curves
footspeed_l / footspeed_r (plant detection) and Disable_FootLock (datacontract226: the only curve consumers in ABP_GR_MotionMatchingBase);
the production loops / pivots carry them, the authored SHM226 clips carried none (gen225/226 strip every curve). Writes footspeed_l/r =
the ball's world-equivalent speed (cm/s: root-relative ball + root translation, per frame) into every SHM226_JogRev clip, computed from the
clip's own tracks (the real plant / swing timing of the new motion, not copied from the loop). Disable_FootLock is not written (absent = 0 =
lock allowed, same as the loops' 0). builtins.V226_FS_DRY prints only. Prints FOOTSPEED226 {...}."""
import unreal as u, json, math, sys, pathlib, importlib, builtins
P = pathlib.Path(u.Paths.project_dir()); sys.path.insert(0, str(P / 'Tools/SHME_V1_20260925'))
import v137_animedit as ae; importlib.reload(ae)
AL = u.AnimationLibrary; DRY = bool(getattr(builtins, 'V226_FS_DRY', False))
NPH = int(getattr(builtins, 'V226_NPH', 32)); V = '/Game/GraceRanger/SHME/Animations/V226/'
CLIPS = [V + 'SHM226_JogRev_%s_P%d' % (f, k) for f in ('B_F', 'F_B') for k in range(NPH)]
def lerp(a, b, t): return tuple(a[i] + (b[i] - a[i]) * t for i in range(len(a)))
out = {'dry': DRY, 'clips': {}}
for path in CLIPS:
    seq = u.load_asset(path)
    if not seq: out['clips'][path.rsplit('/', 1)[-1]] = 'missing'; continue
    names = sorted(str(n) for n in AL.get_animation_track_names(seq)); NK = ae.num_frames(seq) - 1; T = float(seq.get_play_length())
    Lk = ae.read_local(seq, names, list(range(NK + 1)))
    clip = ae.Clip(seq, ['root', 'pelvis', 'foot_l', 'foot_r', 'ball_l', 'ball_r', 'calf_l', 'calf_r', 'thigh_l', 'thigh_r'])
    world = {s: [] for s in ('l', 'r')}
    for k in range(NK + 1):
        loc = {b: Lk[b][k] for b in names}; tmp = {b: [loc[b]] for b in loc}; tmp['root'] = [((0.0, 0.0, 0.0), loc['root'][1], loc['root'][2])]
        for s in ('l', 'r'):
            c = clip.comp('ball_' + s, 0, tmp)[0]; world[s].append(ae.vadd(c, loc['root'][0]))
    dt = T / NK; speeds = {}; SWING_MIN = float(getattr(builtins, 'V226_FS_SWINGMIN', 150.0))
    for s in ('l', 'r'):
        w = world[s]; sp = []
        bz = [clip.comp('ball_' + s, 0, {b: [Lk[b][k]] for b in names})[0][2] for k in range(NK + 1)]; floor = min(bz) + 1.5
        for k in range(NK + 1):
            a = w[max(k - 1, 0)]; b = w[min(k + 1, NK)]; n = (min(k + 1, NK) - max(k - 1, 0)) * dt
            v = math.hypot(b[0] - a[0], b[1] - a[1], b[2] - a[2]) / max(n, 1e-6)
            # v2: the plant-speed curve encodes the DESIGNED plant timing: a foot above its floor (swing, incl. the soft Hermite approach)
            # reads at least SWING_MIN so FootPlacement does not lock it 10-15 cm before the authored plant; on the floor = kinematic (0 when pinned)
            sp.append(v if bz[k] <= floor else max(v, SWING_MIN))
        speeds[s] = sp
    rec = {'frames': NK + 1, 'min_l': round(min(speeds['l']), 1), 'min_r': round(min(speeds['r']), 1), 'max_l': round(max(speeds['l']), 1), 'max_r': round(max(speeds['r']), 1)}
    if not DRY:
        for s in ('l', 'r'):
            cn = 'footspeed_' + s
            try:
                if AL.does_curve_exist(seq, cn, u.RawCurveTrackTypes.RCT_FLOAT): AL.remove_curve(seq, cn, False)
                AL.add_curve(seq, cn, u.RawCurveTrackTypes.RCT_FLOAT)
                AL.add_float_curve_keys(seq, cn, [k * dt for k in range(NK + 1)], speeds[s])
            except Exception as e: rec['err_' + s] = str(e)[:120]
        if getattr(builtins, 'V226_FS_NOLOCK', False):   # v3: Disable_FootLock = 1 over the authored clip (FootPlacement's own per-clip lock switch, read by the node)
            try:
                if AL.does_curve_exist(seq, 'Disable_FootLock', u.RawCurveTrackTypes.RCT_FLOAT): AL.remove_curve(seq, 'Disable_FootLock', False)
                AL.add_curve(seq, 'Disable_FootLock', u.RawCurveTrackTypes.RCT_FLOAT); AL.add_float_curve_keys(seq, 'Disable_FootLock', [0.0, T], [1.0, 1.0]); rec['nolock'] = True
            except Exception as e: rec['err_nolock'] = str(e)[:120]
        rec['saved'] = bool(u.EditorAssetLibrary.save_asset(path, False))
        rec['curves_after'] = [str(c) for c in AL.get_animation_curve_names(seq, u.RawCurveTrackTypes.RCT_FLOAT)]
    out['clips'][path.rsplit('/', 1)[-1]] = rec
out['dirty'] = [q.get_name() for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('FOOTSPEED226 ' + json.dumps(out, default=str))
