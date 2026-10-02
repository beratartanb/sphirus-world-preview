"""GUARDIAN-4 save/reopen verification (FRESH editor, read-only): final face (new DNA, plugin skeleton/ABPs), DNA asset, MHC character, grooms/bindings,
skin/eye/body MIs, reference-expression and rig sequences, garments, Chaos shorts. Writes Saved/Codex/CharacterGuardian6_20261002/reopen_check.json"""
import unreal as u, pathlib, json
R = pathlib.Path(u.Paths.project_dir()).resolve(); O = R/'Saved/Codex/CharacterGuardian6_20261002/reopen_check.json'
G4 = '/Game/Sphirus/CharacterLab/CharacterGuardian6_20261002'; GD = '/Game/Sphirus/CharacterLab/CharacterGuardian_20261001'; CR = '/Game/Sphirus/CharacterLab/CharacterCorrective_20261001'; ME = u.MaterialEditingLibrary
out = {'dirty_before': [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]}; sme = u.get_editor_subsystem(u.SkeletalMeshEditorSubsystem)
def mesh_info(path):
    m = u.load_asset(path); d = {'loaded': m is not None}
    if not m: return d
    d['morph_total'] = len(m.get_editor_property('morph_targets')); d['lod_verts'] = [sme.get_num_verts(m, i) for i in range(sme.get_lod_count(m))]
    d['skeleton'] = m.skeleton.get_path_name().split('/')[-1] if m.skeleton else None; d['pp_abp'] = m.post_process_anim_blueprint.get_path_name().split('/')[-1] if m.post_process_anim_blueprint else None
    d['user_data'] = [x.get_class().get_name() for x in (m.get_editor_property('asset_user_data') or [])]; return d
out['face_s4'] = mesh_info(G4+'/Face/SKM_GD6_Face_s4'); out['henley_g17e'] = mesh_info(GD+'/Outfit/SKM_LK_Henley_g17e'); out['shorts_g16c'] = mesh_info(CR+'/Outfit/SKM_LK_Shorts_g16c')
A = {}
for p in (G4+'/MHC/MHC_GD6_S4', G4+'/MHC/DNA/MHC_GD6_S4_Head', G4+'/Face/Diagnostics/AS_GD6_RefExpression', '/Game/Sphirus/CharacterLab/CharacterGuardian3_20261001/Face/Diagnostics/AS_GD3_FacialRig',
          '/Game/Sphirus/CharacterLab/CharacterGuardian5_20261002/Hair/GR_LK_Hair_Main_h6', '/Game/Sphirus/CharacterLab/CharacterGuardian5_20261002/Hair/GR_LK_Hair_Loose_h6', '/Game/Sphirus/CharacterLab/CharacterGuardian5_20261002/Skin/MI_LK_Face_LOD0_VT_g5k7', '/Game/Sphirus/CharacterLab/CharacterGuardian5_20261002/Skin/MI_GD5_Body_k7', '/Game/Sphirus/CharacterLab/CharacterGuardian3_20261001/Skin/MI_GD3_EyeL_e2', '/Game/Sphirus/CharacterLab/CharacterGuardian3_20261001/Skin/MI_GD3_EyeR_e2', CR+'/Cloth/CA_CR_Shorts_m1'):
    a = u.load_asset(p); A[p.split('/')[-2]+'/'+p.split('/')[-1]] = {'loaded': a is not None, 'class': a.get_class().get_name() if a else None}
    if a and isinstance(a, u.GroomAsset): A[p.split('/')[-2]+'/'+p.split('/')[-1]].update({'lod_mode': str(a.get_editor_property('lod_mode')), 'lods': len(a.get_editor_property('hair_groups_lod')[0].get_editor_property('lods'))})
    if a and isinstance(a, u.MetaHumanCharacter): A[p.split('/')[-2]+'/'+p.split('/')[-1]].update({'fixed_body_type': a.get_editor_property('fixed_body_type'), 'has_face_dna_blendshapes': a.get_editor_property('has_face_dna_blendshapes')})
for b in ('HairMain_s4f', 'HairLoose_s4f', 'EyebrowsM_SlightArch_s4f', 'EyelashesS_Thin_s4f'):
    bd = u.load_asset(f'{G4}/Face/Bindings/GB_GD6_{b}'); A['GB_GD6_'+b] = {'loaded': bd is not None}
    if bd: A['GB_GD6_'+b].update({'groom': bd.get_editor_property('groom').get_name(), 'target': bd.get_editor_property('target_skeletal_mesh').get_name()})
m = u.load_asset('/Game/Sphirus/CharacterLab/CharacterGuardian5_20261002/Skin/MI_LK_Face_LOD0_VT_g5k7'); v = ME.get_material_instance_vector_parameter_value(m, 'Basecolor Global Multiply Post-Bake'); A['Skin/MI_LK_Face_LOD0_VT_g5k7']['tint'] = [round(v.r, 3), round(v.g, 3), round(v.b, 3)]
out['assets'] = A; out['dirty_after'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
O.write_text(json.dumps(out, indent=1)); print('GD6_REOPEN', json.dumps(out)[:3500])
