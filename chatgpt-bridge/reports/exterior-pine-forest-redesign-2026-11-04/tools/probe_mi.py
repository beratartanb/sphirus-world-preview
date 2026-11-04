"""probe_mi.py (control job, read-only): dump the scalar / vector / texture parameter names and values of a few vendor material
instances (for owned-copy tuning). Output: Saved/Codex/PineForestRedesign_20261104/recon/probe_mi.json"""
import unreal as u, json, pathlib
PJ = pathlib.Path(u.Paths.project_dir()); OUT = PJ / 'Saved/Codex/PineForestRedesign_20261104/recon/probe_mi.json'
MIS = ['/Game/PineForestPack/Materials/MaterialInstances/Foliage/MI_DeadLeaves01', '/Game/PineForestPack/Materials/MaterialInstances/Foliage/MI_DeadLeaves02',
       '/Game/PineForestPack/Materials/MaterialInstances/Foliage/MI_FallenNeedle', '/Game/PineForestPack/Materials/MaterialInstances/Foliage/MI_MossLeaf01',
       '/Game/PineForestPack/Materials/MaterialInstances/Rocks/MI_CliffRock01']
res = {}
for p in MIS:
    mi = u.load_asset(p)
    if not mi: res[p] = 'missing'; continue
    row = {'parent': str(mi.get_editor_property('parent').get_path_name()) if mi.get_editor_property('parent') else None, 'scalar': {}, 'vector': {}, 'texture': {}, 'static_switch': {}}
    for n in u.MaterialEditingLibrary.get_scalar_parameter_names(mi): row['scalar'][str(n)] = round(u.MaterialEditingLibrary.get_material_instance_scalar_parameter_value(mi, n), 4)
    for n in u.MaterialEditingLibrary.get_vector_parameter_names(mi): c = u.MaterialEditingLibrary.get_material_instance_vector_parameter_value(mi, n); row['vector'][str(n)] = [round(c.r, 3), round(c.g, 3), round(c.b, 3), round(c.a, 3)]
    for n in u.MaterialEditingLibrary.get_texture_parameter_names(mi): t = u.MaterialEditingLibrary.get_material_instance_texture_parameter_value(mi, n); row['texture'][str(n)] = t.get_path_name() if t else None
    try:
        for n in u.MaterialEditingLibrary.get_static_switch_parameter_names(mi): row['static_switch'][str(n)] = bool(u.MaterialEditingLibrary.get_material_instance_static_switch_parameter_value(mi, n))
    except Exception as ex: row['static_switch'] = repr(ex)[:80]
    res[p] = row
OUT.write_text(json.dumps(res, indent=1)); print('PROBE_MI', len(res))
