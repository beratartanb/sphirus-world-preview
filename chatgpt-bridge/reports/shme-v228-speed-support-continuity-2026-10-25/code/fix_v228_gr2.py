"""fix_v228_gr2.py (editor job) - V2.28 movement patch, second pass. Measured (v228t1 ph3 rhC): CalculateMaxAcceleration = 0 on clip-speed
frames zeroed the CharacterMovement acceleration vector, which SHME reads as the player's intent (HasIntent false 1 frame later,
RedirectEnd 4 = lost, the hold died, Motion Matching went to the walk stop). Changes:
 (a) CalculateMaxAcceleration: the V2.28 Select is bypassed (ReturnValue <- the original source again); the GR228 nodes stay unconnected.
 (b) GR_Impl_CP_PhysicalRedirect: the velocity write pre-compensates the acceleration the CMC will apply this frame along the input:
     v_set = ClipSpeed - GetMaxAcceleration * dt * dot(ActorForward, component DesiredDir)  (friction is 0 on those frames, so after the
     CMC integrates its acceleration the velocity equals ClipSpeed exactly; the acceleration vector itself is untouched = intent kept).
Idempotent per part. builtins.V228_SAVE saves BP_GR_Player + BP_PBI_Player. Prints GR228FIX {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, op, arg
import builtins, json
LS = u.EditorLoadingAndSavingUtils; M = '/Script/Engine.KismetMathLibrary:'
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
PB = '/Game/GraceRanger/BP_GR_Player'; CHILD = '/Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player'
ABPS = ('/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase', '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatching')
COMP = '/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent.BP_SHM_HumanMotionComponent_C'
DAS = {'/Game/GraceRanger/Profiles/DA_GR_LocomotionBehavior', '/Game/GraceRanger/SHME/DA_SHM_Response_Default', '/Game/GraceRanger/Experimental/BodyInertia/DA_PBI_Prototype'}
dirty = list(LS.get_dirty_content_packages()); names = [p.get_name() for p in dirty]
assert all(n in DAS or n in ABPS or n in (PB, CHILD) for n in names), ('unexpected dirty', names)
rl = [p for p in dirty if p.get_name() in DAS or p.get_name() in ABPS]
if rl: LS.reload_packages(rl, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
out = {'reloaded': [p.get_name() for p in rl]}
bp = u.load_asset(PB)
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
# (a) CalculateMaxAcceleration bypass
g2 = G(op(PB) + ':CalculateMaxAcceleration'); N2 = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(g2.path))}
res = [p for p in N2.values() if 'FunctionResult' in p]; assert len(res) == 1, res
cur = src((res[0], 'ReturnValue')); assert len(cur) == 1, cur
if 'SelectFloat' in tid(cur[0][0]) and any('GR228_ClipSpeed' in tid(s[0]) for k in ('bPickA',) for s in src((cur[0][0], k))) or any('GR228' in tid(s[0]) for s in src((cur[0][0], 'bPickA'))):
    old = src((cur[0][0], 'B')); assert len(old) == 1, old
    disconnect((res[0], 'ReturnValue')); connect(old[0], (res[0], 'ReturnValue')); out['accel'] = 'bypassed -> ' + old[0][0].rsplit('.', 1)[-1]
else:
    # the bPickA chain is AND(knob>0.5, ClipSpeedOn): look one level deeper for the GR228 getter
    def has228(p, depth=0):
        if depth > 4: return False
        if 'GR228' in tid(p): return True
        return any(has228(s[0], depth + 1) for q in info(p).input_pins for s in src((p, q.name)))
    if 'SelectFloat' in tid(cur[0][0]) and has228(cur[0][0]):
        old = src((cur[0][0], 'B')); assert len(old) == 1, old
        disconnect((res[0], 'ReturnValue')); connect(old[0], (res[0], 'ReturnValue')); out['accel'] = 'bypassed(deep) -> ' + old[0][0].rsplit('.', 1)[-1]
    else: out['accel'] = 'already/not-ours: ' + tid(cur[0][0])[-40:]
# (b) PhysicalRedirect velocity pre-compensation
g = G(op(PB) + ':GR_Impl_CP_PhysicalRedirect'); N = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(g.path))}
sv = [p for p in N.values() if tid(p).endswith('|SetVelocity') and any('MakeVector' in tid(s[0]) for s in src((p, 'Velocity')))]
mine = None
for p in sv:
    mv = src((p, 'Velocity'))[0][0]
    xs = src((mv, 'X'))
    if xs and 'MapRangeUnclamped' in tid(xs[0][0]) and any('ClipSpeed' in tid(s[0]) for s in src((xs[0][0], 'OutRangeB'))): mine = (p, mv); break
assert mine, ('clip-speed SetVelocity not found', [tid(p)[-30:] for p in sv])
p, mv = mine
if any('GetMaxAcceleration' in tid(s[0]) for q in ('X',) for s0 in src((mv, q)) for s in src((s0[0], 'OutRangeB')) for s in [s]) or out.get('velocity') == 'already':
    out['velocity'] = 'already'
else:
    xs = src((mv, 'X'))[0][0]; ys = src((mv, 'Y'))[0][0]
    spd = src((xs, 'OutRangeB'))[0]
    comp = src((spd[0], 'self'))[0]
    cmc = (N['K2Node_VariableGet_0'], 'CharacterMovement')
    import sys
    def step(name):
        out['step'] = name; print('GR228FIX step ' + name)
    step('amax'); amax = g.pure('/Script/Engine.CharacterMovementComponent:GetMaxAcceleration', {'self': cmc})
    step('dt'); dt = g.get('DeltaTime', COMP, comp)
    step('fwd'); fwd = g.pure('/Script/Engine.Actor:GetActorForwardVector')
    step('ddir'); ddir = g.pure(M + 'Vector_Normal2D', {'A': g.get('DesiredDir', COMP, comp), 'Tolerance': 0.0001})
    step('iF'); iF = g.pure(M + 'Dot_VectorVector', {'A': fwd, 'B': ddir})
    step('adt'); adt = g.mul(amax, dt)
    step('vset'); vset = g.math(spd, g.mul(adt, iF), -1)                      # ClipSpeed - a*dt*iF
    for node in (xs, ys):
        disconnect((node, 'OutRangeB')); connect(vset, (node, 'OutRangeB'))
    out['velocity'] = 'compensated'
st, errs = compile_ok(bp); out['status'] = str(st); out['errs'] = errs[:6]
cb = u.load_asset(CHILD); out['child'] = str(compile_ok(cb)[0])
pawn = u.get_default_object(cb.generated_class()); out['child_profile'] = str(pawn.get_editor_property('GR_Profile'))[:60]
ok = 'UP_TO_DATE' in str(st) and not errs and 'UP_TO_DATE' in out['child'] and 'None' not in out['child_profile']
out['ok'] = ok
if ok and getattr(builtins, 'V228_SAVE', False): save(bp, cb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('GR228FIX ' + json.dumps(out, default=str))
