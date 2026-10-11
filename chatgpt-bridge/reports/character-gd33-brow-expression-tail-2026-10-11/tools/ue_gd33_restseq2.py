"""GD33: second rest-expression sequence AS_GD33_RestCalm2 (GD33 folder, refuses to overwrite) - eye-opening cases at higher weights (the
0.15-0.30 cases of AS_GD33_RestCalm moved the lids by only a few px). Same layout: one case per second, sample at i+0.5 s. Writes
data/rest_cases2.json."""
import unreal as u, json, pathlib
R = pathlib.Path(u.Paths.project_dir()).resolve(); O = R/'Saved/Codex/GD33_Identity_20261011/data'; G = '/Game/Sphirus/CharacterLab/GD33_IdentityMaster_20261011'; EAL = u.EditorAssetLibrary
mesh = u.load_asset('/Game/Sphirus/CharacterLab/GD31_IdentityMaster_20261011/Face/SKM_GD31_Face_g31'); sk = mesh.skeleton
names = {str(n).lower(): str(n) for n in sk.get_curve_meta_data_names()}
LR = lambda k, v: {k+'L': v, k+'R': v}
cases = [('neutral', {}), ('lid60', LR('eyeUpperLidUp', 0.6)), ('lid100', LR('eyeUpperLidUp', 1.0)), ('lid60ld30', {**LR('eyeUpperLidUp', 0.6), **LR('eyeLowerLidDown', 0.3)}),
         ('lid80ld30', {**LR('eyeUpperLidUp', 0.8), **LR('eyeLowerLidDown', 0.3)}), ('wid40', LR('eyeWiden', 0.4)), ('wid40ld30', {**LR('eyeWiden', 0.4), **LR('eyeLowerLidDown', 0.3)})]
resolved = []
for n, vs in cases: resolved.append((n, {names[('ctrl_expressions_'+k).lower()]: v for k, v in vs.items()}))
path = G+'/Face/AS_GD33_RestCalm2'; assert not EAL.does_asset_exist(path)
fac = u.AnimSequenceFactory(); fac.target_skeleton = sk; fac.preview_skeletal_mesh = mesh
seq = u.AssetToolsHelpers.get_asset_tools().create_asset('AS_GD33_RestCalm2', G+'/Face', u.AnimSequence, fac)
ctrl = seq.get_editor_property('controller'); ctrl.set_frame_rate(u.FrameRate(30, 1)); ctrl.set_number_of_frames(u.FrameNumber(len(resolved)*30))
for key in sorted({k for _, vs in resolved for k in vs}):
    u.AnimationLibrary.add_curve(seq, key); times, vals = [], []
    for i, (_, vs) in enumerate(resolved): times += [i+0.05, i+0.95]; vals += [vs.get(key, 0.0), vs.get(key, 0.0)]
    u.AnimationLibrary.add_float_curve_keys(seq, key, times, vals)
ok = EAL.save_loaded_asset(seq, False)
(O/'rest_cases2.json').write_text(json.dumps({'animation': seq.get_path_name().split('.')[0], 'cases': [{'name': n, 'time': i+0.5, 'controls': vs} for i, (n, vs) in enumerate(resolved)]}, indent=1))
print('GD33_RESTSEQ2', ok, len(resolved))
