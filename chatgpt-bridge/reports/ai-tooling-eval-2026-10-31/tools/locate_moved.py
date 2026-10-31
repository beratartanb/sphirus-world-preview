"""locate_moved.py (measure, read-only): where are the P1 instances now? For every G1-G3 move, search ALL foliage components with the same
mesh for instances within 30 cm (xy) of the target and of the original; print component path, index, exact location and z delta."""
import unreal as u, json, os, math

PILOT = r'C:\Users\berat\AppData\Local\Temp\claude\C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS\5f49a232-b001-47ad-8881-1eb04d9cb1c5\scratchpad\pilot'
plan = json.load(open(os.path.join(PILOT, 'plan_p1_resolved.json')))
comps = [c for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors() if a.get_class().get_name() == 'InstancedFoliageActor'
         for c in a.get_components_by_class(u.InstancedStaticMeshComponent)]
out = []
for m in plan['moves']:
    if m['group'] == 'G4_lookback_window':
        continue
    row = {'group': m['group'], 'mesh': m['mesh'], 'plan_comp': m['comp'].rsplit('.', 1)[-1], 'near_target': [], 'near_original': []}
    for c in comps:
        if not c.static_mesh or c.static_mesh.get_name() != m['mesh']:
            continue
        for i in range(c.get_instance_count()):
            L = c.get_instance_transform(i, True).translation
            for k, d in (('near_target', m['target']), ('near_original', m['original'])):
                if math.hypot(L.x - d['loc'][0], L.y - d['loc'][1]) < 30:
                    row[k].append({'comp': c.get_name(), 'idx': i, 'loc': [round(L.x, 2), round(L.y, 2), round(L.z, 2)], 'dz': round(L.z - d['loc'][2], 2)})
    out.append(row)
json.dump(out, open(os.path.join(PILOT, 'locate_moved.json'), 'w'), indent=1)
for r in out:
    print(r['group'][:3], r['mesh'][:24], 'plan', r['plan_comp'], 'T', [(x['comp'][-6:], x['idx'], x['dz']) for x in r['near_target']], 'O', [(x['comp'][-6:], x['idx'], x['dz']) for x in r['near_original']])
