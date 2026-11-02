"""probe250_animgraph.py (measure job, read-only): pose-flow order of ABP_GR_MotionMatchingBase - every graph whose nodes are AnimGraphNode_*,
walked back from each Root / Output pose through the pose input pins (node class, title, pose sources). Prints AGRAPH250 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import pn, info, obj, src
import json
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'
bp = u.load_asset(AP); out = {}
for g in B.list_graphs(bp):
    ns = [pn(n) for n in B.find_nodes(g)]
    anim = [p for p in ns if obj(p).get_class().get_name().startswith('AnimGraphNode_')]
    if not anim: continue
    rec = []
    for p in anim:
        o = obj(p); cls = o.get_class().get_name().replace('AnimGraphNode_', '')
        try: title = str(o.get_node_title(u.NodeTitleType.FULL_TITLE)) if hasattr(o, 'get_node_title') else ''
        except Exception: title = ''
        ins = []
        try:
            for q in info(p).input_pins:
                ss = src((p, q.name))
                for s_ in ss:
                    sc = obj(s_[0]).get_class().get_name().replace('AnimGraphNode_', '').replace('K2Node_', 'K2:')
                    if 'AnimGraphNode' in obj(s_[0]).get_class().get_name(): ins.append('%s<-%s' % (q.name, s_[0].rsplit('.', 1)[-1] + ':' + sc))
        except Exception as e: ins.append('err ' + str(e)[:60])
        rec.append([p.rsplit('.', 1)[-1], cls, title[:60], ins])
    out[g.get_name()] = rec
print('AGRAPH250 ' + json.dumps(out, default=str))
