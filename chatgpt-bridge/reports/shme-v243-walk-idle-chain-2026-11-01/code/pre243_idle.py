"""pre243_idle.py (A/B PRE, in memory only - never saved): the idle TAKEOVER path's sequence players (AnimGraph, SequencePlayer nodes whose
sequence is the vendor 'A_Ranger_Idle_Neutral_CWF') play the V2.42 weighted/breathing idle SHM242_Idle_Weighted instead; compile.
POST = post243_idle.py reloads the ABPs from disk. builtins.V243_IDLE_SEQ optional path. Prints PREIDLE243 ..."""
import unreal as u, builtins
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'
seq = u.load_asset(getattr(builtins, 'V243_IDLE_SEQ', '/Game/GraceRanger/SHME/Animations/V242/SHM242_Idle_Weighted')); assert seq; bp = u.load_asset(AP); n_set = 0; names = []
for g in B.list_graphs(bp):
    for n in B.find_nodes(g):
        if n.get_class().get_name() != 'AnimGraphNode_SequencePlayer': continue
        nd = n.get_editor_property('node'); cur = nd.get_editor_property('sequence')
        if cur and 'A_Ranger_Idle_Neutral_CWF' in cur.get_name():
            nd.set_editor_property('sequence', seq); n.set_editor_property('node', nd); n_set += 1; names.append(g.get_name() + ':' + n.get_name())
u.BlueprintEditorLibrary.compile_blueprint(bp); cp = u.load_asset(AP.replace('Base', '')); u.BlueprintEditorLibrary.compile_blueprint(cp)
print('PREIDLE243 set %d %s status %s' % (n_set, names, bp.get_editor_property('status')))
