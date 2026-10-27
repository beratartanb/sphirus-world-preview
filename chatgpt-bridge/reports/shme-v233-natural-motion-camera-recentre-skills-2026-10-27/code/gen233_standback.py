"""gen233_standback.py (editor job) - V2.33 chain 1: a short backward start FROM A TRUE STAND that begins in the character's own idle
pose and moves with the capsule, in its OWN database (never the shared start databases: V2.32 IS copies were picked by release-repress).

Action contract (sphirus-natural-motion): entry = truly stopped body (both feet planted, speed ~0, no brake), backward intent, jog gait;
frame 0 = the production idle pose (af_Stand_Idle_NaturalBaseline_Phase275 at IDLE_T, every bone); the per-bone idle - clip difference fades
out (minimum-jerk) until the first swing foot has handed over to the clip's own step; ROOT motion = the measured CMC response from a stand
(v = V0 + A * tau, LTP of production j30_slow) blended into the clip's own root over the first step, so the clip trajectory and the capsule
agree from the first frame (MM sees the true trajectory, the planted feet do not travel under the body); each foot is PINNED at its idle
ball position (component space incl. the new root = world-fixed while root = capsule) until its own lift, then hands over (minimum-jerk,
HAND s) to the clip's root-relative swing; the start's feet sit lower than the idle / the loop -> pelvis z offset (planted ball level
difference) faded in with the bridge. Legs re-solved (v137_animedit.solve_leg, leg_guard on write).

builtins.GSB233 = {'dry': True, 'src': ..., 'dst': ..., 'db': ..., 'idle_t': 68.4, 'v0': 10.6, 'a': 166.0, 'hand': 0.25,
'root_blend': [0.45, 0.85]}. Prints GSB233 {...}. Writes only DST (+ DB): run with a manifest listing both as --new."""
import unreal as u, json, math, builtins, pathlib, importlib, sys
P = pathlib.Path(u.Paths.project_dir()).resolve(); sys.path.insert(0, str(P / 'Tools/SHME_V1_20260925'))
import v137_animedit as ae; importlib.reload(ae)
AL = u.AnimationLibrary; EAL = u.EditorAssetLibrary
cfg = dict(getattr(builtins, 'GSB233', {})); builtins.GSB233 = {}   # one-shot (V2.30 builtins trap)
DRY = bool(cfg.get('dry', True))
SRC = cfg.get('src', '/Game/GraceRanger/SHME/Animations/Starts/Jog/SHM_JogQ_af_Loco_Jog_Bwd_Start_AAMS')
DST = cfg.get('dst', '/Game/GraceRanger/SHME/Animations/V233/SHM233_StandBack_Jog_Bwd')
DBP = cfg.get('db', '/Game/GraceRanger/SHME/Animations/V233/PSD_SHM233_StandBackStart')
SEED = cfg.get('seed_db', '/Game/GraceRanger/SHME/Animations/Starts/PSD_SHM_JogStartQ_R')
IDLE = '/Game/ActionAdventureMovementS/Animations/Locomotion/CoreMotionAAMS/Integrated/Phase275Support/Idle/af_Stand_Idle_NaturalBaseline_Phase275'
IDLE_T = float(cfg.get('idle_t', 68.4)); V0 = float(cfg.get('v0', 10.6)); A = float(cfg.get('a', 166.0)); VMAX = float(cfg.get('vmax', 230.0))
HAND = float(cfg.get('hand', 0.25)); RB = cfg.get('root_blend', [0.45, 0.85]); LIFT_Z = 2.0; LIFT_D = 3.0; FPS = 30.0
def mj(x): x = min(1.0, max(0.0, x)); return x * x * x * (10 - 15 * x + 6 * x * x)
def slerp(a, b, t):
    a = ae.qnorm(a); b = ae.qnorm(b); d = sum(a[i] * b[i] for i in range(4))
    if d < 0: b = tuple(-x for x in b); d = -d
    if d > 0.9995: return ae.qnorm(tuple(a[i] + (b[i] - a[i]) * t for i in range(4)))
    th = math.acos(d); s0 = math.sin((1 - t) * th) / math.sin(th); s1 = math.sin(t * th) / math.sin(th)
    return ae.qnorm(tuple(a[i] * s0 + b[i] * s1 for i in range(4)))
