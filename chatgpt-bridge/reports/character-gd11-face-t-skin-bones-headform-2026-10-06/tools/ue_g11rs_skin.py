"""GD11 pass S: lived-in skin variants from k10 (k10 untouched): k11 = stronger baked normal / micro pores / cavity / regional micro detail;
k12 = k11 + small static wrinkle-map weights (forehead lines, crow's feet, under-eye) - test whether the face ABP overrides them at runtime."""
import unreal as u, json
SRC = '/Game/Sphirus/CharacterLab/GD11_HeadRefinementC_20261004/Skin'; DST = '/Game/Sphirus/CharacterLab/GD11_FaceR_20261006/Skin'; EAL = u.EditorAssetLibrary; MEL = u.MaterialEditingLibrary; out = {}
K11 = {'Micro Skin Normal Strength': 1.55, 'Normal Global Strength Post-Bake': 1.35, 'Normal Flatten': 0.18, 'Intensity Forehead': 0.55, 'Intensity Glabellar': 0.55, 'Intensity Eyelids': 0.55,
       'Intensity Maxilla': 0.55, 'Intensity Chin': 0.5, 'Intensity Neutral': 0.45, 'Intensity Nose': 0.5, 'Specular Concavity Multiply': 0.45, 'Roughness Concavity Multiply': 1.6, 'Fake AO Strength': 1.25}
WR = {'head_wm1_normal_head_wm1_browsRaiseInner_L': 0.3, 'head_wm1_normal_head_wm1_browsRaiseInner_R': 0.3, 'head_wm1_normal_head_wm1_browsRaiseOuter_L': 0.25, 'head_wm1_normal_head_wm1_browsRaiseOuter_R': 0.25,
      'head_wm1_normal_head_wm1_squintInner_L': 0.25, 'head_wm1_normal_head_wm1_squintInner_R': 0.25, 'head_wm3_normal_head_wm3_cheekRaiseInner_L': 0.15, 'head_wm3_normal_head_wm3_cheekRaiseInner_R': 0.15,
      'head_wm3_normal_head_wm3_smile_L': 0.12, 'head_wm3_normal_head_wm3_smile_R': 0.12}
for tag, extra in (('gqk11', {}), ('gqk12', WR)):
    for n in ('LOD0', 'LOD1', 'LOD2', 'LOD3', 'LOD4', 'LOD5to7'):
        s, d = f'{SRC}/MI_LK_Face_{n}_VT_gck10', f'{DST}/MI_LK_Face_{n}_VT_{tag}'
        m = EAL.load_asset(d) if EAL.does_asset_exist(d) else EAL.duplicate_asset(s, d); names = [str(x) for x in MEL.get_scalar_parameter_names(m)]
        for k, v in list(K11.items())+list(extra.items()):
            assert k in names, k; MEL.set_material_instance_scalar_parameter_value(m, k, v)
        out[d] = EAL.save_loaded_asset(m, False)
out['dirty'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]; print('SKIN_K11', json.dumps(out))
