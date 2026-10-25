"""probe_order228.py (read-only): exec order of SHM_Snapshot vs Update_MotionMatching calls in the ABP EventGraph (BlueprintUpdateAnimation)."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import src, pn, info, obj
import json
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'
bp = u.load_asset(AP); gp = pn(graph(bp, 'EventGraph')); nodes = [pn(n) for n in B.find_nodes(obj(gp))]
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
succ = {}
for p in nodes:
    for q in info(p).input_pins:
        if q.name == 'execute':
            for s in src((p, 'execute')): succ.setdefault(s[0], []).append(p)
heads = [p for p in nodes if 'BlueprintUpdateAnimation' in tid(p) or 'UpdateAnimation' in tid(p)]
order = []
for h in heads:
    cur = h; seen = 0
    while cur and seen < 60:
        nxt = succ.get(cur)
        if not nxt: break
        cur = nxt[0]; order.append(tid(cur)[-45:]); seen += 1
print('ORDER228 ' + json.dumps({'heads': [tid(h)[-40:] for h in heads], 'chain': order}))
