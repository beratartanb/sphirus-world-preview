"""install238_gaze2.py (editor job) - V2.38 travel gaze, smoothed weight.
Measured (v238c5_j38_c90r_cut3 / c90l_cut3): the travel gaze turned the head onto the travel after the cut (head 43-68 deg vs 10-24 with
pelvis ~85) but SHM225_LookAlpha stepped 0 -> 1 in one frame (the LookAt nodes interpolate the TARGET, not the alpha) -> head pop
125-141 m/s2. Patch on install238_gaze.py's chain: after SetSHM238_GazeOn,
  SHM238_GazeA := FInterpTo(GazeA, GazeOn ? GazeW : 0, world dt, SHM238_GazeRate (4 /s, ~0.3 s))
and the two travel-gaze setters select on (GazeA > 0.01 AND no inspection) with alpha = GazeA (inspection keeps priority).
Idempotent. builtins.V238_SAVE saves. Prints GAZE238B {...}."""
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
ensure_vars(bp, [('SHM238_GazeA', 'float', 'SHM238'), ('SHM238_GazeRate', 'float', 'SHM238')]); compile_ok(bp)
cdo = u.get_default_object(bp.generated_class())
if abs(float(cdo.get_editor_property('SHM238_GazeRate'))) < 1e-6: set_defaults(bp, {'SHM238_GazeRate': 4.0}); compile_ok(bp)
sg = pn(graph(bp, 'SHM_Snapshot')); gs = G(sg); sn = [pn(n) for n in B.find_nodes(obj(sg))]
def nxt_of(p): return [q for q in sn if any(x.name == 'execute' for x in info(q).input_pins) and (p, 'then') in src((q, 'execute'))]
if any('SetSHM238_GazeA' in tid(p) for p in sn): out['snapshot'] = 'already'
else:
    gon = [p for p in sn if tid(p).endswith('SetSHM238_GazeOn')]; assert len(gon) == 1, gon
    n1 = nxt_of(gon[0]); assert len(n1) == 1 and tid(n1[0]).endswith('SetSHM225_LookPoint'), [tid(p) for p in n1]
    n2 = nxt_of(n1[0]); assert len(n2) == 1 and tid(n2[0]).endswith('SetSHM225_LookAlpha'), [tid(p) for p in n2]
    comp = [p for p in sn if 'GetComponentByClass' in tid(p) or 'GetComponentbyClass' in tid(p)]; assert comp; ct = (comp[0], 'ReturnValue')
    disconnect((n1[0], 'execute'))
    tgt = gs.select(gs.get('SHM238_GazeOn'), gs.get('SHM238_GazeW'), 0.0)
    ga = gs.pure('FInterpTo', {'Current': gs.get('SHM238_GazeA'), 'Target': tgt, 'DeltaTime': gs.pure('DT'), 'InterpSpeed': gs.get('SHM238_GazeRate')})
    t = gs.set('SHM238_GazeA', ga, (gon[0], 'then')); connect(t, (n1[0], 'execute'))
    use = gs.AND(gs.within(gs.get('SHM238_GazeA'), 0.01, 1.0e9), gs.within(gs.get('InspectLookAlpha', COMP, ct), -1.0, 0.01))
    # LookPoint: the SelectVector feeding it - re-point its bPickA; LookAlpha: replace its value
    sv = src((n1[0], 'SHM225_LookPoint')); assert len(sv) == 1 and 'SelectVector' in tid(sv[0][0]), sv
    disconnect((sv[0][0], 'bPickA')); connect(use, (sv[0][0], 'bPickA'))
    disconnect((n2[0], 'SHM225_LookAlpha')); connect(gs.select(use, gs.get('SHM238_GazeA'), gs.get('SHM225_LookAlpha')), (n2[0], 'SHM225_LookAlpha'))
    out['snapshot'] = {'gazeon': gon[0].rsplit('.', 1)[-1], 'point': n1[0].rsplit('.', 1)[-1], 'alpha': n2[0].rsplit('.', 1)[-1]}
st, errs = compile_ok(bp); out['abp'] = [str(st), errs[:6]]
cpb = u.load_asset(CPA); out['abp_child'] = str(compile_ok(cpb)[0])
cdo = u.get_default_object(bp.generated_class()); out['knobs'] = {k: float(cdo.get_editor_property(k)) for k in ('SHM238_Gaze', 'SHM238_GazeRate')}
ok = 'UP_TO_DATE' in out['abp'][0] and not out['abp'][1] and 'UP_TO_DATE' in out['abp_child'] and out['knobs']['SHM238_Gaze'] == 0.0
out['ok'] = ok
if ok and getattr(builtins, 'V238_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in LS.get_dirty_content_packages()]
print('GAZE238B ' + json.dumps(out, default=str))
