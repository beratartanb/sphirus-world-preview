"""probe_foliage_mats.py (measure, read-only): materials of the tall soft foliage near the trail and whether they already expose a
camera-distance fade / dither / opacity-mask control (parameter names), plus blend mode. Nothing is edited."""
import unreal as u, json, os

MESHES = {'SM_Pine_Juvenile_01', 'SM_Young_Black_Spruce_01', 'SM_Young_Black_Spruce_02', 'SM_Bush_02', 'SM_Bush_06', 'Pine_08', 'SM_FernWild01'}
OUT = r'C:\Users\berat\AppData\Local\Temp\claude\C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS\5f49a232-b001-47ad-8881-1eb04d9cb1c5\scratchpad\pilot\foliage_materials.json'
MEL = u.MaterialEditingLibrary
seen, res = set(), {}
for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors():
    if a.get_class().get_name() != 'InstancedFoliageActor':
        continue
    for c in a.get_components_by_class(u.InstancedStaticMeshComponent):
        m = c.get_editor_property('static_mesh')
        if not m or m.get_name() not in MESHES or m.get_name() in seen:
            continue
        seen.add(m.get_name()); rows = []
        for k in range(c.get_num_materials()):
            mi = c.get_material(k)
            if not mi:
                continue
            base = mi.get_base_material() if hasattr(mi, 'get_base_material') else mi
            row = {'slot': k, 'material': mi.get_path_name(), 'base': base.get_path_name() if base else None}
            try:
                row['blend_mode'] = str(base.get_editor_property('blend_mode')).split('.')[-1]
                row['dithered_lod_transition'] = base.get_editor_property('dithered_lod_transition')
            except Exception as ex:
                row['blend_mode'] = 'n/a'
            names = []
            for fn in ('get_scalar_parameter_names', 'get_static_switch_parameter_names', 'get_vector_parameter_names'):
                try:
                    names += [str(n) for n in getattr(MEL, fn)(mi)]
                except Exception:
                    pass
            row['n_params'] = len(names)
            row['fade_like_params'] = [n for n in names if any(t in n.lower() for t in ('fade', 'dither', 'camera', 'distance', 'opacity', 'near'))]
            rows.append(row)
        res[m.get_name()] = rows
json.dump(res, open(OUT, 'w'), indent=1)
print('FOLIAGE_MATS', json.dumps({k: [(r['base'].rsplit('/', 1)[-1] if r['base'] else None, r.get('blend_mode'), r['fade_like_params']) for r in v] for k, v in res.items()}))
