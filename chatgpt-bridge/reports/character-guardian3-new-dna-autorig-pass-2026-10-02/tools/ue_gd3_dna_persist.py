"""GUARDIAN-3: persist the auto-rig DNA for a project face mesh (MetaHumanCharacter exports reference a TRANSIENT DNA object, so RigLogic dies
after an editor restart). The in-engine rig DNA of the MHC preview face is duplicated into a saved DNA asset; the face mesh gets a DNA reference via
DNAImporterLibrary.import_and_attach_dna (exported .dna) and that reference is consolidated onto the duplicated in-engine DNA asset.
builtins.GD3_DP = {'name': 'MHC_GD3_N6', 'face': '/Game/.../Face/SKM_GD3_Face_n6r', 'dna_file': abs path, 'dna_asset': '/Game/.../Face/DNA_GD3_N6'}"""
import unreal as u, json, builtins, traceback
C = builtins.GD3_DP; S = u.get_editor_subsystem(u.MetaHumanCharacterEditorSubsystem); EAL = u.EditorAssetLibrary; G = '/Game/Sphirus/CharacterLab/CharacterGuardian3_20261001'; out = {}
def dna_of(mesh):
    for d in (mesh.get_editor_property('asset_user_data') or []):
        if isinstance(d, u.DNAAssetUserData): return d.get_editor_property('dna_asset')
ch = u.load_asset(G+'/MHC/'+C['name'])
try:
    assert S.try_add_object_to_edit(ch); act = S.spawn_meta_human_actor(ch, True)
    fc = [c for c in act.get_components_by_class(u.SkeletalMeshComponent) if c.get_name() == 'Face'][0]; T = dna_of(fc.get_editor_property('skeletal_mesh_asset')); out['transient'] = T.get_path_name() if T else None
    if EAL.does_asset_exist(C['dna_asset']): out['good_exists'] = True; good = u.load_asset(C['dna_asset'])
    else: good = EAL.duplicate_loaded_asset(T, C['dna_asset'])
    out['good'] = good.get_path_name() if good else None; out['good_saved'] = EAL.save_loaded_asset(good, False) if good else None
    act.destroy_actor()
except Exception: out['err1'] = traceback.format_exc()[-800:]
finally:
    S.remove_object_to_edit(ch)
try:
    m = u.load_asset(C['face']); u.DNAImporterLibrary.import_and_attach_dna(C['dna_file'], m, True); X = dna_of(m); out['attached'] = X.get_path_name() if X else None
    if X and good and X != good:
        xp = X.get_path_name().split('.')[0]; EAL.save_loaded_asset(X, False)
        out['consolidated'] = EAL.consolidate_assets(good, [X]); out['after_consolidate'] = (lambda d: d.get_path_name() if d else None)(dna_of(m))
        if EAL.does_asset_exist(xp): out['x_left'] = xp
    out['face_saved'] = EAL.save_loaded_asset(m, False); out['good_saved2'] = EAL.save_loaded_asset(good, False)
except Exception: out['err2'] = traceback.format_exc()[-800:]
out['dirty'] = [x.get_path_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]; print('GD3_DP', json.dumps(out))
