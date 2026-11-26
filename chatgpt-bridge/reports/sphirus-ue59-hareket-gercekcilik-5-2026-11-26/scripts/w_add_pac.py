# w_add_pac.py (write context, in memory - saved later with the impact graph): adds a PhysicalAnimationComponent 'SphPhysAnim' to the player.
import unreal as u
assert not u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world(), 'PIE running'
bp = u.load_asset('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'); sub = u.get_engine_subsystem(u.SubobjectDataSubsystem); L = u.SubobjectDataBlueprintFunctionLibrary
hs = sub.k2_gather_subobject_data_for_blueprint(bp); names = {L.get_object(sub.k2_find_subobject_data_from_handle(h)).get_name().split('_GEN')[0]: h for h in hs if L.get_object(sub.k2_find_subobject_data_from_handle(h))}
if 'SphPhysAnim' not in names:
    root = hs[0]
    nh, fail = sub.add_new_subobject(u.AddNewSubobjectParams(parent_handle=root, new_class=u.PhysicalAnimationComponent, blueprint_context=bp)); print('PAC add', fail, sub.rename_subobject(nh, u.Text('SphPhysAnim')))
u.BlueprintEditorLibrary.compile_blueprint(bp)
print('PAC comps', [L.get_object(sub.k2_find_subobject_data_from_handle(h)).get_name() for h in sub.k2_gather_subobject_data_for_blueprint(bp) if 'Phys' in L.get_object(sub.k2_find_subobject_data_from_handle(h)).get_name()])
