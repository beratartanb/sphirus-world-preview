"""install255_pawn.py (editor job, write manifest = Integrated parent, BP_GR_Player, BP_PBI_Player): V2.55 pawn side of the command truth.
(1) RAW STICK. Integrated parent EventGraph, IA_Move Triggered: GR255_RawX / GR255_RawY := the move action value (before any frame). BP_GR_Player
    GR_UpdateSHMSignals (after SetGR233_MoveLatchYaw): component LocoRawOn := GR255_RawOn > 0.5, LocoRawYaw := DegAtan2(RawX, RawY).
(2) CLIP DIRECTION. V2.28 wrote Velocity = ActorForward * ClipSpeed: the travel of a clip-bound reversal is locked to the BODY axis, so a diagonal command was off by up
    to 45 deg and a moving look swung the travel with the camera (v255a60 fz_sprint_m 14.3 s: command -64, travel -120). After that write, GR_Impl_CP_PhysicalRedirect now
    overrides when component ClipDirOn: Velocity = ClipDir * ClipSpeed - DesiredDir * MaxAccel * dt (Z kept). ClipDir comes from the ABP (install255_abp).
Knobs default off: GR255_RawOn 0; ClipDirOn stays false until the ABP sets it. Idempotent (variable GR255_RawOn). builtins.V255_SAVE saves. Prints PAWN255 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, op, arg
import builtins, json
LS = u.EditorLoadingAndSavingUtils; M = '/Script/Engine.KismetMathLibrary:'
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
PAR = '/Game/ActionAdventureMovementS/Animations/Locomotion/CoreMotionAAMS/Integrated/BP_ExampleCharacter_MotionMatching'
PB = '/Game/GraceRanger/BP_GR_Player'; CHILD = '/Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player'; MM_ = '/Game/ActionAdventureMovementS/Animations/Locomotion/CoreMotionAAMS/Integrated/BP_Player_MM'
COMP = '/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent.BP_SHM_HumanMotionComponent_C'
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
out = {}
par = u.load_asset(PAR); pv = [str(v) for v in B.list_variables(par)]
if 'GR255_RawX' in pv: out['raw'] = 'already'
else:
    ensure_vars(par, [('GR255_RawX', 'float', 'GR255'), ('GR255_RawY', 'float', 'GR255')]); compile_ok(par)
    ge = G(op(PAR) + ':EventGraph'); N = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(ge.path))}
    ia = N['K2Node_EnhancedInputAction_0']; c83 = N['K2Node_CallFunction_83']; nxt = N['K2Node_CallFunction_156']
    assert 'TW_CameraMoveIntent' in tid(nxt) and 'GetMovementInputScaleValue' in tid(c83), (tid(nxt), tid(c83))
    assert [s_ for s_ in src((nxt, 'execute'))] == [(ia, 'Triggered')], src((nxt, 'execute'))
    disconnect((nxt, 'execute'))
    t1 = ge.set('GR255_RawX', (c83, 'ReturnValue_X'), (ia, 'Triggered')); t2 = ge.set('GR255_RawY', (c83, 'ReturnValue_Y'), t1); connect(t2, (nxt, 'execute'))
    out['raw'] = 'wired'
bp = u.load_asset(PB); bv = [str(v) for v in B.list_variables(bp)]
if 'GR255_RawOn' in bv: out['pawn'] = 'already'
else:
    ensure_vars(bp, [('GR255_RawOn', 'float', 'GR255')]); compile_ok(bp); set_defaults(bp, {'GR255_RawOn': 0.0}); compile_ok(bp)
    g = G(op(PB) + ':GR_UpdateSHMSignals'); nd = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(g.path))}
    last = [p for p in nd.values() if tid(p).endswith('|SetGR233_MoveLatchYaw')]; assert len(last) == 1, last; last = last[0]
    comp = nd['K2Node_CallFunction_0']; assert 'GetComponent' in tid(comp), tid(comp); ct = (comp, 'ReturnValue')
    after = []
    for n in B.find_nodes(obj(g.path)):
        for p_ in info(pn(n)).input_pins:
            s_ = src((pn(n), p_.name))
            if (last, 'then') in s_: after.append(((pn(n), p_.name), [x for x in s_ if x != (last, 'then')]))
    for ep, others in after: disconnect(ep)
    on = g.within(g.get('GR255_RawOn'), 0.5, 1.0e9)
    rx = g.get('GR255_RawX'); ry = g.get('GR255_RawY')
    ang = g.pure(M + 'DegAtan2', {'Y': rx, 'X': ry})
    t1 = g.set('LocoRawOn', on, (last, 'then'), COMP, ct); t2 = g.set('LocoRawYaw', ang, t1, COMP, ct)
    for ep, others in after:
        connect(t2, ep)
        for o in others: connect(o, ep)
    # ---- V2.55 clip direction override after the V2.28 velocity write
    g3 = G(op(PB) + ':GR_Impl_CP_PhysicalRedirect'); N3 = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(g3.path))}
    def leaves(ep, d, acc):
        if d > 9: return
        for s_ in src(ep):
            acc.add(tid(s_[0]).rsplit('|', 1)[-1])
            for q in info(s_[0]).input_pins:
                if q.name not in ('execute', 'then'):
                    try: leaves((s_[0], q.name), d + 1, acc)
                    except Exception: pass
    sets = []
    for p in N3.values():
        if tid(p).endswith('|SetVelocity'):
            acc = set(); leaves((p, 'Velocity'), 0, acc)
            if 'GetClipSpeed' in acc and 'GetClipSpeedLat' in acc: sets.append(p)
    assert len(sets) == 1, ('V2.28 Velocity set', [p.rsplit('.', 1)[-1] for p in sets]); vset = sets[0]
    assert not [q for q in N3.values() if any(x.name == 'execute' for x in info(q).input_pins) and (vset, 'then') in src((q, 'execute'))], 'velocity set has a successor'
    cmc = src((vset, 'self'))[0]
    compn = g3.pure('/Script/Engine.Actor:GetComponentByClass', {'ComponentClass': COMP})
    y, n_ = g3.branch(g3.get('ClipDirOn', COMP, compn), (vset, 'then'))
    d = g3.fn('BreakVector', {'InVec': g3.get('ClipDir', COMP, compn)}); dd = g3.fn('BreakVector', {'InVec': g3.get('DesiredDir', COMP, compn)})
    spd = g3.get('ClipSpeed', COMP, compn); vel = g3.fn('BreakVector', {'InVec': g3.pure('/Script/Engine.Actor:GetVelocity')})
    am = g3.pure('/Script/Engine.CharacterMovementComponent:GetMaxAcceleration', {'self': cmc}); dt = g3.pure('/Script/Engine.GameplayStatics:GetWorldDeltaSeconds')
    k = g3.mul(am, dt)
    nv = g3.pure('MakeVector', {'X': g3.sub(g3.mul((d, 'X'), spd), g3.mul((dd, 'X'), k)), 'Y': g3.sub(g3.mul((d, 'Y'), spd), g3.mul((dd, 'Y'), k)), 'Z': (vel, 'Z')})
    sv = g3.record(g3.editor().add_set_member_variable_node('Velocity', '/Script/Engine.MovementComponent'))
    connect(cmc, (sv, 'self')); connect(nv, (sv, 'Velocity')); connect(y, (sv, 'execute'))
    out['pawn'] = {'sig_after': last.rsplit('.', 1)[-1], 'vel_after': vset.rsplit('.', 1)[-1]}
for name, a in (('par', PAR), ('mm', MM_), ('pawn', PB), ('child', CHILD)):
    st, errs = compile_ok(u.load_asset(a)); out[name + '_c'] = [str(st), errs[:4]]
out['ok'] = all('UP_TO_DATE' in out[k][0] and not out[k][1] for k in ('par_c', 'mm_c', 'pawn_c', 'child_c'))
if out['ok'] and getattr(builtins, 'V255_SAVE', False): save(u.load_asset(PAR), u.load_asset(MM_), u.load_asset(PB), u.load_asset(CHILD)); out['saved'] = True
out['dirty'] = [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()]
print('PAWN255 ' + json.dumps(out, default=str))
