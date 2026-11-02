"""probe250_lean.py (measure job, read-only): what drives BlendSpacePlayer_0 (BS1D_Additive_Lean_Run, mesh-space additive on the Motion Matching
output): its PropertyBindings, the blend space axis range, ABP variables named *Lean*, and every graph node that reads/writes them. Prints LEAN250 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import pn, info, obj, src
from editor_toolset.toolsets.object import ObjectTools as O
import json
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'
bp = u.load_asset(AP); out = {}
g = [x for x in B.list_graphs(bp) if x.get_name() == 'AnimGraph'][0]
for n in B.find_nodes(g):
    p = pn(n)
    if p.endswith('BlendSpacePlayer_0'):
        try: out['bindings'] = json.loads(O.get_properties(obj(p), ['PropertyBindings', 'ShowPinForProperties']))
        except Exception as e: out['bind_err'] = str(e)[:300]
bs = u.load_asset('/Game/AAMS/AAMS/Animations/Locomotion/Run/BS1D_Additive_Lean_Run')
try: out['bs'] = json.loads(O.get_properties(bs, ['BlendParameters', 'SampleData', 'AdditiveAnimType']))
except Exception as e: out['bs_err'] = str(e)[:300]
V = [str(v) for v in B.list_variables(bp)]; out['lean_vars'] = [v for v in V if 'lean' in v.lower()]
uses = {}
for gr in B.list_graphs(bp):
    for n in B.find_nodes(gr):
        p = pn(n)
        try: t = str(info(p).type_id)
        except Exception: continue
        for v in out['lean_vars']:
            if t.endswith('|Get' + v) or t.endswith('|Set' + v) or ('Get' + v) in t or ('Set' + v) in t:
                uses.setdefault(v, []).append(gr.get_name() + ':' + p.rsplit('.', 1)[-1] + ':' + t.rsplit('|', 1)[-1])
out['uses'] = uses
cdo = u.get_default_object(bp.generated_class())
out['defaults'] = {}
for v in out['lean_vars']:
    try: out['defaults'][v] = str(cdo.get_editor_property(v))
    except Exception: pass
print('LEAN250 ' + json.dumps(out, default=str)[:20000])
