"""probe250_footaxes.py (measure job, read-only): foot bone orientation (component-space axes) and its LOCAL rotation relative to the calf
for the idle sample, the SHM248 turn crops, the CoreMotionAAMS/Candidate source of the turn starts, the restored JogQ 045 copies and a
normal start (A_CP2_Jog_Fwd_Start). Decomposes the local difference to the idle foot into swing (moves the ankle->ball line) and twist
(roll about the ankle->ball line). Prints FOOTAX250 {...}."""
import unreal as u, json, math, sys, importlib
sys.path.insert(0, r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925')
import v137_animedit as ae; importlib.reload(ae)
ar = u.AssetRegistryHelpers.get_asset_registry()
assets = {}
for a in ar.get_assets_by_class(u.TopLevelAssetPath('/Script/Engine', 'AnimSequence'), True):
    assets.setdefault(str(a.asset_name), []).append(str(a.package_name))
def pose(seq, t):
    o = u.AnimPoseEvaluationOptions(); o.set_editor_property('evaluation_type', u.AnimDataEvalType.RAW)
    return u.AnimPoseExtensions.get_anim_pose_at_time(seq, t, o)
def q_of(p, b, sp):
    tr = u.AnimPoseExtensions.get_bone_pose(p, b, sp); return ae.qnorm(ae.from_ue_q(tr.rotation)), ae.from_ue_v(tr.translation)
def swing_twist(q, axis):
    v = (q[0], q[1], q[2]); pr = ae.vsc(axis, ae.vdot(v, axis)); tw = ae.qnorm((pr[0], pr[1], pr[2], q[3]))
    sw = ae.qnorm(ae.qmul(q, ae.qinv(tw))); a = lambda x: round(math.degrees(2 * math.acos(min(1.0, abs(x[3])))), 1)
    return a(sw), a(tw)
def describe(seq, t, ref=None):
    p = pose(seq, t); r = {}
    for s in 'lr':
        qf, tf = q_of(p, 'foot_' + s, u.AnimPoseSpaces.WORLD); qb, tb = q_of(p, 'ball_' + s, u.AnimPoseSpaces.WORLD)
        ql, _ = q_of(p, 'foot_' + s, u.AnimPoseSpaces.LOCAL)
        ax = {k: [round(x, 2) for x in ae.qrot(qf, v)] for k, v in (('x', (1, 0, 0)), ('y', (0, 1, 0)), ('z', (0, 0, 1)))}
        try:
            ax['skel'] = seq.get_editor_property('skeleton').get_name()
            pz = u.AnimPoseExtensions.get_bone_pose(p, 'pelvis', u.AnimPoseSpaces.WORLD); ax['pelvis_fwd'] = [round(x, 2) for x in ae.qrot(ae.qnorm(ae.from_ue_q(pz.rotation)), (0, 1, 0))]
            ax['heading_ab'] = round(math.degrees(math.atan2(tb[1] - tf[1], tb[0] - tf[0])), 1); ax['pitch'] = round(math.degrees(math.atan2(tf[2] - tb[2], math.hypot(tb[0] - tf[0], tb[1] - tf[1]))), 1)
        except Exception as e: ax['skel'] = 'err ' + str(e)[:60]
        d = ae.vnorm(ae.vsub(tb, tf)); rr = {'ax': ax, 'ankle_ball': [round(x, 2) for x in d], 'ball_z': round(tb[2], 1)}
        if ref:
            qr = ref[s]['ql']; dq = ae.qnorm(ae.qmul(ae.qinv(qr), ql))   # local delta in the reference foot frame
            dloc = ae.qrot(ae.qinv(ref[s]['qf']), ref[s]['d'])            # ankle->ball axis expressed in the reference foot frame
            rr['local_delta_deg'] = round(math.degrees(2 * math.acos(min(1.0, abs(dq[3])))), 1); rr['swing_twist'] = swing_twist(dq, ae.vnorm(dloc))
        rr['ql'] = ql; rr['qf'] = qf; rr['d'] = d; r[s] = rr
    return r
idle = u.load_asset(assets['af_Stand_Idle_NaturalBaseline_Phase275'][0]); ref = describe(idle, 79.40)
out = {'idle': {s: {k: v for k, v in ref[s].items() if k in ('ax', 'ankle_ball', 'ball_z')} for s in 'lr'}, 'clips': {}}
want = ['af_Loco_Jog_Start_TurnL135_Lfoot', 'af_Loco_Jog_Start_TurnR180_Rfoot', 'af_Loco_Jog_Start_TurnL135_Lfoot_AAMS', 'af_Loco_Jog_Bwd_Start', 'af_Loco_Jog_Bwd_Start_AAMS']
for n in want:
    for pth in assets.get(n, []):
        try:
            r = describe(u.load_asset(pth), 0.0, ref)
            out['clips'][pth] = {s: {k: v for k, v in r[s].items() if k in ('ax', 'ankle_ball', 'ball_z', 'local_delta_deg', 'swing_twist')} for s in 'lr'}
        except Exception as e: out['clips'][pth] = 'err ' + str(e)[:120]
print('FOOTAX250 ' + json.dumps(out))
