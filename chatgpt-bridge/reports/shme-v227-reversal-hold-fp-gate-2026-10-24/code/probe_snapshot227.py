"""probe_snapshot227.py (read-only editor job): the SHM_Snapshot node chains V2.27 will patch - SetSHM_FootPlaceOff (value source),
SetSHM_RedirectActive (value source tree), SetSHM_RedirectFrames (value source tree to the (or rdOn tailNow) node) - plus the FootPlacement
nodes' pins (Alpha / bDisableFootPlacement) in FeetIK_Layer. Prints PROBE227 {...}. Nothing is modified."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, src, pn, info, obj
import json
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'
bp = u.load_asset(AP); out = {}
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
def short(p): return p.rsplit('.', 1)[-1]
def tree(ep, depth):
    s = src(ep); res = []
    for (n, pin) in s:
        d = {'node': short(n), 'type': tid(n)[-70:], 'pin': pin}
        if depth > 0:
            ins = {}
            for q in info(n).input_pins:
                if q.name in ('execute', 'self'): continue
                t = tree((n, q.name), depth - 1)
                ins[q.name] = t if t else ('=' + str(getattr(q, 'default_value', ''))[:20])
            d['in'] = ins
        res.append(d)
    return res
sg = pn(graph(bp, 'SHM_Snapshot')); sn = [pn(n) for n in B.find_nodes(obj(sg))]
for key, depth in (('SetSHM_FootPlaceOff', 1), ('SetSHM_RedirectActive', 2), ('SetSHM_RedirectFrames', 5), ('SetSHM_RedirectClass', 1)):
    ps = [p for p in sn if key in tid(p)]
    out[key] = [{'node': short(p), 'pins': [q.name for q in info(p).input_pins], 'tree': tree((p, key.replace('Set', '', 1)), depth)} for p in ps]
out['curve_nodes'] = [{'node': short(p), 'type': tid(p)[-60:], 'defaults': {q.name: str(getattr(q, 'default_value', ''))[:30] for q in info(p).input_pins if q.name == 'CurveName'}} for p in sn if 'GetCurveValue' in tid(p)]
comp = [p for p in sn if 'GetComponentByClass' in tid(p) or 'GetComponentbyClass' in tid(p)]; out['comp_getter'] = [short(p) for p in comp]
hs = [p for p in sn if tid(p).endswith('|GetHumanStateEnabled')]; out['hs_getter'] = [short(p) for p in hs]
fik = pn(graph(bp, 'FeetIK_Layer')); fn_ = [pn(n) for n in B.find_nodes(obj(fik))]
fps = [p for p in fn_ if obj(p).get_class().get_name() == 'AnimGraphNode_FootPlacement']
out['footplacement'] = [{'node': short(p), 'pins': [(q.name, str(getattr(q, 'default_value', ''))[:20]) for q in info(p).input_pins], 'srcs': {q.name: [short(a) + ':' + b for a, b in src((p, q.name))] for q in info(p).input_pins if src((p, q.name))}} for p in fps]
print('PROBE227 ' + json.dumps(out, default=str))
