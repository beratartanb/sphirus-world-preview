"""GD33 lookdev assets (GD33 folder only, refuses to overwrite):
 Looks/MI_GD33_BrowS_l1, _l2 = duplicates of the read-only MI_GD15_BrowS_auburnDark (the c4 brow colour) with hairMelanin 0.72 -> 0.65 / 0.60
   (one / two shade steps lighter; redness and everything else unchanged)
 Face/AS_GD33_RestCalm = RigLogic control-curve sequence on the G31 face skeleton, one case per second (sample at i+0.5 s): neutral and calm
   rest-expression candidates (upper lid raise / widen / inner-brow raise at low weights). Writes data/rest_cases.json."""
import unreal as u, json, pathlib
R = pathlib.Path(u.Paths.project_dir()).resolve(); O = R/'Saved/Codex/GD33_Identity_20261011/data'; G = '/Game/Sphirus/CharacterLab/GD33_IdentityMaster_20261011'
EAL = u.EditorAssetLibrary; MEL = u.MaterialEditingLibrary; out = {}
SRC = '/Game/Sphirus/CharacterLab/GD15_IdentityMaster_20261009/Looks/MI_GD15_BrowS_auburnDark'
for tag, mel in (('l1', 0.65), ('l2', 0.60)):
    dst = f'{G}/Looks/MI_GD33_BrowS_{tag}'; assert not EAL.does_asset_exist(dst), dst
    m = EAL.duplicate_asset(SRC, dst); MEL.set_material_instance_scalar_parameter_value(m, 'hairMelanin', mel); EAL.save_loaded_asset(m, False)
    out[tag] = [dst, round(MEL.get_material_instance_scalar_parameter_value(m, 'hairMelanin'), 3), round(MEL.get_material_instance_scalar_parameter_value(m, 'hairRedness'), 3)]
mesh = u.load_asset('/Game/Sphirus/CharacterLab/GD31_IdentityMaster_20261011/Face/SKM_GD31_Face_g31'); sk = mesh.skeleton
names = {str(n).lower(): str(n) for n in sk.get_curve_meta_data_names()}
LR = lambda k, v: {k+'L': v, k+'R': v}
cases = [('neutral', {}), ('lid15', LR('eyeUpperLidUp', 0.15)), ('lid30', LR('eyeUpperLidUp', 0.30)), ('widen15', LR('eyeWiden', 0.15)),
         ('relax30', LR('eyeRelax', 0.30)), ('brin12', LR('browRaiseIn', 0.12)), ('calm1', {**LR('eyeUpperLidUp', 0.20), **LR('browRaiseIn', 0.10)}),
         ('calm2', {**LR('eyeUpperLidUp', 0.30), **LR('browRaiseIn', 0.15), **LR('browRaiseOuter', 0.05)})]
resolved = []; missing = []
for n, vs in cases:
    r = {}
    for k, v in vs.items():
        full = names.get(('ctrl_expressions_'+k).lower())
        if full is None: missing.append(k)
        else: r[full] = v
    resolved.append((n, r))
assert not missing, missing
path = G+'/Face/AS_GD33_RestCalm'; assert not EAL.does_asset_exist(path)
fac = u.AnimSequenceFactory(); fac.target_skeleton = sk; fac.preview_skeletal_mesh = mesh
seq = u.AssetToolsHelpers.get_asset_tools().create_asset('AS_GD33_RestCalm', G+'/Face', u.AnimSequence, fac)
ctrl = seq.get_editor_property('controller'); ctrl.set_frame_rate(u.FrameRate(30, 1)); ctrl.set_number_of_frames(u.FrameNumber(len(resolved)*30))
for key in sorted({k for _, vs in resolved for k in vs}):
    u.AnimationLibrary.add_curve(seq, key); times, vals = [], []
    for i, (_, vs) in enumerate(resolved): times += [i+0.05, i+0.95]; vals += [vs.get(key, 0.0), vs.get(key, 0.0)]
    u.AnimationLibrary.add_float_curve_keys(seq, key, times, vals)
out['seq_saved'] = EAL.save_loaded_asset(seq, False)
(O/'rest_cases.json').write_text(json.dumps({'animation': seq.get_path_name().split('.')[0], 'cases': [{'name': n, 'time': i+0.5, 'controls': vs} for i, (n, vs) in enumerate(resolved)]}, indent=1))
print('GD33_ASSETS', json.dumps(out))
