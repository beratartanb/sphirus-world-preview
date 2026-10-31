"""probe_landscape.py (measure job, read-only): landscape paint layers + weightmap-related Python API on this build."""
import unreal as u, json, pathlib
P = pathlib.Path(u.Paths.project_dir()) / 'Saved/Codex/ExteriorWorld_XR2_20261031/recon'
land = next(a for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors() if isinstance(a, u.Landscape))
out = {'api': sorted([n for n in dir(land) if 'weight' in n.lower() or 'layer' in n.lower() or 'paint' in n.lower()])}
for k in ('editor_layer_settings', 'target_layers', 'landscape_material'):
    try:
        v = land.get_editor_property(k); out[k] = str(v)[:1500]
    except Exception as ex:
        out[k] = 'n/a ' + str(ex)[:120]
try:
    infos = []
    for s_ in land.get_editor_property('editor_layer_settings'):
        li = s_.get_editor_property('layer_info_obj'); infos.append(li.get_path_name() if li else None)
    out['layer_infos'] = infos
except Exception as ex:
    out['layer_infos'] = 'n/a ' + str(ex)[:200]
m = land.get_editor_property('landscape_material')
try:
    out['mat_parent'] = m.get_editor_property('parent').get_path_name()
    out['mat_scalars'] = [str(p.parameter_info.name) for p in m.get_editor_property('scalar_parameter_values')]
    out['mat_textures'] = [str(p.parameter_info.name) for p in m.get_editor_property('texture_parameter_values')]
except Exception as ex:
    out['mat'] = repr(ex)
out['lib'] = sorted([n for n in dir(u) if 'Landscape' in n])[:80]
(P / 'probe_landscape.json').write_text(json.dumps(out, indent=1))
print('LAND', json.dumps(out)[:2500])
