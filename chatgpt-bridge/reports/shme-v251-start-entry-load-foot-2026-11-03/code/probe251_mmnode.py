"""probe251_mmnode.py (measure job, read-only): Motion Matching node settings (blend time, max active blends, pose jump threshold, play
rate, search throttle, interrupt) from its export text. Prints MMNODE251 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import pn, obj
import json, re
bp = u.load_asset('/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'); out = {}
g = [x for x in B.list_graphs(bp) if x.get_name() == 'AnimGraph'][0]
for n in B.find_nodes(g):
    p = pn(n)
    if not p.endswith('MotionMatching_0'): continue
    t = obj(p).get_editor_property('node').export_text()
    out['export'] = t[:6000]
print('MMNODE251 ' + json.dumps(out))
