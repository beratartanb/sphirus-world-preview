"""probe_fp227.py (read-only): how SHM_FootPlaceOff reaches the FootPlacement node today (property bindings / pins / export text)."""
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
    t = o.get_editor_property('node').export_text(); i = t.find('bDisableFootPlacement'); out['export_disable'] = t[max(0, i - 40): i + 80]
    try: out['props'] = json.loads(O.get_properties(o, ['PropertyBindings', 'ShowPinForProperties']))
    except Exception as e: out['props_err'] = str(e)[:200]
    out['pins'] = [q.name for q in info(p).input_pins]
# any graph node mentioning SHM_FootPlaceOff outside the snapshot
for gname in ('FeetIK_Layer', 'AnimGraph', 'Get_FootPlacementPlantSettings', 'Get_bDisableFootPlacement'):
    try: g = graph(bp, gname)
    except Exception: continue
    if not g: continue
    ns = [pn(n) for n in B.find_nodes(obj(pn(g)))]
    hits = []
    for p in ns:
        try: tid = str(info(p).type_id)
        except Exception: tid = ''
        if 'FootPlaceOff' in tid or 'bDisableFootPlacement' in tid: hits.append(p.rsplit('.', 1)[-1] + ' ' + tid[-60:])
    out['g_' + gname] = hits
out['functions'] = [str(f) for f in B.list_functions(bp) if 'Foot' in str(f) or 'Disable' in str(f)] if hasattr(B, 'list_functions') else 'n/a'
print('PROBEFP227 ' + json.dumps(out, default=str)[:6000])
