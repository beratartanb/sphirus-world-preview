"""install236_resumevar.py (editor job): V2.36 A/B hook for the CP jog start route. Update_MotionMatching's K2Node_CallFunction_40
(SetDatabaseToSearch, Database = literal PSD_CP2_JogStart) - the route a re-press DURING a jog stop takes (j36_rsm: 0.5 s after the release,
still at 100 cm/s, the vendor start is entered mid-stride, 19 cm drag) - reads the new ABP variable SHM236_DB_JogResume (default =
PSD_CP2_JogStart -> production unchanged). Idempotent. builtins.V236_SAVE saves. Prints RESVAR236 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, arg
import builtins
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CP = AP.replace('Base', '')
JS = '/Game/GraceRanger/Animations/CorePerformance/PSD_CP2_JogStart'
bp = u.load_asset(AP); out = {}
ensure_vars(bp, [('SHM236_DB_JogResume', u.PoseSearchDatabase.static_class(), 'SHM')])
compile_ok(bp); set_defaults(bp, {'SHM236_DB_JogResume': u.load_asset(JS)})
gp = pn(graph(bp, 'Update_MotionMatching')); g = G(gp)
nodes = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(gp))}
hits = []
for k, p in nodes.items():
    ni = info(p)
    if 'SetDatabaseToSearch' not in str(ni.type_id): continue
    q = [x for x in ni.input_pins if x.name == 'Database'][0]
    if not src((p, 'Database')) and 'PSD_CP2_JogStart' in str(q.value):
        connect(g.get('SHM236_DB_JogResume'), (p, 'Database')); hits.append([k, 'wired'])
    elif any('SHM236_DB_JogResume' in s_[1] for s_ in src((p, 'Database'))): hits.append([k, 'already'])
out['calls'] = hits
for k, p in nodes.items():               # literal JogStart offered by Select nodes too
    if not k.startswith('K2Node_Select'): continue
    for q in info(p).input_pins:
        if 'PSD_CP2_JogStart' in str(q.value) and not src((p, q.name)): connect(g.get('SHM236_DB_JogResume'), (p, q.name)); out.setdefault('select', []).append([k, q.name])
st, errs = compile_ok(bp); out['status'] = str(st); out['errs'] = errs[:4]
cpb = u.load_asset(CP); out['child'] = str(compile_ok(cpb)[0])
if 'UP_TO_DATE' in str(st) and getattr(builtins, 'V236_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('RESVAR236 ' + json.dumps(out, default=str))
