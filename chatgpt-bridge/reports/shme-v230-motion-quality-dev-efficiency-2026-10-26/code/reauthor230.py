"""reauthor230.py (editor job) - V2.30 character re-authoring of a locomotion clip: natural cadence for the speed it is used at, and a
controlled (non-arcade) upper body. builtins.RA230 = {'clips': [{'path', 'stride', 'pelvis', 'chest', 'head', 'arm'}], 'mode': 'measure' |
'copy' | 'inplace', 'suffix': '_RA230'}.
 stride k : the per-cycle horizontal travel is scaled by k at the SAME cadence (root translation x/y and the feet's forward excursion
            about their cycle mean, so a planted foot stays planted); legs re-solved (V2.10 hinge solver + leg guard). Use k = the play
            rate Motion Matching needed for this clip (rate230) so the clip is played at ~1.0.
 pelvis   : lateral pelvis excursion and pelvis roll about the travel axis kept at this fraction of their oscillation (mean kept).
 chest    : chest (spine_05) roll oscillation fraction, removed half at spine_03 and half at spine_05.
 head     : head roll oscillation fraction after the chest change, removed half at neck_01 and half at head (the head still moves).
 arm      : upper-arm direction in the chest frame kept at this fraction of its excursion about the cycle mean (swing and crossing);
            clavicle at the square root of it.
mode 'measure' only reports the before/after metrics; 'copy' writes a duplicate next to the source (suffix) for review; 'inplace'
writes the source asset (checkpoint it first - DB membership is kept). Prints RA230 {...}."""
import unreal as u, builtins, json, math, sys
sys.path.insert(0, r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925')
import importlib, v137_animedit as ae; importlib.reload(ae)
from v137_animedit import qmul, qinv, qnorm, qrot, qaxis, qbetween, vadd, vsub, vsc, vdot, vcross, vlen, vnorm
EAL = u.EditorAssetLibrary
cfg = getattr(builtins, 'RA230', {}); MODE = cfg.get('mode', 'measure'); SUF = cfg.get('suffix', '_RA230')
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
UP = (0.0, 0.0, 1.0)
BONES = ['root', 'pelvis', 'spine_01', 'spine_02', 'spine_03', 'spine_04', 'spine_05', 'neck_01', 'neck_02', 'head', 'clavicle_l', 'clavicle_r',
         'upperarm_l', 'upperarm_r', 'lowerarm_l', 'lowerarm_r', 'hand_l', 'hand_r', 'thigh_l', 'thigh_r', 'calf_l', 'calf_r', 'foot_l', 'foot_r', 'ball_l', 'ball_r', 'ik_foot_root', 'ik_foot_l', 'ik_foot_r']

def roll_about(q, fwd, ref_axis):
    """roll (deg) about the travel axis fwd of the bone's LATERAL axis ref_axis: its elevation above the horizontal in the plane
    normal to fwd (0 = level shoulders / head; small-angle safe, no +-180 wrap for a lateral axis)"""
    a = qrot(q, ref_axis); a = vsub(a, vsc(fwd, vdot(a, fwd)))
    if vlen(a) < 1e-6: return 0.0
    a = vnorm(a)
    return math.degrees(math.asin(max(-1.0, min(1.0, vdot(a, UP)))))

def roll_sign(q, fwd, ax):
    """+1 if a positive qaxis(fwd, +deg) rotation raises the measured roll, else -1 (handedness-proof)"""
    return 1.0 if roll_about(qnorm(qmul(qaxis(fwd, 1.0), q)), fwd, ax) > roll_about(q, fwd, ax) else -1.0

def metrics(clip, L):
    """head lateral vs root = world sway (pp cm), pelvis lateral vs root (pp), shoulder-line roll (pp deg), hand lateral vs chest (pp), stride:
    root travel per second, foot planted slide (max world drift of the lower foot while it is the support, cm)"""
    nf = clip.nf; hl = []; pl = []; sr = []; hn = []; slide = 0.0; prev = None
    root0 = clip.comp('root', 0, L)[0]; rootN = clip.comp('root', nf - 1, L)[0]
    for f in range(nf):
        (rt, rq) = clip.comp('root', f, L); fwd, left = ae.heading_axes(clip, f, L)
        P = clip.comp('pelvis', f, L)[0]; H = clip.comp('head', f, L)[0]; C = clip.comp('spine_05', f, L)[0]
        cl, cr = clip.comp('clavicle_l', f, L)[0], clip.comp('clavicle_r', f, L)[0]; hd = clip.comp('hand_l', f, L)[0]
        hl.append(vdot(vsub(H, rt), left)); pl.append(vdot(vsub(P, rt), left)); hn.append(vdot(vsub(hd, C), left))
        d = vsub(cl, cr); sr.append(math.degrees(math.atan2(d[2], max(1e-3, math.hypot(d[0], d[1])))))
        fl, fr = clip.comp('foot_l', f, L)[0], clip.comp('foot_r', f, L)[0]
        low = fl if fl[2] < fr[2] else fr; side = 'l' if fl[2] < fr[2] else 'r'
        if prev and prev[0] == side: slide = max(slide, math.hypot(low[0] - prev[1][0], low[1] - prev[1][1]) if False else slide)
        prev = (side, low)
    pp = lambda v: round(max(v) - min(v), 2)
    ln = float(u.AnimationLibrary.get_sequence_length(clip.seq))
    return {'head_lat': pp(hl), 'pelvis_lat': pp(pl), 'shoulder_roll': pp(sr), 'hand_lat': pp(hn), 'speed': round(vlen(vsub(rootN, root0)) / max(ln, 1e-3), 1)}

def foot_world_slide(clip, L):
    """support-foot planted drift in the clip's own world (root motion included): per stance (the lower foot), max horizontal drift"""
    worst = 0.0; cur = None; anchor = None
    for f in range(clip.nf):
        fl, fr = clip.comp('foot_l', f, L)[0], clip.comp('foot_r', f, L)[0]
        side, p = ('l', fl) if fl[2] < fr[2] else ('r', fr)
        if side != cur: cur = side; anchor = p; continue
        worst = max(worst, math.hypot(p[0] - anchor[0], p[1] - anchor[1]))
    return round(worst, 2)

def reauthor(seq, c):
    k = float(c.get('stride', 1.0)); kp = float(c.get('pelvis', 1.0)); kc = float(c.get('chest', 1.0)); kh = float(c.get('head', 1.0)); ka = float(c.get('arm', 1.0))
    sk = [str(b) for b in u.AnimationLibrary.get_animation_track_names(seq)] if hasattr(u.AnimationLibrary, 'get_animation_track_names') else BONES
    clip = ae.Clip(seq, [b for b in BONES if b in sk or not b.startswith('ik_')]); nf = clip.nf
    have = [b for b in BONES if b in clip.local]
    L = {b: list(v) for b, v in clip.local.items()}
    before = metrics(clip, clip.local); before['support_slide'] = foot_world_slide(clip, clip.local)
    src_knee = {s: [clip.comp('calf_' + s, f, clip.local)[0] for f in range(nf)] for s in 'lr'}
    src_foot = {s: [clip.comp('foot_' + s, f, clip.local) for f in range(nf)] for s in 'lr'}
    root_src = [clip.comp('root', f, clip.local) for f in range(nf)]
    # ---- 1) stride: root translation (x, y) about frame 0 by k; feet forward excursion about the cycle mean in the root frame by k
    def lateral_axis(bone):
        fwd, left = ae.heading_axes(clip, 0, L); q = clip.comp(bone, 0, L)[1]; best = None
        for a in ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)):
            d = vdot(qrot(q, a), left)
            if best is None or abs(d) > abs(best[1]): best = (a, d)
        return vsc(best[0], 1.0 if best[1] >= 0 else -1.0)
    feet_target = {}
    if abs(k - 1.0) > 1e-4:
        t0 = L['root'][0][0]
        for f in range(nf):
            lt, lq, ls = L['root'][f]; L['root'][f] = ((t0[0] + k * (lt[0] - t0[0]), t0[1] + k * (lt[1] - t0[1]), lt[2]), lq, ls)
    for s in 'lr':
        rel = []
        for f in range(nf):
            rt, rq = root_src[f]; ft, fq = src_foot[s][f]
            rel.append(qrot(qinv(rq), vsub(ft, rt)))   # foot in the root frame (forward = +Y)
        my = sum(r[1] for r in rel) / nf
        tg = []
        for f in range(nf):
            r = rel[f]; r2 = (r[0], my + k * (r[1] - my), r[2])
            rt2, rq2 = clip.comp('root', f, L)
            tg.append((vadd(rt2, qrot(rq2, r2)), src_foot[s][f][1]))
        feet_target[s] = tg
    # ---- 2) pelvis lateral excursion + roll about the travel axis
    if abs(kp - 1.0) > 1e-4:
        lat = []; rol = []; pax = lateral_axis('pelvis')
        for f in range(nf):
            fwd, left = ae.heading_axes(clip, f, L); P = clip.comp('pelvis', f, L); rt = clip.comp('root', f, L)[0]
            lat.append(vdot(vsub(P[0], rt), left)); rol.append(roll_about(P[1], fwd, pax))
        ml, mr = sum(lat) / nf, sum(rol) / nf
        f0w, _ = ae.heading_axes(clip, 0, L); psg = roll_sign(clip.comp('pelvis', 0, L)[1], f0w, pax)
        for f in range(nf):
            fwd, left = ae.heading_axes(clip, f, L); rq = clip.comp('root', f, L)[1]
            d = vsc(left, (kp - 1.0) * (lat[f] - ml)); lt, lq, ls = L['pelvis'][f]
            L['pelvis'][f] = (vadd(lt, qrot(qinv(rq), d)), lq, ls)
            ae.apply_bone_delta(clip, L, 'pelvis', f, qaxis(fwd, -(1.0 - kp) * (rol[f] - mr) * psg))
    # ---- 3) chest roll, 4) head roll (after the chest), 5) arms toward their mean direction in the chest frame
    def lateral_axis(bone):
        # the bone's local axis that points most along the body's lateral axis at frame 0 (Manny spine/head: not X), sign -> +left
        fwd, left = ae.heading_axes(clip, 0, L); q = clip.comp(bone, 0, L)[1]; best = None
        for a in ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)):
            d = vdot(qrot(q, a), left)
            if best is None or abs(d) > abs(best[1]): best = (a, d)
        return vsc(best[0], 1.0 if best[1] >= 0 else -1.0)
    def osc_fix(bones_split, measure_bone, frac, axis=None):
        if abs(frac - 1.0) < 1e-4: return
        axis = axis or lateral_axis(measure_bone)
        rr = []
        for f in range(nf):
            fwd, _ = ae.heading_axes(clip, f, L); rr.append(roll_about(clip.comp(measure_bone, f, L)[1], fwd, axis))
        m = sum(rr) / nf
        fwd0, _ = ae.heading_axes(clip, 0, L); sg = roll_sign(clip.comp(measure_bone, 0, L)[1], fwd0, axis)
        for f in range(nf):
            fwd, _ = ae.heading_axes(clip, f, L); tot = -(1.0 - frac) * (rr[f] - m) * sg
            for b in bones_split:
                if b in L: ae.apply_bone_delta(clip, L, b, f, qaxis(fwd, tot / len(bones_split)))
    # ---- 2b) head world sway: tilt the trunk at spine_01 about the travel axis so the head's lateral excursion (vs root) is kh of it
    if abs(kh - 1.0) > 1e-4:
        hx = []
        for f in range(nf):
            fwd, left = ae.heading_axes(clip, f, L); hx.append(vdot(vsub(clip.comp('head', f, L)[0], clip.comp('root', f, L)[0]), left))
        mh = sum(hx) / nf
        for f in range(nf):
            fwd, left = ae.heading_axes(clip, f, L); S0 = clip.comp('spine_01', f, L)[0]; Hd = clip.comp('head', f, L)[0]
            lev = max(20.0, Hd[2] - S0[2]); want = -(1.0 - kh) * (hx[f] - mh)
            ang = math.degrees(math.asin(max(-0.5, min(0.5, want / lev))))
            # sign: a +1 deg tilt must move the head toward +left by ~lev*pi/180; flip if it moves the other way
            Q1 = qaxis(fwd, 1.0); tt = vdot(vsub(qrot(Q1, vsub(Hd, S0)), vsub(Hd, S0)), left)
            ae.apply_bone_delta(clip, L, 'spine_01', f, qaxis(fwd, ang if tt > 0 else -ang))
    osc_fix(['spine_03', 'spine_05'], 'spine_05', kc)
    osc_fix(['neck_01', 'head'], 'head', kh)
    if abs(ka - 1.0) > 1e-4:
        for s in 'lr':
            for bone, child, frac in (('clavicle_' + s, 'upperarm_' + s, math.sqrt(ka)), ('upperarm_' + s, 'lowerarm_' + s, ka)):
                dirs = []
                for f in range(nf):
                    Cq = clip.comp('spine_05', f, L)[1]; A = clip.comp(bone, f, L)[0]; Bp = clip.comp(child, f, L)[0]
                    dirs.append(qrot(qinv(Cq), vnorm(vsub(Bp, A))))
                m = vnorm(vsc(vadd(*dirs[:2]) if False else tuple(sum(d[i] for d in dirs) for i in range(3)), 1.0 / nf))
                for f in range(nf):
                    Cq = clip.comp('spine_05', f, L)[1]; d = dirs[f]
                    tgt = vnorm(vadd(vsc(m, 1.0 - frac), vsc(d, frac)))
                    R = qnorm(qmul(qmul(Cq, qbetween(d, tgt)), qinv(Cq)))
                    ae.apply_bone_delta(clip, L, bone, f, R)
    # ---- 6) legs to the (stride-scaled or original) foot targets with the source knee as hint
    for s in 'lr':
        tg = feet_target.get(s) or [src_foot[s][f] for f in range(nf)]
        for f in range(nf):
            ae.solve_leg(clip, L, s, f, tg[f][0], tg[f][1], src_knee[s][f])
    # ---- 7) IK foot bones follow the new feet (LegIK / foot placement read them)
    if all(b in L for b in ('ik_foot_root', 'ik_foot_l', 'ik_foot_r')):
        for s in 'lr':
            for f in range(nf):
                Ft, Fq = clip.comp('foot_' + s, f, L); It, Iq = clip.comp('ik_foot_root', f, L); ls_ = L['ik_foot_' + s][f][2]
                L['ik_foot_' + s][f] = (qrot(qinv(Iq), vsub(Ft, It)), qnorm(qmul(qinv(Iq), Fq)), ls_)
    after = metrics(clip, L); after['support_slide'] = foot_world_slide(clip, L)
    changed = [b for b in have if any(L[b][f] != clip.local[b][f] for f in range(nf))]
    return clip, L, before, after, changed, feet_target