def slerp_id(q, w):
    """rotation q scaled by w (slerp identity -> q)"""
    q = ae.qnorm(q)
    if q[3] < 0: q = (-q[0], -q[1], -q[2], -q[3])
    ang = 2.0 * math.acos(max(-1.0, min(1.0, q[3])))
    if ang < 1e-6: return (0.0, 0.0, 0.0, 1.0)
    s = math.sin(ang / 2.0); ax = (q[0] / s, q[1] / s, q[2] / s); a2 = ang * w / 2.0
    return (ax[0] * math.sin(a2), ax[1] * math.sin(a2), ax[2] * math.sin(a2), math.cos(a2))
out = {'dry': DRY, 'src': SRC, 'dst': DST, 'db': DBP, 'cfg': {k: v for k, v in cfg.items()}}
src = u.load_asset(SRC); idle = u.load_asset(IDLE)
bones = [str(b) for b in AL.get_animation_track_names(src)]
clip = ae.Clip(src, bones + ['ik_foot_l', 'ik_foot_r', 'ik_foot_root'] if 'ik_foot_root' in bones else bones)
N = clip.nf
ic = ae.Clip(idle, bones); fi = min(ic.nf - 1, int(round(IDLE_T * FPS)))
IB = {s: ic.comp('ball_' + s, fi)[0] for s in 'lr'}
IFQ = {s: ic.comp('foot_' + s, fi)[1] for s in 'lr'}   # idle foot rotation: kept while the foot is planted (no swivel)
# clip analysis: balls in component space incl. the ORIGINAL root, lifts, root travel direction / displacement
Bc = {s: [clip.comp('ball_' + s, f)[0] for f in range(N)] for s in 'lr'}
Rt = [clip.local['root'][f][0] for f in range(N)]
lift = {}
for s in 'lr':
    b0 = Bc[s][0]; lift[s] = N - 1
    for f in range(1, N):
        if Bc[s][f][2] - b0[2] > LIFT_Z or math.hypot(Bc[s][f][0] - b0[0], Bc[s][f][1] - b0[1]) > LIFT_D: lift[s] = f; break
first = min('lr', key=lambda s: lift[s]); second = 'r' if first == 'l' else 'l'
dend = ae.vsub(Rt[-1], Rt[0]); dirv = ae.vnorm((dend[0], dend[1], 0.0)) if math.hypot(dend[0], dend[1]) > 1 else (0.0, -1.0, 0.0)
def d_cap(tau):
    """CMC displacement from a stand (measured production response), capped at VMAX"""
    t1 = max(0.0, (VMAX - V0) / A)
    if tau <= t1: return V0 * tau + 0.5 * A * tau * tau
    return V0 * t1 + 0.5 * A * t1 * t1 + VMAX * (tau - t1)
