"""GD33 probe (read-only): brow MI parameters of MI_GD15_BrowS_auburnDark and the RigLogic control curves on the G31 face skeleton that
touch eyes / lids / brows. Writes data/probe.json."""
import unreal as u, json, pathlib
R = pathlib.Path(u.Paths.project_dir()).resolve(); O = R/'Saved/Codex/GD33_Identity_20261011/data'; out = {}
mi = u.load_asset('/Game/Sphirus/CharacterLab/GD15_IdentityMaster_20261009/Looks/MI_GD15_BrowS_auburnDark'); MEL = u.MaterialEditingLibrary
out['mi_parent'] = mi.get_editor_property('parent').get_path_name()
out['mi_scalar'] = {str(n): MEL.get_material_instance_scalar_parameter_value(mi, n) for n in MEL.get_scalar_parameter_names(mi)}
out['mi_vector'] = {str(n): str(MEL.get_material_instance_vector_parameter_value(mi, n)) for n in MEL.get_vector_parameter_names(mi)}
sk = u.load_asset('/Game/Sphirus/CharacterLab/GD31_IdentityMaster_20261011/Face/SKM_GD31_Face_g31').skeleton; out['skeleton'] = sk.get_path_name()
names = [str(n) for n in sk.get_curve_meta_data_names()]
out['ctrl_eye_brow'] = sorted(n for n in names if n.lower().startswith('ctrl_expressions_') and any(k in n.lower() for k in ('eye', 'brow', 'lid')))
(O/'probe.json').write_text(json.dumps(out, indent=1)); print('GD33_PROBE', len(out['mi_scalar']), len(out['ctrl_eye_brow']))
