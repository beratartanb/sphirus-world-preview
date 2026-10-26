"""fix_v231_resolver_name.py (editor job): SHM231_InspectResolve built with KismetSystemLibrary:GetPathName (the DSL has no GetPathName node) ->
replace it by GetObjectName (same source, same consumers) so the resolver id equals the DSL's GetObjectName(hit actor). Prints RESOLVERNAME231."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, connect, src, pn, info, obj
import json
bp = u.load_asset('/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent'); fg = graph(bp, 'SHM231_InspectResolve'); g = G(pn(fg))
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
ns = [pn(n) for n in B.find_nodes(fg)]
old = [p for p in ns if 'GetPathName' in tid(p)]; out = {'old': [o.rsplit('.', 1)[-1] for o in old]}
for o in old:
    s_ = src((o, 'Object')); users = []
    for p in ns:
        for q in info(p).input_pins:
            if (o, 'ReturnValue') in src((p, q.name)): users.append((p, q.name))
    nn = g.pure('/Script/Engine.KismetSystemLibrary:GetObjectName', {'Object': s_[0]} if s_ else {})
    for p, q in users: connect(nn, (p, q))
    for nd in B.find_nodes(fg):
        if pn(nd) == o: B.delete_node(nd)
    out.setdefault('rewired', []).append([q for _, q in users])
st, errs = compile_ok(bp); out['status'] = str(st); out['errs'] = errs[:4]
out['now'] = [tid(pn(n))[-40:] for n in B.find_nodes(fg) if 'Name' in tid(pn(n))]
print('RESOLVERNAME231 ' + json.dumps(out, default=str))
