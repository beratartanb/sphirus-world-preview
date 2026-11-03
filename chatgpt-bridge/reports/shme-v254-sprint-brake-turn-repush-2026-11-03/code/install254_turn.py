"""install254_turn.py (editor job, write manifest = ABP base + child): V2.54 runtime for the planned turn-around clips (gen254_rev.py).
Knob SHM254_Turn (default 0 = production unchanged).
(A) SIGN: the V2.38 yaw contract latches Delta = NormalizeAxis(yaw(DesiredVelocity) - actor yaw) on its rising edge and commands
    Yaw0 + Delta x Turn / 90. For an opposite request Delta is +-180 by noise, so the capsule could turn the other way than the clip's body.
    After SetSHM238_Delta: Delta := (SHM254_Turn > 0.5 AND |curve SHM254_Side| > 0.3 AND |Delta| > 120) ? sign(SHM254_Side) x |Delta| : Delta.
(B) BODY FRAME HAND-OVER: an opposite request is 'backward' in the V2.34 body frame (component LocoYaw = the old travel); when the turn
    is done the facing writer and the backward intent would turn the body back and back-run. On the falling edge of curve SHM254_W
    (the clip's turn finished) the explored body frame is the body (the V2.48 rule): component LocoExplore := true, LocoState := 1,
    LocoOn := true, LocoYaw := actor yaw; the component's exploration then keeps the frame on the held input direction.
Inserted in ABP_GR_MotionMatchingBase.SHM_Snapshot: (A) after SetSHM238_Delta, (B) after SetSHM238_PrevOn. Idempotent (SHM254_Turn).
builtins.V254_SAVE saves. Prints TURN254 {...}."""
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
assert 'SHM238_Delta' in V and 'SHM238_PrevOn' in V, 'V2.38 yaw contract missing'
if 'SHM254_Turn' in V: out['patch'] = 'already'
else:
    ensure_vars(bp, [('SHM254_Turn', 'float', 'SHM'), ('SHM254_PrevW', 'float', 'SHM')]); compile_ok(bp); set_defaults(bp, {'SHM254_Turn': 0.0}); compile_ok(bp)
    sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
    comp = [p for p in sn if 'GetComponentByClass' in tid(p) or 'GetComponentbyClass' in tid(p)]; assert comp, 'component getter'; ct = (comp[0], 'ReturnValue')
    on = gs.within(gs.get('SHM254_Turn'), 0.5, 1.0e9)
    # (A) sign
    sd = [p for p in sn if tid(p).endswith('|SetSHM238_Delta')]; assert len(sd) == 1, sd
    nxtA = succ(sd[0]); assert nxtA, 'Delta successor'
    for tn, tp in nxtA: disconnect((tn, tp))
    side = gs.pure('/Script/Engine.AnimInstance:GetCurveValue', {'CurveName': 'SHM254_Side'})
    sideOK = gs.OR(gs.within(side, 0.3, 1.0e9), gs.within(side, -1.0e9, -0.3))
    absd = gs.pure(M + 'Abs', {'A': gs.get('SHM238_Delta')})
    big = gs.within(absd, 120.0, 1.0e9)
    sgn = gs.select(gs.within(side, 0.0, 1.0e9), 1.0, -1.0)
    newd = gs.select(gs.AND(on, gs.AND(sideOK, big)), gs.mul(absd, sgn), gs.get('SHM238_Delta'))
    tA = gs.set('SHM238_Delta', newd, (sd[0], 'then'))
    for tn, tp in nxtA: connect(tA, (tn, tp))
    # (B) body frame hand-over on the falling edge of SHM254_W
    po = [p for p in sn if tid(p).endswith('|SetSHM238_PrevOn')]; assert len(po) == 1, po
    nxtB = succ(po[0]); assert nxtB, 'PrevOn successor'
    for tn, tp in nxtB: disconnect((tn, tp))
    w = gs.pure('/Script/Engine.AnimInstance:GetCurveValue', {'CurveName': 'SHM254_W'})
    fall = gs.AND(on, gs.AND(gs.within(gs.get('SHM254_PrevW'), 0.3, 1.0e9), gs.within(w, -1.0e9, 0.3)))
    bt, bf = gs.branch(fall, (po[0], 'then'))
    pawn = gs.pure('/Script/Engine.AnimInstance:TryGetPawnOwner')
    yawNow = gs.yaw(gs.pure('/Script/Engine.Actor:K2_GetActorRotation', {'self': pawn}))
    t1 = gs.set('LocoExplore', True, bt, COMP, ct); t2 = gs.set('LocoState', 1.0, t1, COMP, ct); t3 = gs.set('LocoOn', True, t2, COMP, ct); t4 = gs.set('LocoYaw', yawNow, t3, COMP, ct)
    w2 = gs.pure('/Script/Engine.AnimInstance:GetCurveValue', {'CurveName': 'SHM254_W'})
    tw = gs.set('SHM254_PrevW', w2, t4)
    tw2 = gs.set('SHM254_PrevW', gs.pure('/Script/Engine.AnimInstance:GetCurveValue', {'CurveName': 'SHM254_W'}), bf)
    for tn, tp in nxtB: connect(tw, (tn, tp)); connect(tw2, (tn, tp))
    out['wired'] = {'A_after': sd[0].rsplit('.', 1)[-1], 'B_after': po[0].rsplit('.', 1)[-1]}
st_, errs = compile_ok(bp); out['abp'] = [str(st_), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class()); out['knob'] = str(cdo.get_editor_property('SHM254_Turn'))
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child'] and out['knob'] == '0.0'
if out['ok'] and getattr(builtins, 'V254_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()]
print('TURN254 ' + json.dumps(out, default=str))
