"""gen253_settle.py (dry = measure job; write = manifest of the NEW assets only): V2.53 POST-BRAKE BALANCE SETTLE for the jog stop family.
Measured (settle253.py, V2.52 production, 60 FPS): in every SHM237_JogStop_* stop the pelvis is at rest on the frame the feet plant (pelvis
stop time +0.02 s, forward excursion after the plant 0.0, knee/hip loading 0.0-1.2 cm) and chest / head / shoulders stop with it - the body
arrives like a mechanism. A human stopping from a 3 m/s jog loads the hips and knees while braking (eccentric absorption), the trunk keeps
flexing forward after the hips are stopped, the head lags and re-levels, the arms swing on, and everything settles back over the feet with
one small, damped return.
New content (the source clips and database are not modified): /Game/GraceRanger/SHME/Animations/V253/SHM253_JogStop_<bin> = copy of each
production stop bin, extended to the settle end, with a physically driven settle layer:
  drive u(t) = -a_root(t) / A_REF (the clip's own braking deceleration in units of the jog stop's 410 cm/s2 -> light stops get a light
  response; the walk -> stop and jog -> stop amplitude follow the deceleration, not a constant), each segment = a damped 2nd-order system
  y'' = w^2 (u - y) - 2 z w y' with its own period / damping and a small delay along the chain (pelvis -> lower spine -> upper spine ->
  neck/head -> arms), so the segments do not stop on the same frame:
    knee/hip load   pelvis z  -= DIP * y_dip          (T_DIP, Z_DIP)       + a final-plant absorption bump PLANT_DIP
    pelvis travel   pelvis    += PEL_X * y_x * fwd    (T_X, Z_X; back while braking, small forward return after the stop)
    trunk flexion   spine_01..05 pitch forward TRUNK * y_t (T_T, Z_T; spine_04/05 delayed D_UP)
    head            neck_01 / head counter-pitch HEAD_K * trunk(t - D_HEAD) (gaze re-levels late)
    arms            upperarm forward ARM * y_a(t - D_ARM) (T_A, Z_A), lowerarm 0.35 of it
  feet exactly where the source has them (V2.10 hinge leg solver on both legs, knee hint = source knee + pelvis offset); root unchanged.
  Curves: SHM_StopSettle = 1 until the settle end (the V1.3.7 idle takeover snapshots the SETTLED stance), SHM237_FPPelvisOff = 1 until the
  settle end then fade 0.25 s (FootPlacement leaves the pelvis to the clip while it settles), other curves extended with their last value.
  Notifies: BranchIn SHME_V253_Settle (whole clip) into PSD_SHM253_JogStop (settings copied from PSD_SHM237_JogStop) and PoseSearch
  BlockTransition SHME_V253_Block [last plant + 0.05 s, end] (no hop into another bin's settle tail).
Balance check (no correction step is added when it is not needed): extrapolated centre of mass XCoM = pelvis + v / w0 (w0 = sqrt(g / l))
at the last plant must lie between the heels and the balls of the planted feet; the margin is printed per bin.
builtins.V253_SET = {'dry': bool, 'only': [...], 'dip': 2.6, 'trunk': 5.0, 'arm': 4.0, ...}. Prints SET253 {...}."""
import unreal as u, json, builtins, math, sys, importlib
sys.path.insert(0, r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925')
import v137_animedit as ae; importlib.reload(ae)
AL = u.AnimationLibrary; EAL = u.EditorAssetLibrary
cfg = dict(getattr(builtins, 'V253_SET', {})); DRY = bool(cfg.get('dry', True)); ONLY = cfg.get('only')
K = lambda k, d: float(cfg.get(k, d))
A_REF = K('a_ref', 410.0); SETTLE_T = K('settle_t', 1.0); TAIL = K('tail', 0.40); EXTEND = bool(cfg.get('extend', False)); FADE_W = K('fade_w', 0.30)
DIP = K('dip', 2.6); T_DIP = K('t_dip', 0.55); Z_DIP = K('z_dip', 0.62); PLANT_DIP = K('plant_dip', 0.8)
PEL_X = K('pel_x', -1.6); T_X = K('t_x', 1.0); Z_X = K('z_x', 0.45)
TRUNK = K('trunk', 5.0); T_T = K('t_t', 0.80); Z_T = K('z_t', 0.50); D_UP = K('d_up', 0.04)
HEAD_K = K('head_k', 0.55); D_HEAD = K('d_head', 0.08)
ARM = K('arm', 4.0); T_A = K('t_a', 0.85); Z_A = K('z_a', 0.32); D_ARM = K('d_arm', 0.08)
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
SRC_DB = cfg.get('src_db', '/Game/GraceRanger/SHME/Animations/V237/PSD_SHM237_JogStop'); V = '/Game/GraceRanger/SHME/Animations/V253/'
DST_DB = V + 'PSD_SHM253_JogStop'
out = {'dry': DRY, 'cfg': {k: cfg[k] for k in cfg if k != 'only'}, 'clips': {}}
def mj(x): x = min(1.0, max(0.0, x)); return x * x * x * (10 - 15 * x + 6 * x * x)
def bump(t, tc, rise, decay):
    if t < tc - rise: return 0.0
    if t < tc: return mj((t - (tc - rise)) / rise)
    return math.exp(-(t - tc) / decay)
def sim(uu, T, z, dt, sub=8):
    w = 2 * math.pi / T; y = 0.0; v = 0.0; h = dt / sub; o = []
    for x in uu:
        for _ in range(sub):
            acc = w * w * (x - y) - 2 * z * w * v; v += acc * h; y += v * h
        o.append(y)
    return o
def delayed(a, d, dt):
    o = []
    for f in range(len(a)):
        x = f - d / dt
        if x <= 0: o.append(a[0]); continue
        i = int(math.floor(x)); w = x - i; o.append(a[min(i, len(a) - 1)] * (1 - w) + a[min(i + 1, len(a) - 1)] * w)
    return o
src_db = u.load_asset(SRC_DB)
entries = [src_db.get_animation_asset(i) for i in range(src_db.get_num_animation_assets())]
out['src_db'] = {'n': len(entries)}
for k in ('schema', 'normalization_set', 'base_cost_bias', 'continuing_pose_cost_bias', 'looping_cost_bias', 'pose_search_mode'):
    try: out['src_db'][k] = str(src_db.get_editor_property(k))
    except Exception as e: out['src_db'][k] = 'err ' + str(e)[:60]
try:
    ents = src_db.get_editor_property('animation_assets')
    out['src_db']['entry0'] = {p: str(ents[0].get_editor_property(p)) for p in ('mirror_option', 'sampling_range', 'enabled') if hasattr(ents[0], 'get_editor_property')}
except Exception as e: out['src_db']['entry_err'] = str(e)[:120]
dst_db = None
if not DRY:
    if EAL.does_asset_exist(DST_DB): dst_db = u.load_asset(DST_DB)
    else:
        fac = u.DataAssetFactory(); fac.set_editor_property('data_asset_class', u.PoseSearchDatabase)
        dst_db = u.AssetToolsHelpers.get_asset_tools().create_asset(DST_DB.rsplit('/', 1)[1], DST_DB.rsplit('/', 1)[0], u.PoseSearchDatabase, fac); assert dst_db, DST_DB
    for k in ('schema', 'normalization_set', 'base_cost_bias', 'continuing_pose_cost_bias', 'looping_cost_bias', 'exclude_from_database_parameters', 'pose_search_mode', 'kdtree_max_leaf_size', 'kdtree_query_num_neighbors'):
        try: dst_db.set_editor_property(k, src_db.get_editor_property(k))
        except Exception: pass
    assert EAL.save_asset(DST_DB, False); dst_db = u.load_asset(DST_DB)
for seq0 in entries:
    n = seq0.get_name()
    if ONLY and n not in ONLY: continue
    sp = seq0.get_path_name().split('.')[0]
    NAMES = [str(x) for x in AL.get_animation_track_names(seq0)]
    clip = ae.Clip(seq0, NAMES); nf0 = clip.nf; L0 = float(seq0.get_play_length()); dt = L0 / max(1, nf0 - 1)
    src = {b: list(v) for b, v in clip.local.items()}
    R = [clip.comp('root', f, src)[0] for f in range(nf0)]
    D_ = ae.vsub(R[-1], R[0]); FWD = ae.vnorm((D_[0], D_[1], 0.0)); LEFT = ae.vnorm(ae.vcross(FWD, (0.0, 0.0, 1.0)))
    fw = lambda p: p[0] * FWD[0] + p[1] * FWD[1]
    # floors and contact: ball within 1.5 cm of its final height and still (< 0.3 cm / frame) on both feet = planted
    bz = {s: clip.comp('ball_' + s, nf0 - 1, src)[0][2] for s in 'lr'}
    def planted(f, s):
        b = clip.comp('ball_' + s, f, src)[0]; b0 = clip.comp('ball_' + s, max(0, f - 1), src)[0]
        return b[2] < bz[s] + 1.5 and math.hypot(b[0] - b0[0], b[1] - b0[1]) < 0.3
    lastp = next((f for f in range(nf0) if all(planted(g, s) for g in range(f, nf0) for s in 'lr')), nf0 - 1)
    Tp = lastp * dt
    vr = [fw(ae.vsub(R[min(f + 1, nf0 - 1)], R[max(f - 1, 0)])) / (dt * (min(f + 1, nf0 - 1) - max(f - 1, 0))) for f in range(nf0)]
    ar = [(vr[min(f + 1, nf0 - 1)] - vr[max(f - 1, 0)]) / (dt * max(1, min(f + 1, nf0 - 1) - max(f - 1, 0))) for f in range(nf0)]
    Ts = next((f * dt for f in range(nf0) if vr[f] < 2.0 and f > 2), Tp)
    # extend to the settle end
    if EXTEND:
        t_end_settle = max(Tp, Ts) + SETTLE_T; Ln = max(L0, t_end_settle + TAIL); nf = int(math.ceil(Ln / dt - 1e-6)) + 1; Ln = (nf - 1) * dt
    else:
        # v2: no extension (the extended static tails changed the new database's own feature normalisation -> 3 bin hops at the entry,
        # and the V1.3.7 idle takeover snapshots the lower body when the clip's SHM_StopSettle drops): the settle lives inside the
        # source length and reaches exactly zero when the source SHM_StopSettle falls below 0.5
        try:
            tt_, vv_ = AL.get_float_keys(seq0, 'SHM_StopSettle'); t_end_settle = next((tt_[i] for i in range(len(tt_)) if vv_[i] < 0.5), L0 - 0.3)
        except Exception: t_end_settle = Tp + 0.1
        t_end_settle = min(t_end_settle, L0 - 0.3); Ln = L0; nf = nf0
    local = {b: list(v) + [v[-1]] * (nf - nf0) for b, v in src.items()}
    srcx = {b: list(v) for b, v in local.items()}
    uu = [max(0.0, min(1.5, -(ar[f] if f < nf0 else 0.0) / A_REF)) for f in range(nf)]
    uu = [sum(uu[max(0, f - 1):f + 2]) / len(uu[max(0, f - 1):f + 2]) for f in range(nf)]
    y_dip = sim(uu, T_DIP, Z_DIP, dt); y_x = sim(uu, T_X, Z_X, dt); y_t = sim(uu, T_T, Z_T, dt); y_a = sim(uu, T_A, Z_A, dt)
    fade_end = [1.0 - mj((f * dt - (t_end_settle - FADE_W)) / FADE_W) for f in range(nf)]      # exact zero at the settle end
    dip = [(DIP * y_dip[f] + PLANT_DIP * bump(f * dt, Tp, 0.08, 0.22)) * fade_end[f] for f in range(nf)]
    px = [PEL_X * y_x[f] * fade_end[f] for f in range(nf)]
    th = [TRUNK * y_t[f] * fade_end[f] for f in range(nf)]; th_up = delayed(th, D_UP, dt); th_head = delayed(th, D_HEAD, dt)
    arm = [ARM * v_ * fade_end[f] for f, v_ in enumerate(delayed(y_a, D_ARM, dt))]
    feet = {s: [clip.comp('foot_' + s, f, srcx) for f in range(nf)] for s in 'lr'}
    knees = {s: [clip.comp('calf_' + s, f, srcx)[0] for f in range(nf)] for s in 'lr'}
    for f in range(nf):
        off = (FWD[0] * px[f], FWD[1] * px[f], -dip[f])
        par = clip.parent['pelvis']; Qp = clip.comp(par, f, local)[1] if par else (0.0, 0.0, 0.0, 1.0)
        lt, lq, ls = local['pelvis'][f]; local['pelvis'][f] = (ae.vadd(lt, ae.qrot(ae.qinv(Qp), off)), lq, ls)
        for b, k_, src_ in (('spine_01', 0.15, th), ('spine_02', 0.20, th), ('spine_03', 0.25, th), ('spine_04', 0.20, th_up), ('spine_05', 0.20, th_up)):
            if b in local and abs(src_[f]) > 1e-4: ae.apply_bone_delta(clip, local, b, f, ae.qaxis(LEFT, -k_ * src_[f]))
        for b, k_ in (('neck_01', 0.65 * HEAD_K), ('head', 0.35 * HEAD_K)):
            if b in local and abs(th_head[f]) > 1e-4: ae.apply_bone_delta(clip, local, b, f, ae.qaxis(LEFT, k_ * th_head[f]))
        for s in 'lr':
            if abs(arm[f]) > 1e-4:
                ae.apply_bone_delta(clip, local, 'upperarm_' + s, f, ae.qaxis(LEFT, arm[f]))
                if 'lowerarm_' + s in local: ae.apply_bone_delta(clip, local, 'lowerarm_' + s, f, ae.qaxis(LEFT, 0.35 * arm[f]))
            ft, fq = feet[s][f]; ae.solve_leg(clip, local, s, f, ft, fq, ae.vadd(knees[s][f], off))
    for s in 'lr':
        b = 'ik_foot_' + s
        if b in local and 'ik_foot_root' in local:
            for f in range(nf):
                fp, fq = clip.comp('foot_' + s, f, local); pp, pq = clip.comp('ik_foot_root', f, local)
                local[b][f] = (ae.qrot(ae.qinv(pq), ae.vsub(fp, pp)), ae.qnorm(ae.qmul(ae.qinv(pq), fq)), local[b][f][2])
    # checks
    ferr = max(ae.vlen(ae.vsub(clip.comp('foot_' + s, f, local)[0], feet[s][f][0])) for s in 'lr' for f in range(nf))
    pel = [clip.comp('pelvis', f, local)[0] for f in range(nf)]; pel0 = [clip.comp('pelvis', f, srcx)[0] for f in range(nf)]
    w0 = math.sqrt(980.0 / max(50.0, pel0[lastp][2] - bz['l']))
    vp = fw(ae.vsub(pel[min(lastp + 1, nf - 1)], pel[max(lastp - 1, 0)])) / (2 * dt)
    xcom = fw(pel[lastp]) + vp / w0
    heel = max(fw(clip.comp('foot_' + s, lastp, local)[0]) for s in 'lr') - 3.0; toe = max(fw(clip.comp('ball_' + s, lastp, local)[0]) for s in 'lr') + 4.0
    heelmin = min(fw(clip.comp('foot_' + s, lastp, local)[0]) for s in 'lr') - 3.0
    hd = [fw(clip.comp('head', f, local)[0]) - fw(clip.comp('head', f, srcx)[0]) for f in range(nf)]
    rec = {'src': sp, 'len0': round(L0, 3), 'len': round(Ln, 3), 'frames': nf, 'dt': round(dt, 4), 't_stop': round(Ts, 3), 't_last_plant': round(Tp, 3), 'settle_end': round(t_end_settle, 3),
           'u_max': round(max(uu), 2), 'dip_max': round(max(dip), 2), 'dip_at': round(dip.index(max(dip)) * dt, 2), 'pel_x_min': round(min(px), 2), 'pel_x_max': round(max(px), 2),
           'trunk_max': round(max(th), 2), 'trunk_at': round(th.index(max(th)) * dt, 2), 'trunk_min_after': round(min(th[th.index(max(th)):]), 2), 'arm_max': round(max(arm), 2), 'arm_min': round(min(arm), 2),
           'head_fwd_max': round(max(hd), 2), 'head_fwd_min': round(min(hd), 2), 'foot_err_cm': round(ferr, 3),
           'xcom_margin_cm': [round(xcom - heelmin, 1), round(toe - xcom, 1)], 'xcom_inside': heelmin <= xcom <= toe}
    try:
        g = ae.leg_metrics(seq0, local); rec['guard'] = {s_: [round(g[s_]['hinge_min'], 3), g[s_]['backward_frames'], g[s_]['twisted_frames'], round(g[s_]['axis_jump_deg'], 1)] for s_ in g}
    except Exception as e: rec['guard_err'] = str(e)[:120]
    cn = [str(x) for x in AL.get_animation_curve_names(seq0, u.RawCurveTrackTypes.RCT_FLOAT)]
    curves = {}
    for c in cn:
        try:
            tt, vv = AL.get_float_keys(seq0, c); curves[c] = (list(tt), list(vv))
        except Exception as e: rec.setdefault('curve_err', []).append(c + ': ' + str(e)[:60])
    rec['curves'] = sorted(curves)
    rec['notify_tracks'] = [str(t) for t in AL.get_animation_notify_track_names(seq0)]
    if not DRY:
        dp = V + 'SHM253_' + n.split('SHM237_')[-1]
        ae.leg_guard(seq0, local, label=dp)
        if not EAL.does_asset_exist(dp): assert EAL.duplicate_asset(sp, dp), dp
        seq = u.load_asset(dp); c = ae.controller(seq)
        for tr in [str(t) for t in AL.get_animation_notify_track_names(seq)]:
            if tr == 'SHME_V237_JogStop': AL.remove_animation_notify_events_by_track(seq, tr); AL.remove_animation_notify_track(seq, tr)
        try: c.open_bracket(u.Text('SHME V2.53 post-brake settle ' + n), True)
        except Exception: c.open_bracket('SHME V2.53 settle', True)
        try:
            c.set_number_of_frames(u.FrameNumber(nf - 1), True)
            for b in NAMES:
                ks = local[b]
                if not c.set_bone_track_keys(b, [u.Vector(*k[0]) for k in ks], [u.Quat(*k[1]) for k in ks], [u.Vector(*k[2]) for k in ks], True): raise RuntimeError('keys ' + b)
        finally: c.close_bracket(True)
        ts = [f * dt for f in range(nf)]
        def at(tt, vv, t):
            if not tt: return 0.0
            if t <= tt[0]: return vv[0]
            for i in range(1, len(tt)):
                if t <= tt[i]: w = (t - tt[i - 1]) / max(1e-6, tt[i] - tt[i - 1]); return vv[i - 1] * (1 - w) + vv[i] * w
            return vv[-1]
        for cname in [str(x) for x in AL.get_animation_curve_names(seq, u.RawCurveTrackTypes.RCT_FLOAT)]: AL.remove_curve(seq, cname, False)
        for cname, (tt, vv) in curves.items():
            if EXTEND and cname == 'SHM_StopSettle': vals = [1.0 if t <= t_end_settle else max(0.0, 1.0 - (t - t_end_settle) / 0.1) for t in ts]
            elif EXTEND and cname == 'SHM237_FPPelvisOff': vals = [max(at(tt, vv, t), 1.0 - mj((t - t_end_settle) / 0.25)) for t in ts]
            else: vals = [at(tt, vv, t) for t in ts]
            AL.add_curve(seq, cname, u.RawCurveTrackTypes.RCT_FLOAT, False); AL.add_float_curve_keys(seq, cname, ts, vals)
        for tr in [str(t) for t in AL.get_animation_notify_track_names(seq)]:
            if tr.startswith('SHME_V253'): AL.remove_animation_notify_events_by_track(seq, tr); AL.remove_animation_notify_track(seq, tr)
        AL.add_animation_notify_track(seq, 'SHME_V253_Settle')
        ev = AL.add_animation_notify_state_event(seq, 'SHME_V253_Settle', 0.0, Ln - 0.001, u.AnimNotifyState_PoseSearchBranchIn); ev.set_editor_property('database', dst_db)
        AL.add_animation_notify_track(seq, 'SHME_V253_Block')
        AL.add_animation_notify_state_event(seq, 'SHME_V253_Block', Tp + 0.05, max(0.05, Ln - Tp - 0.05 - 0.001), u.AnimNotifyState_PoseSearchBlockTransition)
        try: seq.set_editor_property('loop', False)
        except Exception: pass
        assert EAL.save_loaded_asset(seq, False), dp; rec['dst'] = dp
    out['clips'][n] = rec
if not DRY:
    assert EAL.save_asset(DST_DB, False); db = u.load_asset(DST_DB)
    out['dst_db'] = [db.get_animation_asset(i).get_name() for i in range(db.get_num_animation_assets())]
out['dirty'] = [q.get_name().split('/')[-1] for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('SET253 ' + json.dumps(out, default=str))
