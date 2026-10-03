"""GD11 head refinement: save/reopen verification in a FRESH editor (read-only). Final candidate = face SKM_G11R_Face_r3 (DNA, morphs, LODs),
MHC_G11R_R3 + DNA, hair h32 grooms + materials, the four r3h32 bindings, the rig-test sequence. Writes Saved/Codex/GD11_HeadRefinement_20261003/data/reopen_check.json"""
import unreal as u, pathlib, json
R = pathlib.Path(u.Paths.project_dir()).resolve(); O = R/'Saved/Codex/GD11_HeadRefinement_20261003/data/reopen_check.json'
G = '/Game/Sphirus/CharacterLab/GD11_HeadRefinement_20261003'
out = {'dirty_before': [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]}; sme = u.get_editor_subsystem(u.SkeletalMeshEditorSubsystem)
m = u.load_asset(G+'/Face/SKM_G11R_Face_r3')
out['face_r3'] = {'loaded': m is not None, 'morph_total': len(m.get_editor_property('morph_targets')), 'lod_verts': [sme.get_num_verts(m, i) for i in range(sme.get_lod_count(m))],
                  'user_data': [x.get_class().get_name() for x in (m.get_editor_property('asset_user_data') or [])], 'skeleton': m.skeleton.get_path_name()}
for d in (m.get_editor_property('asset_user_data') or []):
    if isinstance(d, u.DNAAssetUserData): dn = d.get_editor_property('dna_asset'); out['face_r3']['dna'] = dn.get_path_name() if dn else None
A = {}
for p in (G+'/Hair/GR_LK_Hair_Main_h32', G+'/Hair/GR_LK_Hair_Loose_h32', G+'/Hair/MI_GD_Hair_h32', G+'/Hair/MI_GD_HairLoose_h32', G+'/MHC/MHC_G11R_R3', G+'/MHC/DNA/MHC_G11R_R3_Head', G+'/Face/Diagnostics/AS_G11R_FacialRig'):
    g = u.load_asset(p); A[p.split('/')[-1]] = {'loaded': g is not None, 'class': g.get_class().get_name() if g else None}
for b in ('HairMain_r3h32', 'HairLoose_r3h32', 'EyebrowsM_SlightArch_r3h32', 'EyelashesS_Thin_r3h32'):
    bd = u.load_asset(f'{G}/Face/Bindings/GB_G11R_{b}'); A['GB_G11R_'+b] = {'loaded': bd is not None}
    if bd: A['GB_G11R_'+b].update({'groom': bd.get_editor_property('groom').get_name(), 'target': bd.get_editor_property('target_skeletal_mesh').get_name()})
out['assets'] = A; out['dirty_after'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
O.write_text(json.dumps(out, indent=1)); print('G11R_REOPEN', json.dumps(out)[:2500])
