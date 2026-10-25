"""probe_lookat228.py (editor job, READ-ONLY): the three LookAt skeletal-control nodes of ABP_GR_MotionMatchingBase.AnimGraph (spine_03 / neck_01 / head): their FAnimNode_LookAt settings (look at axis / look up axis / clamp / interpolation / target offset) and the alpha source chain (two levels). Prints LOOKAT228."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import src, pn, info, obj
import json
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'
bp = u.load_asset(AP); out = {}
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
def tree(p, depth):
    d = {'type': tid(p)[-50:]}
    if depth <= 0: return d
    try: ipins = info(p).input_pins
    except Exception: return d
    for q in ipins:
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
gp = pn(graph(bp, 'AnimGraph'))
for n in B.find_nodes(obj(gp)):
    if n.get_class().get_name() != 'AnimGraphNode_LookAt': continue
    p = pn(n); d = {'type': tid(p)[-40:]}
    try:
        node = n.get_editor_property('node')
        for k in ('look_at_axis', 'look_up_axis', 'use_look_up_axis', 'look_at_clamp', 'interpolation_type', 'interpolation_time', 'interpolation_trigger_threshold', 'look_at_location', 'bone_to_modify', 'look_at_target', 'alpha', 'alpha_input_type', 'alpha_scale_bias', 'alpha_bool_blend'):
            try:
                v = node.get_editor_property(k)
                try: d[k] = {kk: str(v.get_editor_property(kk))[:40] for kk in ('axis', 'custom_axis', 'in_bone_space', 'bone_name') if True}
                except Exception: d[k] = str(v)[:80]
            except Exception as e: d[k] = 'ERR'
    except Exception as e: d['node_err'] = str(e)[:80]
    d['alpha_src'] = tree(p, 3).get('Alpha')
    out[p.rsplit('.', 1)[-1]] = d
print('LOOKAT228 ' + json.dumps(out, default=str)[:3500])
