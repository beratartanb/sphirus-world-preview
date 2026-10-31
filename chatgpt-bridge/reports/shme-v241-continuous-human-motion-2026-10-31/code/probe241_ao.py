"""probe241_ao.py (measure): nodes of the LookAtAimOffset graph (ABP base / child / linked layer classes) with their AO / blend space
assets and alpha / bone settings. Prints AO241 lines."""
import unreal as u, json
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import pn, info, src
for P in ('/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase', '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatching'):
    bp = u.load_asset(P)
    for g in B.list_graphs(bp):
        if 'AimOffset' not in g.get_name() and 'LookAt' not in g.get_name(): continue
        for n in B.find_nodes(g):
            cls = n.get_class().get_name(); d = {}
            try:
                nd = n.get_editor_property('node')
                for k in ('blend_space', 'alpha', 'b_alpha_bool_enabled', 'alpha_input_type', 'look_at_bone', 'bone_to_modify', 'look_at_target', 'base_pose', 'blend_poses', 'layer_setup'):
                    try: d[k] = str(nd.get_editor_property(k))[:120]
                    except Exception: pass
            except Exception: pass
            ins = []
            try:
                for q in info(pn(n)).input_pins: ins.append('%s<-%s' % (q.name, [s[0].split('.')[-1] + ':' + s[1] for s in src((pn(n), q.name))][:2]))
            except Exception: pass
            print('AO241 %s | %s | %s | %s | %s' % (P.split('/')[-1], g.get_name(), cls, json.dumps(d)[:400], ' '.join(ins)[:300]))
