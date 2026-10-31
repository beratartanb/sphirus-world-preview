"""pilot_scope_probe.py (measure, read-only): packages a rear-trail pilot would touch.
Which level package owns the InstancedFoliageActor(s) and the landscape near the pilot segment, the landscape paint layers available
there, and the existing large structural meshes (logs, roots, rocks) already placed within 25 m (candidates to REUSE by moving).
Output: <OUT>/pilot_scope.json
"""
import unreal as u, json, os, math

W2 = r'C:\Users\berat\AppData\Local\Temp\claude\C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS\5f49a232-b001-47ad-8881-1eb04d9cb1c5\scratchpad\walk2'
C = (2930.0, -2560.0)   # middle of the 16 m pilot segment (walk2 track)
A = u.get_editor_subsystem(u.EditorActorSubsystem)
res = {'centre': C, 'foliage_actors': [], 'landscapes': [], 'structural_instances_25m': {}, 'structural_actors_25m': []}
KEYS = ('log', 'trunk', 'root', 'rock', 'stump', 'branch', 'boulder', 'cliff')
for a in A.get_all_level_actors():
    cls = a.get_class().get_name()
    lvl = a.get_level().get_outer().get_path_name() if a.get_level() else None
    if cls == 'InstancedFoliageActor':
        n = sum(c.get_instance_count() for c in a.get_components_by_class(u.InstancedStaticMeshComponent))
        res['foliage_actors'].append({'label': a.get_actor_label(), 'level': lvl, 'instances': n})
        for c in a.get_components_by_class(u.InstancedStaticMeshComponent):
            m = c.get_editor_property('static_mesh'); mn = m.get_name() if m else ''
            if not any(k in mn.lower() for k in KEYS):
                continue
            cnt = 0
            for i in range(c.get_instance_count()):
                t = c.get_instance_transform(i, True).translation
                if math.hypot(t.x - C[0], t.y - C[1]) <= 2500:
                    cnt += 1
            if cnt:
                res['structural_instances_25m'][mn] = cnt
    elif cls.startswith('Landscape'):
        row = {'label': a.get_actor_label(), 'class': cls, 'level': lvl}
        try:
            mats = a.get_editor_property('landscape_material')
            row['material'] = mats.get_path_name() if mats else None
        except Exception as ex:
            row['material'] = 'n/a'
        try:
            row['layers'] = [str(l.get_editor_property('layer_name')) for l in a.get_editor_property('editor_layer_settings')]
        except Exception as ex:
            row['layers'] = 'n/a %s' % ex
        res['landscapes'].append(row)
    else:
        if a.get_components_by_class(u.StaticMeshComponent) and not a.get_components_by_class(u.InstancedStaticMeshComponent):
            smc = a.get_components_by_class(u.StaticMeshComponent)[0]; m = smc.get_editor_property('static_mesh'); mn = m.get_name() if m else ''
            o = a.get_actor_location()
            if any(k in mn.lower() for k in KEYS) and math.hypot(o.x - C[0], o.y - C[1]) <= 2500:
                res['structural_actors_25m'].append({'label': a.get_actor_label(), 'mesh': mn, 'level': lvl})
json.dump(res, open(os.path.join(W2, 'pilot_scope.json'), 'w'), indent=1)
print('PILOT_SCOPE', json.dumps({'foliage': res['foliage_actors'], 'landscapes': [{k: v for k, v in l.items()} for l in res['landscapes']][:4],
                                 'structural_instances': res['structural_instances_25m'], 'structural_actors': len(res['structural_actors_25m'])})[:3000])
