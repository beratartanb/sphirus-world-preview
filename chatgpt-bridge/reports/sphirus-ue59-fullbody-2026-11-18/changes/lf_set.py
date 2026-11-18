# lf_set.py (runtime, PIE, not saved): builtins.LF = None (remove) or dict(k=InsideK, soft=cm, ppv=dict for PostProcessVolume_15)
import unreal as u, builtins
W = u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world()
sun = [a for a in u.GameplayStatics.get_all_actors_of_class(W, u.DirectionalLight) if a.get_name() == 'DirectionalLight_0'][0].get_components_by_class(u.DirectionalLightComponent)[0]
L = getattr(builtins, 'LF', None)
if L is None: sun.set_light_function_material(None); print('LFSET none')
else:
    host = None
    for a in u.GameplayStatics.get_all_actors_of_class(W, u.StaticMeshActor):
        c = a.static_mesh_component
        if c and c.get_num_materials() > 0: host = c; break
    orig = host.get_material(0)
    mi = host.create_dynamic_material_instance(0, u.load_asset('/Game/Sphirus/Lighting/Day_20261118/M_Sph_SunInterior_LF'))
    host.set_material(0, orig); builtins.LF_KEEP = mi
    mi.set_scalar_parameter_value('InsideK', L.get('k', 0.2)); mi.set_scalar_parameter_value('Soft', L.get('soft', 15.0))
    sun.set_light_function_material(mi)
    r = []
    for n in ('light_function_fade_distance', 'disabled_brightness', 'light_function_scale'):
        try: r.append('%s=%s' % (n, sun.get_editor_property(n)))
        except Exception: pass
    print('LFSET k', L.get('k'), r)
