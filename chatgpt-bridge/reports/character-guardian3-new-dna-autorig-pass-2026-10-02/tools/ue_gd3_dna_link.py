"""GUARDIAN-3: give a project face a PERSISTENT reference to its auto-rig DNA. export_geometry leaves a transient DNA reference (RigLogic dies after
restart). import_and_attach_dna (exported .dna) creates a saved reference, which is then consolidated onto the in-engine DNA asset written by
export_dna (<MHC>/DNA/<name>_Head) - the file-attached DNA alone rotates the head with the plugin face ABPs; the export_dna asset deforms correctly.
builtins.GD3_DL = {'face': mesh path, 'dna_file': abs .dna path, 'dna_asset': '/Game/.../MHC/DNA/<name>_Head'}"""
import unreal as u, json, builtins
C = builtins.GD3_DL; EAL = u.EditorAssetLibrary; out = {}
def dna_of(mesh):
    for d in (mesh.get_editor_property('asset_user_data') or []):
        if isinstance(d, u.DNAAssetUserData): return d.get_editor_property('dna_asset')
m = u.load_asset(C['face']); good = u.load_asset(C['dna_asset']); out['good'] = good.get_class().get_name() if good else None
u.DNAImporterLibrary.import_and_attach_dna(C['dna_file'], m, True); X = dna_of(m); out['attached'] = X.get_path_name() if X else None
if X and good and X != good: EAL.save_loaded_asset(X, False); out['consolidated'] = EAL.consolidate_assets(good, [X])
d = dna_of(m); out['face_dna'] = d.get_path_name() if d else None; out['face_saved'] = EAL.save_loaded_asset(m, False)
out['dirty'] = [x.get_path_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]; print('GD3_DL', json.dumps(out))
