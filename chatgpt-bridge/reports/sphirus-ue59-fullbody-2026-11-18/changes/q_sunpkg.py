import unreal as u
W = u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
for a in u.GameplayStatics.get_all_actors_of_class(W, u.DirectionalLight):
    c = a.get_components_by_class(u.DirectionalLightComponent)[0]
    print('SUNPKG', a.get_name(), a.get_actor_label(), a.get_package().get_name() if hasattr(a, 'get_package') else '?', a.get_outer().get_name(), W.get_path_name(), 'lf', c.get_editor_property('light_function_material'), 'int', c.get_editor_property('intensity'))
