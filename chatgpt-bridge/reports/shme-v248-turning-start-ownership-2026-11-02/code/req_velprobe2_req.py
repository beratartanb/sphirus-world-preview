exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, src, pn, info, obj, op
import json
PB = '/Game/GraceRanger/BP_GR_Player'
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
g = G(op(PB) + ':GR_Impl_CP_PhysicalRedirect'); N = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(g.path))}
def leaves(ep, depth, acc):
    if depth > 7: return
    for n, pin in src(ep):
        t = tid(n).rsplit('|', 1)[-1]
        if t.startswith('Get') or 'Variable' in tid(n): acc.append(t[-30:])
        for q in info(n).input_pins:
            if q.name not in ('self', 'execute'): leaves((n, q.name), depth + 1, acc)
out = {}
for k, p in N.items():
    if tid(p).endswith('SetVelocity'):
        acc = []; leaves((p, 'Velocity'), 0, acc); out[k] = sorted(set(acc))
print('VELPROBE248B ' + json.dumps(out))
