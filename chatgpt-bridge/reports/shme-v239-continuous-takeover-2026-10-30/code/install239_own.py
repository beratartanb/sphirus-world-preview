"""install239_own.py (editor job) - V2.39 PLAN OWNER + TAKEOVER (behind the knob SHM239_Own; 0 = production unchanged).
Why (v238fin4_j38_cc90 30 FPS, v238i60_j38_c90l 60 FPS - the same mechanism): while an authored plan plays, every change of the
component episode CLASS (1 -> 0 with a new input at 6.17 s in cc90; 1 -> 0 with NO input change at 6.05 s in the 60 FPS left cut) restarts
the ABP episode (SHM_RedirectFrames -> 1) and the first-frame bridge route of Update_MotionMatching picks the class route (class 0 ->
PSD_CT_JogSteady; class 2 -> V2.16 RevTurn PSD_SHM215_Rev_*) - the plan is dropped mid-brake, the V2.38 yaw contract keeps turning toward
the old target through the blend, then the actor yaw snaps (70 -> 16 deg in 0.2 s). The episode class is the wrong owner of a running plan.
Owner split:
  player intent            component DesiredVelocity (live, every frame)
  active physical plan     the playing clip's own curves: SHM238_W (plan running), SHM239_Tgt (takeover target + 1000; 0 = source cut,
                           target 90), SHM239_Step (planned touchdown clock)
  database while a plan runs  this owner (Update_MotionMatching entry branch): the plan's CurrentSelectedDatabase, DoNotInterrupt - a
                           component class re-latch can no longer re-route it
  continue vs take over    SHM239_TkReq: the intent differs from the plan target by > SHM239_TkThr (35, plan units = deg); kept while
                           > SHM239_TkKeep (20); dropped when the intent returns, on release, or when the plan ends
  take-over moment         SHM239_TkGo = TkReq AND the plan's touchdown clock steps (the next REAL planned touchdown: momentum changes
                           only through a contact; the swing in the air is committed) -> database PSD_SHM239_Tk_Back (target 0 = the old
                           travel) or _Opp (target -90 = the opposite side), ForceInterruptAndInvalidateContinuingPose; MM enters the
                           takeover clip whose frame 0 is this cut at this touchdown (pose + trajectory)
  release (no input)       the owner yields (normal stop routing), as before V2.39
SHM_Snapshot vars (after SetSHM238_PrevOn): SHM239_W, Step, PrevStep, TgtC, PT, Rel, OwnOn, HasIn, TkReq, TkTgt, TkGo.
Idempotent. builtins.V239_SAVE saves. Prints OWN239 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, arg
import builtins, json
LS = u.EditorLoadingAndSavingUtils; M = '/Script/Engine.KismetMathLibrary:'
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CPA = AP.replace('Base', '')
COMP = '/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent.BP_SHM_HumanMotionComponent_C'
V9 = '/Game/GraceRanger/SHME/Animations/V239'
DAS = {'/Game/GraceRanger/Profiles/DA_GR_LocomotionBehavior', '/Game/GraceRanger/SHME/DA_SHM_Response_Default', '/Game/GraceRanger/Experimental/BodyInertia/DA_PBI_Prototype'}
dirty = list(LS.get_dirty_content_packages()); names = [p.get_name() for p in dirty]
assert all(n in DAS or n in (AP, CPA) for n in names), ('unexpected dirty', names)
if dirty: LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
out = {'reloaded': names}
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
bp = u.load_asset(AP)
DBC = u.PoseSearchDatabase.static_class()
ensure_vars(bp, [('SHM239_Own', 'float', 'SHM239'), ('SHM239_TkThr', 'float', 'SHM239'), ('SHM239_TkKeep', 'float', 'SHM239'),
                 ('SHM239_W', 'float', 'SHM239'), ('SHM239_Step', 'float', 'SHM239'), ('SHM239_PrevStep', 'float', 'SHM239'),
                 ('SHM239_TgtC', 'float', 'SHM239'), ('SHM239_PT', 'float', 'SHM239'), ('SHM239_Rel', 'float', 'SHM239'),
                 ('SHM239_TkTgt', 'float', 'SHM239'), ('SHM239_OwnOn', 'bool', 'SHM239'), ('SHM239_HasIn', 'bool', 'SHM239'),
                 ('SHM239_TkReq', 'bool', 'SHM239'), ('SHM239_TkGo', 'bool', 'SHM239'),
                 ('SHM239_DB_Back', DBC, 'SHM239'), ('SHM239_DB_Opp', DBC, 'SHM239')]); compile_ok(bp)
dfl = {'SHM239_TkThr': 35.0, 'SHM239_TkKeep': 20.0}
cdo = u.get_default_object(bp.generated_class())
need = {k: v for k, v in dfl.items() if abs(float(cdo.get_editor_property(k))) < 1e-6}
for k, nm in (('SHM239_DB_Back', 'PSD_SHM239_Tk_Back'), ('SHM239_DB_Opp', 'PSD_SHM239_Tk_Opp')):
    if cdo.get_editor_property(k) is None: d = u.load_asset(V9 + '/' + nm); assert d, nm; need[k] = d
if need: set_defaults(bp, need); compile_ok(bp)
# ---- 1. SHM_Snapshot: intent vs plan, takeover request / moment
sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
if any(tid(p).endswith('SetSHM239_TkGo') for p in sn): out['snapshot'] = 'already'
else:
    last = [p for p in sn if tid(p).endswith('SetSHM238_PrevOn')]; assert len(last) == 1, [tid(p) for p in sn if 'PrevOn' in tid(p)]
    comp = [p for p in sn if 'GetComponentByClass' in tid(p) or 'GetComponentbyClass' in tid(p)]; assert comp; ct = (comp[0], 'ReturnValue')
    nxt = [p for p in sn if any(q.name == 'execute' for q in info(p).input_pins) and (last[0], 'then') in src((p, 'execute'))]
    for x in nxt: disconnect((x, 'execute'))
    cv = lambda nm: gs.pure('/Script/Engine.AnimInstance:GetCurveValue', {'CurveName': nm})
    t = gs.set('SHM239_W', cv('SHM238_W'), (last[0], 'then'))
    t = gs.set('SHM239_Step', cv('SHM239_Step'), t)
    t = gs.set('SHM239_TgtC', cv('SHM239_Tgt'), t)
    tk = gs.within(gs.get('SHM239_TgtC'), 500.0, 1.0e9)
    t = gs.set('SHM239_PT', gs.select(tk, gs.sub(gs.get('SHM239_TgtC'), 1000.0), 90.0), t)
    dvv = gs.fn('BreakVector', {'InVec': gs.get('DesiredVelocity', COMP, ct)})
    desYaw = gs.pure(M + 'DegAtan2', {'Y': (dvv, 'Y'), 'X': (dvv, 'X')})
    na = gs.pure(M + 'NormalizeAxis', {'Angle': gs.sub(desYaw, gs.get('SHM238_Yaw0'))})
    t = gs.set('SHM239_Rel', gs.pure(M + 'SafeDivide', {'A': gs.mul(na, 90.0), 'B': gs.get('SHM238_Delta')}), t)
    t = gs.set('SHM239_OwnOn', gs.AND(gs.within(gs.get('SHM239_Own'), 0.5, 1.0e9), gs.within(gs.get('SHM239_W'), 0.3, 1.0e9)), t)
    t = gs.set('SHM239_HasIn', gs.within(gs.pure(M + 'VSize', {'A': gs.get('DesiredVelocity', COMP, ct)}), 30.0, 1.0e9), t)
    diff = gs.pure(M + 'Abs', {'A': gs.sub(gs.get('SHM239_Rel'), gs.get('SHM239_PT'))})
    rel = gs.get('SHM239_Rel')
    cand = gs.select(gs.within(rel, -1.0e9, -45.0), -90.0, gs.select(gs.within(rel, -45.0, 45.0), 0.0, 999.0))
    live = gs.AND(gs.get('SHM239_OwnOn'), gs.get('SHM239_HasIn'))
    newreq = gs.AND(gs.AND(live, gs.within(diff, gs.get('SHM239_TkThr'), 1.0e9)), gs.AND(gs.within(gs.get('SHM239_TgtC'), -1.0e9, 500.0), gs.within(cand, -1000.0, 500.0)))
    keep = gs.AND(gs.AND(gs.get('SHM239_TkReq'), live), gs.within(diff, gs.get('SHM239_TkKeep'), 1.0e9))
    t = gs.set('SHM239_TkTgt', gs.select(gs.AND(newreq, gs.NOT(gs.get('SHM239_TkReq'))), cand, gs.get('SHM239_TkTgt')), t)
    req = gs.OR(newreq, keep)
    stepup = gs.within(gs.sub(gs.get('SHM239_Step'), gs.get('SHM239_PrevStep')), 0.5, 1.0e9)
    t = gs.set('SHM239_TkGo', gs.AND(req, stepup), t)
    t = gs.set('SHM239_TkReq', gs.AND(gs.OR(gs.AND(gs.AND(live, gs.within(diff, gs.get('SHM239_TkThr'), 1.0e9)), gs.AND(gs.within(gs.get('SHM239_TgtC'), -1.0e9, 500.0), gs.within(cand, -1000.0, 500.0))),
                                                gs.AND(gs.AND(gs.get('SHM239_TkReq'), live), gs.within(diff, gs.get('SHM239_TkKeep'), 1.0e9))), gs.NOT(gs.get('SHM239_TkGo'))), t)
    t = gs.set('SHM239_PrevStep', gs.get('SHM239_Step'), t)
    for x in nxt: connect(t, (x, 'execute'))
    out['snapshot'] = {'after': last[0].rsplit('.', 1)[-1], 'next': [x.rsplit('.', 1)[-1] for x in nxt]}
# ---- 2. Update_MotionMatching entry: the plan owns the database while it runs
gp = pn(graph(bp, 'Update_MotionMatching')); g = G(gp); nodes = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(gp))}
entry = nodes['K2Node_FunctionEntry_0']
if any(tid(p).endswith('GetSHM239_TkGo') for p in nodes.values()): out['umm'] = 'already'
else:
    firsts = [p for p in nodes.values() if any(q.name == 'execute' for q in info(p).input_pins) and (entry, 'then') in src((p, 'execute'))]
    assert len(firsts) == 1, firsts
    sdb = [p for p in nodes.values() if 'SetDatabaseToSearch' in tid(p)]; mm = src((sdb[0], 'MotionMatchingNode')); assert mm, 'mm node source'; mm = mm[0]
    disconnect((firsts[0], 'execute'))
    own_t, own_e = g.branch(g.AND(g.get('SHM239_OwnOn'), g.get('SHM239_HasIn')), (entry, 'then'))
    connect(own_e, (firsts[0], 'execute'))
    go_t, go_e = g.branch(g.get('SHM239_TkGo'), own_t)
    op_t, op_e = g.branch(g.within(g.get('SHM239_TkTgt'), -1.0e9, -45.0), go_t)
    for tt, var in ((op_t, 'SHM239_DB_Opp'), (op_e, 'SHM239_DB_Back')):
        sc = g.set('CurrentSelectedDatabase', g.get(var), tt)
        s1 = g.fn('/Script/PoseSearch.MotionMatchingAnimNodeLibrary:SetDatabaseToSearch'); connect(sc, (s1, 'execute')); connect(mm, (s1, 'MotionMatchingNode'))
        connect(g.get(var), (s1, 'Database')); arg(s1, 'InterruptMode', 'ForceInterruptAndInvalidateContinuingPose')
    s2 = g.fn('/Script/PoseSearch.MotionMatchingAnimNodeLibrary:SetDatabaseToSearch'); connect(go_e, (s2, 'execute')); connect(mm, (s2, 'MotionMatchingNode'))
    connect(g.get('CurrentSelectedDatabase'), (s2, 'Database')); arg(s2, 'InterruptMode', 'DoNotInterrupt')
    out['umm'] = {'first': firsts[0].rsplit('.', 1)[-1], 'mm': mm[0].rsplit('.', 1)[-1]}
st, errs = compile_ok(bp); out['abp'] = [str(st), errs[:6]]
cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class())
out['knobs'] = {k: (cdo.get_editor_property(k).get_name() if hasattr(cdo.get_editor_property(k), 'get_name') else float(cdo.get_editor_property(k)))
                for k in ('SHM239_Own', 'SHM239_TkThr', 'SHM239_TkKeep', 'SHM239_DB_Back', 'SHM239_DB_Opp')}
ok = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child'] and out['knobs']['SHM239_Own'] == 0.0
out['ok'] = ok
if ok and getattr(builtins, 'V239_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('OWN239 ' + json.dumps(out, default=str))
