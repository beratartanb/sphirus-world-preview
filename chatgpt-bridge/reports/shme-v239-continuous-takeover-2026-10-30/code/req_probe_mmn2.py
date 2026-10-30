exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'
bp = u.load_asset(AP); ag = pn(graph(bp, 'AnimGraph')) if False else None
from qa_graph import pn, obj
ag = pn(graph(bp, 'AnimGraph'))
for n in B.find_nodes(obj(ag)):
    if n.get_class().get_name() != 'AnimGraphNode_MotionMatching': continue
    nd = n.get_editor_property('node'); s = nd.export_text() if hasattr(nd, 'export_text') else str(nd)
    print('NODETXT', s[:3000])
