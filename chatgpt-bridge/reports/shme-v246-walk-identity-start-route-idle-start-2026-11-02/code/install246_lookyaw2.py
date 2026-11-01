"""install246_lookyaw2.py (editor job, write manifest = ABP base + child): V2.46 look yaw source inside the ABP (the pawn-side writer of
install246_lookyaw.py could not connect the ABP cast to a cross-class set node). At the entry of Update_MotionMatching:
  SHM246_LookYaw := PreviousDesiredControllerYaw   (the AAMS ABP's controller-yaw copy, refreshed every update)
so the look-relative lateral-start route (install246_lookroute.py) reads a live look yaw. Idempotent (marker: a set node of SHM246_LookYaw
in the graph). builtins.V246_SAVE saves. Prints LOOKYAW246B {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, arg
import builtins, json
LS = u.EditorLoadingAndSavingUtils
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CPA = AP.replace('Base', '')
out = {}
dirty = [p for p in LS.get_dirty_content_packages() if 'ABP_GR_MotionMatching' in p.get_name() or 'BP_GR_Player' in p.get_name() or 'BP_PBI_Player' in p.get_name()]
if dirty:
    out['reloaded'] = [p.get_name().split('/')[-1] for p in dirty]; LS.reload_packages(dirty, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); u.SystemLibrary.collect_garbage()
bp = u.load_asset(AP); assert 'SHM246_LookYaw' in [str(v) for v in B.list_variables(bp)], 'run install246_lookroute.py first'
gp = pn(graph(bp, 'Update_MotionMatching')); g = G(gp); nodes = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(gp))}
marker = [k for k, p in nodes.items() if k.startswith('K2Node_VariableSet') and any(q.name == 'SHM246_LookYaw' for q in info(p).input_pins)]
if marker: out['patch'] = 'already'
else:
    ent = g.entry(); nxt = [p for p in nodes.values() if any(q.name == 'execute' for q in info(p).input_pins) and ent in src((p, 'execute'))]
    assert len(nxt) == 1, ('entry successor', [p.rsplit('.', 1)[-1] for p in nxt]); tgt = nxt[0]; out['entry_successor'] = tgt.rsplit('.', 1)[-1]
    disconnect((tgt, 'execute'))
    tail = g.set('SHM246_LookYaw', g.get('PreviousDesiredControllerYaw'), ent)
    connect(tail, (tgt, 'execute')); out['wired'] = True
for name, a in (('abp', bp), ('abp_child', u.load_asset(CPA))):
    st, errs = compile_ok(a); out[name] = [str(st), errs[:4]]
out['ok'] = all('UP_TO_DATE' in out[k][0] and not out[k][1] for k in ('abp', 'abp_child'))
if out['ok'] and getattr(builtins, 'V246_SAVE', False): save(bp, u.load_asset(CPA)); out['saved'] = True
out['dirty'] = [q.get_name().split('/')[-1] for q in LS.get_dirty_content_packages()]
print('LOOKYAW246B ' + json.dumps(out, default=str))
