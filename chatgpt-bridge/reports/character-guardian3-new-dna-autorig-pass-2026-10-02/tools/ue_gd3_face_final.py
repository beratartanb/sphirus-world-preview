"""GUARDIAN-3: rigged MHC head -> project face asset WITH a persisted DNA (RigLogic after restart).
Order matters: export_geometry -> rename_asset(export -> Face/<dst>) while the DNA is still the transient in-memory rig DNA -> move that DNA object
under the final mesh (sub-object, unique name) -> save -> project setup in place (plugin RigLogic post-process ABP, P material slots, P physics asset).
builtins.GD3_FF = {'name': 'MHC_GD3_N6', 'dst': 'SKM_GD3_Face_n6'}"""
import unreal as u, json, builtins, time, traceback
C = builtins.GD3_FF; S = u.get_editor_subsystem(u.MetaHumanCharacterEditorSubsystem); EAL = u.EditorAssetLibrary; G = '/Game/Sphirus/CharacterLab/CharacterGuardian3_20261001'; out = {}
dst = G+'/Face/'+C['dst']; exp = G+'/MHC/ExportF/'+C['name']+'_Head'
for p in (dst, exp):
    if EAL.does_asset_exist(p):
        a = u.load_asset(p); EAL.delete_loaded_asset(a)
        if EAL.does_asset_exist(p): EAL.delete_asset(p)
    out['pre_exists_'+p.split('/')[-1]] = EAL.does_asset_exist(p)
ch = u.load_asset(G+'/MHC/'+C['name'])
try:
    assert S.try_add_object_to_edit(ch)
    gp = u.MetaHumanGeometryExportParams(); gp.project_path = G+'/MHC/ExportF'; gp.head_skeletal_mesh = True; gp.body_skeletal_mesh = False; gp.full_body_skeletal_mesh = False; gp.overwrite_existing_assets = True
    u.MetaHumanCharacterExportBlueprintLibrary.export_geometry(ch, gp)
finally:
    S.remove_object_to_edit(ch)
out['renamed_asset'] = EAL.rename_asset(exp, dst); m = u.load_asset(dst)
def dna_of(mesh):
    for d in (mesh.get_editor_property('asset_user_data') or []):
        if isinstance(d, u.DNAAssetUserData): return d.get_editor_property('dna_asset')
dna = dna_of(m); out['dna_before'] = dna.get_path_name() if dna else None
if dna and dna.get_outermost().get_name().startswith('/Engine/Transient'): out['dna_moved'] = dna.rename(C['dst']+'_DNA_'+time.strftime('%H%M%S'), m)
dna = dna_of(m); out['dna_after'] = dna.get_path_name() if dna else None
P = u.load_asset('/Game/Sphirus/CharacterLab/CharacterGuardian2_20261001/Face/SKM_GD_FaceMesh_p')
m.set_editor_property('post_process_anim_blueprint', u.load_class(None, '/MetaHumanCharacter/Face/ABP_Face_PostProcess.ABP_Face_PostProcess_C'))
pm = P.get_editor_property('materials'); new = []
for i, s in enumerate(m.get_editor_property('materials')):
    ns = u.SkeletalMaterial(); ns.set_editor_property('material_interface', pm[i].get_editor_property('material_interface') if i < len(pm) else s.get_editor_property('material_interface')); ns.set_editor_property('material_slot_name', s.get_editor_property('material_slot_name')); new.append(ns)
m.set_editor_property('materials', new); m.set_editor_property('physics_asset', P.get_editor_property('physics_asset'))
dna = dna_of(m); out['dna_after_setup'] = dna.get_path_name() if dna else None
out['saved'] = EAL.save_loaded_asset(m, False); out['morphs'] = len(m.get_editor_property('morph_targets')); out['skeleton'] = m.skeleton.get_path_name()
out['dirty'] = [x.get_path_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]; print('GD3_FF', json.dumps(out))
