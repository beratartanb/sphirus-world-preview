"""gen253_apa.py (dry = measure job; write = manifest of the NEW assets only): V2.53 APA v3 = the V2.52 anticipatory weight transfer
(gen252_apa.py v2, blend-compensated) re-shaped so it cannot produce artificial motion at any entry phase.
Measured (stance253.py, v252f60 wstart / taps, same session V2.51 content vs V2.52 APA): the transfer itself is right (pelvis toward the
stance foot before swing toe-off, feet exact), but the visible lateral pelvis acceleration rose from 4-22 to 13-27 m/s2 in the short
toe-off starts (BL 0.13-0.20 s, RL, LL): smoothstep rise (acceleration step at both ends) x shift / w(toe) (up to 8 cm in the clip) x the
rising blend weight.
v3: (1) minimum-jerk quintic rise 0 -> toe-off and quintic fade (no acceleration steps), (2) the shift is capped so that the VISIBLE
pelvis (blend weight w(t) x shift x p(t), HermiteCubic BLEND from the clip start, evaluated numerically with its 2nd derivative) never
exceeds A_VIS m/s2 lateral acceleration, (3) target / roll / feet / database handling as V2.52. Sources = the original SHM_StartTransfer_*
clips (not the V2.52 copies). Output /Game/GraceRanger/SHME/Animations/V253/SHM253_StartTransfer_<dir>_<foot>_APA3 + PSD_SHM253_StartTransferAPA_L/_R
(BranchIn SHME_V253_APA_<side>). builtins.V253_APA = {'dry': bool, 'tgt': 0.37, 'maxd': 8.0, 'fade': 0.35, 'roll': 2.0, 'blend': 0.5, 'avis': 3.0}.
Prints APA253 {...}."""
import unreal as u, json, builtins, math, sys, importlib
sys.path.insert(0, r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925')
import v137_animedit as ae; importlib.reload(ae)
L = u.AnimationLibrary; EAL = u.EditorAssetLibrary
cfg = dict(getattr(builtins, 'V253_APA', {})); DRY = bool(cfg.get('dry', True)); TGT = float(cfg.get('tgt', 0.37)); MAXD = float(cfg.get('maxd', 8.0)); AVIS = float(cfg.get('avis', 3.0))
FADE = float(cfg.get('fade', 0.35)); ROLL = float(cfg.get('roll', 2.0)); BLEND = float(cfg.get('blend', 0.5))
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
F = '/Game/GraceRanger/SHME/Animations/StartTransfer/'; V = '/Game/GraceRanger/SHME/Animations/V253/'
out = {'dry': DRY, 'cfg': {'tgt': TGT, 'maxd': MAXD, 'fade': FADE, 'roll': ROLL, 'avis': AVIS}, 'clips': {}, 'dbs': {}}
def smooth(x): x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)
def mj(x): x = max(0.0, min(1.0, x)); return x * x * x * (10 - 15 * x + 6 * x * x)
def prof(t, toe_t):
    return mj(t / max(toe_t, 1e-3)) if t <= toe_t else 1.0 - mj((t - toe_t) / max(FADE, 1e-3))
def vis_acc_per_cm(toe_t):
    # visible lateral offset per cm of clip shift = w(t) * p(t) (HermiteCubic blend from the clip start); max |2nd derivative| [cm/s2 per cm]
    h = 1.0 / 240.0; n = int((toe_t + FADE + 0.05) / h) + 2
    v = [(smooth((k * h) / BLEND) if BLEND > 0 else 1.0) * prof(k * h, toe_t) for k in range(n)]
    return max(abs(v[k + 1] - 2 * v[k] + v[k - 1]) / (h * h) for k in range(1, n - 1))
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
        dp = V + 'PSD_SHM253_StartTransferAPA_' + s
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
    D_need = max(0.0, (t_vis - TGT) * width / max(w, 0.15)); apc = vis_acc_per_cm(toe * dt); D_acc = AVIS * 100.0 / max(apc, 1e-6)
    D = min(MAXD, D_need, D_acc)
    rec = {'d_need': round(D_need, 2), 'd_acc_cap': round(D_acc, 2), 'vis_acc_ms2': round(D * apc / 100.0, 2),'swing': sw, 'toe_off': round(toe * dt, 3), 'width': round(width, 1), 't_toe_src': round(t_toe, 2), 'blend_w_toe': round(w, 2), 't_vis_src': round(t_vis, 2), 't_vis_after': round(t_vis - w * D / width, 2), 'shift_cm': round(D, 2), 'dbs': member[n]}
    local = {k: list(v) for k, v in c.local.items()}
    if D > 0.2:
        tgt_feet = {s_: [c.comp('foot_' + s_, f) for f in range(nf)] for s_ in 'lr'}
        knees = {s_: [c.comp('calf_' + s_, f)[0] for f in range(nf)] for s_ in 'lr'}
        Tf = FADE / max(dt, 1e-6); fwd_roll_axis = ae.vnorm(ae.vcross((0.0, 0.0, 1.0), axis))
        for f in range(nf):
            p = prof(f * dt, toe * dt)
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
        dp = V + 'SHM253_' + n[4:] + '_APA3'
        if not EAL.does_asset_exist(dp): assert EAL.duplicate_asset(sp, dp), dp
        seq = u.load_asset(dp)
        if D > 0.2: ae.write_tracks(seq, local, ['pelvis', 'thigh_l', 'calf_l', 'foot_l', 'thigh_r', 'calf_r', 'foot_r'], note='SHME V2.53 anticipatory weight transfer v3', guard=True)
        tn = [str(t) for t in L.get_animation_notify_track_names(seq)]
        for tr in tn:
            if tr.startswith('SHME_StartTransfer_Role') or tr.startswith('SHME_V252_APA') or tr.startswith('SHME_V253_APA'):
                L.remove_animation_notify_events_by_track(seq, tr); L.remove_animation_notify_track(seq, tr)
        for s in member[n]:
            tr = 'SHME_V253_APA_' + s; L.add_animation_notify_track(seq, tr)
            ev = L.add_animation_notify_state_event(seq, tr, 0.0, float(seq.get_play_length()) - 0.001, u.AnimNotifyState_PoseSearchBranchIn)
            ev.set_editor_property('database', dst_db[s])
        assert EAL.save_asset(dp, False), dp; rec['dst'] = dp
    out['clips'][n] = rec
if not DRY:
    for s in 'LR':
        dp = V + 'PSD_SHM253_StartTransferAPA_' + s; assert EAL.save_asset(dp, False); db = u.load_asset(dp)
        out['dbs'][s] = [db.get_animation_asset(i).get_name() for i in range(db.get_num_animation_assets())]
    for s in 'LR':
        db = src_db[s]; out['dbs']['src_' + s] = [db.get_animation_asset(i).get_name() for i in range(db.get_num_animation_assets())]
out['dirty'] = [q.get_name().split('/')[-1] for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('APA253 ' + json.dumps(out, default=str))
