exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import src, pn, info, obj
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'
bp = u.load_asset(AP); gp = pn(graph(bp, 'Update_MotionMatching')); nodes = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(gp))}
def tid(p):
    try: return str(info(p).type_id)
    except Exception as e: return 'ERR'
print('N', len(nodes))
ex = {}
for k, p in nodes.items():
    for q in info(p).input_pins:
        if q.name == 'execute':
            for s in src((p, 'execute')): ex.setdefault(s[0].rsplit('.', 1)[-1], []).append((s[1], k))
seen = set(); stack = [('K2Node_FunctionEntry_0', 0)]
while stack:
    k, d = stack.pop()
    if k in seen or d > 14: continue
    seen.add(k); print('  ' * min(d, 12) + k, tid(nodes[k])[-60:], [(a, b) for a, b in ex.get(k, [])][:4])
    for a, b in reversed(ex.get(k, [])): stack.append((b, d + 1))
dbs = [k for k, p in nodes.items() if 'SetDatabaseToSearch' in tid(p) or 'SetDatabasesToSearch' in tid(p)]
print('SETDB', len(dbs), dbs[:30])
