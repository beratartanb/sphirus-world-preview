"""install238_yaw.py (editor job) - V2.38 clip-bound HEADING contract (the V2.28 clip-speed contract extended to the direction).
Why: in a hard jog 90 the capsule heading is GR's look/turn slew (88 deg in 0.5 s at 0.9 g, the same with any animation - measured
v238base / v238jc1), so an authored brake -> plant -> transfer -> push whose root turns where its contacts can turn it slides against the
capsule. While an authored redirect clip carrying SHM238_Turn / SHM238_W is in the pose AND the V2.28 clip-speed contract is on
(SHM228_On: episode alive, clip speed bound), the capsule heading follows the clip's designed heading change:
  ABP_GR_MotionMatchingBase.SHM_Snapshot (after the V2.28 chain):
    T = Turn / W (W > 0.3)   On = knob SHM238_Yaw > 0.5 & W > 0.3 & SHM228_On
    rising On: Yaw0 := actor yaw, Delta := NormalizeAxis(yaw(component DesiredVelocity) - actor yaw)   (the request, signed)
    Cmd = Yaw0 + Delta * (T + Lead*(T - PrevT)) / 90   (one-frame look-ahead as V2.28; the clips turn 90 at their end)
    component ClipYaw := Cmd, ClipYawOn := On
  BP_GR_Player.GR_Impl_CP_PhysicalRedirect: in the V2.28 clip-speed branch, before Velocity := Forward * ClipSpeed:
    ClipYawOn -> K2_SetActorRotation(0, ClipYaw, 0) (so the forward of that velocity write is the designed heading)
Installed OFF (SHM238_Yaw = 0 = production unchanged). Idempotent. builtins.V238_SAVE saves. Prints YAW238 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, op, arg
import builtins, json
LS = u.EditorLoadingAndSavingUtils; M = '/Script/Engine.KismetMathLibrary:'
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CPA = AP.replace('Base', '')
COMPP = '/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent'; COMP = COMPP + '.BP_SHM_HumanMotionComponent_C'
PB = '/Game/GraceRanger/BP_GR_Player'; CHILD = '/Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player'
DAS = {'/Game/GraceRanger/Profiles/DA_GR_LocomotionBehavior', '/Game/GraceRanger/SHME/DA_SHM_Response_Default', '/Game/GraceRanger/Experimental/BodyInertia/DA_PBI_Prototype'}
dirty = list(LS.get_dirty_content_packages()); names = [p.get_name() for p in dirty]
KEEP = bool(getattr(builtins, 'V238_KEEP', False))      # resume an install whose earlier steps are already in memory (never reload class BPs then)
assert all(n in DAS or n in (AP, CPA) or (KEEP and n == COMPP) for n in names), ('unexpected dirty', names)   # harness abp_flags dirty the ABP CDOs
rl = [p for p in dirty if p.get_name() in DAS or (not KEEP and p.get_name() in (AP, CPA))]
if rl: LS.reload_packages(rl, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
out = {'reloaded': names}
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
# ---- 1. component contract variables
cb = u.load_asset(COMPP)
ensure_vars(cb, [('ClipYaw', 'float', 'SHM|V238'), ('ClipYawOn', 'bool', 'SHM|V238')])
st, errs = compile_ok(cb); out['component'] = [str(st), errs[:4]]
# ---- 2. ABP snapshot
bp = u.load_asset(AP)
ensure_vars(bp, [('SHM238_Yaw', 'float', 'SHM238'), ('SHM238_T', 'float', 'SHM238'), ('SHM238_PrevT', 'float', 'SHM238'), ('SHM238_Yaw0', 'float', 'SHM238'),
                 ('SHM238_Delta', 'float', 'SHM238'), ('SHM238_Cmd', 'float', 'SHM238'), ('SHM238_PrevOn', 'bool', 'SHM238'), ('SHM238_On', 'bool', 'SHM238')]); compile_ok(bp)
sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
if any('SetSHM238_Cmd' in tid(p) for p in sn): out['snapshot'] = 'already'
else:
    last = [p for p in sn if tid(p).endswith('SetClipSpeedOn')]; assert len(last) == 1, [tid(p) for p in sn if 'ClipSpeed' in tid(p)]
    comp = [p for p in sn if 'GetComponentByClass' in tid(p) or 'GetComponentbyClass' in tid(p)]; assert comp, 'component getter'; ct = (comp[0], 'ReturnValue')
    nxt = [p for p in sn if any(q.name == 'execute' for q in info(p).input_pins) and (last[0], 'then') in src((p, 'execute'))]
    for x in nxt: disconnect((x, 'execute'))
    vT = gs.pure('/Script/Engine.AnimInstance:GetCurveValue', {'CurveName': 'SHM238_Turn'}); vW = gs.pure('/Script/Engine.AnimInstance:GetCurveValue', {'CurveName': 'SHM238_W'})
    wOK = gs.within(vW, 0.3, 1.0e9)
    on = gs.AND(gs.AND(gs.within(gs.get('SHM238_Yaw'), 0.5, 1.0e9), wOK), gs.get('SHM228_On'))
    tail = gs.set('SHM238_On', on, (last[0], 'then'))
    tail = gs.set('SHM238_T', gs.select(wOK, gs.pure(M + 'SafeDivide', {'A': vT, 'B': vW}), 0.0), tail)
    rise = gs.AND(gs.get('SHM238_On'), gs.NOT(gs.get('SHM238_PrevOn')))
    pawn = gs.pure('/Script/Engine.AnimInstance:TryGetPawnOwner')
    yawNow = gs.yaw(gs.pure('/Script/Engine.Actor:K2_GetActorRotation', {'self': pawn}))
    dvv = gs.fn('BreakVector', {'InVec': gs.get('DesiredVelocity', COMP, ct)})
    yawDes = gs.pure(M + 'DegAtan2', {'Y': (dvv, 'Y'), 'X': (dvv, 'X')})
    delta = gs.pure(M + 'NormalizeAxis', {'Angle': gs.sub(yawDes, yawNow)})
    tail = gs.set('SHM238_Yaw0', gs.select(rise, yawNow, gs.get('SHM238_Yaw0')), tail)
    tail = gs.set('SHM238_Delta', gs.select(rise, delta, gs.get('SHM238_Delta')), tail)
    lead = gs.select(gs.get('SHM238_PrevOn'), gs.get('SHM228_LeadFrames'), 0.0)
    tl = gs.math(gs.get('SHM238_T'), gs.mul(lead, gs.sub(gs.get('SHM238_T'), gs.get('SHM238_PrevT'))), 1)
    frac = gs.pure(M + 'MapRangeUnclamped', {'Value': tl, 'InRangeA': 0.0, 'InRangeB': 90.0, 'OutRangeA': 0.0, 'OutRangeB': 1.0})
    tail = gs.set('SHM238_Cmd', gs.math(gs.get('SHM238_Yaw0'), gs.mul(frac, gs.get('SHM238_Delta')), 1), tail)
    tail = gs.set('ClipYaw', gs.get('SHM238_Cmd'), tail, COMP, ct)
    tail = gs.set('ClipYawOn', gs.get('SHM238_On'), tail, COMP, ct)
    tail = gs.set('SHM238_PrevT', gs.get('SHM238_T'), tail)
    tail = gs.set('SHM238_PrevOn', gs.get('SHM238_On'), tail)
    for x in nxt: connect(tail, (x, 'execute'))
    out['snapshot'] = {'after': last[0].rsplit('.', 1)[-1], 'next': [x.rsplit('.', 1)[-1] for x in nxt]}
st, errs = compile_ok(bp); out['abp'] = [str(st), errs[:6]]
cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class()); out['knob'] = float(cdo.get_editor_property('SHM238_Yaw'))
# ---- 3. GR: heading write inside the V2.28 clip-speed branch
pb = u.load_asset(PB)
g = G(op(PB) + ':GR_Impl_CP_PhysicalRedirect'); N = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(g.path))}
if any('ClipYawOn' in tid(p) for p in N.values()): out['gr'] = 'already'
else:
    def mentions(p, key, depth):                       # does this node's input chain read `key` (the V2.28 velocity write reads ClipSpeed)?
        if key in tid(p): return True
        if depth <= 0: return False
        try: pins = info(p).input_pins
        except Exception: return False
        return any(mentions(s_[0], key, depth - 1) for q in pins if q.name not in ('execute', 'self') for s_ in src((p, q.name)))
    rot = N['K2Node_CallFunction_23']; assert 'SetActorRotation' in tid(rot), tid(rot)   # the V2.28 branch hangs on the look-driven rotation's 'then'
    def ex_src(p): return src((p, 'execute'))
    sv = [p for p in N.values() if 'VariableSet' in p and tid(p).endswith('SetVelocity') and any('IfThenElse' in e[0] and (rot, 'then') in ex_src(e[0]) for e in ex_src(p))]
    assert len(sv) == 1, (len(sv), [tid(p) for p in N.values() if 'VariableSet' in p])
    ex = src((sv[0], 'execute')); assert len(ex) == 1, ex
    disconnect((sv[0], 'execute'))
    comp = g.pure('/Script/Engine.Actor:GetComponentByClass', {'ComponentClass': COMP})
    y, n = g.branch(g.get('ClipYawOn', COMP, comp), ex[0])
    r = g.call('/Script/Engine.Actor:K2_SetActorRotation', y, {'NewRotation': g.rot(g.get('ClipYaw', COMP, comp)), 'bTeleportPhysics': False})
    connect(r, (sv[0], 'execute')); connect(n, (sv[0], 'execute'))
    out['gr'] = {'velocity_set': sv[0].rsplit('.', 1)[-1], 'from': ex[0][0].rsplit('.', 1)[-1] + '.' + ex[0][1]}
st, errs = compile_ok(pb); out['gr_status'] = [str(st), errs[:6]]
ch = u.load_asset(CHILD); out['child'] = str(compile_ok(ch)[0])
pawn = u.get_default_object(ch.generated_class()); out['child_profile'] = str(pawn.get_editor_property('GR_Profile'))[:60]
ok = all('UP_TO_DATE' in x for x in (out['component'][0], out['abp'][0], out['abp_child'], out['gr_status'][0], out['child'])) and not out['component'][1] \
     and not out['abp'][1] and not out['gr_status'][1] and 'None' not in out['child_profile'] and out['knob'] == 0.0
out['ok'] = ok
if ok and getattr(builtins, 'V238_SAVE', False): save(cb, bp, cpb, pb, ch); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('YAW238 ' + json.dumps(out, default=str))