def d_clip(f): return ae.vdot(ae.vsub(Rt[f], Rt[0]), dirv)
# planted ball heights of the clip after its first lift (where the original feet sit) vs the idle balls
def planted_z(s):
    zs = [Bc[s][f][2] for f in range(N) if f > lift[s] and math.hypot(*(ae.vsub(Bc[s][f], Bc[s][f - 1])[:2])) < 0.6]
    return sorted(zs)[len(zs) // 2] if zs else Bc[s][0][2]
dz = 0.5 * ((IB['l'][2] - planted_z('l')) + (IB['r'][2] - planted_z('r')))
out['analysis'] = {'frames': N, 'idle_frame': fi, 'first_swing': first, 'lift_t': {s: round(lift[s] / FPS, 2) for s in 'lr'},
                   'stance_off_cm': {s: round(ae.vlen(ae.vsub(IB[s], Bc[s][0])), 1) for s in 'lr'},
                   'ball_z': {'idle': {s: round(IB[s][2], 1) for s in 'lr'}, 'clip_planted': {s: round(planted_z(s), 1) for s in 'lr'}}, 'pelvis_dz': round(dz, 2),
                   'root_dir': [round(x, 2) for x in dirv],
                   'root_vs_capsule_cm': {('%.2f' % (f / FPS)): [round(d_clip(f), 1), round(d_cap(f / FPS), 1)] for f in range(0, N, 3)}}
# per-bone idle - clip(0) difference (largest)
dif = []
for b in bones:
    if b == 'root' or b not in ic.local: continue
    t0, q0, _ = clip.local[b][0]; ti, qi, _ = ic.local[b][fi]
    qd = ae.qnorm(ae.qmul(qi, ae.qinv(q0))); ang = math.degrees(2 * math.acos(min(1.0, abs(qd[3]))))
    dif.append((round(ang, 1), round(ae.vlen(ae.vsub(ti, t0)), 1), b))
out['analysis']['bone_diff_top'] = sorted(dif, reverse=True)[:12]
DB_ONLY = bool(cfg.get('db_only', False))
EXIT = cfg.get('exit_loops', ['/Game/GraceRanger/Animations/LocomotionBehavior/RearRevision/A_RB_Jog_Rear'])
if not DRY and not DB_ONLY:
    assert not EAL.does_asset_exist(DST), 'DST exists: ' + DST
    EAL.make_directory(DST.rsplit('/', 1)[0])
    seq = EAL.duplicate_asset(SRC, DST)
    # strip the inherited PoseSearch notifies (a copy with BranchIn joins the shared start DBs - V2.11 / V2.32 trap)
    for cls in (u.AnimNotifyState_PoseSearchBranchIn, u.AnimNotifyState_PoseSearchExcludeFromDatabase, u.AnimNotifyState_PoseSearchModifyCost,
                u.AnimNotifyState_PoseSearchBlockTransition, u.AnimNotifyState_PoseSearchOverrideContinuingPoseCostBias):
        try: AL.remove_animation_notify_events_by_notify_class(seq, cls)
        except Exception: pass
    local = {b: list(v) for b, v in clip.local.items()}
    FB = min(N - 1, lift[first] + int(round(HAND * FPS)))          # bridge end = first swing handed over
    # 1 bridge: every bone except root starts at the idle pose; the difference fades out by FB
    for b in bones:
        if b == 'root' or b not in ic.local: continue
        t0, q0, _ = clip.local[b][0]; ti, qi, _ = ic.local[b][fi]
        Dt = ae.vsub(ti, t0); Dq = ae.qnorm(ae.qmul(qi, ae.qinv(q0)))
        for f in range(0, FB + 1):
            w = 1.0 - mj(f / float(max(FB, 1))); lt, lq, ls = local[b][f]
            local[b][f] = (ae.vadd(lt, ae.vsc(Dt, w)), ae.qnorm(ae.qmul(slerp_id(Dq, w), lq)), ls)
    # 2 pelvis level (the start's feet sit lower than the idle / loop): + dz on the pelvis translation, faded in over the bridge
    for f in range(N):
        w = mj(f / float(max(FB, 1)))
        lt, lq, ls = local['pelvis'][f]; local['pelvis'][f] = ((lt[0], lt[1], lt[2] + dz * w), lq, ls)
    # 3 root = measured capsule response, blended into the clip's own root VELOCITY between RB[0] and RB[1] s and integrated (continuous)
    f0, f1 = int(RB[0] * FPS), int(RB[1] * FPS); prev = Rt[0]
    for f in range(N):
        w = 1.0 if f <= f0 else (1.0 - mj((f - f0) / float(max(f1 - f0, 1))) if f < f1 else 0.0)
        if f == 0: tgt = Rt[0]
        else:
            vc = ae.vsc(dirv, d_cap(f / FPS) - d_cap((f - 1) / FPS)); vo = ae.vsub(Rt[f], Rt[f - 1])
            tgt = ae.vadd(prev, (w * vc[0] + (1 - w) * vo[0], w * vc[1] + (1 - w) * vo[1], vo[2]))
        prev = tgt
        lt, lq, ls = local['root'][f]; local['root'][f] = (tgt, lq, ls)
    # 4 feet: pinned at the idle balls (component incl. the new root) until their own lift, then minimum-jerk hand-over (HAND s) into the
    #   clip's ROOT-RELATIVE swing carried by the new root (comp' = comp_orig - root_orig + root_new)
    err = {}
    for s in 'lr':
        lf = lift[s]; fh = min(N - 1, lf + int(round(HAND * FPS))); e_ = 0.0
        for f in range(N):
            rel = ae.vsub(Bc[s][f], Rt[f]); own = ae.vadd(rel, local['root'][f][0]); own = (own[0], own[1], own[2] + dz)
            if f <= lf: tgt = IB[s]
            elif f <= fh:
                pin_off = ae.vsub(IB[s], ae.vadd(ae.vsub(Bc[s][lf], Rt[lf]), local['root'][lf][0])); pin_off = (pin_off[0], pin_off[1], pin_off[2] - dz)
                w = 1.0 - mj((f - lf) / float(max(fh - lf, 1))); tgt = ae.vadd(own, ae.vsc(pin_off, w))
            else: tgt = own
            fp, fq = clip.comp('foot_' + s, f, local); bp, _ = clip.comp('ball_' + s, f, local)
            # planted: the IDLE foot rotation (world-fixed, no swivel); hand-over: rotation eases into the clip's own swing rotation
            if f <= lf: tq = IFQ[s]
            elif f <= fh: tq = slerp(IFQ[s], fq, mj((f - lf) / float(max(fh - lf, 1))))
            else: tq = fq
            ball_in_foot = ae.qrot(ae.qinv(fq), ae.vsub(bp, fp))          # ball offset in the foot frame (bone lengths kept)
            ae.solve_leg(clip, local, s, f, ae.vsub(tgt, ae.qrot(tq, ball_in_foot)), tq, clip.comp('calf_' + s, f, local)[0])
            e_ = max(e_, ae.vlen(ae.vsub(clip.comp('ball_' + s, f, local)[0], tgt)))
        err[s] = round(e_, 2)
    for s in ('l', 'r'):
        b = 'ik_foot_' + s
        if b in local and 'ik_foot_root' in local:
            for f in range(N):
                fp, fq = clip.comp('foot_' + s, f, local); pp, pq = clip.comp('ik_foot_root', f, local)
                local[b][f] = (ae.qrot(ae.qinv(pq), ae.vsub(fp, pp)), ae.qnorm(ae.qmul(ae.qinv(pq), fq)), local[b][f][2])
    clip.seq = seq
    ae.write_tracks(seq, local, [b for b in local if b in bones], note='SHME V2.33 stand back start (idle bridge, capsule root, pinned feet)')
if not DRY:
    seq = u.load_asset(DST)
    # own database (fresh asset on the start schema) + full-window BranchIn on the new clip and on the backward jog loop (exit inside the DB)
    if not EAL.does_asset_exist(DBP):
        seed = u.load_asset(SEED)
        fac = u.DataAssetFactory(); fac.set_editor_property('data_asset_class', u.PoseSearchDatabase)   # (V2.26 path; PoseSearchDatabaseFactory returns None)
        db = u.AssetToolsHelpers.get_asset_tools().create_asset(DBP.rsplit('/', 1)[1], DBP.rsplit('/', 1)[0], u.PoseSearchDatabase, fac); assert db, DBP
        for k in ('schema', 'normalization_set'):
            try: db.set_editor_property(k, seed.get_editor_property(k))
            except Exception as e: out['db_prop_' + k] = str(e)[:120]
        for k in ('base_cost_bias', 'continuing_pose_cost_bias', 'looping_cost_bias'):
            try: db.set_editor_property(k, seed.get_editor_property(k))
            except Exception: pass
        EAL.save_asset(DBP, False)
    db = u.load_asset(DBP)
    tr = 'SHME_V233_StandBack'
    for cp in [DST] + list(EXIT):
        cs = u.load_asset(cp); names = [str(t) for t in AL.get_animation_notify_track_names(cs)]
        if tr in names: AL.remove_animation_notify_track(cs, tr)
        AL.add_animation_notify_track(cs, tr)
        st = AL.add_animation_notify_state_event(cs, tr, 0.0, float(cs.get_play_length()) - 0.001, u.AnimNotifyState_PoseSearchBranchIn)
        st.set_editor_property('database', db)
        out.setdefault('saved_clips', {})[cp.rsplit('/', 1)[-1]] = bool(EAL.save_asset(cp, False))
    if hasattr(u.PoseSearchLibrary, 'clear_pose_search_databases_management'): u.PoseSearchLibrary.clear_pose_search_databases_management()
    db = u.load_asset(DBP); out['saved_db'] = bool(EAL.save_asset(DBP, False))
    out['db_entries'] = [db.get_animation_asset(i).get_name() for i in range(db.get_num_animation_assets()) if db.get_animation_asset(i)]
    if not DB_ONLY: out['ball_err'] = err; out['bridge_end_t'] = round(FB / FPS, 2)
    nc = ae.Clip(seq, ['ball_l', 'ball_r', 'root']); out['check'] = {s: {'f0_vs_idle_cm': round(ae.vlen(ae.vsub(nc.comp('ball_' + s, 0)[0], IB[s])), 2)} for s in 'lr'}
(P / 'Saved/Codex/SHME_V233_20261027' / ('gsb233_%s.json' % ('dry' if DRY else 'write'))).write_text(json.dumps(out, indent=1, default=str))
print('GSB233 ' + json.dumps({k: out[k] for k in out if k in ('dry', 'analysis', 'ball_err', 'db_entries', 'saved_clips', 'saved_db', 'check', 'bridge_end_t')}, default=str))
