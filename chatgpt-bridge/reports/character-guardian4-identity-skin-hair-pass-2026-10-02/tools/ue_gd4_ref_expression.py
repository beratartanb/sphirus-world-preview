"""GUARDIAN-4 pass: REFERENCE_EXPRESSION (calm-serious-alert, NOT sad) QA pose, kept SEPARATE from the identity neutral (nothing baked into the sculpt).
AnimSequence of RigLogic control curves (ctrl_expressions_*) on the shared face archetype skeleton, one case per second (sample at i+0.5 s):
neutral / ref_expr_soft / ref_expr / ref_expr_firm - calm, serious, controlled, alert: mouth corners very slightly down, light lip press,
light inner squint (attentive), slightly heavy lids, faint brow down. Created in <Guardian2>/Face/Diagnostics. Writes gd4_expr_cases.json."""
import unreal as u, json, pathlib
P = pathlib.Path(u.Paths.project_dir()).resolve(); O = P/'Saved/Codex/CharacterGuardian4_20261002'; dest = '/Game/Sphirus/CharacterLab/CharacterGuardian4_20261002/Face/Diagnostics'
import builtins; mesh = u.load_asset(getattr(builtins, 'GD3_SEQ_MESH', '/Game/Sphirus/CharacterLab/CharacterGuardian4_20261002/Face/SKM_GD4_Face_e1')); sk = mesh.skeleton
names = {str(n).lower(): str(n) for n in sk.get_curve_meta_data_names()}
LR = lambda k, v: {k+'L': v, k+'R': v}
def expr(s): return {**LR('mouthCornerDepress', 0.12*s), **LR('mouthLipsPress', 0.10*s), **LR('eyeSquintInner', 0.14*s), **LR('eyeBlink', 0.06*s), **LR('browDown', 0.06*s), **LR('eyeCheekRaise', 0.04*s)}
cases = [('neutral', {}), ('ref_expr_soft', expr(0.6)), ('ref_expr', expr(1.0)), ('ref_expr_firm', expr(1.5))]
missing = []; resolved = []
for n, vs in cases:
    r = {}
    for k, v in vs.items():
        full = names.get(('ctrl_expressions_'+k).lower())
        if full is None: missing.append(k)
        else: r[full] = v
    resolved.append((n, r))
assert not missing, missing
path = dest+'/AS_GD4_RefExpression'
if u.EditorAssetLibrary.does_asset_exist(path): seq = u.load_asset(path)
else:
    fac = u.AnimSequenceFactory(); fac.target_skeleton = sk; fac.preview_skeletal_mesh = mesh
    seq = u.AssetToolsHelpers.get_asset_tools().create_asset('AS_GD4_RefExpression', dest, u.AnimSequence, fac)
ctrl = seq.get_editor_property('controller'); ctrl.set_frame_rate(u.FrameRate(30, 1)); ctrl.set_number_of_frames(u.FrameNumber(len(resolved)*30))
for key in sorted({k for _, vs in resolved for k in vs}):
    u.AnimationLibrary.add_curve(seq, key); times, vals = [], []
    for i, (_, vs) in enumerate(resolved): times += [i+0.05, i+0.95]; vals += [vs.get(key, 0.0), vs.get(key, 0.0)]
    u.AnimationLibrary.add_float_curve_keys(seq, key, times, vals)
saved = u.EditorAssetLibrary.save_loaded_asset(seq, False)
(O/'gd4_expr_cases.json').write_text(json.dumps({'animation': seq.get_path_name().split('.')[0], 'cases': [{'name': n, 'time': i+0.5, 'controls': vs} for i, (n, vs) in enumerate(resolved)]}, indent=1))
print('GD4_EXPR', saved, len(resolved), seq.get_path_name(), json.dumps([p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]))
