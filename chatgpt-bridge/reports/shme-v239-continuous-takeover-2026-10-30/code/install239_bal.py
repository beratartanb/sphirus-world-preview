"""install239_bal.py (editor job) - V2.39 live balance / momentum read (lightweight, explainable; NOT a balance controller).
Every frame, from live game state only (no animation phase): capsule velocity v (2D, heading hv), the player's desired direction (component
DesiredVelocity), and the per-contact impulse budget the plans use (SHM239_Bc = 0.55 g x one contact period 0.31 s = 167 cm/s):
  dA    = |NormalizeAxis(desired yaw - hv)|                       requested change of the travel direction
  vt    = 0.55 * min(|desired|, v)                                speed the first new support keeps (the plans' plant exit speed)
  dv    = sqrt(v^2 + vt^2 - 2 v vt cos dA)                         velocity change the supports must deliver
  NeedN = dv / Bc                                                  support contacts needed at the budget
  Bal   = 3 if SHM239_Ext (unexplained external residual = loss-of-balance CANDIDATE)
          0 if no input / v < 120 / dA < 35 (Stable: steering, no plan change)
          1 if NeedN <= 1.75 (Controlled Redirect: brake + support change inside the normal contact rhythm)
          2 otherwise (Recovery Step: an extra braking / catch support is needed)
Telemetry-only (SHM239_Bal, SHM239_NeedN): the plans' own contact roles come from simulating the INHERITED velocity through the same
budget (gen239_tk); this read states, frame by frame, which class the live state is in, so the chosen plan can be checked against it.
Idempotent (marker SHM239_Bc). builtins.V239_SAVE saves. Prints BAL239 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj
import builtins, json
LS = u.EditorLoadingAndSavingUtils; M = '/Script/Engine.KismetMathLibrary:'
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CPA = AP.replace('Base', '')
COMP = '/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent.BP_SHM_HumanMotionComponent_C'
DAS = {'/Game/GraceRanger/Profiles/DA_GR_LocomotionBehavior', '/Game/GraceRanger/SHME/DA_SHM_Response_Default', '/Game/GraceRanger/Experimental/BodyInertia/DA_PBI_Prototype'}
dirty = list(LS.get_dirty_content_packages()); names = [p.get_name() for p in dirty]
assert all(n in DAS or n in (AP, CPA) for n in names), ('unexpected dirty', names)
if dirty: LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
out = {'reloaded': names}
bp = u.load_asset(AP)
if 'SHM239_Bc' in [str(v) for v in B.list_variables(bp)]: out['patch'] = 'already'
else:
    ensure_vars(bp, [('SHM239_Bc', 'float', 'SHM239'), ('SHM239_Bal', 'float', 'SHM239'), ('SHM239_NeedN', 'float', 'SHM239')]); compile_ok(bp)
    set_defaults(bp, {'SHM239_Bc': 167.0}); compile_ok(bp)
    sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
    comp = [p for p in sn if 'GetComponentByClass' in tid(p) or 'GetComponentbyClass' in tid(p)]; assert comp; ct = (comp[0], 'ReturnValue')
    last = [p for p in sn if tid(p).endswith('SetSHM239_ConPrev')]; assert len(last) == 1, 'install239_ext first'
    nxt = [p for p in sn if any(q.name == 'execute' for q in info(p).input_pins) and (last[0], 'then') in src((p, 'execute'))]
    for x in nxt: disconnect((x, 'execute'))
    pawn = gs.pure('/Script/Engine.AnimInstance:TryGetPawnOwner')
    vv = gs.pure('/Script/Engine.Actor:GetVelocity', {'self': pawn}); vb = gs.fn('BreakVector', {'InVec': vv})
    v = gs.pure(M + 'VSize', {'A': gs.pure(M + 'MakeVector', {'X': (vb, 'X'), 'Y': (vb, 'Y'), 'Z': 0.0})})
    hv = gs.pure(M + 'DegAtan2', {'Y': (vb, 'Y'), 'X': (vb, 'X')})
    dvv = gs.get('DesiredVelocity', COMP, ct); db = gs.fn('BreakVector', {'InVec': dvv})
    des = gs.pure(M + 'DegAtan2', {'Y': (db, 'Y'), 'X': (db, 'X')}); dsp = gs.pure(M + 'VSize', {'A': dvv})
    dA = gs.pure(M + 'Abs', {'A': gs.pure(M + 'NormalizeAxis', {'Angle': gs.sub(des, hv)})})
    vt = gs.mul(gs.pure(M + 'FMin', {'A': dsp, 'B': v}), 0.55)
    dv2 = gs.math(gs.math(gs.mul(v, v), gs.mul(vt, vt), 1), gs.mul(gs.mul(gs.mul(v, vt), 2.0), gs.pure(M + 'DegCos', {'A': dA})), -1)
    dv = gs.pure(M + 'Sqrt', {'A': gs.pure(M + 'FMax', {'A': dv2, 'B': 0.0})})
    t = gs.set('SHM239_NeedN', gs.pure(M + 'SafeDivide', {'A': dv, 'B': gs.get('SHM239_Bc')}), (last[0], 'then'))
    stable = gs.OR(gs.OR(gs.within(dsp, -1.0, 30.0), gs.within(v, -1.0, 120.0)), gs.within(dA, -1.0, 35.0))
    cls = gs.select(stable, 0.0, gs.select(gs.within(gs.get('SHM239_NeedN'), -1.0, 1.75), 1.0, 2.0))
    t = gs.set('SHM239_Bal', gs.select(gs.get('SHM239_Ext'), 3.0, cls), t)
    for x in nxt: connect(t, (x, 'execute'))
    out['patch'] = 'live balance read'
st, errs = compile_ok(bp); out['abp'] = [str(st), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child']
if out['ok'] and getattr(builtins, 'V239_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('BAL239 ' + json.dumps(out, default=str))
