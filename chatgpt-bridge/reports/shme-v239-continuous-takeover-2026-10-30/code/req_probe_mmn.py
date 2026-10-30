exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import src, pn, info, obj
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'
bp = u.load_asset(AP); ag = pn(graph(bp, 'AnimGraph'))
for n in B.find_nodes(obj(ag)):
    if n.get_class().get_name() != 'AnimGraphNode_MotionMatching': continue
    p = pn(n)
    for q in info(p).input_pins:
        s = src((p, q.name)); print('PIN', q.name, repr(q.value)[:40], [(x[0].rsplit('.', 1)[-1], x[1], str(info(x[0]).type_id)[-40:]) for x in s][:2])
    try:
        nd = n.get_editor_property('node'); print('NODE', {k: str(nd.get_editor_property(k))[:60] for k in ('blend_time', 'max_active_blends', 'pose_jump_threshold_time', 'pose_reselect_history', 'search_throttle_time', 'use_inertial_blend', 'reset_on_becoming_relevant', 'should_filter_notifies', 'player_play_rate', 'blend_profile')})
    except Exception as e: print('NODEERR', str(e)[:200])
