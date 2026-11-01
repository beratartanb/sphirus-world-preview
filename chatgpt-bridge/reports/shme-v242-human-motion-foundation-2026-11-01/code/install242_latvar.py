"""install242_latvar.py (editor job): V2.42 A/B hook for the LATERAL jog stop database (vendor PSD_LS_CoreLateralStop, chosen by K2Node_Select_3 Option 1 under LS_LateralBrake). The Select pin
(K2Node_CallFunction_42 SetDatabaseToSearch, Database = literal PSD_LS_CoreLateralStop) reads the new ABP variable SHM242_DB_LatStop instead
(default = PSD_LS_CoreLateralStop -> production behaviour unchanged until the variable is set); every CurrentSelectedDatabase writer whose literal is
PSD_LS_CoreLateralStop reads it too (telemetry / hold logic name the database actually searched). Idempotent. builtins.V242_SAVE saves.
Prints LATVAR242 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, arg
import builtins
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; CP = AP.replace('Base', '')
JS = '/Game/GraceRanger/Animations/LookStrafe/PSD_LS_CoreLateralStop'
bp = u.load_asset(AP); out = {}
ensure_vars(bp, [('SHM242_DB_LatStop', u.PoseSearchDatabase.static_class(), 'SHM')])
compile_ok(bp); set_defaults(bp, {'SHM242_DB_LatStop': u.load_asset(JS)})
gp = pn(graph(bp, 'Update_MotionMatching')); g = G(gp)
nodes = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(gp))}
cf = nodes['K2Node_CallFunction_42']; dbp = [q for q in info(cf).input_pins if q.name == 'Database'][0]
out['cf42_before'] = {'value': str(dbp.value)[-60:], 'src': [s[0].rsplit('.', 1)[-1] for s in src((cf, 'Database'))]}
out['cf42'] = 'skipped (forward stop route, not the lateral DB)'   # V2.42: only the Select_3 Option 1 literal (and CSD writers) carry the lateral DB
out['select'] = []
for k, p in nodes.items():               # V2.36b: a Select node (K2Node_Select_3) also offers the literal PSD_LS_CoreLateralStop to a database search
    if not k.startswith('K2Node_Select'): continue
    for q in info(p).input_pins:
        if 'PSD_LS_CoreLateralStop' in str(q.value) and not src((p, q.name)):
            connect(g.get('SHM242_DB_LatStop'), (p, q.name)); out['select'].append([k, q.name, 'wired'])
        elif q.name.startswith('Option') and src((p, q.name)) and any('SHM242' in s_[1] for s_ in src((p, q.name))): out['select'].append([k, q.name, 'already'])
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
    if not srcs and 'PSD_LS_CoreLateralStop' in str(q.value):
        connect(g.get('SHM242_DB_LatStop'), (p, 'CurrentSelectedDatabase')); d['wired'] = True
    out['csd'].append(d)
st, errs = compile_ok(bp); out['status'] = str(st); out['errs'] = errs[:4]
cpb = u.load_asset(CP); out['child'] = str(compile_ok(cpb)[0])
if 'UP_TO_DATE' in str(st) and getattr(builtins, 'V242_SAVE', False): save(bp, cpb); out['saved'] = True
out['dirty'] = [q.get_name() for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('LATVAR242 ' + json.dumps(out, default=str))
