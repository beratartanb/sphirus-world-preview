"""install254_v2.py (editor job, write manifest = ABP base + child): V2.54 second runtime pass for the planned turn-around (knob SHM254_Turn).
Measured (v254d60 s54_revR rvc): (1) HAND-OVER SNAP - on the frame the clip's yaw contract ends (curve SHM254_W falls) GR's facing slew
    (CP_PhysicalRedirect RInterpTo_Constant x GR241_YawRateK) still ran at 450 deg/s toward its look target: actor yaw 179.7 -> 172.2 in one
    frame, then back to 180 at 40 deg/s; the curvature lean (CurveLeanDeg) swung -4 -> +4 deg and the head 15 cm sideways in the re-push.
    Fix: SHM254_HoK := 0 on that falling edge, ramps back to 1 in 0.2 s (HoK += dt / 0.2); pawn GR241_YawRateK := SHM239_Ext ? PushYawK : HoK
    (written here AND as the else-input of the V2.41 select, so the write order in SHM_Snapshot does not matter).
(2) INTENT CANCEL - a short opposite tap then W still played the whole 180 (the V2.54 route hold ignored the new input).
    SHM254_Cancel := on AND curve SHM254_Own > 0.3 AND (Cancel OR (valid AND (NOT HasIntent OR |NormalizeAxis(yaw(DesiredVelocity) -
    (SHM238_Yaw0 + SHM238_Delta))| > SHM254_CancelDeg))), valid = SHM238_On OR curve SHM254_W < 0.3 (latched plan target);
    the hold (Update_MotionMatching entry branch) adds AND NOT Cancel; SHM238_On adds AND NOT Cancel (the clip stops steering the capsule).
Spliced after the two SetSHM254_PrevW nodes of install254_turn (B). Knob off -> HoK stays 1, Cancel stays false (production unchanged).
Idempotent (variable SHM254_HoK). builtins.V254_SAVE saves. Prints V2254 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, arg
import builtins, json
LS = u.EditorLoadingAndSavingUtils; M = '/Script/Engine.KismetMathLibrary:'
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CPA = AP.replace('Base', '')
COMP = '/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent.BP_SHM_HumanMotionComponent_C'; PAWN = '/Game/GraceRanger/BP_GR_Player'
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
assert 'SHM254_Hold' in V and 'SHM254_PrevW' in V, 'install254_turn + install254_hold first'
if 'SHM254_HoK' in V: out['patch'] = 'already'
else:
    ensure_vars(bp, [('SHM254_HoK', 'float', 'SHM'), ('SHM254_Cancel', 'bool', 'SHM'), ('SHM254_CancelDeg', 'float', 'SHM')]); compile_ok(bp)
    set_defaults(bp, {'SHM254_HoK': 1.0, 'SHM254_CancelDeg': 75.0}); compile_ok(bp)
    pcls = u.load_asset(PAWN).generated_class()
    sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
    comp = [p for p in sn if 'GetComponentByClass' in tid(p) or 'GetComponentbyClass' in tid(p)]; assert comp, 'component getter'; ct = (comp[0], 'ReturnValue')
    pw = [p for p in sn if tid(p).endswith('|SetSHM254_PrevW')]; assert len(pw) == 2, pw
    nx = succ(pw[0]); assert nx and sorted(nx) == sorted(succ(pw[1])), (nx, succ(pw[1]))
    fall = [p for p in pw if any('SetLocoYaw' in tid(s_[0]) for s_ in src((p, 'execute')))]; assert len(fall) == 1, ('falling PrevW', [[tid(s_[0]) for s_ in src((p, 'execute'))] for p in pw])
    other = [p for p in pw if p != fall[0]][0]
    keep = {x: [s_ for s_ in src(x) if s_[0] not in pw] for x in nx}
    for x in nx: disconnect(x)
    for x in nx:
        for s_ in keep[x]: connect(s_, x)
    on = gs.within(gs.get('SHM254_Turn'), 0.5, 1.0e9)
    w = gs.pure('/Script/Engine.AnimInstance:GetCurveValue', {'CurveName': 'SHM254_W'})
    # hand-over yaw-rate ramp: 0 on the falling edge, back to 1 in 0.2 s
    t0 = gs.set('SHM254_HoK', 0.0, (fall[0], 'then'))
    dt = gs.pure('/Script/Engine.GameplayStatics:GetWorldDeltaSeconds')
    inc = gs.pure(M + 'FMin', {'A': gs.math(gs.get('SHM254_HoK'), gs.mul(dt, 5.0)), 'B': 1.0})
    ti = gs.set('SHM254_HoK', inc, t0)
    connect((other, 'then'), (ti[0], 'execute'))
    # pawn yaw-rate factor (V2.41 select semantics, the hand-over ramp instead of 1)
    pawn = gs.pure('/Script/Engine.AnimInstance:TryGetPawnOwner')
    cth, cvv = gs.cast(pawn, pcls, ti)
    k = gs.select(gs.get('SHM239_Ext'), gs.get('SHM241_PushYawK'), gs.get('SHM254_HoK'))
    tk = gs.set('GR241_YawRateK', k, cth, PAWN + '.BP_GR_Player_C', cvv)
    # intent cancel (latched until the clip's own window ends)
    own = gs.pure('/Script/Engine.AnimInstance:GetCurveValue', {'CurveName': 'SHM254_Own'})
    dv = gs.get('DesiredVelocity', COMP, ct); hasI = gs.get('HasIntent', COMP, ct)
    ydv = gs.yaw(gs.pure(M + 'Conv_VectorToRotator', {'InVec': dv}))
    tgt = gs.math(gs.get('SHM238_Yaw0'), gs.get('SHM238_Delta'))
    dif = gs.pure(M + 'Abs', {'A': gs.pure(M + 'NormalizeAxis', {'Angle': gs.sub(ydv, tgt)})})
    trig = gs.OR(gs.NOT(hasI), gs.within(dif, gs.get('SHM254_CancelDeg'), 1.0e9))
    valid = gs.OR(gs.get('SHM238_On'), gs.within(w, -1.0e9, 0.3))
    canc = gs.AND(gs.AND(on, gs.within(own, 0.3, 1.0e9)), gs.OR(gs.get('SHM254_Cancel'), gs.AND(valid, trig)))
    tc = gs.set('SHM254_Cancel', canc, tk)
    tc2 = gs.set('SHM254_Cancel', canc, (cth[0], 'CastFailed'))
    for tn, tp in nx: connect(tc, (tn, tp)); connect(tc2, (tn, tp))
    # SHM238_On AND NOT Cancel
    so = [p for p in sn if tid(p).endswith('|SetSHM238_On')]; assert len(so) == 1, so
    s0 = src((so[0], 'SHM238_On')); assert len(s0) == 1, s0
    disconnect((so[0], 'SHM238_On')); connect(gs.AND(s0[0], gs.NOT(gs.get('SHM254_Cancel'))), (so[0], 'SHM238_On'))
    # V2.41 select else-input := HoK
    for p in [p for p in sn if tid(p).endswith('|SetGR241_YawRateK')]:
        sel = src((p, 'GR241_YawRateK'))
        if sel and 'SelectFloat' in tid(sel[0][0]):
            disconnect((sel[0][0], 'B')); connect(gs.get('SHM254_HoK'), (sel[0][0], 'B')); out.setdefault('sel241', []).append(sel[0][0].rsplit('.', 1)[-1])
    # hold: AND NOT Cancel
    mg = pn(graph(bp, 'Update_MotionMatching')); gm = G(mg); N = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(mg))}
    br = succ(N['K2Node_FunctionEntry_0']); assert len(br) == 1 and 'IfThenElse' in br[0][0], br
    c0 = src((br[0][0], 'Condition')); assert len(c0) == 1, c0
    disconnect((br[0][0], 'Condition')); connect(gm.AND(c0[0], gm.NOT(gm.get('SHM254_Cancel'))), (br[0][0], 'Condition'))
    out['wired'] = {'after': [p.rsplit('.', 1)[-1] for p in pw], 'fall': fall[0].rsplit('.', 1)[-1], 'next': [x[0].rsplit('.', 1)[-1] for x in nx], 'hold_branch': br[0][0].rsplit('.', 1)[-1]}
st_, errs = compile_ok(bp); out['abp'] = [str(st_), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class()); out['knob'] = str(cdo.get_editor_property('SHM254_Turn')); out['hok'] = str(cdo.get_editor_property('SHM254_HoK'))
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child'] and out['knob'] == '0.0' and out['hok'] == '1.0'
if out['ok'] and getattr(builtins, 'V254_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()]
print('V2254 ' + json.dumps(out, default=str))
