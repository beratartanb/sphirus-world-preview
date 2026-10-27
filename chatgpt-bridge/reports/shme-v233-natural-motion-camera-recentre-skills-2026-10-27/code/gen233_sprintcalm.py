"""gen233_sprintcalm.py (editor job) - V2.33 5E sprint attitude CANDIDATE: copies of the production sprint loops with a calmer, less athletic
upper body; legs / pelvis / root untouched (ground contact unchanged). Per clip (looping cycle):
  lean    the trunk's forward lean is reduced by LEAN deg: a component-space rotation about the body's lateral axis at spine_01 (children
          follow) and the opposite at neck_01 (the head keeps looking ahead);
  sway    spine_01..05 / neck / head deviations from their cycle mean (lateral sway, twist) scaled by K_TRUNK, head K_HEAD;
  arms    clavicle / upperarm / lowerarm deviations from their mean scaled by K_CLAV / K_ARM (swing kept, smaller, same phase).
Copies get their own database (fresh, seeded from the production sprint DB schema) + full-window BranchIn; the inherited PoseSearch
notifies are stripped. Candidate = ABP flag SHM211_DB_Sprint -> the new DB (no graph change). builtins.SC233 = {'dry': True, 'db': <prod
sprint DB path>, 'lean': 12, 'k_trunk': 0.6, 'k_head': 0.5, 'k_clav': 0.7, 'k_arm': 0.8}. Prints SC233 {...} (dry: the DB's clips +
per-clip trunk lean / head lateral / arm swing measured on the source)."""
import unreal as u, json, math, builtins, pathlib, importlib, sys
P = pathlib.Path(u.Paths.project_dir()).resolve(); sys.path.insert(0, str(P / 'Tools/SHME_V1_20260925'))
import v137_animedit as ae; importlib.reload(ae)
AL = u.AnimationLibrary; EAL = u.EditorAssetLibrary
cfg = dict(getattr(builtins, 'SC233', {})); builtins.SC233 = {}
DRY = bool(cfg.get('dry', True)); DBSRC = cfg.get('db'); LEAN = float(cfg.get('lean', 12.0))
KT = float(cfg.get('k_trunk', 0.6)); KH = float(cfg.get('k_head', 0.5)); KC = float(cfg.get('k_clav', 0.7)); KA = float(cfg.get('k_arm', 0.8))
DIR = '/Game/GraceRanger/SHME/Animations/V233/SprintCalm'; DBN = DIR + '/PSD_SHM233_SprintCalm'
TRUNK = ['spine_01', 'spine_02', 'spine_03', 'spine_04', 'spine_05', 'neck_01', 'neck_02']; HEAD = ['head']
CLAV = ['clavicle_l', 'clavicle_r']; ARM = ['upperarm_l', 'upperarm_r', 'lowerarm_l', 'lowerarm_r']
def qmean(qs):
    a = qs[0]; acc = [0.0, 0.0, 0.0, 0.0]
    for q in qs:
        if sum(q[i] * a[i] for i in range(4)) < 0: q = tuple(-x for x in q)
        for i in range(4): acc[i] += q[i]
    return ae.qnorm(tuple(acc))
def slerp_id(q, w):
    q = ae.qnorm(q)
    if q[3] < 0: q = (-q[0], -q[1], -q[2], -q[3])
    ang = 2.0 * math.acos(max(-1.0, min(1.0, q[3])))
    if ang < 1e-6: return (0.0, 0.0, 0.0, 1.0)
    s = math.sin(ang / 2.0); ax = (q[0] / s, q[1] / s, q[2] / s); a2 = ang * w / 2.0
    return (ax[0] * math.sin(a2), ax[1] * math.sin(a2), ax[2] * math.sin(a2), math.cos(a2))
def measure(clip, local=None):
    """trunk lean (pelvis->neck vs up, deg), head lateral range (cm, body frame), wrist swing range (cm, fore-aft)"""
    N = clip.nf; lean = []; hx = []; wl = []
    for f in range(N):
        pv = clip.comp('pelvis', f, local)[0]; nk = clip.comp('neck_01', f, local)[0]; hd = clip.comp('head', f, local)[0]
        fwd, left = ae.heading_axes(clip, f, local)
        d = ae.vsub(nk, pv); lean.append(math.degrees(math.atan2(ae.vdot(d, fwd), d[2])))
        hx.append(ae.vdot(ae.vsub(hd, pv), left)); wl.append(ae.vdot(ae.vsub(clip.comp('hand_l', f, local)[0], pv), fwd))
    return {'lean_deg': round(sum(lean) / len(lean), 1), 'head_lat_cm': round(max(hx) - min(hx), 1), 'hand_swing_cm': round(max(wl) - min(wl), 1)}
