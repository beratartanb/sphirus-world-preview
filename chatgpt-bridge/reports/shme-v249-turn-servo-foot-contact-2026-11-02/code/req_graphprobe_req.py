"""graphprobe (measure): V2.49 wiring facts needed for the root-motion turn owner.
1. Update_MotionMatching: exec predecessors (4 levels) of the two V2.48 route branches (K2Node_IfThenElse_80/81) with their condition sources
   (how StartSide L/R is chosen), and the entry node's first successor.
2. BP_GR_Player GR_Impl_CP_PhysicalRedirect: entry successor, any FunctionResult node / outputs.
3. ABP AnimGraph: OrientationWarping / StrideWarping / FootPlacement nodes and what feeds their alpha / enable pins."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, src, pn, info, obj, op
import json
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'; PB = '/Game/GraceRanger/BP_GR_Player'
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
def short(p): return p.rsplit('.', 1)[-1] + ':' + tid(p).rsplit('|', 1)[-1][-40:]
out = {}
bp = u.load_asset(AP); gp = pn(graph(bp, 'Update_MotionMatching')); N = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(gp))}
def preds(p): return [s_[0] for s_ in src((p, 'execute'))] if any(q.name == 'execute' for q in info(p).input_pins) else []
def cond(p):
    s_ = src((p, 'Condition')) if any(q.name == 'Condition' for q in info(p).input_pins) else []
    if not s_: return None
    n = s_[0][0]; return short(n) + ' <- ' + str([short(x[0]) for q in info(n).input_pins for x in src((n, q.name))][:4])
for k in ('K2Node_IfThenElse_80', 'K2Node_IfThenElse_81'):
    chain = []; cur = [N[k]]
    for lvl in range(5):
        nxt = []
        for c in cur:
            for p in preds(c): chain.append([lvl, short(p), cond(p)]); nxt.append(p)
        cur = nxt[:3]
    out[k] = chain
ent = [p for p in N.values() if 'FunctionEntry' in p]; out['mm_entry_succ'] = [short(pn(q.node)) for e in ent for o in info(e).output_pins if o.name == 'then' for q in o.connected_pins]
g2 = G(op(PB) + ':GR_Impl_CP_PhysicalRedirect'); N2 = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(g2.path))}
out['pr_results'] = [short(p) for p in N2.values() if 'FunctionResult' in p]
ent2 = [p for p in N2.values() if 'FunctionEntry' in p]; out['pr_entry'] = [short(p) for p in ent2]
out['pr_entry_succ'] = [short(pn(q.node)) for e in ent2 for o in info(e).output_pins if o.name == 'then' for q in o.connected_pins]
out['pr_entry_outputs'] = [o.name for e in ent2 for o in info(e).output_pins]
ag = []
for gr in B.list_graphs(bp):
    if gr.get_name() != 'AnimGraph': continue
    for n in B.find_nodes(gr):
        cn = n.get_class().get_name()
        if any(k in cn for k in ('OrientationWarping', 'StrideWarping', 'FootPlacement')):
            p = pn(n); pins = {}
            for q in info(p).input_pins:
                s_ = src((p, q.name))
                if s_ or 'lpha' in q.name or 'nable' in q.name: pins[q.name] = [short(x[0]) for x in s_][:2] or str(q.value)[:30]
            ag.append([cn, p.rsplit('.', 1)[-1], pins])
out['animgraph_warp'] = ag
print('GRAPHPROBE249 ' + json.dumps(out, default=str))
