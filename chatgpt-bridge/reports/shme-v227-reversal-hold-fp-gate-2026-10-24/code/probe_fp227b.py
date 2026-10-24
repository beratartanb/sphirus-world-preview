exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import pn, info, obj, src
from editor_toolset.toolsets.object import ObjectTools as O
import json
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'
bp = u.load_asset(AP); out = {}
fik = pn(graph(bp, 'FeetIK_Layer')); fn_ = [pn(n) for n in B.find_nodes(obj(fik))]
for p in fn_:
    o = obj(p)
    if o.get_class().get_name() != 'AnimGraphNode_FootPlacement': continue
    t = o.get_editor_property('node').export_text(); out['has_disable_in_export'] = 'bDisableFootPlacement' in t
    out['export_head'] = t[:300]
    try:
        pr = json.loads(O.get_properties(o, ['PropertyBindings']))
        out['bindings'] = pr.get('PropertyBindings')
    except Exception as e: out['bind_err'] = str(e)[:200]
    out['pins'] = [(q.name, [a.rsplit('.', 1)[-1] + ':' + b for a, b in src((p, q.name))]) for q in info(p).input_pins]
    try: out['all_props'] = json.loads(O.get_properties(o, ['node']))
    except Exception as e: out['node_err'] = str(e)[:100]
hits = []
for p in fn_:
    try: tid = str(info(p).type_id)
    except Exception: tid = ''
    if 'FootPlaceOff' in tid or 'DisableFootPlacement' in tid: hits.append(p.rsplit('.', 1)[-1] + ' ' + tid[-70:])
out['feetik_hits'] = hits
s = json.dumps(out, default=str); open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Saved/Codex/SHME_V227_20261024/probe_fp227.json', 'w', encoding='utf8').write(s)
print('PROBEFP227B ' + s[:1500])
