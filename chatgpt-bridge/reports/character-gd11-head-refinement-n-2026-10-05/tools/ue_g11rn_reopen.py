"""GD11 head refinement C: save/reopen verification in a FRESH editor (read-only). Final candidate = face SKM_G11RN_Face_f4ab (DNA, morphs, LODs),
MHC_G11RN_F4AB + DNA, hair h37 grooms + materials, the four f3h37 bindings, the rig-test sequence. Writes Saved/Codex/GD11_HeadRefinementN_20261005/data/reopen_check.json"""
import unreal as u, pathlib, json
R = pathlib.Path(u.Paths.project_dir()).resolve(); O = R/'Saved/Codex/GD11_HeadRefinementN_20261005/data/reopen_check.json'
G = '/Game/Sphirus/CharacterLab/GD11_HeadRefinementN_20261005'
out = {'dirty_before': [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]}; sme = u.get_editor_subsystem(u.SkeletalMeshEditorSubsystem)
m = u.load_asset('/Game/Sphirus/CharacterLab/GD11_HeadRefinementN_20261005/Face/SKM_G11RN_Face_n1')
out['face_n1'] = {'loaded': m is not None, 'morph_total': len(m.get_editor_property('morph_targets')), 'lod_verts': [sme.get_num_verts(m, i) for i in range(sme.get_lod_count(m))],
                  'user_data': [x.get_class().get_name() for x in (m.get_editor_property('asset_user_data') or [])], 'skeleton': m.skeleton.get_path_name()}
for d in (m.get_editor_property('asset_user_data') or []):
    if isinstance(d, u.DNAAssetUserData): dn = d.get_editor_property('dna_asset'); out['face_n1']['dna'] = dn.get_path_name() if dn else None
A = {}
for p in (G+'/Hair/GR_LK_Hair_Main_h49a', G+'/Hair/GR_LK_Hair_Loose_h49a', G+'/Hair/MI_GD_Hair_h49a', G+'/Hair/MI_GD_HairLoose_h49a', G+'/Hair/SM_LK_HairHelmet_h49a', '/Game/Sphirus/CharacterLab/GD11_HeadRefinementN_20261005/MHC/MHC_G11RN_N1', '/Game/Sphirus/CharacterLab/GD11_HeadRefinementN_20261005/MHC/DNA/MHC_G11RN_N1_Head'):
    g = u.load_asset(p); A[p.split('/')[-1]] = {'loaded': g is not None, 'class': g.get_class().get_name() if g else None}
for b in ('HairMain_n1h49a', 'HairLoose_n1h49a', 'EyebrowsM_Fine_n1h49a', 'EyelashesS_Thin_n1h49a'):
    bd = u.load_asset(f'{G}/Face/Bindings/GB_G11RN_{b}'); A['GB_G11RN_'+b] = {'loaded': bd is not None}
    if bd: A['GB_G11RN_'+b].update({'groom': bd.get_editor_property('groom').get_name(), 'target': bd.get_editor_property('target_skeletal_mesh').get_name()})
out['assets'] = A; out['dirty_after'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
O.write_text(json.dumps(out, indent=1)); print('G11RN_REOPEN', json.dumps(out)[:2500])
# groom LOD table as saved (verifies the retuned LOD chain survived the reopen)
L = {}
for part in ('Main', 'Loose'):
    g = u.load_asset(G+'/Hair/GR_LK_Hair_%s_h49a' % part)
    L[part] = [[round(l.get_editor_property('curve_decimation'), 2), round(l.get_editor_property('screen_size'), 2), round(l.get_editor_property('thickness_scale'), 2), str(l.get_editor_property('geometry_type')).split('.')[-1][:7]] for l in g.get_editor_property('hair_groups_lod')[0].get_editor_property('lods')]
out['groom_lod_table'] = L; O.write_text(json.dumps(out, indent=1)); print('G11RN_REOPEN2', json.dumps(L))
