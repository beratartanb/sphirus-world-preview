"""install246_lookyaw.py (editor job, write manifest = BP_GR_Player + BP_PBI_Player; run AFTER install246_lookroute.py): the pawn writes the
control (look) yaw into the ABP every frame: GR_UpdateRig, right after SetLS_LookDriven (K2Node_VariableSet_17, self = the ABP cast
K2Node_DynamicCast_1): ABP.SHM246_LookYaw := BreakRotator(GetControlRotation).Yaw. Idempotent (marker: a set node of SHM246_LookYaw in
the graph). builtins.V246_SAVE saves. Prints LOOKYAW246 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, arg
import builtins, json
LS = u.EditorLoadingAndSavingUtils
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
PAWN = '/Game/GraceRanger/BP_GR_Player'; CHILD = '/Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player'
ABPC = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase.ABP_GR_MotionMatchingBase_C'
out = {}
dirty = [p for p in LS.get_dirty_content_packages() if p.get_name() in (PAWN, CHILD)]
if dirty:
    out['reloaded'] = [p.get_name().split('/')[-1] for p in dirty]; LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
pb = u.load_asset(PAWN); gp = pn(graph(pb, 'GR_UpdateRig')); g = G(gp); nodes = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(gp))}
marker = [k for k, p in nodes.items() if k.startswith('K2Node_VariableSet') and any(q.name == 'SHM246_LookYaw' for q in info(p).input_pins)]
if marker: out['patch'] = 'already'
else:
    vs17 = nodes['K2Node_VariableSet_17']; assert any(q.name == 'LS_LookDriven' for q in info(vs17).input_pins), 'VariableSet_17 is not SetLS_LookDriven'
    cast = nodes['K2Node_DynamicCast_1']; outs = [q.name for q in info(cast).output_pins if q.name not in ('then', 'CastFailed', 'bSuccess')]; assert len(outs) == 1, outs
    nxt = [p for p in nodes.values() if any(q.name == 'execute' for q in info(p).input_pins) and (vs17, 'then') in src((p, 'execute'))]
    assert len(nxt) == 1, ('successor', [p.rsplit('.', 1)[-1] for p in nxt]); tgt = nxt[0]; out['successor'] = tgt.rsplit('.', 1)[-1]
    disconnect((tgt, 'execute'))
    tail = g.set('SHM246_LookYaw', g.yaw(g.pure('Control')), (vs17, 'then'), owner=ABPC, target=(cast, outs[0]))
    connect(tail, (tgt, 'execute')); out['cast_pin'] = outs[0]
for name, a in (('pawn', pb), ('pawn_child', u.load_asset(CHILD))):
    st, errs = compile_ok(a); out[name] = [str(st), errs[:4]]
out['ok'] = all('UP_TO_DATE' in out[k][0] and not out[k][1] for k in ('pawn', 'pawn_child'))
if out['ok'] and getattr(builtins, 'V246_SAVE', False): save(pb, u.load_asset(CHILD)); out['saved'] = True
out['dirty'] = [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()]
print('LOOKYAW246 ' + json.dumps(out, default=str))
