# w_trav_create.py (write, gated; movement pass 4): project-owned traversal component.
# 1. duplicates the vendor GASP component /Game/Blueprints/AC_TraversalLogic to /Game/Sphirus/Player/Traversal/AC_Sph_Traversal
#    (vendor original untouched; the copy's ledge step is replaced by generic geometry probing in m_trav5_mcp.py);
# 2. adds it to BP_HybridA_Player as component 'SphTraversal' (in memory; saved with the pass-4 save job).
import unreal as u
assert not u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world(), 'PIE running'
EAL = u.EditorAssetLibrary; DST = '/Game/Sphirus/Player/Traversal/AC_Sph_Traversal'
if not EAL.does_asset_exist(DST):
    a = EAL.duplicate_asset('/Game/Blueprints/AC_TraversalLogic', DST); assert a, 'duplicate failed'
c = u.load_asset(DST); u.BlueprintEditorLibrary.compile_blueprint(c); print('TRAVC copy', c.get_path_name(), 'saved', EAL.save_loaded_asset(c, False))
bp = u.load_asset('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player')
sub = u.get_engine_subsystem(u.SubobjectDataSubsystem); hs = sub.k2_gather_subobject_data_for_blueprint(bp)
have = [u.SubobjectDataBlueprintFunctionLibrary.get_object(sub.k2_find_subobject_data_from_handle(h)) for h in hs]
names = [o.get_name() for o in have if o]
if not any('SphTraversal' in n for n in names):
    p = u.AddNewSubobjectParams(parent_handle=hs[0], new_class=c.generated_class(), blueprint_context=bp)
    h, fail = sub.add_new_subobject(p); print('TRAVC add', fail)
    try: sub.rename_subobject(h, u.Text('SphTraversal'))
    except Exception as e: print('TRAVC rename', e)
    u.BlueprintEditorLibrary.compile_blueprint(bp)
hs = sub.k2_gather_subobject_data_for_blueprint(bp)
print('TRAVC comps', [o.get_name() for o in [u.SubobjectDataBlueprintFunctionLibrary.get_object(sub.k2_find_subobject_data_from_handle(h)) for h in hs] if o and 'Travers' in o.get_class().get_name()])
