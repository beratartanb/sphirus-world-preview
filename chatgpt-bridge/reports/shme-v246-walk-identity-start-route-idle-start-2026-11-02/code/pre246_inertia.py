"""pre246_inertia.py (A/B PRE, in memory - never saved): the contact-planned START evaluator hand-over (AnimGraph BlendListByBool_3:
pose 0 = SequenceEvaluator_0 (CP start), pose 1 = cached MM pose, active <- CP_StartOwned, BlendTime 0.12/0.18 = fixed crossfade) switches
to TransitionType Inertialization (the downstream Inertialization_0 node already exists), so a start blends from the CURRENT pose (live
weighted idle, moved stop tail) with velocity continuity instead of a fixed crossfade. Optional builtins.V246_INERTIA_STOP also switches
BlendListByBool_4 (CP stop). POST = post246_inertia.py reloads the ABPs. Prints PREINERTIA246 ..."""
import unreal as u, builtins, json
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'
bp = u.load_asset(AP); out = {}; targets = ['AnimGraphNode_BlendListByBool_3'] + (['AnimGraphNode_BlendListByBool_4'] if getattr(builtins, 'V246_INERTIA_STOP', False) else [])
for g in B.list_graphs(bp):
    for n in B.find_nodes(g):
        if n.get_name() in targets:
            nd = n.get_editor_property('node'); before = str(nd.get_editor_property('transition_type'))
            E = getattr(u, 'BlendListTransitionType', None) or getattr(u, 'TransitionType', None)
            if E is None: E = next(getattr(u, k) for k in dir(u) if 'Transition' in k and hasattr(getattr(u, k), 'INERTIALIZATION'))
            nd.set_editor_property('transition_type', E.INERTIALIZATION); n.set_editor_property('node', nd)
            out[n.get_name()] = {'graph': g.get_name(), 'before': before, 'after': str(n.get_editor_property('node').get_editor_property('transition_type'))}
u.BlueprintEditorLibrary.compile_blueprint(bp); cp = u.load_asset(AP.replace('Base', '')); u.BlueprintEditorLibrary.compile_blueprint(cp)
out['status'] = str(bp.get_editor_property('status'))
print('PREINERTIA246 ' + json.dumps(out, default=str))
