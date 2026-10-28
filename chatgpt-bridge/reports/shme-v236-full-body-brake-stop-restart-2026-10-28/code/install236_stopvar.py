"""install236_stopvar.py (editor job): V2.36 A/B hook for the jog stop database. Update_MotionMatching's forward jog stop route
(K2Node_CallFunction_42 SetDatabaseToSearch, Database = literal PSD_CP2_JogStop) reads the new ABP variable SHM236_DB_JogStop instead
(default = PSD_CP2_JogStop -> production behaviour unchanged until the variable is set); every CurrentSelectedDatabase writer whose literal is
PSD_CP2_JogStop reads it too (telemetry / hold logic name the database actually searched). Idempotent. builtins.V236_SAVE saves.
Prints STOPVAR236 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, arg
import builtins
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CP = AP.replace('Base', '')
JS = '/Game/GraceRanger/Animations/CorePerformance/PSD_CP2_JogStop'
bp = u.load_asset(AP); out = {}
ensure_vars(bp, [('SHM236_DB_JogStop', u.PoseSearchDatabase.static_class(), 'SHM')])
compile_ok(bp); set_defaults(bp, {'SHM236_DB_JogStop': u.load_asset(JS)})
gp = pn(graph(bp, 'Update_MotionMatching')); g = G(gp)
nodes = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(gp))}
cf = nodes['K2Node_CallFunction_42']; dbp = [q for q in info(cf).input_pins if q.name == 'Database'][0]
out['cf42_before'] = {'value': str(dbp.value)[-60:], 'src': [s[0].rsplit('.', 1)[-1] for s in src((cf, 'Database'))]}
if not src((cf, 'Database')):
    assert 'PSD_CP2_JogStop' in str(dbp.value), dbp.value
    connect(g.get('SHM236_DB_JogStop'), (cf, 'Database')); out['cf42'] = 'wired'
else: out['cf42'] = 'already'
out['select'] = []
for k, p in nodes.items():               # V2.36b: a Select node (K2Node_Select_3) also offers the literal PSD_CP2_JogStop to a database search
    if not k.startswith('K2Node_Select'): continue
    for q in info(p).input_pins:
        if 'PSD_CP2_JogStop' in str(q.value) and not src((p, q.name)):
            connect(g.get('SHM236_DB_JogStop'), (p, q.name)); out['select'].append([k, q.name, 'wired'])
        elif q.name.startswith('Option') and src((p, q.name)) and any('SHM236' in s_[1] for s_ in src((p, q.name))): out['select'].append([k, q.name, 'already'])
    outs_ = [x.name for x in info(p).output_pins]
    out.setdefault('select_out', {})[k] = outs_
out['csd'] = []
for k, p in nodes.items():
    if not k.startswith('K2Node_VariableSet'): continue
    ni = info(p)
    if 'CurrentSelectedDatabase' not in [q.name for q in ni.input_pins]: continue
    q = [q for q in ni.input_pins if q.name == 'CurrentSelectedDatabase'][0]
    srcs = src((p, 'CurrentSelectedDatabase'))
    d = {'node': k, 'value': str(q.value)[-50:], 'src': [s[0].rsplit('.', 1)[-1] + ':' + s[1] for s in srcs]}
    if not srcs and 'PSD_CP2_JogStop' in str(q.value):
        connect(g.get('SHM236_DB_JogStop'), (p, 'CurrentSelectedDatabase')); d['wired'] = True
    out['csd'].append(d)
st, errs = compile_ok(bp); out['status'] = str(st); out['errs'] = errs[:4]
cpb = u.load_asset(CP); out['child'] = str(compile_ok(cpb)[0])
if 'UP_TO_DATE' in str(st) and getattr(builtins, 'V236_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('STOPVAR236 ' + json.dumps(out, default=str))
