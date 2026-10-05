"""GUARDIAN-3: project face asset from an auto-rigged MetaHumanCharacter head export (new DNA, joints in the project frame because the MHC
character carries our B2 body as a fixed whole rig). Duplicates <MHC>/Export/<src> -> CharacterGuardian3/Face/<dst>, assigns the project face
skeleton copy (same 875-bone archetype hierarchy) and the project RigLogic post-process ABP, copies the 15 material slots of the P face (same slot
layout; skin is overridden per QA config) and the P physics asset. The DNA user data of the export (NEW DNA) is kept.
builtins.GD3_FS = {'src': '/Game/.../MHC/Export/MHC_GD3_N2_Head', 'dst': 'SKM_GD3_Face_n2'}  (src is MOVED to dst)"""
import unreal as u, json, builtins
C = builtins.GD3_FS; EAL = u.EditorAssetLibrary; F = '/Game/Sphirus/CharacterLab/GD11_HeadRefinementM_20261005/Face'; out = {}
P = u.load_asset('/Game/Sphirus/CharacterLab/CharacterGuardian2_20261001/Face/SKM_GD_FaceMesh_p')
dst = F+'/'+C['dst']
if EAL.does_asset_exist(dst):
    a = u.load_asset(dst); EAL.delete_loaded_asset(a)
    if EAL.does_asset_exist(dst): EAL.delete_asset(dst)
# MOVE (not duplicate): the export keeps its persisted DNA sub-object (ue_gd3_export_persist.py); duplicate_asset drops the DNA reference
assert EAL.rename_asset(C['src'], dst), 'rename failed'; m = u.load_asset(dst)
sk = P.skeleton; out['skeleton_before'] = m.skeleton.get_path_name()
try: m.set_editor_property('skeleton', sk); out['skeleton_set'] = True
except Exception as e: out['skeleton_set'] = str(e)
out['skeleton_after'] = m.skeleton.get_path_name()
m.set_editor_property('post_process_anim_blueprint', u.load_class(None, C.get('pp_abp', '/MetaHumanCharacter/Face/ABP_Face_PostProcess.ABP_Face_PostProcess_C'))); out['pp_abp'] = m.post_process_anim_blueprint.get_path_name() if m.post_process_anim_blueprint else None
pm = P.get_editor_property('materials'); mm = m.get_editor_property('materials'); new = []
for i, s in enumerate(mm):
    ns = u.SkeletalMaterial(); ns.set_editor_property('material_interface', pm[i].get_editor_property('material_interface') if i < len(pm) else s.get_editor_property('material_interface'))
    ns.set_editor_property('material_slot_name', s.get_editor_property('material_slot_name'))
    new.append(ns)
m.set_editor_property('materials', new); out['materials'] = [x.get_editor_property('material_interface').get_name() for x in m.get_editor_property('materials')]
out['slot_names_new'] = [str(s.get_editor_property('material_slot_name')) for s in mm]; out['slot_names_P'] = [str(s.get_editor_property('material_slot_name')) for s in pm]
try: m.set_editor_property('physics_asset', P.get_editor_property('physics_asset')); out['phys'] = True
except Exception as e: out['phys'] = str(e)
ud = [d.get_class().get_name() for d in (m.get_editor_property('asset_user_data') or [])]; out['user_data'] = ud
for d in (m.get_editor_property('asset_user_data') or []):
    if isinstance(d, u.DNAAssetUserData): dn = d.get_editor_property('dna_asset'); out['dna'] = dn.get_path_name() if dn else None
out['morphs'] = len(m.get_editor_property('morph_targets')); out['saved'] = EAL.save_loaded_asset(m, False)
out['dirty'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('GD3_FS', json.dumps(out))
