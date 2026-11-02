exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, src, pn, info, obj, op
import json
PB = '/Game/GraceRanger/BP_GR_Player'
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
g = G(op(PB) + ':GR_Impl_CP_PhysicalRedirect'); N = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(g.path))}
out = {}
for k, p in N.items():
    if not tid(p).endswith('SetVelocity'): continue
    v = src((p, 'Velocity')); d = {'vel_src': [tid(x[0])[-40:] + ':' + x[1] for x in v]}
    if v:
        n = v[0][0]; d['ins'] = {q.name: [tid(x[0])[-45:] for x in src((n, q.name))] for q in info(n).input_pins if src((n, q.name))}
        for q in info(n).input_pins:
            for x in src((n, q.name)):
                d['ins2_' + q.name] = {r.name: [tid(y[0])[-40:] for y in src((x[0], r.name))] for r in info(x[0]).input_pins if src((x[0], r.name))}
    out[k] = d
print('VELPROBE248 ' + json.dumps(out))