out = {'dry': DRY, 'cfg': cfg, 'clips': {}}
db = u.load_asset(DBSRC); names = [db.get_animation_asset(i) for i in range(db.get_num_animation_assets())]
srcs = [a.get_path_name().split('.')[0] for a in names if a and a.get_class().get_name() == 'AnimSequence']
out['db_clips'] = [s.rsplit('/', 1)[-1] for s in srcs]
BONES = TRUNK + HEAD + CLAV + ARM + ['pelvis', 'root', 'hand_l', 'hand_r']
newdb = None
if not DRY:
    EAL.make_directory(DIR)
    if not EAL.does_asset_exist(DBN):
        fac = u.DataAssetFactory(); fac.set_editor_property('data_asset_class', u.PoseSearchDatabase)
        newdb = u.AssetToolsHelpers.get_asset_tools().create_asset(DBN.rsplit('/', 1)[1], DIR, u.PoseSearchDatabase, fac); assert newdb
        for k in ('schema', 'normalization_set', 'base_cost_bias', 'continuing_pose_cost_bias', 'looping_cost_bias'):
            try: newdb.set_editor_property(k, db.get_editor_property(k))
            except Exception as e: out.setdefault('db_prop_err', []).append([k, str(e)[:80]])
        EAL.save_asset(DBN, False)
    newdb = u.load_asset(DBN)
for sp in srcs:
    nm = sp.rsplit('/', 1)[-1]; info = {}
    seq = u.load_asset(sp); clip = ae.Clip(seq, BONES); info['before'] = measure(clip)
    # always computed from the ORIGINAL clip (idempotent re-runs); 'preview' measures the result without writing (sign / size check)
    cc = clip; local = {b: list(v) for b, v in clip.local.items()}; N = clip.nf
    for b, k in [(x, KT) for x in TRUNK] + [(x, KH) for x in HEAD] + [(x, KC) for x in CLAV] + [(x, KA) for x in ARM]:
        if b not in local: continue
        qm = qmean([local[b][f][1] for f in range(N)])
        for f in range(N):
            t, q, s_ = local[b][f]; dev = ae.qnorm(ae.qmul(q, ae.qinv(qm)))
            local[b][f] = (t, ae.qnorm(ae.qmul(slerp_id(dev, k), qm)), s_)
    if LEAN:
        for f in range(N):
            fwd, left = ae.heading_axes(cc, f, local)
            ae.apply_bone_delta(cc, local, 'spine_01', f, ae.qaxis(left, LEAN))    # +LEAN about the heading 'left' axis = upright (dry run 2026-10-27: -LEAN leaned 24 -> 35 deg)
            ae.apply_bone_delta(cc, local, 'neck_01', f, ae.qaxis(left, -LEAN))
    info['after'] = measure(cc, local)
    if DRY: out['clips'][nm] = info; continue
    dst = DIR + '/SHM233_Calm_' + nm
    if not EAL.does_asset_exist(dst): EAL.duplicate_asset(sp, dst)
    cs = u.load_asset(dst)
    for cls in (u.AnimNotifyState_PoseSearchBranchIn, u.AnimNotifyState_PoseSearchExcludeFromDatabase, u.AnimNotifyState_PoseSearchModifyCost,
                u.AnimNotifyState_PoseSearchBlockTransition, u.AnimNotifyState_PoseSearchOverrideContinuingPoseCostBias):
        try: AL.remove_animation_notify_events_by_notify_class(cs, cls)
        except Exception: pass
    ae.write_tracks(cs, local, [b for b in TRUNK + HEAD + CLAV + ARM if b in local], note='SHME V2.33 calm sprint upper body', guard=False)
    tr = 'SHME_V233_SprintCalm'
    if tr not in [str(t) for t in AL.get_animation_notify_track_names(cs)]: AL.add_animation_notify_track(cs, tr)
    st = AL.add_animation_notify_state_event(cs, tr, 0.0, float(cs.get_play_length()) - 0.001, u.AnimNotifyState_PoseSearchBranchIn)
    st.set_editor_property('database', newdb)
    info['saved'] = bool(EAL.save_asset(dst, False))
    out['clips'][nm] = info
if not DRY:
    if hasattr(u.PoseSearchLibrary, 'clear_pose_search_databases_management'): u.PoseSearchLibrary.clear_pose_search_databases_management()
    nd = u.load_asset(DBN); out['saved_db'] = bool(EAL.save_asset(DBN, False))
    out['db_entries'] = [nd.get_animation_asset(i).get_name() for i in range(nd.get_num_animation_assets()) if nd.get_animation_asset(i)]
print('SC233 ' + json.dumps(out, default=str))
