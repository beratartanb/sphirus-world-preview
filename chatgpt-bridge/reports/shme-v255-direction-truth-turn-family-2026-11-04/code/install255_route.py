"""install255_route.py (editor job, write manifest = ABP base + child): V2.55 ONE turn route in front of every older family (knob SHM255_Ctl).
Why: a hard reversal below sprint class went through 5 families (JogRev F_B bins, LoadRev, SlowRev, BackLink, rear runs): back-running clips with a body-axis capsule (v255e60 fz_sprint_m 38.5 s).
SHM_Snapshot (after SetSHM255_Prev228): spd, ra = NormalizeAxis(yaw(input) - yaw(velocity)), align = |NormalizeAxis(yaw(velocity) - actor yaw)|;
  want = Ctl AND HasIntent AND Grounded AND spd >= SHM255_RouteMinV AND |ra| >= SHM255_RevMin AND align < 60 (moving along the body) AND NOT Own (no plan playing);
  right = (20 <= |ra| <= 150) ? ra > 0 : SupportSide > 0.5 (near 180 the support foot chooses the side; otherwise the requested side);
  SHM255_RouteDB := spd >= SHM255_SprintV ? (right ? DB_R : DB_L) : (right ? DB_JogR : DB_JogL); SHM255_RouteOn := want; SHM227_Thr := false while want (a forced switch is ignored under the search throttle).
Update_MotionMatching entry: Branch(SHM255_RouteOn) -> CurrentSelectedDatabase := RouteDB, SetDatabaseToSearch(RouteDB, InterruptOnDatabaseChange), nothing else this frame.
Exit: the V4 'ended' and the slow branch use curve SHM255_Phase > 1.5 AND Own < 0.3 (a blended Own at the entry is not an end); a plan that ended below CancelMinV leaves for the steady jog.
Idempotent (variable SHM255_RouteOn). builtins.V255_SAVE saves. Prints ROUTE255 {...}."""
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
assert 'SHM255_Ctl' in V, 'install255_abp first'
if 'SHM255_RouteOn' in V: out['patch'] = 'already'
else:
    PSD = u.PoseSearchDatabase.static_class()
    ensure_vars(bp, [('SHM255_RouteOn', 'bool', 'SHM'), ('SHM255_RouteDB', PSD, 'SHM'), ('SHM255_DB_JogR', PSD, 'SHM'), ('SHM255_DB_JogL', PSD, 'SHM'), ('SHM255_RevMin', 'float', 'SHM'), ('SHM255_RouteMinV', 'float', 'SHM'), ('SHM255_SprintV', 'float', 'SHM')]); compile_ok(bp)
    set_defaults(bp, {'SHM255_RevMin': 115.0, 'SHM255_RouteMinV': 190.0, 'SHM255_SprintV': 400.0}); compile_ok(bp)
    sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
    comp = [p for p in sn if 'GetComponentByClass' in tid(p) or 'GetComponentbyClass' in tid(p)]; assert comp; ct = (comp[0], 'ReturnValue')
    pv = [p for p in sn if tid(p).endswith('|SetSHM255_Prev228')]; assert len(pv) == 1, pv
    nx = succ(pv[0]); assert len(nx) == 1, nx; disconnect(nx[0])
    ctl = gs.within(gs.get('SHM255_Ctl'), 0.5, 1.0e9)
    pawn = gs.pure('/Script/Engine.AnimInstance:TryGetPawnOwner'); vel = gs.pure('/Script/Engine.Actor:GetVelocity', {'self': pawn})
    spd = gs.pure(M + 'VSize', {'A': vel}); yv = gs.yaw(gs.pure(M + 'Conv_VectorToRotator', {'InVec': vel}))
    ydv = gs.yaw(gs.pure(M + 'Conv_VectorToRotator', {'InVec': gs.get('DesiredVelocity', COMP, ct)}))
    ra = gs.pure(M + 'NormalizeAxis', {'Angle': gs.sub(ydv, yv)}); ara = gs.pure(M + 'Abs', {'A': ra})
    ay = gs.yaw(gs.pure('/Script/Engine.Actor:K2_GetActorRotation', {'self': pawn}))
    al = gs.pure(M + 'Abs', {'A': gs.pure(M + 'NormalizeAxis', {'Angle': gs.sub(yv, ay)})})
    own = gs.pure('/Script/Engine.AnimInstance:GetCurveValue', {'CurveName': 'SHM254_Own'})
    want = gs.AND(gs.AND(ctl, gs.get('HasIntent', COMP, ct)), gs.AND(gs.AND(gs.get('Grounded', COMP, ct), gs.within(spd, gs.get('SHM255_RouteMinV'), 1.0e9)),
                  gs.AND(gs.within(ara, gs.get('SHM255_RevMin'), 1.0e9), gs.AND(gs.within(al, -1.0, 60.0), gs.within(own, -1.0e9, 0.3)))))
    sideReq = gs.within(ara, 20.0, 150.0)
    right = gs.OR(gs.AND(sideReq, gs.within(ra, 0.0, 1.0e9)), gs.AND(gs.NOT(sideReq), gs.within(gs.get('SupportSide', COMP, ct), 0.5, 1.0e9)))
    bS, bJ = gs.branch(gs.within(spd, gs.get('SHM255_SprintV'), 1.0e9), (pv[0], 'then'))
    sR, sL = gs.branch(right, bS); jR, jL = gs.branch(right, bJ)
    tails = [gs.set('SHM255_RouteDB', gs.get('SHM255_DB_R'), sR), gs.set('SHM255_RouteDB', gs.get('SHM255_DB_L'), sL), gs.set('SHM255_RouteDB', gs.get('SHM255_DB_JogR'), jR), gs.set('SHM255_RouteDB', gs.get('SHM255_DB_JogL'), jL)]
    r1 = gs.set('SHM255_RouteOn', want, tails[0])
    for t_ in tails[1:]: connect(t_, (r1[0], 'execute'))
    r2 = gs.set('SHM227_Thr', gs.AND(gs.get('SHM227_Thr'), gs.NOT(gs.get('SHM255_RouteOn'))), r1)
    connect(r2, nx[0])
    # ---- Update_MotionMatching
    mg = pn(graph(bp, 'Update_MotionMatching')); g = G(mg); N = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(mg))}
    entry = N['K2Node_FunctionEntry_0']; first = succ(entry); assert len(first) == 1 and 'IfThenElse' in first[0][0], first
    slow = first[0][0]; v4 = [x for x in succ(slow, 'else')]; assert len(v4) == 1 and 'IfThenElse' in v4[0][0], v4; v4 = v4[0][0]
    ref = [p for p in N.values() if 'SetDatabaseToSearch' in tid(p) and src((p, 'MotionMatchingNode'))][0]; mm = src((ref, 'MotionMatchingNode'))[0]
    ph = g.within(g.pure('/Script/Engine.AnimInstance:GetCurveValue', {'CurveName': 'SHM255_Phase'}), 1.5, 1.0e9)
    # V4 'ended': the OR's second input gets the phase gate
    c = src((v4, 'Condition')); assert len(c) == 1 and 'BooleanOR' in tid(c[0][0]) or 'OR' in tid(c[0][0]).upper(), c
    orn = c[0][0]; e0 = src((orn, 'B')); assert len(e0) == 1, e0
    disconnect((orn, 'B')); connect(g.AND(e0[0], ph), (orn, 'B'))
    # slow branch: also a plan that ended below CancelMinV
    c2 = src((slow, 'Condition')); assert len(c2) == 1, c2
    dbn = g.pure('/Script/Engine.KismetSystemLibrary:GetObjectName', {'Object': g.get('CurrentSelectedDatabase')})
    mine = g.pure('/Script/Engine.KismetStringLibrary:Contains', {'SearchIn': dbn, 'Substring': 'SHM254', 'bUseCase': False, 'bSearchFromEnd': False})
    ctl2 = g.within(g.get('SHM255_Ctl'), 0.5, 1.0e9); fast = g.within(g.get('SHM28_Speed'), g.get('SHM254_CancelMinV'), 1.0e9)
    own2 = g.pure('/Script/Engine.AnimInstance:GetCurveValue', {'CurveName': 'SHM254_Own'})
    endl = g.AND(g.AND(ctl2, mine), g.AND(g.NOT(fast), g.AND(ph, g.within(own2, -1.0e9, 0.3))))
    disconnect((slow, 'Condition')); connect(g.OR(c2[0], endl), (slow, 'Condition'))
    # route first
    disconnect((slow, 'execute'))
    bt, bf = g.branch(g.get('SHM255_RouteOn'), (entry, 'then')); connect(bf, (slow, 'execute'))
    sc = g.set('CurrentSelectedDatabase', g.get('SHM255_RouteDB'), bt)
    s = g.fn('/Script/PoseSearch.MotionMatchingAnimNodeLibrary:SetDatabaseToSearch'); connect(sc, (s, 'execute')); connect(mm, (s, 'MotionMatchingNode'))
    connect(g.get('SHM255_RouteDB'), (s, 'Database')); arg(s, 'InterruptMode', 'InterruptOnDatabaseChange')
    out['wired'] = {'slow': slow.rsplit('.', 1)[-1], 'v4': v4.rsplit('.', 1)[-1]}
st_, errs = compile_ok(bp); out['abp'] = [str(st_), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class()); out['knob'] = str(cdo.get_editor_property('SHM255_Ctl'))
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child'] and out['knob'] == '0.0'
if out['ok'] and getattr(builtins, 'V255_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()]
print('ROUTE255 ' + json.dumps(out, default=str))
