"""GUARDIAN-9 save/reopen verification (FRESH editor, read-only): locked GUARDIAN-7 C8 face (DNA, morphs, LODs), GUARDIAN-8 hair h23 grooms and
the four GUARDIAN-8 bindings to the C8 face. Writes Saved/Codex/CharacterGuardian9_20261002/reopen_check.json"""
import unreal as u, pathlib, json
R = pathlib.Path(u.Paths.project_dir()).resolve(); O = R/'Saved/Codex/CharacterGuardian9_20261002/reopen_check.json'
G7 = '/Game/Sphirus/CharacterLab/CharacterGuardian7_20261002'; G8 = '/Game/Sphirus/CharacterLab/CharacterGuardian9_20261002'
out = {'dirty_before': [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]}; sme = u.get_editor_subsystem(u.SkeletalMeshEditorSubsystem)
m = u.load_asset(G8+'/Face/SKM_GD9_Face_g')
out['face_g'] = {'loaded': m is not None, 'morph_total': len(m.get_editor_property('morph_targets')), 'lod_verts': [sme.get_num_verts(m, i) for i in range(sme.get_lod_count(m))],
                  'user_data': [x.get_class().get_name() for x in (m.get_editor_property('asset_user_data') or [])]}
A = {}
for p in ('/Game/Sphirus/CharacterLab/CharacterGuardian8_20261002/Hair/GR_LK_Hair_Main_h23', '/Game/Sphirus/CharacterLab/CharacterGuardian8_20261002/Hair/GR_LK_Hair_Loose_h23', G8+'/MHC/MHC_GD9_G', G8+'/MHC/DNA/MHC_GD9_G_Head'):
    g = u.load_asset(p); A[p.split('/')[-1]] = {'loaded': g is not None, 'class': g.get_class().get_name() if g else None}
for b in ('HairMain_gh23', 'HairLoose_gh23', 'EyebrowsM_SlightArch_gh23', 'EyelashesS_Thin_gh23'):
    bd = u.load_asset(f'{G8}/Face/Bindings/GB_GD9_{b}'); A['GB_GD9_'+b] = {'loaded': bd is not None}
    if bd: A['GB_GD9_'+b].update({'groom': bd.get_editor_property('groom').get_name(), 'target': bd.get_editor_property('target_skeletal_mesh').get_name()})
out['assets'] = A; out['dirty_after'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
O.write_text(json.dumps(out, indent=1)); print('GD9_REOPEN', json.dumps(out)[:2500])
