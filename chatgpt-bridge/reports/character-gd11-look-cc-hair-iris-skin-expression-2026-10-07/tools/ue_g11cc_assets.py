"""pass CC (overall look): (1) resting-expression face sequence (RigLogic control curves, one case per second) for captures,
(2) dark-brown iris e3k (copy of e3g; lower value, brown multiply), (3) matte skin k17 (copy of k16; specular down, roughness up, tone unchanged).
Only new assets; nothing existing is modified."""
import unreal as u, json
EAL = u.EditorAssetLibrary; MEL = u.MaterialEditingLibrary; out = {}; D = '/Game/Sphirus/CharacterLab/GD11_FaceR_20261006'
mesh = u.load_asset(D+'/Face/SKM_G11RR_Face_ss4'); sk = mesh.skeleton; names = {str(n).lower(): str(n) for n in sk.get_curve_meta_data_names()}
LR = lambda k, v: {k+'L': v, k+'R': v}
cases = [('neutral', {}),
         ('rest_a', {**LR('eyeBlink', 0.12), **LR('browDown', 0.10), **LR('browLateral', 0.10), **LR('mouthCornerDepress', 0.18), **LR('mouthLipsPress', 0.12)}),
         ('rest_b', {**LR('eyeBlink', 0.2), **LR('eyeSquintInner', 0.08), **LR('browDown', 0.15), **LR('browLateral', 0.18), **LR('mouthCornerDepress', 0.28), **LR('mouthLipsPress', 0.2)}),
         ('lids_only', LR('eyeBlink', 0.15))]
missing = []; resolved = []
for n, vs in cases:
    r = {}
    for k, v in vs.items():
        full = names.get(('ctrl_expressions_'+k).lower())
        if full is None: missing.append(k)
        else: r[full] = v
    resolved.append((n, r))
out['missing'] = sorted(set(missing))
path = D+'/Face/Diagnostics/AS_G11CC_RestFace'; assert not EAL.does_asset_exist(path)
fac = u.AnimSequenceFactory(); fac.target_skeleton = sk; fac.preview_skeletal_mesh = mesh
seq = u.AssetToolsHelpers.get_asset_tools().create_asset('AS_G11CC_RestFace', D+'/Face/Diagnostics', u.AnimSequence, fac)
ctrl = seq.get_editor_property('controller'); ctrl.set_frame_rate(u.FrameRate(30, 1)); ctrl.set_number_of_frames(u.FrameNumber(len(resolved)*30))
for key in sorted({k for _, vs in resolved for k in vs}):
    u.AnimationLibrary.add_curve(seq, key); times, vals = [], []
    for i, (_, vs) in enumerate(resolved): times += [i+0.05, i+0.95]; vals += [vs.get(key, 0.0), vs.get(key, 0.0)]
    u.AnimationLibrary.add_float_curve_keys(seq, key, times, vals)
out['seq'] = [seq.get_path_name(), EAL.save_loaded_asset(seq, False), {n: i+0.5 for i, (n, _) in enumerate(resolved)}]
EYE = {'Iris Primary Color Value': 0.62, 'Iris Secondary Color Value': 0.22, 'Iris Global Saturation': 0.8, 'Iris Shadow Details Amount': 0.7}
for s in ('L', 'R'):
    src, dst = f'{D}/Skin/MI_G11RV_Eye{s}_e3g', f'{D}/Skin/MI_G11CC_Eye{s}_e3k'; assert not EAL.does_asset_exist(dst); m = EAL.duplicate_asset(src, dst)
    for k, v in EYE.items(): MEL.set_material_instance_scalar_parameter_value(m, k, v)
    MEL.set_material_instance_vector_parameter_value(m, 'Iris Color Multiply', u.LinearColor(0.78, 0.56, 0.38, 1.0)); out[dst] = EAL.save_loaded_asset(m, False)
SKN = {'Specular Global Multiply Post-Bake': 0.7, 'Roughness Global Multiply Post-Bake': 1.12}
for n in ('LOD0', 'LOD1', 'LOD2', 'LOD3', 'LOD4', 'LOD5to7'):
    src, dst = f'{D}/Skin/MI_LK_Face_{n}_VT_gqk16', f'{D}/Skin/MI_LK_Face_{n}_VT_gqk17'; assert not EAL.does_asset_exist(dst); m = EAL.duplicate_asset(src, dst)
    for k, v in SKN.items(): MEL.set_material_instance_scalar_parameter_value(m, k, v)
    out[dst] = EAL.save_loaded_asset(m, False)
out['dirty'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]; print('G11CC', json.dumps(out))
