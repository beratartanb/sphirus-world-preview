import unreal as u
land = next(a for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors() if isinstance(a, u.Landscape))
for n in ('render_weightmap', 'render_weightmaps', 'landscape_import_weightmap_from_render_target', 'get_target_layer_names', 'landscape_export_heightmap_to_render_target'):
    print('DOC', n, '::', (getattr(land, n).__doc__ or '')[:700].replace('\n', ' | '))
print('LAYERS', land.get_target_layer_names(False) if True else '')
