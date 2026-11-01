exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, disconnect, src, pn, info, obj, arg
import json
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'
bp = u.load_asset(AP); gp = pn(graph(bp, 'Update_MotionMatching')); nodes = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(gp))}
out = {'choosers': []}
for k, p in nodes.items():
    if 'EvaluateChooser' in k:
        ni = info(p); out['choosers'].append({'node': k, 'pins': [(q.name, str(q.value)[-90:]) for q in ni.input_pins]})
# chooser table contents (first chooser asset found in pins)
for ch in out['choosers']:
    for name, val in ch['pins']:
        if 'Chooser' in val or 'CHT_' in val or 'CT_' in val:
            path = val.split("'")[1] if "'" in val else val
            try:
                ct = u.load_asset(path.split('.')[0] if ':' not in path else path); ch['asset'] = path
                props = [x for x in dir(ct) if not x.startswith('_')][:60]; ch['props'] = props
                for pr in ('results_structs', 'results', 'columns_structs', 'output_object_type', 'result_type'):
                    try: ch[pr] = str(ct.get_editor_property(pr))[:600]
                    except Exception as e: ch[pr] = 'ERR ' + str(e)[:60]
            except Exception as e: ch['asset_err'] = str(e)[:100]
print('CHOOSER244 ' + json.dumps(out, default=str))
