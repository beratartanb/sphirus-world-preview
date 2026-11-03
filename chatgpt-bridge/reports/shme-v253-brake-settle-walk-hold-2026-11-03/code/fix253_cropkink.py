"""fix253_cropkink.py (dry = measure job; write = manifest of the listed crops): V2.53 owner of the 180 deg turning-start pop.
Measured (probe253_clips.py, root frame of the clip, 30 fps keys): SHM248_Jog_Start_TurnR180_crop has ONE key (0.900 s, where its root yaw
reaches 180) at which every upper-body segment changes velocity at once (spine_05-pelvis 32, head-spine 18, upperarm-clavicle 34 cm/s per
key; neighbours 2-14), shoulder 101 / head 77 cm/s in the root frame. In game the crop plays at 1.12x from 0.842 (14.983 s) and reaches
that key on 15.033 = the measured 79 m/s2 pop; the servo release happens on the same frame only because the turn ends there (all release
owners, Steering, StrideWarping, OffsetRootBone, Inertialization, DeadBlending, OrientationWarping, FootPlacement were eliminated: pop
unchanged; the next clip does not matter: F_Lfoot 79 / CP2 72).
Fix (content, legs and pelvis untouched -> foot contact unchanged): for every *_crop in /Game/GraceRanger/SHME/Animations/V248 the keys whose
upper-body segment velocity change exceeds max(MIN_DV, K x local median) are re-keyed: local rotations of spine_01..05, neck, head,
clavicles, arms and hands at k-1, k, k+1 replaced by a C1 cubic Hermite (quaternion components, sign aligned, normalised) between keys k-2
and k+2 with finite-difference tangents. builtins.V253_KINK = {'dry': bool, 'k': 2.5, 'min_dv': 20.0, 'only': [...]}. Prints KINK253 {...}."""
import unreal as u, json, builtins, math, sys, importlib
sys.path.insert(0, r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925')
import v137_animedit as ae; importlib.reload(ae)
AL = u.AnimationLibrary; EAL = u.EditorAssetLibrary
cfg = dict(getattr(builtins, 'V253_KINK', {})); DRY = bool(cfg.get('dry', True)); KF = float(cfg.get('k', 2.5)); MIN_DV = float(cfg.get('min_dv', 12.0)); ONLY = cfg.get('only')
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
F = '/Game/GraceRanger/SHME/Animations/V248'
UPPER = ['spine_01', 'spine_02', 'spine_03', 'spine_04', 'spine_05', 'neck_01', 'neck_02', 'head', 'clavicle_l', 'clavicle_r', 'upperarm_l', 'upperarm_r', 'lowerarm_l', 'lowerarm_r', 'hand_l', 'hand_r']
PAIRS = [('pelvis', 'root'), ('spine_05', 'pelvis'), ('head', 'spine_05'), ('clavicle_r', 'spine_05'), ('clavicle_l', 'spine_05'), ('upperarm_r', 'clavicle_r'), ('upperarm_l', 'clavicle_l')]
ar = u.AssetRegistryHelpers.get_asset_registry()
names = sorted(str(a.asset_name) for a in ar.get_assets_by_path(F, False) if str(a.asset_class_path.asset_name) == 'AnimSequence' and str(a.asset_name).endswith('_crop'))
out = {'dry': DRY, 'clips': {}}
def seg_dv(c, local):
    nf = c.nf; R = []
    for f in range(nf):
        rt, rq = c.comp('root', f, local); iq = ae.qinv(rq)
        R.append({b: ae.qrot(iq, ae.vsub(c.comp(b, f, local)[0], rt)) for b in set([x for p in PAIRS for x in p]) if b != 'root'}); R[-1]['root'] = (0.0, 0.0, 0.0)
    dv = {}
    for a, b in PAIRS:
        r = lambda k: ae.vsub(R[k][a], R[k][b]); lst = [0.0]
        for f in range(1, nf - 1): lst.append(ae.vlen(ae.vsub(ae.vsub(r(f + 1), r(f)), ae.vsub(r(f), r(f - 1)))) / c.dt)
        dv[a + '-' + b] = lst + [0.0]
    return dv
def align(q, ref): return q if sum(q[i] * ref[i] for i in range(4)) >= 0 else tuple(-x for x in q)
for n in names:
    if ONLY and n not in ONLY: continue
    p = F + '/' + n; seq = u.load_asset(p)
    bones = [b for b in UPPER if b in [str(x) for x in AL.get_animation_track_names(seq)]]
    LEGS = ['thigh_l', 'calf_l', 'foot_l', 'ball_l', 'thigh_r', 'calf_r', 'foot_r', 'ball_r']
    c = ae.Clip(seq, bones + ['root', 'pelvis'] + LEGS); nf = c.nf; c.dt = float(seq.get_play_length()) / max(1, nf - 1)
    local = {b: list(v) for b, v in c.local.items()}
    dv0 = seg_dv(c, local); spikes = []
    for f in range(2, nf - 2):
        hit = []
        for kp, lst in dv0.items():
            nb = sorted(lst[g] for g in range(max(1, f - 5), min(nf - 1, f + 6)) if abs(g - f) > 1); med = nb[len(nb) // 2] if nb else 0.0
            if lst[f] > max(MIN_DV, KF * med): hit.append('%s %.0f/%.0f' % (kp, lst[f], med))
        if len(hit) >= 2: spikes.append((f, hit, len(hit)))
    feet0 = {sd: [c.comp('foot_' + sd, k) for k in range(nf)] for sd in 'lr'}; knee0 = {sd: [c.comp('calf_' + sd, k)[0] for k in range(nf)] for sd in 'lr'}
    for f, _, _ in spikes:
        if f < 3 or f > nf - 4: continue
        # pelvis translation (cubic Hermite, same keys)
        tq = [local['pelvis'][k][0] for k in range(nf)]
        for j, k in enumerate((f - 1, f, f + 1)):
            s_ = (j + 1) / 4.0; h00 = 2 * s_ ** 3 - 3 * s_ ** 2 + 1; h10 = s_ ** 3 - 2 * s_ ** 2 + s_; h01 = -2 * s_ ** 3 + 3 * s_ ** 2; h11 = s_ ** 3 - s_ ** 2
            m0 = [(tq[f - 1][i] - tq[f - 3][i]) / 2.0 for i in range(3)]; m1 = [(tq[f + 3][i] - tq[f + 1][i]) / 2.0 for i in range(3)]
            nt = tuple(h00 * tq[f - 2][i] + h10 * 4 * m0[i] + h01 * tq[f + 2][i] + h11 * 4 * m1[i] for i in range(3))
            lt, lq, ls = local['pelvis'][k]; local['pelvis'][k] = (nt, lq, ls)
        for b in ['pelvis'] + bones:
            q = [local[b][k][1] for k in range(nf)]
            a0, a1 = q[f - 2], align(q[f + 2], q[f - 2])
            m0 = [(align(q[f - 1], a0)[i] - align(q[f - 3], a0)[i]) / 2.0 for i in range(4)]
            m1 = [(align(q[f + 3], a0)[i] - align(q[f + 1], a0)[i]) / 2.0 for i in range(4)]
            for j, k in enumerate((f - 1, f, f + 1)):
                s = (j + 1) / 4.0; h00 = 2 * s ** 3 - 3 * s ** 2 + 1; h10 = s ** 3 - 2 * s ** 2 + s; h01 = -2 * s ** 3 + 3 * s ** 2; h11 = s ** 3 - s ** 2
                qq = ae.qnorm(tuple(h00 * a0[i] + h10 * 4 * m0[i] + h01 * a1[i] + h11 * 4 * m1[i] for i in range(4)))
                lt, lq, ls = local[b][k]; local[b][k] = (lt, align(qq, lq), ls)
        for k in (f - 1, f, f + 1):
            for sd in 'lr':
                ft, fq = feet0[sd][k]; ae.solve_leg(c, local, sd, k, ft, fq, knee0[sd][k])
    dv1 = seg_dv(c, local)
    ferr = max(ae.vlen(ae.vsub(c.comp('foot_' + sd, k, local)[0], feet0[sd][k][0])) for sd in 'lr' for k in range(nf))
    rec = {'foot_err_cm': round(ferr, 3), 'frames': nf, 'spikes': [[round(f * c.dt, 3), h, {kp: round(dv1[kp][f], 1) for kp in dv1}] for f, h, _ in spikes], 'max_before': {kp: round(max(v), 1) for kp, v in dv0.items()}, 'max_after': {kp: round(max(v), 1) for kp, v in dv1.items()}}
    if spikes and not DRY:
        ae.write_tracks(seq, local, ['pelvis'] + bones + ['thigh_l', 'calf_l', 'foot_l', 'thigh_r', 'calf_r', 'foot_r'], note='SHME V2.53 crop kink re-key', guard=True)
        assert EAL.save_loaded_asset(seq, False), p; rec['saved'] = True
    out['clips'][n] = rec
out['dirty'] = [q.get_name().split('/')[-1] for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('KINK253 ' + json.dumps(out, default=str))
