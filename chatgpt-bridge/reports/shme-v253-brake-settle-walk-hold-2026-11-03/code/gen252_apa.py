"""gen252_apa.py (dry = measure job; write = manifest of the NEW assets only): V2.52 ANTICIPATORY WEIGHT TRANSFER for the walk starts.
Measured (probe252_starttransfer): in the 14 SHM_StartTransfer_* clips the pelvis is still centred (t = 0.42-0.70 on the stance->swing
foot axis, stance width 28 cm) when the swing foot leaves the floor: the body lifts a leg that still carries weight. In human gait
initiation the centre of mass moves toward the stance limb BEFORE swing toe-off (here: to t ~ 0.37, i.e. 3-4 cm), so the stance leg is
loaded and the swing foot is free.
New content (the source clips are not modified): /Game/GraceRanger/SHME/Animations/V252/SHM252_StartTransfer_<dir>_<foot>_APA =
duplicate of each clip with a pelvis weight transfer baked in:
  shift(t) = D * p(t) toward the stance foot along the frame-0 stance->swing axis, D = clamp((t_toe - TGT) * width, 0, MAXD),
  p = smoothstep 0 -> 1 from frame 0 to swing toe-off, then smoothstep 1 -> 0 over FADE s (the step itself carries the body on),
  feet kept exactly where the source has them (V2.10 hinge leg solver on both legs, knee hint = the source knee), the trunk follows
  the pelvis (children unchanged), a small pelvis roll ROLL deg * p(t) lowers the swing-side hip as the stance hip takes the load.
The copies lose the source 'SHME_StartTransfer_Role' track (it would keep them in the source databases) and get a full-window PoseSearch
BranchIn into new databases PSD_SHM252_StartTransferAPA_L / _R (same membership and settings as PSD_SHM_StartTransfer_L / _R).
A/B / promotion = the ABP variables SHM_StartTransferDB_L / _R. builtins.V252_APA = {'dry': bool, 'tgt': 0.37, 'maxd': 5.0, 'fade': 0.3,
'roll': 2.0, 'blend': 0.5}. Prints APA252 {...}."""
import unreal as u, json, builtins, math, sys, importlib
sys.path.insert(0, r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925')
import v137_animedit as ae; importlib.reload(ae)
L = u.AnimationLibrary; EAL = u.EditorAssetLibrary
cfg = dict(getattr(builtins, 'V252_APA', {})); DRY = bool(cfg.get('dry', True)); TGT = float(cfg.get('tgt', 0.37)); MAXD = float(cfg.get('maxd', 5.0))
FADE = float(cfg.get('fade', 0.3)); ROLL = float(cfg.get('roll', 2.0)); BLEND = float(cfg.get('blend', 0.5))
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
F = '/Game/GraceRanger/SHME/Animations/StartTransfer/'; V = '/Game/GraceRanger/SHME/Animations/V252/'
out = {'dry': DRY, 'cfg': {'tgt': TGT, 'maxd': MAXD, 'fade': FADE, 'roll': ROLL}, 'clips': {}, 'dbs': {}}
def smooth(x): x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)
def proj(p, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]; dd = dx * dx + dy * dy or 1.0
    return ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / dd
src_db = {s: u.load_asset(F + 'PSD_SHM_StartTransfer_' + s) for s in 'LR'}
member = {}
for s, db in src_db.items():
    for i in range(db.get_num_animation_assets()): member.setdefault(db.get_animation_asset(i).get_name(), []).append(s)
# the role track content (what the copies must not keep)
try:
    s0 = u.load_asset(F + 'SHM_StartTransfer_F_Rfoot'); evs = s0.get_editor_property('notifies')
    out['role_track_events'] = [[str(e.get_editor_property('track_index')), str(e.get_editor_property('notify_state_class') or e.get_editor_property('notify')), round(float(e.get_editor_property('trigger_time_offset') if False else 0), 2)] for e in evs][:12]
