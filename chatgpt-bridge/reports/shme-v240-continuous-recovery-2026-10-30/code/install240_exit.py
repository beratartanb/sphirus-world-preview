"""install240_exit.py (editor job) - V2.40: a takeover plan HANDS its final heading to the body frame when it ends (behind SHM239_Own).
Measured (v240c30_j39_lr_tk vs j39_rl_tk, 30 FPS): during the takeover the actor yaw follows the plan exactly (+90 = travel at 7.2 s), but
when the plan's W ends GR's facing writer (CP_PhysicalRedirect reads the SHME body frame GR234_LocoYaw = component LocoYaw, V2.34) turned
the actor back to the frame's 0 deg in 0.5 s while the capsule kept travelling at +88: a sideways jog (A_CT_Jog_Right) and a lateral stop
(A_LS_Jog_Right_Stop, 36 cm). The component re-latched its frame to the new direction in rl (-90 at 6.57) but not in lr: its frame rule
does not know a takeover. Exit order: the plan owns heading until its W ends -> on that frame the body frame takes the plan's final heading:
  SHM240_WasTk := SHM239_OwnOn AND curve SHM239_Tgt > 500        (a takeover plan was running last frame)
  on WasTk AND NOT OwnOn: component LocoYaw := actor yaw, LocoState := 1 (the latched state the component itself uses)
One frame, at the plan's own end - no hold, no delay. Idempotent (marker SHM240_WasTk). builtins.V240_SAVE saves. Prints EXIT240 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj
import builtins, json
LS = u.EditorLoadingAndSavingUtils
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
if 'SHM240_WasTk' in [str(v) for v in B.list_variables(bp)]: out['patch'] = 'already'
else:
    ensure_vars(bp, [('SHM240_WasTk', 'bool', 'SHM240')]); compile_ok(bp)
    sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
    comp = [p for p in sn if 'GetComponentByClass' in tid(p) or 'GetComponentbyClass' in tid(p)]; assert comp; ct = (comp[0], 'ReturnValue')
    last = [p for p in sn if tid(p).endswith('SetSHM240_EDB')]; assert len(last) == 1
    nxt = [p for p in sn if any(q.name == 'execute' for q in info(p).input_pins) and (last[0], 'then') in src((p, 'execute'))]
    for x in nxt: disconnect((x, 'execute'))
    castn = [s_[0] for s_ in src((last[0], 'execute'))]; assert len(castn) == 1          # the cast whose 'then' feeds SetSHM240_EDB
    pawn = gs.pure('/Script/Engine.AnimInstance:TryGetPawnOwner')
    yaw = gs.yaw(gs.pure('/Script/Engine.Actor:K2_GetActorRotation', {'self': pawn}))
    exitnow = gs.AND(gs.within(gs.get('SHM239_Own'), 0.5, 1.0e9), gs.AND(gs.get('SHM240_WasTk'), gs.NOT(gs.get('SHM239_OwnOn'))))
    bt, be = gs.branch(exitnow, (last[0], 'then'))
    t = gs.set('LocoYaw', yaw, bt, COMP, ct); t = gs.set('LocoState', 1.0, t, COMP, ct)
    tgt = gs.pure('/Script/Engine.AnimInstance:GetCurveValue', {'CurveName': 'SHM239_Tgt'})
    w1 = gs.set('SHM240_WasTk', gs.AND(gs.get('SHM239_OwnOn'), gs.within(tgt, 500.0, 1.0e9)), t)
    connect(be, (w1[0], 'execute')); connect((castn[0], 'CastFailed'), (w1[0], 'execute'))   # a failed cast must not stop the snapshot
    for x in nxt: connect(w1, (x, 'execute'))
    out['patch'] = 'exit hand-off to the body frame'
st, errs = compile_ok(bp); out['abp'] = [str(st), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child']
if out['ok'] and getattr(builtins, 'V240_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('EXIT240 ' + json.dumps(out, default=str))
