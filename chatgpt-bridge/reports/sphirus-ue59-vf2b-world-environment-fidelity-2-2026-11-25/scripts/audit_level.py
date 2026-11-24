# VF2B read-only level audit: sublevels, actor folders, wall/fireplace/workshop meshes + materials, lights, post, sky, water, foliage counts.
import unreal as u, collections, json
W = u.EditorLevelLibrary.get_editor_world()
print('AL world', W.get_path_name())
for sl in u.EditorLevelUtils.get_levels(W): print('AL level', sl.get_outer().get_path_name(), len(u.EditorLevelUtils.get_levels(W)))
acts = u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors()
print('AL actors', len(acts))
byf = collections.Counter(); bycls = collections.Counter(); bylvl = collections.Counter()
rows = []
for a in acts:
    f = str(a.get_folder_path()); byf[f] += 1; bycls[a.get_class().get_name()] += 1; lv = a.get_outer().get_outer().get_name(); bylvl[lv] += 1
    l = a.get_actor_location(); e = a.get_actor_bounds(False)[1]
    row = {'n': a.get_actor_label(), 'c': a.get_class().get_name(), 'f': f, 'lv': lv, 'p': [round(l.x), round(l.y), round(l.z)], 'e': [round(e.x), round(e.y), round(e.z)]}
    sm = a.get_component_by_class(u.StaticMeshComponent)
    if sm and sm.get_editor_property('static_mesh'):
        row['m'] = sm.get_editor_property('static_mesh').get_path_name().split('.')[0]; row['mat'] = [m.get_path_name().split('.')[0] if m else None for m in sm.get_materials()][:4]
    rows.append(row)
json.dump(rows, open(u.Paths.project_dir() + 'Saved/UE59Work/vf2b/level_actors.json', 'w'))
print('AL levels', dict(bylvl))
print('AL classes', bycls.most_common(40))
print('AL folders', sorted(byf.items(), key=lambda x: -x[1])[:90])
for a in acts:
    cn = a.get_class().get_name()
    if cn in ('PostProcessVolume', 'ExponentialHeightFog', 'SkyLight', 'DirectionalLight', 'SkyAtmosphere', 'VolumetricCloud') or 'Water' in cn or 'Sky' in cn or 'Weather' in cn or 'DayBoot' in cn or 'TimeOfDay' in cn:
        print('AL env', cn, a.get_actor_label(), str(a.get_folder_path()), a.get_outer().get_outer().get_name())
n = 0
for a in acts:
    if isinstance(a, u.InstancedFoliageActor):
        for c in a.get_components_by_class(u.InstancedStaticMeshComponent):
            m = c.get_editor_property('static_mesh'); k = c.get_instance_count(); n += k
            if k: print('AL foliage', m.get_name() if m else None, k, 'cull', c.get_editor_property('instance_end_cull_distance'), 'shadow', c.get_editor_property('cast_shadow'))
print('AL foliage total', n)
lights = [a for a in acts if isinstance(a, u.Light)]
print('AL lights', len(lights), collections.Counter((a.get_class().get_name(), bool(a.light_component.get_editor_property('cast_shadows'))) for a in lights))
print('AL dirty', [p.get_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()], [p.get_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_map_packages()])
