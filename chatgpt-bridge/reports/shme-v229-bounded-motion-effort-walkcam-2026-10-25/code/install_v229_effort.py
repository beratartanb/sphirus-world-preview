"""install_v229_effort.py (editor job) - V2.29 effort consumer on the movement side (BP_GR_Player). The SHME component computes
EffortAccScale / EffortTurnScale (SHM_UpdateState, 1.0 when DA_SHM EffortEnabled is false = the switch; installed OFF):
 (a) CalculateMaxAcceleration: ReturnValue = old x guard(EffortAccScale)   (re-acceleration after repeated hard efforts is slower; the
     acceleration vector keeps its direction and stays > 0: SHME's intent read is unchanged)
 (b) GR_Impl_CP_PhysicalRedirect: the final GroundFriction (the V2.28 Select(clip-speed on -> 0, else redirect friction)) gets its
     redirect-friction branch x guard(EffortTurnScale): CMC friction is what turns / reverses the velocity toward the input, so a busy
     support (acceleration against the new request) or accumulated exertion redirects more slowly = the body carries further, MM plans
     the extra braking / support steps from that trajectory. Clip-speed frames (friction 0, V2.28) are untouched.
guard(x) = x if 0.05 < x < 10 else 1.0 (a component that never ticked -> 0 -> neutral). Idempotent (EffortAccScale getter present).
builtins.V229_SAVE saves BP_GR_Player + BP_PBI_Player. Prints EFFORT229 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, op, arg
import builtins, json
LS = u.EditorLoadingAndSavingUtils
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
PB = '/Game/GraceRanger/BP_GR_Player'; CHILD = '/Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player'
COMP = '/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent.BP_SHM_HumanMotionComponent_C'
DAS = {'/Game/GraceRanger/Profiles/DA_GR_LocomotionBehavior', '/Game/GraceRanger/SHME/DA_SHM_Response_Default', '/Game/GraceRanger/Experimental/BodyInertia/DA_PBI_Prototype'}
dirty = list(LS.get_dirty_content_packages()); names = [p.get_name() for p in dirty]
assert all(n in DAS or n in (PB, CHILD) for n in names), ('unexpected dirty', names)
rl = [p for p in dirty if p.get_name() in DAS]
if rl: LS.reload_packages(rl, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
out = {'reloaded': [p.get_name() for p in rl]}
bp = u.load_asset(PB)
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
def guard(g, name, comp):
    x = g.get(name, COMP, comp)
    return g.select(g.within(x, 0.05, 10.0), x, 1.0)
# (a) max acceleration
g2 = G(op(PB) + ':CalculateMaxAcceleration'); N2 = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(g2.path))}
if any('EffortAccScale' in tid(p) for p in N2.values()): out['accel'] = 'already'
else:
    res = [p for p in N2.values() if 'FunctionResult' in p]; assert len(res) == 1, res
    old = src((res[0], 'ReturnValue')); assert len(old) == 1, old
    comp2 = g2.pure('/Script/Engine.Actor:GetComponentByClass', {'ComponentClass': COMP})
    nv = g2.mul(old[0], guard(g2, 'EffortAccScale', comp2))
    disconnect((res[0], 'ReturnValue')); connect(nv, (res[0], 'ReturnValue'))
    out['accel'] = {'old': old[0][0].rsplit('.', 1)[-1]}
# (b) redirect friction
g = G(op(PB) + ':GR_Impl_CP_PhysicalRedirect'); N = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(g.path))}
if any('EffortTurnScale' in tid(p) for p in N.values()): out['friction'] = 'already'
else:
    fs = [p for p in N.values() if tid(p).endswith('|SetGroundFriction')]
    cand = []
    for p in fs:
        s0 = src((p, 'GroundFriction'))
        if len(s0) == 1 and 'SelectFloat' in tid(s0[0][0]):
            sel = s0[0][0]
            if any('ClipSpeedOn' in tid(q[0]) or 'GR228' in tid(q[0]) or 'ANDBoolean' in tid(q[0]) for q in src((sel, 'bPickA'))): cand.append((p, sel))
    assert len(cand) == 1, ('friction set', [(tid(p)[-30:], [tid(q[0])[-30:] for q in src((p, 'GroundFriction'))]) for p in fs])
    fset, sel = cand[0]
    ob = src((sel, 'B')); assert len(ob) == 1, ('B source', ob)
    comp = g.pure('/Script/Engine.Actor:GetComponentByClass', {'ComponentClass': COMP})
    nb = g.mul(ob[0], guard(g, 'EffortTurnScale', comp))
    disconnect((sel, 'B')); connect(nb, (sel, 'B'))
    out['friction'] = {'set': fset.rsplit('.', 1)[-1], 'select': sel.rsplit('.', 1)[-1], 'old': ob[0][0].rsplit('.', 1)[-1]}
st, errs = compile_ok(bp); out['status'] = str(st); out['errs'] = errs[:6]
cb = u.load_asset(CHILD); out['child'] = str(compile_ok(cb)[0])
pawn = u.get_default_object(cb.generated_class()); out['child_profile'] = str(pawn.get_editor_property('GR_Profile'))[:60]
ok = 'UP_TO_DATE' in str(st) and not errs and 'UP_TO_DATE' in out['child'] and 'None' not in out['child_profile']
out['ok'] = ok
if ok and getattr(builtins, 'V229_SAVE', False): save(bp, cb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('EFFORT229 ' + json.dumps(out, default=str))
