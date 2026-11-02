"""fix249_footpivot.py (editor job; dry = measure, write = manifest of the 22 project copies): V2.49 foot repair v3 - BALL-PIVOT stance.
History: v2 (fix249_footpitch.py) flattened the foot about the ANKLE; the authored pivot of these turning starts rotates the foot about
the BALL, so with the ball moved 14 cm in front of the ankle the planted ball swept an arc during the pivot (v249ecap: 29 cm).
v3, per frame and foot, from the ORIGINAL data (the unmodified CoreMotionAAMS/Candidate source of each copy; the copy's legs must equal
the source's except the foot bone touched by v2, which is restored):
  if the original ball is below the floor contact height Zb:
     ball'  = (ball.x, ball.y, Zb)                         the pivot point stays where it was authored, on the floor
     ankle' = (ball'.xy - u * h, ankle.z)  with h = sqrt(L^2 - (ankle.z - Zb)^2), u = the foot's horizontal heading (ankle->ball, or the
              foot's forward axis when that projection is short), L = ankle-ball length -> the heel sits behind the ball at the authored
              ankle height (a heel-raised pivot on the ball of the foot)
     foot rotation' = shortest arc (ball - ankle) -> (ball' - ankle') applied to the original foot rotation
     thigh / calf re-solved with ae.solve_leg (knee kept a hinge, original knee as the plane hint)
  else: original (swing, heel strike, real toe-off untouched)
Zb = ball height of A_CP2_Jog_Fwd_Start frame 0. builtins.V249_FV = {'dry': bool}. Prints FOOTPIVOT249 {...}."""
import unreal as u, json, builtins, math, sys, importlib
sys.path.insert(0, r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925')
import v137_animedit as ae; importlib.reload(ae)
EAL = u.EditorAssetLibrary
cfg = dict(getattr(builtins, 'V249_FV', {})); DRY = bool(cfg.get('dry', True))
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
ar = u.AssetRegistryHelpers.get_asset_registry()
allseq = {}
for a in ar.get_assets_by_class(u.TopLevelAssetPath('/Script/Engine', 'AnimSequence'), True): allseq.setdefault(str(a.asset_name), []).append(str(a.package_name))
def one(n): return [p for p in allseq.get(n, []) if not p.startswith('/Game/GraceRanger/SHME/')] or None   # every same-named non-SHME clip; the one whose legs match is used
targets = []
for n, ps in allseq.items():
    for p in ps:
        if not p.startswith('/Game/GraceRanger/SHME/'): continue
        if n.startswith('SHM_JogQ_af_'): targets.append((p, one(n[len('SHM_JogQ_'):])))
        elif n.startswith('SHM232_IS_af_'): targets.append((p, one(n[len('SHM232_IS_'):])))
        elif n.startswith('SHM248_Jog_Start_Turn') and n.endswith('_crop'):
            s, d = n[len('SHM248_Jog_Start_Turn')], n[len('SHM248_Jog_Start_Turn') + 1:len('SHM248_Jog_Start_Turn') + 4]
            targets.append((p, one('af_Loco_Jog_Start_Turn%s%s_%sfoot_AAMS' % (s, d, s))))
targets.sort()
ref = ae.Clip(u.load_asset([p for p in allseq['A_CP2_Jog_Fwd_Start']][0]), ['ball_l', 'ball_r'])
ZB = 0.5 * (ref.comp('ball_l', 0)[0][2] + ref.comp('ball_r', 0)[0][2])
LEG = ['thigh_l', 'calf_l', 'foot_l', 'ball_l', 'thigh_r', 'calf_r', 'foot_r', 'ball_r']

def arc_leg(c, local, s, f, An, Qd):
    """minimal-arc two-bone solve that KEEPS the authored bone rolls: the knee stays in the plane (hip, authored knee, new ankle) and
    bends the authored way; thigh and calf get the shortest rotation that moves them onto the new knee / ankle (no twist rebuild, so no
    roll jump between repaired and untouched frames); the foot gets the target component rotation Qd."""
    th, ca, fo = 'thigh_' + s, 'calf_' + s, 'foot_' + s
    H = c.comp(th, f, local)[0]; K = c.comp(ca, f, local)[0]; A = c.comp(fo, f, local)[0]
    l1 = ae.vlen(ae.vsub(K, H)); l2 = ae.vlen(ae.vsub(A, K))
    d = ae.vsub(An, H); dl = max(min(ae.vlen(d), l1 + l2 - 1e-3), abs(l1 - l2) + 1e-3); dn = ae.vnorm(d)
    pk = ae._perp(ae.vsub(K, H), dn); pk = ae.vnorm(pk) if ae.vlen(pk) > 1e-6 else ae.vnorm(ae._perp(ae.qrot(c.comp(ca, f, local)[1], ae.ZAX), dn))
    a = (l1 * l1 - l2 * l2 + dl * dl) / (2.0 * dl); hgt = math.sqrt(max(l1 * l1 - a * a, 0.0))
    Kn = ae.vadd(ae.vadd(H, ae.vsc(dn, a)), ae.vsc(pk, hgt)); At = ae.vadd(H, ae.vsc(dn, dl))
    ae.apply_bone_delta(c, local, th, f, ae.qbetween(ae.vnorm(ae.vsub(K, H)), ae.vnorm(ae.vsub(Kn, H))))
    K2 = c.comp(ca, f, local)[0]; A2 = c.comp(fo, f, local)[0]
    ae.apply_bone_delta(c, local, ca, f, ae.qbetween(ae.vnorm(ae.vsub(A2, K2)), ae.vnorm(ae.vsub(At, K2))))
    Qc = c.comp(ca, f, local)[1]; lt, lq, ls = local[fo][f]; local[fo][f] = (lt, ae.qnorm(ae.qmul(ae.qinv(Qc), Qd)), ls)

def roll_leg(c, local, s, f, At, Qd):
    """v3e hinge solve that KEEPS the authored axes: the knee bends in the plane whose normal is the authored calf hinge axis (calf local Z,
    projected), the thigh and calf are rebuilt as full frames whose roll axes are their OWN authored Z axes projected onto the new bone
    directions -> repaired frames carry the authored knee axis, so there is no axis jump against untouched neighbours."""
    th, ca, fo = 'thigh_' + s, 'calf_' + s, 'foot_' + s
    (H, qH), (K, qK) = c.comp(th, f, local), c.comp(ca, f, local)
    l1 = ae.vlen(local[ca][f][0]); l2 = ae.vlen(local[fo][f][0])
    d = ae.vsub(At, H); dl = max(min(ae.vlen(d), l1 + l2 - 1e-3), abs(l1 - l2) + 1e-3); dn = ae.vnorm(d)
    zc = ae.qrot(qK, ae.ZAX); zt = ae.qrot(qH, ae.ZAX)
    n_t = ae._perp(zc, dn); n_t = ae.vnorm(n_t) if ae.vlen(n_t) > 1e-6 else ae.vnorm(ae._perp(zt, dn))
    a = (l1 * l1 - l2 * l2 + dl * dl) / (2.0 * dl); hgt = math.sqrt(max(l1 * l1 - a * a, 0.0))
    side = ae.vcross(dn, n_t)
    if ae.vdot(side, ae.vsub(K, H)) < 0 and False: side = ae.vsc(side, -1.0)
    Kn = ae.vadd(ae.vadd(H, ae.vsc(dn, a)), ae.vsc(side, hgt)); An = ae.vadd(H, ae.vsc(dn, dl))
    # keep the authored bend direction: the knee goes to the side of the authored knee
    if ae.vdot(ae.vsub(Kn, ae.vadd(H, ae.vsc(dn, a))), ae.vsub(K, ae.vadd(H, ae.vsc(dn, ae.vdot(ae.vsub(K, H), dn))))) < 0:
        Kn = ae.vsub(ae.vadd(H, ae.vsc(dn, a)), ae.vsc(side, hgt))
    Qth = ae.q_from_two(ae.vnorm(local[ca][f][0]), ae.ZAX, ae.vsub(Kn, H), zt)
    Qca = ae.q_from_two(ae.vnorm(local[fo][f][0]), ae.ZAX, ae.vsub(An, Kn), zc)
    _, Qp = c.comp(c.parent[th], f, local)
    lt, lq, ls = local[th][f]; local[th][f] = (lt, ae.qnorm(ae.qmul(ae.qinv(Qp), Qth)), ls)
    lt, lq, ls = local[ca][f]; local[ca][f] = (lt, ae.qnorm(ae.qmul(ae.qinv(Qth), Qca)), ls)
    lt, lq, ls = local[fo][f]; local[fo][f] = (lt, ae.qnorm(ae.qmul(ae.qinv(Qca), Qd)), ls)
def pitch(A, B): return math.degrees(math.atan2(-(B[2] - A[2]), math.hypot(B[0] - A[0], B[1] - A[1])))
out = {'dry': DRY, 'zb': round(ZB, 2), 'clips': {}, 'saved': 0, 'skipped': []}
for tp, sp in targets:
    if not sp and not cfg.get('self_source'): out['skipped'].append([tp.split('/')[-1], 'no source']); continue
    T = u.load_asset(tp); ct = ae.Clip(T, LEG); nf = ct.nf; cs = None; diffs = []
    if cfg.get('self_source'): sp = []; cs = ct      # v3b: the copy itself is the original (restored from its pre-v2 backup)
    for cand in sp:
        S_ = u.load_asset(cand); cs_ = ae.Clip(S_, LEG)
        if cs_.nf < nf: diffs.append([cand.split('/')[-3], 'short']); continue
        diff = 0.0
        for b in ('thigh_l', 'calf_l', 'thigh_r', 'calf_r'):
            for f in range(nf):
                qa, qb = ct.local[b][f][1], cs_.local[b][f][1]; diff = max(diff, 1.0 - abs(sum(x * y for x, y in zip(qa, qb))))
        diffs.append([cand.split('/')[-3], '%.1e' % diff])
        if diff <= 1e-4: cs = cs_; break
    if cs is None: out['skipped'].append([tp.split('/')[-1], diffs]); continue
    local = {k: list(v) for k, v in ct.local.items()}
    for b in ('foot_l', 'foot_r', 'ball_l', 'ball_r'): local[b] = [cs.local[b][f] for f in range(nf)]     # restore the original feet (undo v2)
    info = {}
    for s in ('l', 'r'):
        nfix = 0; pb, pa, slide_b, slide_a, zmin = [], [], 0.0, 0.0, 9e9; prevB0 = prevB1 = None; prev_u = None
        for f in range(nf):
            A, Q = ct.comp('foot_' + s, f, local); B = ct.comp('ball_' + s, f, local)[0]; K = ct.comp('calf_' + s, f, local)[0]
            pb.append(pitch(A, B))
            if B[2] < ZB - 0.05:
                L = ae.vlen(ae.vsub(B, A)); dz = max(0.0, A[2] - ZB); h = math.sqrt(max(L * L - dz * dz, 0.0))
                hor = (B[0] - A[0], B[1] - A[1], 0.0)
                lat = ae.qrot(Q, ae.ZAX); fw = ae.vnorm(ae.vcross(lat, (0.0, 0.0, 1.0)))     # v3d: ALWAYS the foot's own forward axis
                ref_dir = hor if ae.vlen(hor) > 0.5 else (prev_u if prev_u else hor)
                uu = fw if ae.vdot(fw, ref_dir) >= 0 else ae.vsc(fw, -1.0); prev_u = uu
                Bn = (B[0], B[1], ZB); An = (Bn[0] - uu[0] * h, Bn[1] - uu[1] * h, A[2] if dz > 0 else ZB)
                R = ae.qbetween(ae.vnorm(ae.vsub(B, A)), ae.vnorm(ae.vsub(Bn, An)))
                roll_leg(ct, local, s, f, An, ae.qnorm(ae.qmul(R, Q))); nfix += 1      # v3e: only repaired frames, authored axes kept
            A2 = ct.comp('foot_' + s, f, local)[0]; B2 = ct.comp('ball_' + s, f, local)[0]
            pa.append(pitch(A2, B2)); zmin = min(zmin, B2[2])
            # planted-ball travel while on the floor (before / after): the pivot must not slide
            Bo = ct.comp('ball_' + s, f, {**local, **{k: [cs.local[k][g] for g in range(nf)] for k in ('thigh_' + s, 'calf_' + s, 'foot_' + s, 'ball_' + s)}})[0]
            if prevB0 is not None and Bo[2] < ZB + 2.0: slide_b += math.hypot(Bo[0] - prevB0[0], Bo[1] - prevB0[1])
            if prevB1 is not None and B2[2] < ZB + 2.0: slide_a += math.hypot(B2[0] - prevB1[0], B2[1] - prevB1[1])
            prevB0, prevB1 = Bo, B2
        info[s] = {'fixed': nfix, 'nf': nf, 'f0': [round(pb[0], 1), round(pa[0], 1)], 'mean': [round(sum(pb) / nf, 1), round(sum(pa) / nf, 1)],
                   'min_ball_z': round(zmin, 1), 'floor_ball_travel_cm': [round(slide_b, 1), round(slide_a, 1)]}
    out['clips'][tp.split('/')[-1]] = info
    orig = {k: [ct.local[k][g] for g in range(nf)] for k in ct.local}
    info['metrics'] = {k: [v['hinge_min'], v['axis_jump_deg'], v['ref_jump_deg'], v['twisted_frames'], v['backward_frames']] for k, v in ae.leg_metrics(T, local, ref_local=orig).items()}
    if not DRY:
        info['guard'] = ae.leg_guard(T, local, ref_local=orig, label=tp.split('/')[-1])
        ae.write_tracks(T, local, LEG, note='SHME V2.49 ball-pivot stance repair', guard=False)
        assert EAL.save_asset(tp, False), tp; out['saved'] += 1
out['n'] = len(targets)
out['dirty'] = [q.get_name().split('/')[-1] for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('FOOTPIVOT249 ' + json.dumps(out))
