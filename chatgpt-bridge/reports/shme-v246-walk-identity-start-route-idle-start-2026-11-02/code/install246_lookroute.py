"""install246_lookroute.py (editor job, write manifest = ABP base + child): V2.46 look-relative LATERAL START route.
The LS lateral-start condition in Update_MotionMatching tests |Direction| in [65,115] where Direction = CalculateDirection(Velocity, actor
rotation) = BODY-relative. With look-driven locomotion the request is LOOK-relative: after an explored strafe the body can face 56-180 deg
away from the look, so a "left" request reads as 33 deg (turning jog start) or ~180 deg (BACKWARD jog start: 23+39 cm foot pivot at real
time, V2.45 j45_sl). Patch (knob SHM246_LookRoute, default False = unchanged): the InRange node (K2Node_CallFunction_60) reads
  Select(SHM246_LookRoute AND LS_LookDriven, |CalculateDirection(Acceleration, Rotator(0, SHM246_LookYaw, 0))|, |Direction|)
Acceleration = the movement INPUT direction (non-zero on the first intent frame, when the route is decided); SHM246_LookYaw is written by
the pawn every frame (install246_lookyaw.py). Idempotent (variables). builtins.V246_SAVE saves. Prints LOOKROUTE246 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, arg
import builtins, json
LS = u.EditorLoadingAndSavingUtils
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CPA = AP.replace('Base', '')
out = {}
dirty = [p for p in LS.get_dirty_content_packages() if 'ABP_GR_MotionMatching' in p.get_name()]
if dirty:
    out['reloaded'] = [p.get_name().split('/')[-1] for p in dirty]; LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
bp = u.load_asset(AP)
if 'SHM246_LookRoute' in [str(v) for v in B.list_variables(bp)]: out['patch'] = 'already'
else:
    ensure_vars(bp, [('SHM246_LookYaw', 'float', 'SHM'), ('SHM246_LookRoute', 'bool', 'SHM')]); compile_ok(bp)
    set_defaults(bp, {'SHM246_LookYaw': 0.0, 'SHM246_LookRoute': False}); compile_ok(bp)
    gp = pn(graph(bp, 'Update_MotionMatching')); g = G(gp); nodes = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(gp))}
    cf60 = nodes['K2Node_CallFunction_60']; old = src((cf60, 'Value')); assert len(old) == 1, old; out['value_before'] = old[0][0].rsplit('.', 1)[-1]
    assert any(q.name == 'Min' and abs(float(str(q.value)) - 65.0) < 1e-3 for q in info(cf60).input_pins), 'not the LS lateral InRange node'
    disconnect((cf60, 'Value'))
    dirlook = g.pure('/Script/Engine.AnimInstance:CalculateDirection', {'Velocity': g.get('Acceleration'), 'BaseRotation': g.rot(g.get('SHM246_LookYaw'))})
    cond = g.AND(g.get('SHM246_LookRoute'), g.get('LS_LookDriven'))
    connect(g.select(cond, g.pure('Abs', {'A': dirlook}), old[0]), (cf60, 'Value'))
    out['value_after'] = [s_[0].rsplit('.', 1)[-1] for s_ in src((cf60, 'Value'))]
for name, a in (('abp', bp), ('abp_child', u.load_asset(CPA))):
    st, errs = compile_ok(a); out[name] = [str(st), errs[:4]]
out['ok'] = all('UP_TO_DATE' in out[k][0] and not out[k][1] for k in ('abp', 'abp_child'))
if out['ok'] and getattr(builtins, 'V246_SAVE', False): save(bp, u.load_asset(CPA)); out['saved'] = True
cdo = u.get_default_object(bp.generated_class()); out['defaults'] = {'route': bool(cdo.get_editor_property('SHM246_LookRoute')), 'yaw': cdo.get_editor_property('SHM246_LookYaw')}
out['dirty'] = [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()]
print('LOOKROUTE246 ' + json.dumps(out, default=str))
