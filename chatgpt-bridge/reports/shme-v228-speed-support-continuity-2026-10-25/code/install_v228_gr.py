"""install_v228_gr.py (editor job) - V2.28 deliverable 1, movement side: while the SHME component reports ClipSpeedOn (an authored
reversal clip is in the pose and the ABP episode is alive), BP_GR_Player drives the capsule from the clip's designed speed instead of the
friction brake: at the END of GR_Impl_CP_PhysicalRedirect (after the look-driven SetActorRotation / its else branch, i.e. after every other
velocity write of this frame) Velocity = ActorForward * ClipSpeed (Z kept); GroundFriction = 0 and CalculateMaxAcceleration = 0 on those
frames so the CharacterMovementComponent neither rotates nor accelerates that velocity (collision sweeps, gravity and the player's new
intent are untouched: a new intent ends the component episode -> ClipSpeedOn false -> the normal CMC/friction path resumes the same frame).
Profile knob GR228_ClipSpeed (BP_GR_MotionProfile, DA_GR_LocomotionBehavior; default 0 = installed OFF) gates everything on the movement
side; the ABP knob SHM228_ClipSpeed gates the contract on the animation side. Idempotent (GR228_ClipSpeed getter present in the graph).
builtins.V228_SAVE saves BP_GR_Player, BP_PBI_Player, BP_GR_MotionProfile (and the DA only if dirty). Prints GR228 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, op, arg
import builtins, json
LS = u.EditorLoadingAndSavingUtils; M = '/Script/Engine.KismetMathLibrary:'
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
PB = '/Game/GraceRanger/BP_GR_Player'; PC = '/Game/GraceRanger/Profiles/BP_GR_MotionProfile'; CHILD = '/Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player'
DA = '/Game/GraceRanger/Profiles/DA_GR_LocomotionBehavior'; PCC = op(PC) + '_C'
COMP = '/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent.BP_SHM_HumanMotionComponent_C'
DAS = {DA, '/Game/GraceRanger/SHME/DA_SHM_Response_Default', '/Game/GraceRanger/Experimental/BodyInertia/DA_PBI_Prototype'}
dirty = list(LS.get_dirty_content_packages()); names = [p.get_name() for p in dirty]
assert all(n in DAS or n in (PB, CHILD, PC) for n in names), ('unexpected dirty', names)
rl = [p for p in dirty if p.get_name() in DAS]
if rl: LS.reload_packages(rl, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
out = {'reloaded': [p.get_name() for p in rl]}
prof = u.load_asset(PC)
ensure_vars(prof, [('GR228_ClipSpeed', 'float', 'V228')]); B.set_variable_instance_editable(prof, 'GR228_ClipSpeed', True)
out['profile'] = str(compile_ok(prof)[0]); set_defaults(prof, {'GR228_ClipSpeed': 0.0})
bp = u.load_asset(PB)
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
def comp_on(g):
    comp = g.pure('/Script/Engine.Actor:GetComponentByClass', {'ComponentClass': COMP})
    knob = g.get('GR228_ClipSpeed', PCC, g.get('GR_Profile'))
    on = g.AND(g.within(knob, 0.5, 1.0e9), g.get('ClipSpeedOn', COMP, comp))
    return comp, on
# ---- GR_Impl_CP_PhysicalRedirect
g = G(op(PB) + ':GR_Impl_CP_PhysicalRedirect'); N = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(g.path))}
if any('GR228_ClipSpeed' in tid(p) for p in N.values()): out['redirect'] = 'already'
else:
    fset = N['K2Node_VariableSet_0']; assert 'SetGroundFriction' in tid(fset), tid(fset)
    cmc = (N['K2Node_VariableGet_0'], 'CharacterMovement'); assert 'CharacterMovement' in tid(N['K2Node_VariableGet_0']), tid(N['K2Node_VariableGet_0'])
    rot = N['K2Node_CallFunction_23']; assert 'SetActorRotation' in tid(rot), tid(rot)
    br0 = N['K2Node_IfThenElse_0']
    exec_in = lambda p: [q for q in N.values() if any(x.name == 'execute' for x in info(q).input_pins) and (p in src((q, 'execute')))]
    assert not exec_in((rot, 'then')), 'SetActorRotation has a successor'
    assert not exec_in((br0, 'else')), 'IfThenElse_0 else has a successor'
    comp, on = comp_on(g)
    spd = g.get('ClipSpeed', COMP, comp)
    fwd = g.pure('/Script/Engine.Actor:GetActorForwardVector')
    vel = g.pure('/Script/Engine.Actor:GetVelocity')
    bf = g.fn('BreakVector', {'InVec': fwd}); bv = g.fn('BreakVector', {'InVec': vel})
    nv = g.pure('MakeVector', {'X': g.mul((bf, 'X'), spd), 'Y': g.mul((bf, 'Y'), spd), 'Z': (bv, 'Z')})
    y, n = g.branch(on, (rot, 'then')); connect((br0, 'else'), (y[0], 'execute'))
    sv = g.record(g.editor().add_set_member_variable_node('Velocity', '/Script/Engine.MovementComponent'))
    connect(cmc, (sv, 'self')); connect(nv, (sv, 'Velocity')); connect(y, (sv, 'execute'))
    # friction 0 on clip-speed frames
    fo = src((fset, 'GroundFriction')); assert len(fo) == 1, fo
    disconnect((fset, 'GroundFriction')); connect(g.select(on, 0.0, fo[0]), (fset, 'GroundFriction'))
    out['redirect'] = {'branch': y[0].rsplit('.', 1)[-1], 'set': sv.rsplit('.', 1)[-1], 'friction_old': fo[0][0].rsplit('.', 1)[-1]}
# ---- CalculateMaxAcceleration: 0 on clip-speed frames
g2 = G(op(PB) + ':CalculateMaxAcceleration'); N2 = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(g2.path))}
if any('GR228_ClipSpeed' in tid(p) for p in N2.values()): out['accel'] = 'already'
else:
    res = [p for p in N2.values() if 'FunctionResult' in p]; assert len(res) == 1, res
    old = src((res[0], 'ReturnValue')); assert len(old) == 1, old
    comp2, on2 = comp_on(g2)
    disconnect((res[0], 'ReturnValue')); connect(g2.select(on2, 0.0, old[0]), (res[0], 'ReturnValue'))
    out['accel'] = {'old': old[0][0].rsplit('.', 1)[-1]}
st, errs = compile_ok(bp); out['status'] = str(st); out['errs'] = errs[:6]
cb = u.load_asset(CHILD); out['child'] = str(compile_ok(cb)[0])
pawn = u.get_default_object(cb.generated_class()); out['child_profile'] = str(pawn.get_editor_property('GR_Profile'))[:60]
da = u.load_asset(DA); out['da_knob'] = float(da.get_editor_property('GR228_ClipSpeed'))
ok = 'UP_TO_DATE' in str(st) and not errs and 'UP_TO_DATE' in out['child'] and 'None' not in out['child_profile'] and out['da_knob'] == 0.0
out['ok'] = ok
if ok and getattr(builtins, 'V228_SAVE', False):
    save(bp, cb, prof)
    if DA in [p.get_name() for p in LS.get_dirty_content_packages()]: save(da)
    out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('GR228 ' + json.dumps(out, default=str))
