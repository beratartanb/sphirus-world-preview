import unreal as u
W = u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world(); o = []
for cv in ('r.MegaLights.Allow', 'r.MegaLights.EnableForProject', 'r.MegaLights.DirectionalLights', 'r.Shadow.Virtual.Enable', 'r.Shadow.Virtual.SMRT.RayCountDirectional', 'r.Lumen.DiffuseIndirect.Allow', 'r.Lumen.Reflections.Allow', 'r.ContactShadows', 'r.SubsurfaceScattering', 'r.SSS.Burley.Quality', 'r.Substrate', 'r.Lumen.ScreenProbeGather.ShortRangeAO', 'r.RayTracing.Shadows', 'r.HairStrands.Enable', 'r.TSR.ShadingRejection.Flickering', 'r.LocalExposure', 'r.Shadow.Virtual.SMRT.SamplesPerRayDirectional', 'r.Lumen.HardwareRayTracing', 'r.DistanceFieldShadowing', 'r.Shadow.Denoiser', 'r.MegaLights.Denoiser'):
    try: o.append('%s = %s' % (cv, u.SystemLibrary.get_console_variable_float_value(cv)))
    except Exception: o.append('%s ?' % cv)
sun = [a for a in u.GameplayStatics.get_all_actors_of_class(W, u.DirectionalLight)][0].get_components_by_class(u.DirectionalLightComponent)[0]
for n in ('light_source_angle', 'light_source_soft_angle', 'source_angle', 'contact_shadow_length', 'cast_shadows', 'cast_ray_traced_shadows', 'transmission', 'atmosphere_sun_light', 'specular_scale', 'diffuse_scale', 'shadow_source_angle_factor', 'use_inset_shadows_for_movable_objects', 'cast_translucent_shadows', 'mega_lights_shadow_method', 'allow_mega_lights', 'light_function_material', 'cast_cloud_shadows', 'intensity_units'):
    try: o.append('sun.%s = %s' % (n, sun.get_editor_property(n)))
    except Exception: pass
open(u.Paths.project_dir() + 'Saved/UE59Work/probe/cv_dump.txt', 'w').write('\n'.join(o)); print('CVDUMP', len(o))
