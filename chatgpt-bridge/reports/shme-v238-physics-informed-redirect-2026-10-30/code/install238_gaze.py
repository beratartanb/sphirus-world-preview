"""install238_gaze.py (editor job) - V2.38 travel gaze while the camera is catching up (head / chest not locked to the camera).
Measured (v238c4_j38_c90r o and cut2, balance238): after a jog 90 the pelvis faces the new line (84 deg) while the chest swings 40-70 and
the head stays at 10-25 deg for 1.5-3 s: the AAMS LookAtAimOffset layer (vendor ABP_AAMS_ActionLayer_MM, AimYaw from the control
rotation = the manual-look feature) keeps aiming spine / neck / head at the camera direction, and the auto recentre (CamRecState 1
pending -> 3 recentring) only reaches the new line at ~8.5 s (54 deg/s after a 1.5 s wait).
Fix (GR-owned, behind knob SHM238_Gaze; vendor layer untouched): in SHM_Snapshot, after SHM225_LookAlpha / LookPoint are written from the
inspection focus, while NO inspection target (InspectLookAlpha < 0.01), the camera owner says the player is not steering it
(component CamRecState in [0.5, 3.5] = recentre pending / active) and Speed > SHM238_GazeMinSpeed, the existing LookAt chain (spine_03 /
neck_01 / head, clamps 25 / 30 / 35, 0.25 s interpolation) aims at the travel: point = actor + velocity dir * 500 + 60 up, alpha
SHM238_GazeW. Manual look (CamRecState 0) and inspection keep priority. Idempotent. builtins.V238_SAVE saves. Prints GAZE238 {...}."""
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
out = {'reloaded': names}
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
bp = u.load_asset(AP)
ensure_vars(bp, [('SHM238_Gaze', 'float', 'SHM238'), ('SHM238_GazeW', 'float', 'SHM238'), ('SHM238_GazeMinSpeed', 'float', 'SHM238'), ('SHM238_GazeOn', 'bool', 'SHM238')]); compile_ok(bp)
cdo = u.get_default_object(bp.generated_class())
if abs(float(cdo.get_editor_property('SHM238_GazeW'))) < 1e-6: set_defaults(bp, {'SHM238_GazeW': 1.0, 'SHM238_GazeMinSpeed': 150.0}); compile_ok(bp)
sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
if any('SetSHM238_GazeOn' in tid(p) for p in sn): out['snapshot'] = 'already'
else:
    lp = [p for p in sn if tid(p).endswith('SetSHM225_LookPoint')]; la = [p for p in sn if tid(p).endswith('SetSHM225_LookAlpha')]
    assert len(lp) == 1 and len(la) == 1, (lp, la)
    # the later of the two setters in the exec chain: walk from LookAlpha's 'then' and see if LookPoint follows (else the other way round)
    def follows(a, b, depth=6):
        cur = [a]
        for _ in range(depth):
            nx = [p for p in sn for c in cur if any(q.name == 'execute' for q in info(p).input_pins) and (c, 'then') in src((p, 'execute'))]
            if b in nx: return True
            cur = nx
        return False
    last = lp[0] if follows(la[0], lp[0]) else la[0]
    comp = [p for p in sn if 'GetComponentByClass' in tid(p) or 'GetComponentbyClass' in tid(p)]; assert comp; ct = (comp[0], 'ReturnValue')
    nxt = [p for p in sn if any(q.name == 'execute' for q in info(p).input_pins) and (last, 'then') in src((p, 'execute'))]
    for x in nxt: disconnect((x, 'execute'))
    on = gs.AND(gs.AND(gs.within(gs.get('SHM238_Gaze'), 0.5, 1.0e9), gs.within(gs.get('InspectLookAlpha', COMP, ct), -1.0, 0.01)),
                gs.AND(gs.within(gs.get('CamRecState', COMP, ct), 0.5, 3.5), gs.within(gs.get('Speed', COMP, ct), gs.get('SHM238_GazeMinSpeed'), 1.0e9)))
    tail = gs.set('SHM238_GazeOn', on, (last, 'then'))
    pawn = gs.pure('/Script/Engine.AnimInstance:TryGetPawnOwner')
    loc = gs.fn('BreakVector', {'InVec': gs.pure('/Script/Engine.Actor:K2_GetActorLocation', {'self': pawn})})
    dv = gs.fn('BreakVector', {'InVec': gs.pure('Vector_Normal2D', {'A': gs.get('PlanarVelocity', COMP, ct)})})
    pt = gs.pure('MakeVector', {'X': gs.math((loc, 'X'), gs.mul((dv, 'X'), 500.0)), 'Y': gs.math((loc, 'Y'), gs.mul((dv, 'Y'), 500.0)), 'Z': gs.math((loc, 'Z'), 60.0)})
    tail = gs.set('SHM225_LookPoint', gs.pure('SelectVector', {'A': pt, 'B': gs.get('SHM225_LookPoint'), 'bPickA': gs.get('SHM238_GazeOn')}), tail)
    tail = gs.set('SHM225_LookAlpha', gs.select(gs.get('SHM238_GazeOn'), gs.get('SHM238_GazeW'), gs.get('SHM225_LookAlpha')), tail)
    for x in nxt: connect(tail, (x, 'execute'))
    out['snapshot'] = {'after': last.rsplit('.', 1)[-1], 'next': [x.rsplit('.', 1)[-1] for x in nxt]}
st, errs = compile_ok(bp); out['abp'] = [str(st), errs[:6]]
cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class()); out['knobs'] = {k: float(cdo.get_editor_property(k)) for k in ('SHM238_Gaze', 'SHM238_GazeW', 'SHM238_GazeMinSpeed')}
ok = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child'] and out['knobs']['SHM238_Gaze'] == 0.0
out['ok'] = ok
if ok and getattr(builtins, 'V238_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('GAZE238 ' + json.dumps(out, default=str))
