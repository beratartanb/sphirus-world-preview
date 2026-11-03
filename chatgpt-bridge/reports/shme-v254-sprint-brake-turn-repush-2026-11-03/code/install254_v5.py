"""install254_v5.py (editor job, write manifest = ABP base + child): V2.54 the authored turn-around keeps its own head / chest.
Measured (v254fcap s54_revR rvcS + LTP toes / shoulders): after the turn the feet point along the new travel (toes 150-180 deg) but the
shoulder line stays ~25 deg behind and the face looks back toward the camera (old travel) from the turn (6.5 s) until the V2.38 travel
gaze switches on at 7.2 s: the vendor AAMS LookAtAimOffset layer aims spine / neck / head at the control rotation while the camera auto
recentre is idle (CamRecState 0 for a 180 - error > CamRecMaxErr), and the V2.38 gaze only runs while CamRecState is 1..3.
Patch (SHM_Snapshot, vendor layer untouched):
  plan = SHM254_Turn > 0.5 AND curve SHM254_Own > 0.3 AND component InspectLookAlpha < 0.01
  SetSHM238_GazeOn := old OR plan
  every travel-gaze LookPoint select (SelectVector whose A is the velocity point): A := plan ? actor + actor forward x 500 + 60 up : old A
(the LookAt chain aims along the body's own facing = no aim offset on top of the clip's authored head / chest lead; the V2.38 GazeA
smoothing still fades it in/out). Inspection keeps priority. Idempotent (variable SHM254_V5). builtins.V254_SAVE saves. Prints V5254 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, arg
import builtins, json
LS = u.EditorLoadingAndSavingUtils
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CPA = AP.replace('Base', '')
COMP = '/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent.BP_SHM_HumanMotionComponent_C'
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
out = {}
dirty = [p for p in LS.get_dirty_content_packages() if 'ABP_GR_MotionMatching' in p.get_name()]
if dirty:
    out['reloaded'] = [p.get_name().split('/')[-1] for p in dirty]; LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
bp = u.load_asset(AP); V = [str(v) for v in B.list_variables(bp)]
assert 'SHM254_CancelMinV' in V and 'SHM238_GazeOn' in V, 'install254_v4 / V2.38 gaze first'
if 'SHM254_V5' in V: out['patch'] = 'already'
else:
    ensure_vars(bp, [('SHM254_V5', 'bool', 'SHM')]); compile_ok(bp)
    sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
    comp = [p for p in sn if 'GetComponentByClass' in tid(p) or 'GetComponentbyClass' in tid(p)]; assert comp, 'component getter'; ct = (comp[0], 'ReturnValue')
    own = gs.pure('/Script/Engine.AnimInstance:GetCurveValue', {'CurveName': 'SHM254_Own'})
    plan = gs.AND(gs.AND(gs.within(gs.get('SHM254_Turn'), 0.5, 1.0e9), gs.within(own, 0.3, 1.0e9)), gs.within(gs.get('InspectLookAlpha', COMP, ct), -1.0, 0.01))
    go = [p for p in sn if tid(p).endswith('|SetSHM238_GazeOn')]; assert len(go) == 1, go
    g0 = src((go[0], 'SHM238_GazeOn')); assert len(g0) == 1, g0
    disconnect((go[0], 'SHM238_GazeOn')); connect(gs.OR(g0[0], plan), (go[0], 'SHM238_GazeOn'))
    pawn = gs.pure('/Script/Engine.AnimInstance:TryGetPawnOwner')
    loc = gs.fn('BreakVector', {'InVec': gs.pure('/Script/Engine.Actor:K2_GetActorLocation', {'self': pawn})})
    fw = gs.fn('BreakVector', {'InVec': gs.pure('/Script/Engine.Actor:GetActorForwardVector', {'self': pawn})})
    fpt = gs.pure('MakeVector', {'X': gs.math((loc, 'X'), gs.mul((fw, 'X'), 500.0)), 'Y': gs.math((loc, 'Y'), gs.mul((fw, 'Y'), 500.0)), 'Z': gs.math((loc, 'Z'), 60.0)})
    out['lookpoint'] = []
    for p in [p for p in sn if tid(p).endswith('|SetSHM225_LookPoint')]:
        s = src((p, 'SHM225_LookPoint'))
        if not s or 'SelectVector' not in tid(s[0][0]): continue
        a0 = src((s[0][0], 'A'))
        if not a0 or 'MakeVector' not in tid(a0[0][0]): continue
        disconnect((s[0][0], 'A')); connect(gs.pure('SelectVector', {'A': fpt, 'B': a0[0], 'bPickA': plan}), (s[0][0], 'A')); out['lookpoint'].append(p.rsplit('.', 1)[-1])
    assert out['lookpoint'], 'travel-gaze LookPoint select not found'
st_, errs = compile_ok(bp); out['abp'] = [str(st_), errs[:6]]; cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class()); out['knob'] = str(cdo.get_editor_property('SHM254_Turn'))
out['ok'] = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child'] and out['knob'] == '0.0'
if out['ok'] and getattr(builtins, 'V254_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()]
print('V5254 ' + json.dumps(out, default=str))
