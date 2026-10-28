"""gen235_stop.py (editor job): V2.35 stop re-plan of a project stop clip IN PLACE (root track, length, curves and the distance timeline are
kept, so the CP stop distance matching and the SHM_StopSettle curve behave as before).
Diagnosis (probe235_stopbody on SHM_A_CP2_Jog_Fwd_Stop, the jog forward stop every j35 / j30 chain ends in): the brake step lands 55-63 cm
ahead of the final root, the closing step leaves a 41 cm staggered stance, and 0.3 s AFTER the stop the lead foot is pulled 43 cm BACK to
square the stance (the 'frozen long stance, then a correction step' the user sees); the arms drop from jog carriage to hanging in 0.2 s.
Plan (data-driven per foot from the clip's own contacts):
  * FINAL landing of each foot = its first landing once the root is slower than SLOW (cm/s); that landing is re-targeted to the foot's
    FINAL idle position (no later step: the post-stop correction step is removed, the foot stays planted there); the swing into it keeps its
    own shape plus an offset that fades in with a minimum-jerk curve (no lunge, no slide), swing apex capped at APEX cm above the floor.
  * legs re-solved (v137_animedit.solve_leg) with the clip's own knee hint; pelvis / root untouched.
  * upper body (spine, neck, head, clavicles, arms): zero-phase Gaussian smoothing (SIGMA s) of the local rotations inside the stop window
    [W0, W1] s -> the jog carriage decays into the idle hang over ~0.4 s instead of 0.2 s, same start and end poses.
builtins.G235S = {'dry_run': True, 'clips': [...], 'slow': 120.0, 'apex': 9.0, 'sigma': 0.07, 'w0': 0.85, 'w1': 1.9}. Prints G235S {...}
(per clip: per foot final landing frame, re-target distance, removed steps, apex before / after, planted drift, foot error)."""
import unreal as u, json, math, builtins, pathlib, importlib, sys
P = pathlib.Path(u.Paths.project_dir()).resolve(); sys.path.insert(0, str(P / 'Tools/SHME_V1_20260925'))
import v137_animedit as ae; importlib.reload(ae)
AL = u.AnimationLibrary; EAL = u.EditorAssetLibrary
cfg = dict(getattr(builtins, 'G235S', {})); DRY = bool(cfg.get('dry_run', True))
CLIPS = cfg.get('clips', ['/Game/GraceRanger/SHME/Animations/Stops/SHM_A_CP2_Jog_Fwd_Stop'])
SLOW = float(cfg.get('slow', 120.0)); APEX = float(cfg.get('apex', 15.0)); SIGMA = float(cfg.get('sigma', 0.07)); W0 = float(cfg.get('w0', 0.85)); W1 = float(cfg.get('w1', 1.9))
FPS = 30.0
def mj(x): x = min(1.0, max(0.0, x)); return x * x * x * (10 - 15 * x + 6 * x * x)
def slerp(a, b, t):
    d = sum(a[i] * b[i] for i in range(4))
    if d < 0: b = tuple(-x for x in b); d = -d
    if d > 0.9995: return ae.qnorm(tuple(a[i] + (b[i] - a[i]) * t for i in range(4)))
    th = math.acos(min(d, 1.0)); s = math.sin(th)
    return tuple((math.sin((1 - t) * th) * a[i] + math.sin(t * th) * b[i]) / s for i in range(4))
def qavg(qs, ws):
    ref = qs[0]; acc = [0.0, 0.0, 0.0, 0.0]
    for q, w in zip(qs, ws):
        if sum(q[i] * ref[i] for i in range(4)) < 0: q = tuple(-x for x in q)
        for i in range(4): acc[i] += w * q[i]
    return ae.qnorm(tuple(acc))
