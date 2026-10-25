"""probe_jr228.py (editor job, READ-ONLY): the jog-reversal database route: SetSHM_RedirectDB_JR (and SHM224_RevIntent / RevMir setters) in SHM_Snapshot with their value sources three levels deep; the Update_MotionMatching branch conditions that lead to SetDatabaseToSearch(SHM_RedirectDB_JR). Prints JR228; writes probe_jr228.json."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, src, pn, info, obj
import json, pathlib
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'
bp = u.load_asset(AP); out = {}
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
def tree(p, depth):
    d = {'type': tid(p)[-55:]}
    if depth <= 0: return d
    for q in info(p).input_pins:
        if q.name in ('execute', 'self'): continue
        sv = src((p, q.name))
        if sv: d[q.name] = [tree(s[0], depth - 1) for s in sv]
        else:
            for a in ('default_value', 'default', 'value'):
                if hasattr(q, a):
                    dv = str(getattr(q, a))[:40]
                    if dv not in ('', 'None'): d[q.name] = dv
                    break
    return d
nodes = []
for gn in ('SHM_Snapshot', 'Update_MotionMatching', 'EventGraph', 'SHM_RedirectRoute', 'SHM_Route'):
    try: nodes += [pn(n) for n in B.find_nodes(obj(pn(graph(bp, gn))))]
    except Exception: pass
for p in nodes:
    t = tid(p)
    if any(k in t for k in ('SetSHM_RedirectDB_JR', 'SetSHM224_RevIntent', 'SetSHM224_RevMir', 'SetSHM224_EarlyRev')):
        out[p.rsplit('.', 1)[-1] + ' ' + t[-30:]] = tree(p, 3)
gp2 = pn(graph(bp, 'Update_MotionMatching')); nodes2 = [pn(n) for n in B.find_nodes(obj(gp2))]
for p in nodes2:
    t = tid(p)
    if 'SetDatabaseToSearch' in t and any('SHM_RedirectDB_JR' in tid(s[0]) for s in src((p, 'Database'))):
        ex = src((p, 'execute'))
        chain = []
        for s in ex:
            n = s[0]; chain.append(tree(n, 1))
            # the branch condition
            if 'IfThenElse' in n or 'Dal' in tid(n):
                chain.append({'branch_cond': tree(n, 3)})
            else:
                e2 = src((n, 'execute')); chain.append({'prev': [tree(x[0], 3) for x in e2]})
        out['UMM ' + p.rsplit('.', 1)[-1]] = chain
pathlib.Path(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Saved/Codex/SHME_V228_20261025/probe_jr228.json').write_text(json.dumps(out, indent=1, default=str), encoding='utf8')
print('JR228 ' + json.dumps(out, default=str)[:3800])
