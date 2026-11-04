"""probe255_dbs.py (measure): every PoseSearchDatabase variable of the ABP with its default and where Update_MotionMatching reads it. Read only."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import pn, info, obj
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'
bp = u.load_asset(AP); cdo = u.get_default_object(bp.generated_class()); rows = []
for v in B.list_variables(bp):
    n = str(v)
    try: x = cdo.get_editor_property(n)
    except Exception: continue
    if isinstance(x, u.PoseSearchDatabase): rows.append((n, x.get_name()))
print('DBVARS255 ' + json.dumps(rows) if 'json' in globals() else rows)
import json
mg = pn(graph(bp, 'Update_MotionMatching')); ns = [pn(n) for n in B.find_nodes(obj(mg))]
seen = {}
for p in ns:
    t = str(info(p).type_id)
    if '|Get' in t and any(k in t for k in ('DB', 'Route', 'Redirect')): seen[t.rsplit('|', 1)[-1]] = seen.get(t.rsplit('|', 1)[-1], 0) + 1
print('UMM255 ' + json.dumps(seen))
