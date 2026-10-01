"""FACE-MATCH pass: facial-rig validation sequence (RigLogic control curves ctrl_expressions_*) on the shared face archetype
skeleton, one case per second (sample at i+0.5 s). Created once in <lookdev>/Face/Diagnostics. Writes gd3_face_cases.json."""
import unreal as u, json, pathlib
P = pathlib.Path(u.Paths.project_dir()).resolve(); O = P/'Saved/Codex/CharacterGuardian3_20261001'; dest = '/Game/Sphirus/CharacterLab/CharacterGuardian3_20261001/Face/Diagnostics'
import builtins; mesh = u.load_asset(getattr(builtins, 'GD3_SEQ_MESH', '/Game/Sphirus/CharacterLab/CharacterGuardian3_20261001/Face/SKM_GD3_Face_n2')); sk = mesh.skeleton
names = {str(n).lower(): str(n) for n in sk.get_curve_meta_data_names()}
L4 = lambda k: {k+s: 1.0 for s in ('UL', 'UR', 'DL', 'DR')}
LR = lambda k, v=1.0: {k+'L': v, k+'R': v}
cases = [('neutral', {}), ('blink', LR('eyeBlink')), ('blink_left', {'eyeBlinkL': 1}), ('blink_right', {'eyeBlinkR': 1}), ('look_up', LR('eyeLookUp')), ('look_down', LR('eyeLookDown')),
         ('look_left', LR('eyeLookLeft')), ('look_right', LR('eyeLookRight')), ('brows_up', {**LR('browRaiseIn'), **LR('browRaiseOuter')}), ('brows_down', LR('browDown')),
         ('smile', {**LR('mouthCornerPull'), **LR('eyeCheekRaise', 0.5)}), ('frown', LR('mouthCornerDepress')), ('lips_closed', {**LR('mouthLipsPress', 0.6), **L4('mouthLipsTogether')}),
         ('mouth_open', {'jawOpen': 0.45, **LR('mouthUpperLipRaise', 0.5), **LR('mouthLowerLipDepress', 0.5)}), ('jaw_open', {'jawOpen': 1.0}), ('jaw_left', {'jawLeft': 1.0}), ('jaw_right', {'jawRight': 1.0}),
         ('ph_oo', {**L4('mouthFunnel'), 'jawOpen': 0.15}), ('ph_ee', {**LR('mouthStretch', 0.8), **LR('mouthCornerPull', 0.3), 'jawOpen': 0.1}), ('ph_mbp', {**LR('mouthLipsPress'), **L4('mouthLipsTogether')}),
         ('ph_w', {**L4('mouthLipsPurse')}), ('cheek_compress', {**LR('eyeCheekRaise'), **LR('mouthCornerPull', 0.6), **LR('eyeSquintInner', 0.6)}),
         ('extreme', {'jawOpenExtreme': 1.0, **LR('browRaiseIn'), **LR('browRaiseOuter'), **LR('mouthStretch', 0.6)})]
missing = []; resolved = []
for n, vs in cases:
    r = {}
    for k, v in vs.items():
        full = names.get(('ctrl_expressions_'+k).lower())
        if full is None: missing.append(k)
        else: r[full] = v
    resolved.append((n, r))
assert not missing, missing
path = dest+'/AS_GD3_FacialRig'
if u.EditorAssetLibrary.does_asset_exist(path): seq = u.load_asset(path)
else:
    fac = u.AnimSequenceFactory(); fac.target_skeleton = sk; fac.preview_skeletal_mesh = mesh
    seq = u.AssetToolsHelpers.get_asset_tools().create_asset('AS_GD3_FacialRig', dest, u.AnimSequence, fac)
ctrl = seq.get_editor_property('controller'); ctrl.set_frame_rate(u.FrameRate(30, 1)); ctrl.set_number_of_frames(u.FrameNumber(len(resolved)*30))
for key in sorted({k for _, vs in resolved for k in vs}):
    u.AnimationLibrary.add_curve(seq, key); times, vals = [], []
    for i, (_, vs) in enumerate(resolved): times += [i+0.05, i+0.95]; vals += [vs.get(key, 0.0), vs.get(key, 0.0)]
    u.AnimationLibrary.add_float_curve_keys(seq, key, times, vals)
saved = u.EditorAssetLibrary.save_loaded_asset(seq, False)
(O/'gd3_face_cases.json').write_text(json.dumps({'animation': seq.get_path_name().split('.')[0], 'cases': [{'name': n, 'time': i+0.5, 'controls': vs} for i, (n, vs) in enumerate(resolved)]}, indent=1))
print('FM_FACE_SEQ', saved, len(resolved), seq.get_path_name())
