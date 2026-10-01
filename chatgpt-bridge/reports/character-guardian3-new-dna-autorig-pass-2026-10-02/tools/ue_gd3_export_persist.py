"""GUARDIAN-3: (re)export the rigged MHC head geometry and PERSIST its DNA. MetaHumanCharacter export_geometry leaves the mesh's DNAAssetUserData
pointing at a transient DNA object (/Engine/Transient.*_DNA) -> RigLogic works only in the creating session. The DNA object is renamed into the
export mesh (sub-object) so it is saved with the package. builtins.GD3_EP = {'name': 'MHC_GD3_N6'}"""
import unreal as u, json, builtins, traceback, time
C = builtins.GD3_EP; S = u.get_editor_subsystem(u.MetaHumanCharacterEditorSubsystem); EAL = u.EditorAssetLibrary; F = '/Game/Sphirus/CharacterLab/CharacterGuardian3_20261001/MHC'; out = {}
ch = u.load_asset(F+'/'+C['name'])
try:
    assert S.try_add_object_to_edit(ch)
    gp = u.MetaHumanGeometryExportParams(); gp.project_path = F+'/Export'; gp.head_skeletal_mesh = True; gp.body_skeletal_mesh = False; gp.full_body_skeletal_mesh = False; gp.overwrite_existing_assets = True
    u.MetaHumanCharacterExportBlueprintLibrary.export_geometry(ch, gp)
finally:
    S.remove_object_to_edit(ch)
e = u.load_asset(F+'/Export/'+C['name']+'_Head')
for d in (e.get_editor_property('asset_user_data') or []):
    if isinstance(d, u.DNAAssetUserData):
        dna = d.get_editor_property('dna_asset'); out['before'] = dna.get_path_name() if dna else None
        if dna and dna.get_outermost().get_name().startswith('/Engine/Transient'):
            out['renamed'] = dna.rename(C['name']+'_FaceDNA_'+time.strftime('%H%M%S'), e)   # unique: renaming onto an existing sub-object is a fatal error
        dna = d.get_editor_property('dna_asset'); out['after'] = dna.get_path_name() if dna else None
out['saved'] = EAL.save_loaded_asset(e, False); out['dirty'] = [x.get_path_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('GD3_EP', json.dumps(out))
