"""probe241_gr.py (measure job): every actor-rotation writer in BP_GR_Player / BP_PBI_Player graphs (SetActorRotation family,
SetControlRotation, cm RotationRate / bOrientRotationToMovement setters) with its graph, node, exec source chain (3 back) and the inputs of
its rotation pin. Prints GRROT241 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import pn, info, src
import json
KEYS = ('SetActorRotation', 'K2_SetActorRotation', 'SetActorRelativeRotation', 'AddActorWorldRotation', 'AddActorLocalRotation', 'SetControlRotation', 'SetWorldRotation',
        'SetRotationRate', 'Set bOrientRotationToMovement', 'SetbOrientRotationToMovement', 'SetbUseControllerDesiredRotation', 'K2_SetWorldRotation', 'SetActorTransform')
out = {}
for P in ('/Game/GraceRanger/BP_GR_Player', '/Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player'):
    bp = u.load_asset(P); res = []; sizes = {}
    for g in B.list_graphs(bp):
        ns = B.find_nodes(g); sizes[g.get_name()] = len(ns)
        for n in ns:
            t = str(info(pn(n)).type_id)
            if any(k in t for k in KEYS) or ('RotationRate' in t and 'Set' in t):
                def back(p, d):
                    if d == 0: return []
                    try:
                        s = src((p, 'execute'))
                    except Exception: return []
                    r = []
                    for q in s[:2]:
                        qp = q.split(':')[0] if isinstance(q, str) else str(q)
                        full = pn(n).rsplit('.', 1)[0] + '.' + qp.split('.')[-1] if '.' not in qp else qp
                        try: r.append([qp.split('.')[-1], str(info(full).type_id)[-60:], back(full, d - 1)])
                        except Exception: r.append([qp.split('.')[-1], '?', []])
                    return r
                pins = {}
                try:
                    for ip in info(pn(n)).input_pins:
                        if ip.name in ('NewRotation', 'NewControlRotation', 'DeltaRotation', 'NewTransform', 'self', 'bTeleport', 'Target'):
                            pins[str(ip.name)] = [str(x)[-70:] for x in src((pn(n), ip.name))]
                except Exception: pass
                res.append({'graph': g.get_name(), 'node': pn(n).split('.')[-1], 'type': t[-70:], 'exec_back': back(pn(n), 3), 'pins': pins})
    out[P.split('/')[-1]] = {'writers': res, 'big_graphs': {k: v for k, v in sorted(sizes.items(), key=lambda x: -x[1])[:15]}}
print('GRROT241 ' + json.dumps(out, default=str))
