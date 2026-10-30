"""install239_ext.py (editor job) - V2.39: planned velocity change vs REAL external effect (behind SHM239_Own; residual, not a new detector).
V2.38 silenced the recovery families 1 / 6 for the whole plan + 1.6 s (FamOff), because the SHME push detector (pushRaw) reads the clip's
own speed restore as a shove. That also blocked real shoves / wall hits during a plan. With the V2.28 clip-speed contract the capsule
velocity is DEFINED by the plan: GR writes Velocity = Forward * ClipSpeed every tick. So the plan can explain its own velocity exactly:
  commanded (frame N) = last frame's component ClipSpeed along the actor yaw   (what GR wrote this tick, ClipSpeedOn last frame)
  measured  (frame N) = pawn velocity after movement (2D)
  SHM239_Resid = |measured - commanded| (0 when the clip did not own the speed)
  SHM239_Ext   = (SHM239_Own AND Resid > SHM239_ExtThr 80 cm/s) latched SHM239_ExtHold 0.6 s   (impulse, wall, ledge: the plan cannot
                 explain it; planned acceleration is inside the commanded value, so it never trips this)
While Ext: the plan YIELDS - SHM238_FamOff, SHM239_OwnOn, SHM238_On and the component ClipSpeedOn are AND NOT Ext: the capsule keeps
the real velocity (CMC), the database owner and the clip contracts stand down, and the existing pushRaw recovery (families 1 / 6) may act.
Idempotent (marker SHM239_ExtThr). builtins.V239_SAVE saves. Prints EXT239 {...}."""
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
if 'SHM239_ExtThr' in [str(v) for v in B.list_variables(bp)]: out['patch'] = 'already'
else:
    ensure_vars(bp, [('SHM239_ExtThr', 'float', 'SHM239'), ('SHM239_ExtHold', 'float', 'SHM239'), ('SHM239_Resid', 'float', 'SHM239'),
                     ('SHM239_Ext', 'bool', 'SHM239'), ('SHM239_ExtT0', 'float', 'SHM239'), ('SHM239_CsPrev', 'float', 'SHM239'), ('SHM239_ConPrev', 'bool', 'SHM239')]); compile_ok(bp)
    set_defaults(bp, {'SHM239_ExtThr': 80.0, 'SHM239_ExtHold': 0.6}); compile_ok(bp)
    sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
    comp = [p for p in sn if 'GetComponentByClass' in tid(p) or 'GetComponentbyClass' in tid(p)]; assert comp; ct = (comp[0], 'ReturnValue')
    last = [p for p in sn if tid(p).endswith('SetSHM239_TkPar')]; assert len(last) == 1
    nxt = [p for p in sn if any(q.name == 'execute' for q in info(p).input_pins) and (last[0], 'then') in src((p, 'execute'))]
    for x in nxt: disconnect((x, 'execute'))
    pawn = gs.pure('/Script/Engine.AnimInstance:TryGetPawnOwner')
    vel = gs.fn('BreakVector', {'InVec': gs.pure('/Script/Engine.Actor:GetVelocity', {'self': pawn})})
    yaw = gs.yaw(gs.pure('/Script/Engine.Actor:K2_GetActorRotation', {'self': pawn}))
    cx = gs.mul(gs.pure(M + 'DegCos', {'A': yaw}), gs.get('SHM239_CsPrev')); cy = gs.mul(gs.pure(M + 'DegSin', {'A': yaw}), gs.get('SHM239_CsPrev'))
    res = gs.pure(M + 'VSize', {'A': gs.pure(M + 'MakeVector', {'X': gs.math((vel, 'X'), cx, -1), 'Y': gs.math((vel, 'Y'), cy, -1), 'Z': 0.0})})
    t = gs.set('SHM239_Resid', gs.select(gs.get('SHM239_ConPrev'), res, 0.0), (last[0], 'then'))
    now = gs.pure('Now')
    hit = gs.AND(gs.AND(gs.within(gs.get('SHM239_Own'), 0.5, 1.0e9), gs.get('SHM239_ConPrev')), gs.within(gs.get('SHM239_Resid'), gs.get('SHM239_ExtThr'), 1.0e9))
    t = gs.set('SHM239_ExtT0', gs.select(hit, now, gs.get('SHM239_ExtT0')), t)
    t = gs.set('SHM239_Ext', gs.OR(hit, gs.AND(gs.get('SHM239_Ext'), gs.within(gs.sub(now, gs.get('SHM239_ExtT0')), -1.0e9, gs.get('SHM239_ExtHold')))), t)
    t = gs.set('SHM239_CsPrev', gs.get('ClipSpeed', COMP, ct), t)
    t = gs.set('SHM239_ConPrev', gs.get('ClipSpeedOn', COMP, ct), t)
    for x in nxt: connect(t, (x, 'execute'))
    out['patch'] = {'residual': 'added'}
    # the plan yields while Ext
    for suffix, pin in (('SetSHM238_FamOff', 'SHM238_FamOff'), ('SetSHM239_OwnOn', 'SHM239_OwnOn'), ('SetSHM238_On', 'SHM238_On'), ('SetClipSpeedOn', 'ClipSpeedOn')):
        ss = [p for p in sn if tid(p).endswith(suffix)]; assert ss, suffix
        for s_ in ss:
            old = src((s_, pin)); assert len(old) == 1, (suffix, old)
            disconnect((s_, pin)); connect(gs.AND(old[0], gs.NOT(gs.get('SHM239_Ext'))), (s_, pin))
        out['patch'][suffix] = len(ss)
st, errs = compile_ok(bp); out['abp'] = [str(st), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child']
if out['ok'] and getattr(builtins, 'V239_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('EXT239 ' + json.dumps(out, default=str))
