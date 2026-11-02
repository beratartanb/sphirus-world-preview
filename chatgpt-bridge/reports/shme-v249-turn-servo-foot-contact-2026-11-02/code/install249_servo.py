"""install249_servo.py (editor job, write manifest = ABP base + child; after install249_rm.py and add249_rootcurves.py):
V2.49 CAPSULE POSITION SERVO for the cropped turning start. Engine root motion is unusable here (the Motion Matching blend-stack sample graph
carries a ResetRoot node: RootMotionFromEverything consumed zero root motion, capsule frozen - v249a60 rm). The capsule is instead locked to
the clip's root PATH (not its speed estimate):
  SHM249_RM = 1 -> servo (new);  SHM249_RM >= 2 -> the engine-root-motion experiment (SetRootMotionMode + pawn skip), kept for reference.
SHM_Snapshot, after SetSHM238_PrevOn (the end of the V2.28 / V2.38 contract writes, so this overrides them):
  servo = SHM249_Owned AND 0.5 <= RM < 1.5 AND curve SHM226_W > 0.3
  rx, ry, sy = SHM249_RX / W, SHM249_RY / W, SHM241_SYaw / W            (clip root pose since frame 0, blend-weight normalised)
  first servo frame: AnchorYaw := actorYaw - sy; Anchor := actorPos - Fwd(AnchorYaw)*rx - Right(AnchorYaw)*ry ; Prev := current
  e* = v + Lead * (v - Prev*)        (Lead = SHM249_Lead frames: the curve is the PREVIOUS evaluation, the velocity acts NEXT frame)
  target yaw = AnchorYaw + esy ; target pos = Anchor + Fwd(AnchorYaw)*erx + Right(AnchorYaw)*ery
  vel = (target - actorPos) / dt ; component ClipYaw := target yaw, ClipYawOn := true, ClipSpeed := vel . Fwd(target yaw),
  ClipSpeedLat := vel . Right(target yaw), ClipSpeedOn := true          (BP_GR_Player V2.28/V2.48 branch applies them unchanged)
Also: component RootMotionOwned := SHM249_Owned AND RM >= 1.5 (the pawn skips its redirect only in the engine mode); the SetRootMotionMode
branch runs only for RM >= 1.5. Idempotent (variable SHM249_Lead). builtins.V249_SAVE saves. Prints SERVO249 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, arg, value
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
bp = u.load_asset(AP); Vs = [str(v) for v in B.list_variables(bp)]
assert 'SHM249_RM' in Vs, 'install249_rm.py first'
if 'SHM249_Lead' in Vs: out['patch'] = 'already'
else:
    F = 'float'
    ensure_vars(bp, [('SHM249_Lead', F, 'SHM'), ('SHM249_AX', F, 'SHM'), ('SHM249_AY', F, 'SHM'), ('SHM249_AYaw', F, 'SHM'), ('SHM249_PRX', F, 'SHM'), ('SHM249_PRY', F, 'SHM'),
                     ('SHM249_PSY', F, 'SHM'), ('SHM249_Servo', 'bool', 'SHM'), ('SHM249_PrevServo', 'bool', 'SHM'), ('SHM249_ErrCm', F, 'SHM')]); compile_ok(bp)
    set_defaults(bp, {'SHM249_Lead': 2.0}); compile_ok(bp)
    sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
    comp = [p for p in sn if 'GetComponentByClass' in tid(p) or 'GetComponentbyClass' in tid(p)]; assert comp, 'component getter'; ct = (comp[0], 'ReturnValue')
    # -- engine mode only for RM >= 1.5
    rmo = [p for p in sn if tid(p).endswith('|SetRootMotionOwned')]; assert len(rmo) == 1, rmo
    o_ = src((rmo[0], 'RootMotionOwned')); disconnect((rmo[0], 'RootMotionOwned'))
    connect(gs.AND(o_[0], gs.within(gs.get('SHM249_RM'), 1.5, 1.0e9)), (rmo[0], 'RootMotionOwned'))
    ins = [p for p in sn if 'InRange' in tid(p) and any(tid(s_[0]).endswith('|GetSHM249_RM') for s_ in src((p, 'Value')))]
    brc = [p for p in ins if any('IfThenElse' in pn(q.node) for o in info(p).output_pins if o.name == 'ReturnValue' for q in o.connected_pins)]
    assert len(brc) == 1, ('engine-mode branch InRange', [p.rsplit('.', 1)[-1] for p in brc]); value((brc[0], 'Min'), 1.5); out['engine_gate'] = brc[0].rsplit('.', 1)[-1]
    # -- servo block after SetSHM238_PrevOn
    po = [p for p in sn if tid(p).endswith('|SetSHM238_PrevOn')]; assert len(po) == 1, po
    nxt = succ(po[0]); assert nxt, 'PrevOn successor'
    for tn, tp in nxt: disconnect((tn, tp))
    curve = lambda nm: gs.pure('/Script/Engine.AnimInstance:GetCurveValue', {'CurveName': nm})
    W = curve('SHM226_W'); div = lambda a: gs.pure(M + 'SafeDivide', {'A': a, 'B': W})
    pawn = gs.pure('/Script/Engine.AnimInstance:TryGetPawnOwner', {})
    loc = gs.pure('/Script/Engine.Actor:K2_GetActorLocation', {'self': pawn}); lb = gs.fn('BreakVector', {'InVec': loc})
    ayaw = gs.yaw(gs.pure('/Script/Engine.Actor:K2_GetActorRotation', {'self': pawn}))
    servo = gs.AND(gs.AND(gs.get('SHM249_Owned'), gs.within(gs.get('SHM249_RM'), 0.5, 1.5)), gs.within(W, 0.3, 1.0e9))
    t0 = gs.set('SHM249_Servo', servo, (po[0], 'then'))
    bt, bf = gs.branch(gs.get('SHM249_Servo'), t0)
    # first frame: anchor
    first = gs.NOT(gs.get('SHM249_PrevServo'))
    ft, ff = gs.branch(first, bt)
    rx, ry, sy = div(curve('SHM249_RX')), div(curve('SHM249_RY')), div(curve('SHM241_SYaw'))
    a1 = gs.set('SHM249_AYaw', gs.math(ayaw, sy, -1), ft)
    fwdA = lambda: gs.pure(M + 'GetForwardVector', {'InRot': gs.rot(gs.get('SHM249_AYaw'))}); rgtA = lambda: gs.pure(M + 'GetRightVector', {'InRot': gs.rot(gs.get('SHM249_AYaw'))})
    def comp_xy(vec_fn, k):
        b = gs.fn('BreakVector', {'InVec': vec_fn()}); return (b, k)
    # Anchor = loc - fwdA*rx - rgtA*ry  (x and y separately)
    ax = gs.math(gs.math((lb, 'X'), gs.mul(comp_xy(fwdA, 'X'), rx), -1), gs.mul(comp_xy(rgtA, 'X'), ry), -1)
    ay = gs.math(gs.math((lb, 'Y'), gs.mul(comp_xy(fwdA, 'Y'), rx), -1), gs.mul(comp_xy(rgtA, 'Y'), ry), -1)
    a2 = gs.set('SHM249_AX', ax, a1); a3 = gs.set('SHM249_AY', ay, a2)
    a4 = gs.set('SHM249_PRX', rx, a3); a5 = gs.set('SHM249_PRY', ry, a4); a6 = gs.set('SHM249_PSY', sy, a5)
    # every servo frame (after the anchor on the first one)
    ext = lambda v, pv: gs.math(v, gs.mul(gs.math(v, gs.get(pv), -1), gs.get('SHM249_Lead')), 1)
    erx, ery, esy = ext(rx, 'SHM249_PRX'), ext(ry, 'SHM249_PRY'), ext(sy, 'SHM249_PSY')
    tyaw = gs.math(gs.get('SHM249_AYaw'), esy, 1)
    tx = gs.math(gs.math(gs.get('SHM249_AX'), gs.mul(comp_xy(fwdA, 'X'), erx), 1), gs.mul(comp_xy(rgtA, 'X'), ery), 1)
    ty = gs.math(gs.math(gs.get('SHM249_AY'), gs.mul(comp_xy(fwdA, 'Y'), erx), 1), gs.mul(comp_xy(rgtA, 'Y'), ery), 1)
    dt = gs.pure('/Script/Engine.GameplayStatics:GetWorldDeltaSeconds', {})
    vx = gs.pure(M + 'SafeDivide', {'A': gs.math(tx, (lb, 'X'), -1), 'B': dt}); vy = gs.pure(M + 'SafeDivide', {'A': gs.math(ty, (lb, 'Y'), -1), 'B': dt})
    vel = gs.pure('MakeVector', {'X': vx, 'Y': vy, 'Z': 0.0})
    fT = gs.pure(M + 'GetForwardVector', {'InRot': gs.rot(tyaw)}); rT = gs.pure(M + 'GetRightVector', {'InRot': gs.rot(tyaw)})
    s1 = gs.set('ClipYaw', tyaw, a6, COMP, ct); connect(ff, (s1[0], 'execute'))
    s2 = gs.set('ClipYawOn', True, s1, COMP, ct)
    s3 = gs.set('ClipSpeed', gs.pure(M + 'Dot_VectorVector', {'A': vel, 'B': fT}), s2, COMP, ct)
    s4 = gs.set('ClipSpeedLat', gs.pure(M + 'Dot_VectorVector', {'A': vel, 'B': rT}), s3, COMP, ct)
    s5 = gs.set('ClipSpeedOn', True, s4, COMP, ct)
    s6 = gs.set('SHM249_ErrCm', gs.pure(M + 'VSize', {'A': gs.pure('MakeVector', {'X': gs.math(tx, (lb, 'X'), -1), 'Y': gs.math(ty, (lb, 'Y'), -1), 'Z': 0.0})}), s5)
    s7 = gs.set('SHM249_PRX', rx, s6); s8 = gs.set('SHM249_PRY', ry, s7); s9 = gs.set('SHM249_PSY', sy, s8)
    e1 = gs.set('SHM249_PrevServo', gs.get('SHM249_Servo'), s9); connect(bf, (e1[0], 'execute'))
    for tn, tp in nxt: connect(e1, (tn, tp))
    out['servo'] = {'after': po[0].rsplit('.', 1)[-1], 'next': [a.rsplit('.', 1)[-1] for a, _ in nxt]}
st_, errs = compile_ok(bp); out['abp'] = [str(st_), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class()); out['knobs'] = {k: str(cdo.get_editor_property(k)) for k in ('SHM249_RM', 'SHM249_Lead', 'SHM248_On')}
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child'] and out['knobs']['SHM249_RM'] == '0.0'
if out['ok'] and getattr(builtins, 'V249_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()]
print('SERVO249 ' + json.dumps(out, default=str))
