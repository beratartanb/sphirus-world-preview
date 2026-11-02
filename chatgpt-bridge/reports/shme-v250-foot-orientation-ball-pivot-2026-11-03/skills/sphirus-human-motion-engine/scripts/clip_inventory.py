"""V2.8 read-only animation inventory (editor job). For every PoseSearch database under /Game (not Rollbacks / QA / vendor demo
copies) that is referenced by the production AnimBPs, a chooser table or the SHME component, and for the CP sequence-evaluator
clips, writes per clip: path, source family (folder), skeleton, length, frames, root entry / exit speed (cm/s over the first / last
0.1 s), root distance, travel direction vs the initial facing (deg), facing change (deg), support foot at start / end (lower ball),
per-foot contact intervals (ball within 2 cm of the clip's lowest ball height), float curves (distance / speed curves flagged),
looping flag, and database membership. JSON -> Saved/Codex/SHME_V28_20261015/inventory.json (+ a compact markdown table)."""
import unreal as u, json, math, pathlib, importlib, sys
P = pathlib.Path(u.Paths.project_dir()).resolve(); sys.path.insert(0, str(P / 'Tools/SHME_V1_20260925'))
import v137_animedit as ae; importlib.reload(ae)
AL = u.AnimationLibrary; EAL = u.EditorAssetLibrary
OUT = P / 'Saved/Codex/SHME_V28_20261015'
OWNERS = ('/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase', '/Game/GraceRanger/Animations/ABP_GR_MotionMatchingBase',
          '/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent')
CP_CLIPS = ['/Game/GraceRanger/Animations/LookStrafe/Sample/A_LS_M_Relaxed_Walk_Start_F_Lfoot', '/Game/GraceRanger/Animations/LookStrafe/Sample/A_LS_M_Relaxed_Walk_Start_F_Rfoot',
            '/Game/GraceRanger/Experimental/BodyInertia/Transitions/A_TC_WalkStart_R', '/Game/GraceRanger/Animations/LookStrafe/Sample/A_LS_M_Relaxed_Walk_Stop_F_Lfoot',
            '/Game/GraceRanger/Animations/LookStrafe/Sample/A_LS_M_Relaxed_Walk_Stop_F_Rfoot', '/Game/GraceRanger/Animations/Continuity/SampleReference/A_CT_Ref_Walk_Stop_F_Lfoot',
            '/Game/GraceRanger/Animations/Continuity/SampleReference/A_CT_Ref_Walk_Stop_F_Rfoot']
ar = u.AssetRegistryHelpers.get_asset_registry()
dbs = {}
for ad in ar.get_assets_by_class(u.TopLevelAssetPath('/Script/PoseSearch', 'PoseSearchDatabase'), True):
    p = str(ad.package_name)
    if '/Rollbacks/' in p or '/QA/' in p: continue
    refs = [str(x) for x in EAL.find_package_referencers_for_asset(p, False)]
    owner = [r for r in refs if r in OWNERS or '/CHT_' in r or 'Chooser' in r]
    if not owner: continue
    dbs[p] = {'refs': owner}
clips = {}
def clip_info(path):
    seq = u.load_asset(path)
    if not seq or type(seq).__name__ != 'AnimSequence': return {'err': 'not a sequence'}
    try: c = ae.Clip(seq, ['root', 'pelvis', 'ball_l', 'ball_r'])
    except Exception as e: return {'err': str(e)[:120]}
    nf = c.nf; L = float(seq.get_play_length()); dt = L / max(nf - 1, 1); k = max(1, int(round(0.1 / dt)))
    rt = [c.comp('root', f) for f in range(nf)]; R = [x[0] for x in rt]
    def sp(a, b): return ae.vlen(ae.vsub(R[b], R[a])) / max((b - a) * dt, 1e-6)
    fwd0 = ae.qrot(rt[0][1], (0.0, 1.0, 0.0)); fwd1 = ae.qrot(rt[-1][1], (0.0, 1.0, 0.0))
    tr = ae.vsub(R[-1], R[0])
    def ang(a, b): return math.degrees(math.atan2(a[0] * b[1] - a[1] * b[0], a[0] * b[0] + a[1] * b[1]))
    bl = {s: [c.comp('ball_' + s, f)[0][2] - R[f][2] for f in range(nf)] for s in ('l', 'r')}
    cont = {}
    for s in ('l', 'r'):
        lo = min(bl[s]); segs = []; cur = None
        for f in range(nf):
            if bl[s][f] < lo + 2.0: cur = cur or [f, f]; cur[1] = f
            elif cur: segs.append(cur); cur = None
        if cur: segs.append(cur)
        cont[s] = [[round(a * dt, 2), round(b * dt, 2)] for a, b in segs]
    try: cn = [str(n) for n in AL.get_animation_curve_names(seq, u.RawCurveTrackTypes.RCT_FLOAT)]
    except Exception: cn = []
    try: lp = bool(seq.get_editor_property('loop'))
    except Exception: lp = None
    try: sk = seq.get_editor_property('skeleton').get_name()
    except Exception: sk = None
    sup = lambda f: 'L' if bl['l'][f] < bl['r'][f] - 0.5 else ('R' if bl['r'][f] < bl['l'][f] - 0.5 else 'both')
    pz = [c.comp('pelvis', f)[0][2] - R[f][2] for f in range(nf)]
    return {'len': round(L, 3), 'frames': nf, 'skeleton': sk, 'loop': lp, 'v_in': round(sp(0, min(k, nf - 1)), 0), 'v_out': round(sp(max(0, nf - 1 - k), nf - 1), 0),
            'dist': round(math.hypot(tr[0], tr[1]), 1), 'dir_deg': round(ang(fwd0, tr), 0) if math.hypot(tr[0], tr[1]) > 5 else None, 'turn_deg': round(ang(fwd0, fwd1), 0),
            'support_in': sup(0), 'support_out': sup(nf - 1), 'contacts': cont, 'pelvis_range_cm': round(max(pz) - min(pz), 1), 'pelvis_end_minus_start': round(pz[-1] - pz[0], 1),
            'curves': cn, 'distance_curve': any('istance' in x for x in cn), 'family': '/'.join(path.split('/')[2:-1])}
for p in sorted(dbs):
    db = u.load_asset(p); mem = []
    for i in range(db.get_num_animation_assets()):
        a = db.get_animation_asset(i)
        if not a: continue
        ap = a.get_path_name().split('.')[0]; mem.append(ap)
        if ap not in clips: clips[ap] = {'dbs': []}
        clips[ap]['dbs'].append(p.rsplit('/', 1)[-1])
    dbs[p]['members'] = mem; dbs[p]['tags'] = [str(t) for t in (db.get_editor_property('tags') or [])]
for ap in CP_CLIPS: clips.setdefault(ap, {'dbs': []})['cp_evaluator'] = True
for ap in clips:
    try: clips[ap].update(clip_info(ap))
    except Exception as e: clips[ap]['err'] = str(e)[:160]
(OUT / 'inventory.json').write_text(json.dumps({'databases': dbs, 'clips': clips}, indent=1), encoding='utf8')
print('INVENTORY', json.dumps({'databases': len(dbs), 'clips': len(clips)}))