except Exception as e: out['role_err'] = str(e)[:200]
dst_db = {}
if not DRY:
    for s in 'LR':
        dp = V + 'PSD_SHM252_StartTransferAPA_' + s
        if EAL.does_asset_exist(dp): db = u.load_asset(dp)
        else:
            fac = u.DataAssetFactory(); fac.set_editor_property('data_asset_class', u.PoseSearchDatabase)
            db = u.AssetToolsHelpers.get_asset_tools().create_asset(dp.rsplit('/', 1)[1], dp.rsplit('/', 1)[0], u.PoseSearchDatabase, fac); assert db, dp
        for k in ('schema', 'normalization_set', 'base_cost_bias', 'continuing_pose_cost_bias', 'looping_cost_bias', 'exclude_from_database_parameters', 'pose_search_mode', 'kdtree_max_leaf_size', 'kdtree_query_num_neighbors'):
            try: db.set_editor_property(k, src_db[s].get_editor_property(k))
            except Exception: pass
        assert EAL.save_asset(dp, False); dst_db[s] = u.load_asset(dp)
for n in sorted(member):
    sp = F + n; seq0 = u.load_asset(sp); sw = 'l' if n.endswith('_Lfoot') else 'r'; st = 'r' if sw == 'l' else 'l'
    c = ae.Clip(seq0, ['foot_l', 'foot_r', 'ball_l', 'ball_r', 'pelvis', 'spine_05']); nf = c.nf; Ln = seq0.get_play_length(); dt = Ln / max(1, nf - 1)
    a0 = c.comp('foot_' + sw, 0)[0][2]; b0 = c.comp('ball_' + sw, 0)[0][2]; toe = None
    for f in range(nf):
        if toe is None and c.comp('ball_' + sw, f)[0][2] > b0 + 1.5: toe = f
    toe = toe if toe is not None else max(1, nf // 6)
    scen = lambda f, side: [(c.comp('foot_' + side, f)[0][i] + c.comp('ball_' + side, f)[0][i]) / 2 for i in range(3)]
    S0, W0 = scen(0, st), scen(0, sw); width = math.hypot(W0[0] - S0[0], W0[1] - S0[1]); axis = ae.vnorm((W0[0] - S0[0], W0[1] - S0[1], 0.0))
    t_toe = proj(c.comp('pelvis', toe)[0], scen(toe, st), scen(toe, sw))
    # v2: the start is entered from the idle through the Motion Matching blend (BlendTime 0.5 s, HermiteCubic): at swing toe-off only
    # w(t_toe) of this clip is visible, the rest is the centred idle (t 0.5). Shift so that the VISIBLE pelvis reaches TGT, capped.
    w = smooth((toe * dt) / BLEND) if BLEND > 0 else 1.0; t_vis = (1 - w) * 0.5 + w * t_toe
    D = max(0.0, min(MAXD, (t_vis - TGT) * width / max(w, 0.15)))
    rec = {'swing': sw, 'toe_off': round(toe * dt, 3), 'width': round(width, 1), 't_toe_src': round(t_toe, 2), 'blend_w_toe': round(w, 2), 't_vis_src': round(t_vis, 2), 't_vis_after': round(t_vis - w * D / width, 2), 'shift_cm': round(D, 2), 'dbs': member[n]}
    local = {k: list(v) for k, v in c.local.items()}
    if D > 0.2:
        tgt_feet = {s_: [c.comp('foot_' + s_, f) for f in range(nf)] for s_ in 'lr'}
        knees = {s_: [c.comp('calf_' + s_, f)[0] for f in range(nf)] for s_ in 'lr'}
        Tf = FADE / max(dt, 1e-6); fwd_roll_axis = ae.vnorm(ae.vcross((0.0, 0.0, 1.0), axis))
        for f in range(nf):
            p = smooth(f / max(1, toe)) if f <= toe else 1.0 - smooth((f - toe) / max(1.0, Tf))
            if p <= 1e-4: continue
            off = ae.vsc(axis, -D * p)                                          # toward the stance foot
            par = c.parent['pelvis']; Qp = c.comp(par, f, local)[1] if par else (0.0, 0.0, 0.0, 1.0)
            lt, lq, ls = local['pelvis'][f]; local['pelvis'][f] = (ae.vadd(lt, ae.qrot(ae.qinv(Qp), off)), lq, ls)
            if ROLL > 0: ae.apply_bone_delta(c, local, 'pelvis', f, ae.qaxis(fwd_roll_axis, (ROLL * p) * (1 if sw == 'r' else -1)))
            for s_ in 'lr':
                ft, fq = tgt_feet[s_][f]; ae.solve_leg(c, local, s_, f, ft, fq, ae.vadd(knees[s_][f], off))
        t_after = proj(c.comp('pelvis', toe, local)[0], [(c.comp('foot_' + st, toe, local)[0][i] + c.comp('ball_' + st, toe, local)[0][i]) / 2 for i in range(3)], [(c.comp('foot_' + sw, toe, local)[0][i] + c.comp('ball_' + sw, toe, local)[0][i]) / 2 for i in range(3)])
        ferr = max(ae.vlen(ae.vsub(c.comp('foot_' + s_, f, local)[0], c.comp('foot_' + s_, f)[0])) for s_ in 'lr' for f in range(nf))
        rec.update({'t_toe_after': round(t_after, 2), 'foot_err_cm': round(ferr, 2)})
        try:
            g = ae.leg_metrics(seq0, local); g0 = ae.leg_metrics(seq0, {k: list(v) for k, v in c.local.items()})
            rec['guard'] = {s_: [round(g[s_]['hinge_min'], 3), g[s_]['backward_frames'], g[s_]['twisted_frames'], round(g[s_]['axis_jump_deg'], 1), round(g0[s_]['axis_jump_deg'], 1)] for s_ in g}
        except Exception as e: rec['guard_err'] = str(e)[:120]
    if not DRY:
        dp = V + 'SHM252_' + n[4:] + '_APA'
        if not EAL.does_asset_exist(dp): assert EAL.duplicate_asset(sp, dp), dp
        seq = u.load_asset(dp)
        if D > 0.2: ae.write_tracks(seq, local, ['pelvis', 'thigh_l', 'calf_l', 'foot_l', 'thigh_r', 'calf_r', 'foot_r'], note='SHME V2.52 anticipatory weight transfer', guard=True)
        tn = [str(t) for t in L.get_animation_notify_track_names(seq)]
        for tr in tn:
            if tr.startswith('SHME_StartTransfer_Role') or tr.startswith('SHME_V252_APA'):
                L.remove_animation_notify_events_by_track(seq, tr); L.remove_animation_notify_track(seq, tr)
        for s in member[n]:
            tr = 'SHME_V252_APA_' + s; L.add_animation_notify_track(seq, tr)
            ev = L.add_animation_notify_state_event(seq, tr, 0.0, float(seq.get_play_length()) - 0.001, u.AnimNotifyState_PoseSearchBranchIn)
            ev.set_editor_property('database', dst_db[s])
        assert EAL.save_asset(dp, False), dp; rec['dst'] = dp
    out['clips'][n] = rec
if not DRY:
    for s in 'LR':
        dp = V + 'PSD_SHM252_StartTransferAPA_' + s; assert EAL.save_asset(dp, False); db = u.load_asset(dp)
        out['dbs'][s] = [db.get_animation_asset(i).get_name() for i in range(db.get_num_animation_assets())]
    for s in 'LR':
        db = src_db[s]; out['dbs']['src_' + s] = [db.get_animation_asset(i).get_name() for i in range(db.get_num_animation_assets())]
out['dirty'] = [q.get_name().split('/')[-1] for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('APA252 ' + json.dumps(out, default=str))