def build(path):
    seq = u.load_asset(path); names = [str(n) for n in AL.get_animation_track_names(seq)]
    N = ae.num_frames(seq); L = ae.read_local(seq, names, list(range(N)))
    clip = ae.Clip(seq, ['root', 'pelvis', 'foot_l', 'foot_r', 'ball_l', 'ball_r', 'calf_l', 'calf_r'])
    orig = {s: [clip.comp('foot_' + s, f, L) for f in range(N)] for s in 'lr'}
    ball = {s: [clip.comp('ball_' + s, f, L)[0] for f in range(N)] for s in 'lr'}
    knee = {s: [clip.comp('calf_' + s, f, L)[0] for f in range(N)] for s in 'lr'}
    ry = [L['root'][f][0][1] for f in range(N)]
    vr = [abs(ry[min(N - 1, f + 1)] - ry[max(0, f - 1)]) * FPS / (min(N - 1, f + 1) - max(0, f - 1)) for f in range(N)]
    bz0 = {s: min(b[2] for b in ball[s]) for s in 'lr'}
    # contact threshold per foot: the idle stance carries the ball higher than the jog stance (flat foot), so the final pose sets it too
    zc = {s: max(bz0[s] + 1.5, ball[s][N - 1][2] + 1.0) for s in 'lr'}
    planted = {s: [ball[s][f][2] < zc[s] for f in range(N)] for s in 'lr'}
    info = {'frames': N, 'feet': {}}
    tgt = {s: [orig[s][f] for f in range(N)] for s in 'lr'}
    BL = {}
    for s in 'lr':
        lands = [f for f in range(1, N) if planted[s][f] and not planted[s][f - 1]]
        fin = next((f for f in lands if vr[f] < SLOW), None)
        if fin is None: info['feet'][s] = 'no slow landing'; continue
        lift = max([f for f in range(1, fin) if planted[s][f - 1] and not planted[s][f]] or [max(0, fin - 10)])
        endF = orig[s][N - 1]; d = ae.vsub(endF[0], orig[s][fin][0]); d = (d[0], d[1], 0.0)
        later = [f for f in lands if f > fin]; apex0 = max(ball[s][f][2] for f in range(lift, fin + 1)) - bz0[s]
        sc = min(1.0, APEX / apex0) if apex0 > 1e-3 else 1.0
        # r3: the horizontal re-target must be COMPLETE before the foot gets low (FootPlacement plants a low foot; a foot still moving
        # back under the plant was locked, then released = the 10.6 cm r2 stop slip). f_low = first frame after the apex below zc + 4 cm.
        fap = max(range(lift, fin + 1), key=lambda f: ball[s][f][2]); f_low = next((f for f in range(fap, fin + 1) if ball[s][f][2] < zc[s] + 0.5 * (ball[s][fap][2] - zc[s])), fin)
        dl = ae.vsub(endF[0], orig[s][f_low][0]); dl = (dl[0], dl[1], 0.0)
        ballE = ball[s][N - 1]; BL[s] = L['ball_' + s][N - 1][0]   # final ball (component) and the ball's local offset in the foot frame
        # r4: halfway down (zc + 4 cm still let FootPlacement plant the closing foot 4.6 cm short -> the next start read a staggered
        # stance and chose the turning start TurnL04, j34_chain1 92 cm); the last half of every final swing is vertical
        for f in range(lift, N):
            p, q = orig[s][f]
            if f < fin:
                x = (f - lift) / max(1, fin - lift); off = ae.vsc(dl, mj((f - lift) / max(1, f_low - lift)))   # r5: offset to the final spot measured AT f_low (r3/r4 used the landing frame -> 45-55 cm jump at f_low, 60 FPS pop)
                zf = 1.0 - (1.0 - sc) * mj((x - 0.35) / 0.4)   # cap only the forward half of the swing (the knee-high 'march'); the heel kick behind stays
                z = orig[s][lift][0][2] + (p[2] - orig[s][lift][0][2]) * zf if p[2] > orig[s][lift][0][2] else p[2]
                if f < f_low: tgt[s][f] = ((p[0] + off[0], p[1] + off[1], z), q)
                else:   # r5: from f_low the foot comes straight down in 4 frames (the vendor landing hovered ~0.3 s at 5 cm = a hanging foot)
                    # r6: the BALL is planned (FootPlacement plants the ball): it sits on its final spot and the foot pivots around it
                    # (r5 planned the ankle; with the toes still up the ball touched 5 cm short and was locked there)
                    if f == f_low: zb0 = ball[s][f][2] + (z - p[2])
                    w = mj((f - f_low) / 4.0); qq = slerp(q, orig[s][fin][1], w)
                    bt = (ballE[0], ballE[1], zb0 * (1 - w) + ballE[2] * w)
                    tgt[s][f] = (ae.vsub(bt, ae.qrot(qq, BL[s])), qq)
            else:
                qq = slerp(orig[s][fin][1], endF[1], mj((f - fin) / 6.0)); tgt[s][f] = (ae.vsub(ballE, ae.qrot(qq, BL[s])), qq)
        info['feet'][s] = {'lift': lift, 'final_land': fin, 'retarget_cm': round(math.hypot(d[0], d[1]), 1), 'removed_landings': later,
                           'f_low': f_low, 'apex_before': round(apex0, 1), 'apex_after': round(apex0 * sc, 1), 'root_v_at_land': round(vr[fin], 1)}
    # trunk (spine / neck / head, NOT the arms: their swing stays phase-locked to the legs): slower uprighting after the stop entry.
    # The vendor stop straightens the jog lean in 0.15 s right where MM enters (ct 0.43-0.6) = the visible 'pop upright'; the trunk clock
    # tau = T0 + D * (0.5 x + 0.5 x^2) runs at half speed at T0 and catches up by T0 + D (same start, same end pose).
    TR = [b for b in names if b.startswith(('spine_', 'neck_', 'head'))]; T0 = float(cfg.get('trunk_t0', 0.45)); TD = float(cfg.get('trunk_d', 1.15))
    if cfg.get('trunk_slow', True):
        src_tr = {b: list(L[b]) for b in TR}   # read the ORIGINAL keys (tau <= t, so in-place reads would see remapped frames)
        for b in TR:
            for f in range(N):
                t = f / FPS
                if t <= T0 or t >= T0 + TD: continue
                x = (t - T0) / TD; tau = (T0 + TD * (0.5 * x + 0.5 * x * x)) * FPS; i = min(N - 2, int(tau)); w = tau - i
                L[b][f] = (L[b][f][0], slerp(src_tr[b][i][1], src_tr[b][i + 1][1], w), L[b][f][2])
    # upper body: zero-phase Gaussian smoothing of local rotations inside [W0, W1]
    UB = [b for b in names if b.startswith(('spine_', 'neck_', 'head', 'clavicle_', 'upperarm_', 'lowerarm_', 'hand_'))]
    rad = int(math.ceil(3 * SIGMA * FPS)); new = {b: list(L[b]) for b in names}
    for b in UB:
        for f in range(N):
            t = f / FPS
            if t < W0 or t > W1: continue
            ks = range(max(0, f - rad), min(N - 1, f + rad) + 1); ws = [math.exp(-0.5 * ((k - f) / (SIGMA * FPS)) ** 2) for k in ks]
            q = qavg([L[b][k][1] for k in ks], ws)
            e = min(1.0, (t - W0) / 0.15, (W1 - t) / 0.15)   # fade the filter in / out at the window edges
            new[b][f] = (L[b][f][0], slerp(L[b][f][1], q, e), L[b][f][2])
    for f in range(N):
        for s in 'lr':
            ae.solve_leg(clip, new, s, f, tgt[s][f][0], tgt[s][f][1], knee[s][f])
    for s in 'lr':
        b = 'ik_foot_' + s
        if b in names and 'ik_foot_root' in names:
            for f in range(N):
                fp, fq = clip.comp('foot_' + s, f, new); pp, pq = clip.comp('ik_foot_root', f, new)
                new[b][f] = (ae.qrot(ae.qinv(pq), ae.vsub(fp, pp)), ae.qnorm(ae.qmul(ae.qinv(pq), fq)), new[b][f][2])
    err = 0.0; drift = 0.0
    for s in 'lr':
        for f in range(N):
            err = max(err, ae.vlen(ae.vsub(clip.comp('foot_' + s, f, new)[0], tgt[s][f][0])))
            if f and clip.comp('ball_' + s, f, new)[0][2] < bz0[s] + 1.0 and clip.comp('ball_' + s, f - 1, new)[0][2] < bz0[s] + 1.0:
                a_, b_ = clip.comp('ball_' + s, f - 1, new)[0], clip.comp('ball_' + s, f, new)[0]; dd = math.hypot(b_[0] - a_[0], b_[1] - a_[1]); drift += dd if dd > 0.05 else 0.0
    info.update(foot_err=round(err, 2), planted_drift=round(drift, 2),
                final_feet_rel_root={s: [round(clip.comp('ball_' + s, N - 1, new)[0][i] - L['root'][N - 1][0][i], 1) for i in range(2)] for s in 'lr'})
    return seq, names, new, info
out = {'dry': DRY, 'cfg': cfg, 'clips': {}}
for path in CLIPS:
    try:
        seq, names, new, info = build(path)
        if not DRY:
            ae.write_tracks(seq, new, sorted(names), note='SHME V2.35 stop re-plan (final landings, no correction step, smoothed upper body)')
            info['saved'] = bool(EAL.save_loaded_asset(seq, False))
    except Exception:
        import traceback; info = {'err': traceback.format_exc()[-900:]}
    out['clips'][path.rsplit('/', 1)[-1]] = info
out['dirty'] = [q.get_name() for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('G235S ' + json.dumps(out, default=str))
