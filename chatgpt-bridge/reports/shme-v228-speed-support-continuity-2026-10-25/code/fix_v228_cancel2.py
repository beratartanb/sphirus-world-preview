"""fix_v228_cancel2.py (editor job) - cancel path, second pass. Measured (v228t4 dbl rhCR): the cancel fired (IntentEnd suppressed) but no new
search followed: the clip stayed F_B_P14 and the clip-bound capsule ran BACKWARD for 3 s against a held W (a control lock). Two changes and a
safety:
 (a) the V2.27 search throttle (AnimGraph MM SearchThrottleTime = FMax(old, Select(Thr, ThrottleT, 0))) is lifted on the reroute frame:
     Select picks ThrottleT only when Thr AND NOT SHM228_Reroute (the snapshot runs before Update_MotionMatching in the same frame);
 (b) the reroute SetDatabaseToSearch uses InterruptOnDatabaseChangeAndInvalidateContinuingPose;
 (c) safety: while an authored clip drives the capsule, a designed speed that opposes the player's intent along the actor forward for more
     than SHM228_AgainstMax s (0.08) kills the hold (SHM228_Dead latch path): SHM228_AgainstT accumulates while HasIntent & |DesV| > 30 &
     DesV * dot(forward, DesiredDir) < 0; reset otherwise. Dead := OR(old, AgainstT > AgainstMax).
Idempotent (SHM228_AgainstT present). builtins.V228_SAVE saves. Prints CANCEL228B {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, arg, value
import builtins, json
LS = u.EditorLoadingAndSavingUtils; M = '/Script/Engine.KismetMathLibrary:'
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CP = AP.replace('Base', '')
COMP = '/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent.BP_SHM_HumanMotionComponent_C'
DAS = {'/Game/GraceRanger/Profiles/DA_GR_LocomotionBehavior', '/Game/GraceRanger/SHME/DA_SHM_Response_Default', '/Game/GraceRanger/Experimental/BodyInertia/DA_PBI_Prototype'}
dirty = list(LS.get_dirty_content_packages()); names = [p.get_name() for p in dirty]
assert all(n in DAS or n in (AP, CP) for n in names), ('unexpected dirty', names)
rl = [p for p in dirty if p.get_name() in DAS or p.get_name() in (AP, CP)]
if rl: LS.reload_packages(rl, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
out = {'reloaded': [p.get_name() for p in rl]}
bp = u.load_asset(AP)
ensure_vars(bp, [('SHM228_AgainstT', 'float', 'SHM228'), ('SHM228_AgainstMax', 'float', 'SHM228'), ('SHM228_ThrOK', 'bool', 'SHM228')]); compile_ok(bp)
cdo = u.get_default_object(bp.generated_class())
if abs(float(cdo.get_editor_property('SHM228_AgainstMax'))) < 1e-6: set_defaults(bp, {'SHM228_AgainstMax': 0.08}); compile_ok(bp)
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
# ---- (c) snapshot safety
sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
if any('SetSHM228_AgainstT' in tid(p) for p in sn): out['snapshot'] = 'already'
else:
    dd = [p for p in sn if 'SetSHM227_Dead' in tid(p)]; assert len(dd) == 1, dd
    comp = [p for p in sn if 'GetComponentByClass' in tid(p) or 'GetComponentbyClass' in tid(p)]; assert comp; ct = (comp[0], 'ReturnValue')
    prev_exec = src((dd[0], 'execute')); assert len(prev_exec) == 1
    disconnect((dd[0], 'execute'))
    dv = gs.get('SHM228_DesV')
    pawn = gs.pure('/Script/Engine.AnimInstance:TryGetPawnOwner')
    fwd = gs.pure('/Script/Engine.Actor:GetActorForwardVector', {'self': pawn})
    ddir = gs.pure(M + 'Vector_Normal2D', {'A': gs.get('DesiredDir', COMP, ct), 'Tolerance': 0.0001})
    along = gs.pure(M + 'Dot_VectorVector', {'A': fwd, 'B': ddir})
    fast = gs.OR(gs.within(dv, 30.0, 1.0e9), gs.within(dv, -1.0e9, -30.0))
    against = gs.AND(gs.AND(gs.get('HasIntent', COMP, ct), fast), gs.within(gs.mul(dv, along), -1.0e9, -1.0))
    dt = gs.get('DeltaTime', COMP, ct)
    acc = gs.select(against, gs.math(gs.get('SHM228_AgainstT'), dt, 1), 0.0)
    t1 = gs.set('SHM228_AgainstT', acc, prev_exec[0]); connect(t1, (dd[0], 'execute'))
    do = src((dd[0], 'SHM227_Dead')); assert len(do) == 1
    disconnect((dd[0], 'SHM227_Dead')); connect(gs.OR(do[0], gs.within(gs.get('SHM228_AgainstT'), gs.get('SHM228_AgainstMax'), 1.0e9)), (dd[0], 'SHM227_Dead'))
    rrs = [p for p in sn if 'SetSHM228_Reroute' in tid(p)]; assert len(rrs) == 1, rrs
    nxt2 = [p for p in sn if any(q.name == 'execute' for q in info(p).input_pins) and (rrs[0], 'then') in src((p, 'execute'))]
    for x in nxt2: disconnect((x, 'execute'))
    t2 = gs.set('SHM228_ThrOK', gs.AND(gs.get('SHM227_Thr'), gs.NOT(gs.get('SHM228_Reroute'))), (rrs[0], 'then'))
    for x in nxt2: connect(t2, (x, 'execute'))
    out['snapshot'] = 'wired'
# ---- (a) AnimGraph throttle: Select bPickA <- SHM228_ThrOK (= Thr AND NOT Reroute, computed in the snapshot)
ag = pn(graph(bp, 'AnimGraph')); ga = G(ag); an = [pn(n) for n in B.find_nodes(obj(ag))]
sel = [p for p in an if 'SelectFloat' in tid(p) and any('SHM227_ThrottleT' in tid(s[0]) for s in src((p, 'A')))]
assert len(sel) == 1, ('throttle select', [tid(p)[-30:] for p in sel])
pk = src((sel[0], 'bPickA')); assert len(pk) == 1
if 'SHM228_ThrOK' in tid(pk[0][0]): out['throttle'] = 'already'
else:
    disconnect((sel[0], 'bPickA')); connect(ga.get('SHM228_ThrOK'), (sel[0], 'bPickA')); out['throttle'] = 'wired'
# ---- (b) reroute call interrupt mode
ug = pn(graph(bp, 'Update_MotionMatching')); un = [pn(n) for n in B.find_nodes(obj(ug))]
def branch_reads_reroute(n):
    if not any(q.name == 'Condition' for q in info(n).input_pins): return False
    return any('SHM228_Reroute' in tid(s[0]) for s in src((n, 'Condition')))
rr = [p for p in un if 'SetDatabaseToSearch' in tid(p) and any(s0[1] == 'then' and branch_reads_reroute(s0[0]) for s0 in src((p, 'execute')))]
assert len(rr) == 1, ('reroute call', len(rr))
value((rr[0], 'InterruptMode'), 'InterruptOnDatabaseChangeAndInvalidateContinuingPose'); out['reroute_interrupt'] = 'set'
st, errs = compile_ok(bp); out['status'] = str(st); out['errs'] = errs[:6]
cpb = u.load_asset(CP); out['child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class()); out['knobs'] = {k: float(cdo.get_editor_property(k)) for k in ('SHM227_RevHold', 'SHM228_ClipSpeed', 'SHM228_RelHold', 'SHM228_CancelOn', 'SHM228_AgainstMax')}
ok = 'UP_TO_DATE' in str(st) and not errs and 'UP_TO_DATE' in out['child'] and out['knobs']['SHM228_CancelOn'] == 0.0
out['ok'] = ok
if ok and getattr(builtins, 'V228_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('CANCEL228B ' + json.dumps(out, default=str))
