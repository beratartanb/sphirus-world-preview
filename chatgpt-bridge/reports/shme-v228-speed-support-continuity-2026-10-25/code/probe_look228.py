"""probe_look228.py (editor job, READ-ONLY): how the inspection look point reaches the head. In ABP_GR_MotionMatchingBase (and the child):
every graph node whose type id or pin sources mention SHM225_Look / InspectLook / LookAt / AimOffset / Look At, with their input pins and
default values (LookAt node: look at location / alpha / clamp angle / interpolation / look-at axis), the variable list matching Look / Inspect,
and the AnimGraph node class histogram. Prints LOOK228; writes probe_look228.json. No save."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, src, pn, info, obj, op
import json, pathlib
out = {}
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
for AP in ('/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase',):
    bp = u.load_asset(AP); key = AP.rsplit('/', 1)[-1]; d = {}
    try: d['vars'] = [v for v in B.list_variables(bp) if any(k in str(v).lower() for k in ('look', 'inspect', 'aim', 'head'))]
    except Exception as e: d['vars'] = 'ERR ' + str(e)[:80]
    graphs = []
    for gname in ('AnimGraph', 'SHM_Snapshot'):
        try:
            g = graph(bp, gname); gp = pn(g); graphs.append((gname, gp))
        except Exception as e: d['graph_err_' + gname] = str(e)[:100]
    hits = []
    for gname, gp in graphs:
        try: nodes = [pn(n) for n in B.find_nodes(obj(gp))]
        except Exception as e: d['nodes_err_' + gname] = str(e)[:100]; continue
        hist = {}
        for p in nodes:
            try: c = obj(p).get_class().get_name()
            except Exception: c = 'ERR'
            hist[c] = hist.get(c, 0) + 1
        d['hist_' + gname] = {k: v for k, v in sorted(hist.items(), key=lambda x: -x[1])[:14]}
        for p in nodes:
            t = tid(p); cls = obj(p).get_class().get_name()
            interesting = any(k in t for k in ('SHM225_Look', 'InspectLook', 'LookAt', 'Look At', 'AimOffset', 'LookPoint', 'LookAlpha')) or 'LookAt' in cls or 'AimOffset' in cls
            if not interesting: continue
            pins = {}
            try: ipins = info(p).input_pins
            except Exception: ipins = []
            for q in ipins:
                sv = src((p, q.name))
                dv = None
                for a in ('default_value', 'default', 'value'):
                    if hasattr(q, a): dv = str(getattr(q, a))[:60]; break
                pins[q.name] = ([s[0].rsplit('.', 1)[-1] + ':' + s[1] for s in sv] if sv else dv)
            hits.append({'graph': gname, 'node': p.rsplit('.', 1)[-1], 'class': cls, 'type': t[-70:], 'pins': pins})
    d['hits'] = hits[:40]
    out[key] = d
pathlib.Path(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Saved/Codex/SHME_V228_20261025/probe_look228.json').write_text(json.dumps(out, indent=1, default=str), encoding='utf8')
print('LOOK228 ' + json.dumps(out, default=str)[:3500])
