exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import src, pn, info, obj
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'
bp = u.load_asset(AP); gp = pn(graph(bp, 'Update_MotionMatching')); nodes = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(gp))}
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return 'ERR'
ex = {}
for k, p in nodes.items():
    for q in info(p).input_pins:
        if q.name == 'execute':
            for s in src((p, 'execute')): ex.setdefault(s[0].rsplit('.', 1)[-1], []).append((s[1], k))
def show(k, d=0):
    p = nodes[k]; ins = {q.name: [(s[0].rsplit('.', 1)[-1], s[1], tid(s[0])[-40:]) for s in src((p, q.name))] for q in info(p).input_pins if q.name not in ('execute',)}
    print('  ' * d + k, tid(p)[-50:], {a: b for a, b in ins.items() if b}, [q.name + '=' + str(q.default_value)[:30] for q in info(p).input_pins if hasattr(q, 'default_value') and q.name in ('Min', 'Max', 'Value', 'InterruptMode')])
    for a, b in ex.get(k, []):
        if d < 6: print('  ' * d + ' ->' + a); show(b, d + 1)
show(ex['K2Node_FunctionEntry_0'][0][1])
