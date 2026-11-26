# w_hair_bind.py (write, gated): binds the approved C49 h1 bun groom (main + loose strands, authored on SKM_GD38_Face_t38) to the
# current player face SKM_MHC_Sph8_FaceMesh with a transfer binding (source GD38 face -> target Sph8 face, the route used for Hazel:
# GB_HF_*). Groom assets and materials are not modified. Prints the hair MI parameters (colour check).
import unreal as u, time
assert not u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world(), 'PIE running'
E = u.EditorAssetLibrary; H = '/Game/Sphirus/CharacterLab/CharacterCohesion_C49_20261104/Hair/'; DST = '/Game/Sphirus/CharacterLab/B13_20261126/Hair/'
FACE = u.load_asset('/Game/Sphirus/CharacterLab/Sph_20261108/Built/MHC_Sph8/Face/SKM_MHC_Sph8_FaceMesh'); SRC = u.load_asset('/Game/Sphirus/CharacterLab/GD38_IdentityMaster_20261011/Face/SKM_GD38_Face_t38')
assert FACE and SRC
for g, b in (('GR_C49_HairMain_h1', 'GB_Sph8_HairMainH1'), ('GR_C49_HairLoose_h1', 'GB_Sph8_HairLooseH1')):
    t = time.time(); gb = u.GroomLibrary.create_new_groom_binding_asset_with_path(DST + b, u.load_asset(H + g), FACE, 100, SRC, 0)
    assert gb, b
    print('HB', b, 'target', gb.get_editor_property('target_skeletal_mesh').get_name(), 'source', gb.get_editor_property('source_skeletal_mesh').get_name(), 's', round(time.time() - t, 1), 'saved', E.save_loaded_asset(gb, False))
for mi in ('MI_C49_HairMain_h1', 'MI_C49_HairLoose_h1'):
    m = u.load_asset(H + mi); ML = u.MaterialEditingLibrary
    print('HB mi', mi, 'parent', m.get_editor_property('parent').get_name(), {p.parameter_info.name: round(p.parameter_value, 3) for p in m.get_editor_property('scalar_parameter_values')})
