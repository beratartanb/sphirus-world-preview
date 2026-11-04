"""install255_v5.py (editor job, write manifest = ABP base + child): V2.55 plan state instead of blended curves + no free speed in any phase (knob SHM255_Ctl).
Measured (v255j60 fz_sprint_m 31.2 s, frame by frame): a NEW entry blends over the old clip's tail, so the blended curves read Own 0.14 / Phase 1.8 on the first frames of the new clip: the 'ended' test fired and threw the
body out of the clip it had just entered (head pop 280), and after that cancel the V2.28 contract re-armed and took the capsule 136 -> 249 cm/s in ONE frame.
(1) STATE. SHM_Snapshot: fire = InPlan AND Own < 0.3 AND Phase > 1.5; InPlan := Own > 0.7 OR (InPlan AND NOT fire AND Own > 0.02); Ended := (Ended OR fire) AND NOT RouteOn AND the selected database is a plan database.
    A blend-in never sets InPlan (Own has to pass 0.7 first), so it cannot end anything. Update_MotionMatching reads SHM255_Ended instead of the curves.
(2) SPEED. While a plan is in the pose (Own or W > 0.02) and the commanded speed is forward: ClipSpeed := FClamp(ClipSpeed, speed - BrakeRate dt, speed + SHM255_AccRate dt).
Spliced after the install255_v4 SetClipSpeed and in the V4 / slow branch conditions. Idempotent (variable SHM255_InPlan). builtins.V255_SAVE saves. Prints V5255 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, arg
import builtins, json
LS = u.EditorLoadingAndSavingUtils; M = '/Script/Engine.KismetMathLibrary:'
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CPA = AP.replace('Base', '')
COMP = '/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent.BP_SHM_HumanMotionComponent_C'
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
def succ(p, pin='then'):
    return [(pn(q.node), [x.name for x in info(pn(q.node)).input_pins if x.pin_id.index_id == q.index_id][0]) for o in info(p).output_pins if str(o.name) == pin for q in o.connected_pins]
out = {}
dirty = [p for p in LS.get_dirty_content_packages() if 'ABP_GR_MotionMatching' in p.get_name()]
if dirty:
    out['reloaded'] = [p.get_name().split('/')[-1] for p in dirty]; LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
bp = u.load_asset(AP); V = [str(v) for v in B.list_variables(bp)]
assert 'SHM255_BrakeRate' in V, 'install255_v4 first'
if 'SHM255_InPlan' in V: out['patch'] = 'already'
else:
    ensure_vars(bp, [('SHM255_InPlan', 'bool', 'SHM'), ('SHM255_Ended', 'bool', 'SHM'), ('SHM255_AccRate', 'float', 'SHM')]); compile_ok(bp); set_defaults(bp, {'SHM255_AccRate': 800.0}); compile_ok(bp)
    sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
    comp = [p for p in sn if 'GetComponentByClass' in tid(p) or 'GetComponentbyClass' in tid(p)]; assert comp; ct = (comp[0], 'ReturnValue')
    def curve(n): return gs.pure('/Script/Engine.AnimInstance:GetCurveValue', {'CurveName': n})
    ctl = gs.within(gs.get('SHM255_Ctl'), 0.5, 1.0e9)
    # the last ClipSpeed setter of install255_v4: its predecessor is the install255_v3 setter fed by SetSHM255_NoGain
    ng = [p for p in sn if tid(p).endswith('|SetSHM255_NoGain')]; assert len(ng) == 1, ng
    c3 = [x[0] for x in succ(ng[0]) if tid(x[0]).endswith('|SetClipSpeed')]; assert len(c3) == 1; c4 = [x[0] for x in succ(c3[0]) if tid(x[0]).endswith('|SetClipSpeed')]; assert len(c4) == 1, succ(c3[0]); c4 = c4[0]
    nx = succ(c4); assert len(nx) == 1 and len(src(nx[0])) == 1, nx; disconnect(nx[0])
    spd = gs.pure(M + 'VSize', {'A': gs.pure('/Script/Engine.Actor:GetVelocity', {'self': gs.pure('/Script/Engine.AnimInstance:TryGetPawnOwner')})})
    dt = gs.pure('/Script/Engine.GameplayStatics:GetWorldDeltaSeconds')
    lo = gs.sub(spd, gs.mul(gs.get('SHM255_BrakeRate'), dt)); hi = gs.math(spd, gs.mul(gs.get('SHM255_AccRate'), dt))
    cur = gs.get('ClipSpeed', COMP, ct)
    plan = gs.AND(ctl, gs.AND(gs.OR(gs.within(curve('SHM254_Own'), 0.02, 1.0e9), gs.within(curve('SHM254_W'), 0.02, 1.0e9)), gs.within(cur, 0.0, 1.0e9)))
    t = gs.set('ClipSpeed', gs.select(plan, gs.pure(M + 'FClamp', {'Value': cur, 'Min': lo, 'Max': hi}), cur), (c4, 'then'), COMP, ct)
    own = curve('SHM254_Own'); ph = curve('SHM255_Phase')
    fire = gs.AND(gs.get('SHM255_InPlan'), gs.AND(gs.within(own, -1.0e9, 0.3), gs.within(ph, 1.5, 1.0e9)))
    t1 = gs.set('SHM255_InPlan', gs.OR(gs.within(own, 0.7, 1.0e9), gs.AND(gs.AND(gs.get('SHM255_InPlan'), gs.NOT(fire)), gs.within(own, 0.02, 1.0e9))), t)
    dbn = gs.pure('/Script/Engine.KismetSystemLibrary:GetObjectName', {'Object': gs.get('CurrentSelectedDatabase')})
    mine = gs.pure('/Script/Engine.KismetStringLibrary:Contains', {'SearchIn': dbn, 'Substring': 'SHM254', 'bUseCase': False, 'bSearchFromEnd': False})
    # fire is evaluated from the state before t1 through a stored copy: Ended latches on Own falling while the previous InPlan was true
    fire2 = gs.AND(gs.within(own, -1.0e9, 0.3), gs.within(ph, 1.5, 1.0e9))
    t2 = gs.set('SHM255_Ended', gs.AND(gs.AND(gs.OR(gs.get('SHM255_Ended'), gs.AND(fire2, gs.NOT(gs.get('SHM255_InPlan')))), gs.NOT(gs.get('SHM255_RouteOn'))), mine), t1)
    connect(t2, nx[0])
    # ---- Update_MotionMatching
    mg = pn(graph(bp, 'Update_MotionMatching')); g = G(mg); N = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(mg))}
    entry = N['K2Node_FunctionEntry_0']; first = succ(entry); assert len(first) == 1 and 'IfThenElse' in first[0][0], first
    route = first[0][0]; slow = succ(route, 'else'); assert len(slow) == 1 and 'IfThenElse' in slow[0][0], slow; slow = slow[0][0]
    v4 = succ(slow, 'else'); assert len(v4) == 1 and 'IfThenElse' in v4[0][0], v4; v4 = v4[0][0]
    fast = g.within(g.get('SHM28_Speed'), g.get('SHM254_CancelMinV'), 1.0e9); ctl2 = g.within(g.get('SHM255_Ctl'), 0.5, 1.0e9)
    c = src((v4, 'Condition')); assert len(c) == 1, c; orn = c[0][0]; disconnect((orn, 'B')); connect(g.AND(g.AND(ctl2, g.get('SHM255_Ended')), fast), (orn, 'B'))
    c2 = src((slow, 'Condition')); assert len(c2) == 1, c2; or2 = c2[0][0]; disconnect((or2, 'B')); connect(g.AND(g.AND(ctl2, g.get('SHM255_Ended')), g.NOT(fast)), (or2, 'B'))
    out['wired'] = {'speed_after': c4.rsplit('.', 1)[-1], 'v4': v4.rsplit('.', 1)[-1], 'slow': slow.rsplit('.', 1)[-1]}
st_, errs = compile_ok(bp); out['abp'] = [str(st_), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class()); out['knob'] = str(cdo.get_editor_property('SHM255_Ctl'))
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child'] and out['knob'] == '0.0'
if out['ok'] and getattr(builtins, 'V255_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()]
print('V5255 ' + json.dumps(out, default=str))