out = {'mode': MODE, 'clips': {}}
for c in cfg.get('clips', []):
    seq = u.load_asset(c['path']); assert seq, c['path']
    target = seq
    if MODE == 'copy':
        dst = c['path'] + SUF
        if EAL.does_asset_exist(dst): EAL.delete_asset(dst)
        target = EAL.duplicate_asset(c['path'], dst); assert target
    k0 = float(c.get('stride', 1.0)); rec = {'params': c, 'tries': []}
    for frac in ((1.0, 0.7, 0.4) if MODE in ('copy', 'inplace') else (1.0,)):
        cc = dict(c); cc['stride'] = round(1.0 - (1.0 - k0) * frac, 3)
        clip, L, before, after, changed, ft = reauthor(target, cc)
        rec.update({'before': before, 'after': after, 'changed': changed, 'stride_used': cc['stride']})
        if MODE not in ('copy', 'inplace'): break
        try:
            tg = {s: ft[s] for s in ft} if ft else None
            rec['guard'] = ae.leg_guard(target, L, targets=tg, ref_local=clip.local, label=target.get_name())
        except Exception as e:
            rec['tries'].append({'stride': cc['stride'], 'guard_fail': str(e)[-220:]}); continue
        ae.write_tracks(target, L, changed, note='SHME V2.30 re-author', guard=False)
        target.modify(True); EAL.save_loaded_asset(target, False); rec['saved'] = target.get_path_name(); break
    out['clips'][c['path'].rsplit('/', 1)[-1]] = rec
out['dirty'] = [p.get_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('RA230 ' + json.dumps(out, default=str))
