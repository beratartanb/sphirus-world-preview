"""GD35 probe (read-only): face skin MI (GD31 n3 LOD0) and body MI parameters with their current values and the parent chain."""
import unreal as u, json, pathlib
O = pathlib.Path(u.Paths.project_dir()).resolve()/'Saved/Codex/GD35_Identity_20261011/data'; MEL = u.MaterialEditingLibrary; out = {}
for p in ('/Game/Sphirus/CharacterLab/GD31_IdentityMaster_20261011/Looks/MI_GD31_Face_LOD0_s1t6n_n3', '/Game/Sphirus/CharacterLab/GD15_IdentityMaster_20261009/Looks/MI_GD15_Body_s1'):
    m = u.load_asset(p); chain = []; x = m
    while isinstance(x, u.MaterialInstance): chain.append(x.get_path_name()); x = x.get_editor_property('parent')
    chain.append(x.get_path_name() if x else None)
    out[p] = {'chain': chain, 'scalar': {str(n): round(MEL.get_material_instance_scalar_parameter_value(m, n), 4) for n in MEL.get_scalar_parameter_names(m)},
              'vector': {str(n): [round(c, 4) for c in (lambda v: (v.r, v.g, v.b, v.a))(MEL.get_material_instance_vector_parameter_value(m, n))] for n in MEL.get_vector_parameter_names(m)}}
(O/'skin_probe.json').write_text(json.dumps(out, indent=1)); print('GD35_PROBE', {k: (len(v['scalar']), len(v['vector'])) for k, v in out.items()})
