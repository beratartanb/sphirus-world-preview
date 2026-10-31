"""pre241_ao.py (A/B PRE, in memory only - never saved): the vendor aim offset node of the LookAtAimOffset layer (ABP_GR_MotionMatchingBase,
BlendSpacePlayer -> BS_Neutral_AO_Stand) plays the V2.41 regional copy BS_SHM241_AO_Head; compile. POST = post241_ao.py reloads the ABPs
from disk. builtins.V241_AOBS optional path. Prints PREAO241 ..."""
import unreal as u, builtins
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'
bs = u.load_asset(getattr(builtins, 'V241_AOBS', '/Game/GraceRanger/SHME/Animations/V241/AO/BS_SHM241_AO_Head')); bp = u.load_asset(AP); n_set = 0
for g in B.list_graphs(bp):
    if g.get_name() != 'LookAtAimOffset': continue
    for n in B.find_nodes(g):
        if n.get_class().get_name() != 'AnimGraphNode_BlendSpacePlayer': continue
        nd = n.get_editor_property('node'); cur = nd.get_editor_property('blend_space')
        if cur and 'AO' in cur.get_name():
            nd.set_editor_property('blend_space', bs); n.set_editor_property('node', nd); n_set += 1
u.BlueprintEditorLibrary.compile_blueprint(bp); cp = u.load_asset(AP.replace('Base', '')); u.BlueprintEditorLibrary.compile_blueprint(cp)
chk = [n.get_editor_property('node').get_editor_property('blend_space').get_name() for g in B.list_graphs(bp) if g.get_name() == 'LookAtAimOffset' for n in B.find_nodes(g) if n.get_class().get_name() == 'AnimGraphNode_BlendSpacePlayer']
print('PREAO241 set %d now %s status %s' % (n_set, chk, bp.get_editor_property('status')))
