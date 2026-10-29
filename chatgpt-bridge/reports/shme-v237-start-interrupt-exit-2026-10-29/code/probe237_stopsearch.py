"""probe237_stopsearch.py (editor job, read-only): every database-search call in Update_MotionMatching of ABP_GR_MotionMatchingBase -
node, function, the Database pin (literal or source node) and the InterruptMode pin (literal or source) - to find why the jog stop entry
re-selects a new stop bin at clip time 0 on consecutive frames. Prints SS237 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, src, pn, info, obj
import json
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'
bp = u.load_asset(AP); out = {'calls': []}
gp = pn(graph(bp, 'Update_MotionMatching'))
for n in [pn(x) for x in B.find_nodes(obj(gp))]:
    k = n.rsplit('.', 1)[-1]
    if not k.startswith('K2Node_CallFunction'): continue
    I = info(n); names = [q.name for q in I.input_pins]
    if 'Database' not in names and 'Databases' not in names: continue
    d = {'node': k, 'title': str(getattr(I, 'title', ''))[:60]}
    for q in I.input_pins:
        if q.name in ('Database', 'Databases', 'InterruptMode', 'bForceInterrupt', 'ForceInterrupt'):
            d[q.name] = {'value': str(q.value)[-50:], 'src': [s[0].rsplit('.', 1)[-1] for s in src((n, q.name))]}
    d['pins'] = names
    out['calls'].append(d)
out['dirty'] = [q.get_name() for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('SS237 ' + json.dumps(out, default=str))
