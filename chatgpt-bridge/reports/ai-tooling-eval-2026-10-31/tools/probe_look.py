"""probe_look.py (measure, read-only): look-dev owners and reusable assets for the Environment Visual Master Pass.
1. Every light / sky / fog / post-process actor in the loaded world: class, label, level, and its key properties (component-level).
2. Reusable environment assets already in the project: decal materials (name contains Decal), static meshes used in the editor world
   that look structural (rock / stone / cliff / embank / root / log / trunk / stump / moss / litter / leaves / branch / debris), with usage counts.
Nothing is edited. Output: <PILOT>/look_probe.json"""
import unreal as u, json, os, collections

PILOT = r'C:\Users\berat\AppData\Local\Temp\claude\C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS\5f49a232-b001-47ad-8881-1eb04d9cb1c5\scratchpad\pilot'
A = u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors()


def P(o, k):
    try:
        v = o.get_editor_property(k)
    except Exception as ex:
        return 'n/a'
    if hasattr(v, 'get_path_name') and not isinstance(v, str):
        return v.get_path_name()
    if isinstance(v, float):
        return round(v, 4)
    if hasattr(v, 'r') and hasattr(v, 'g'):
        return [round(v.r, 3), round(v.g, 3), round(v.b, 3)]
    return v if isinstance(v, (int, bool, str)) else str(v)[:160]


LIGHT_KEYS = {
    'DirectionalLightComponent': ['intensity', 'light_color', 'temperature', 'use_temperature', 'light_source_angle', 'light_source_soft_angle', 'volumetric_scattering_intensity',
                                  'cast_shadows', 'atmosphere_sun_light', 'indirect_lighting_intensity', 'shadow_amount', 'cast_cloud_shadows', 'enable_light_shaft_bloom'],
    'SkyLightComponent': ['intensity', 'light_color', 'source_type', 'real_time_capture', 'lower_hemisphere_is_black', 'lower_hemisphere_color', 'volumetric_scattering_intensity',
                          'indirect_lighting_intensity', 'sky_distance_threshold', 'cubemap'],
    'ExponentialHeightFogComponent': ['fog_density', 'fog_height_falloff', 'fog_inscattering_luminance', 'directional_inscattering_luminance', 'directional_inscattering_exponent',
                                      'start_distance', 'fog_cutoff_distance', 'fog_max_opacity', 'volumetric_fog', 'volumetric_fog_scattering_distribution', 'volumetric_fog_albedo',
                                      'volumetric_fog_extinction_scale', 'volumetric_fog_distance', 'volumetric_fog_start_distance', 'second_fog_data'],
    'SkyAtmosphereComponent': ['rayleigh_scattering_scale', 'mie_scattering_scale', 'mie_anisotropy', 'multi_scattering_factor', 'sky_luminance_factor', 'aerial_pespective_view_distance_scale', 'height_fog_contribution'],
}
PP_KEYS = ['auto_exposure_method', 'auto_exposure_bias', 'auto_exposure_min_brightness', 'auto_exposure_max_brightness', 'auto_exposure_speed_up', 'auto_exposure_speed_down',
           'local_exposure_highlight_contrast_scale', 'local_exposure_shadow_contrast_scale', 'local_exposure_detail_strength', 'bloom_intensity', 'vignette_intensity',
           'color_saturation', 'color_contrast', 'color_gamma', 'color_gain', 'color_offset', 'color_saturation_shadows', 'color_saturation_highlights', 'white_temp', 'white_tint',
           'film_slope', 'film_toe', 'film_shoulder', 'ambient_occlusion_intensity', 'ambient_occlusion_radius', 'indirect_lighting_intensity', 'lumen_scene_lighting_quality',
           'lumen_final_gather_quality', 'lumen_scene_detail', 'lumen_reflection_quality', 'scene_fringe_intensity', 'sharpen', 'color_grading_lut', 'dynamic_global_illumination_method']
res = {'look_actors': [], 'decals': [], 'structural_meshes': {}}
for a in A:
    cls = a.get_class().get_name()
    if cls in ('DirectionalLight', 'SkyLight', 'ExponentialHeightFog', 'SkyAtmosphere', 'PostProcessVolume', 'VolumetricCloud', 'PointLight', 'SpotLight', 'RectLight'):
        row = {'class': cls, 'label': a.get_actor_label(), 'level': a.get_level().get_outer().get_name() if a.get_level() else None,
               'loc': [round(a.get_actor_location().x), round(a.get_actor_location().y), round(a.get_actor_location().z)],
               'rot': [round(a.get_actor_rotation().pitch, 2), round(a.get_actor_rotation().yaw, 2), round(a.get_actor_rotation().roll, 2)],
               'hidden_in_game': a.is_hidden_ed() if hasattr(a, 'is_hidden_ed') else None}
        for comp_cls, keys in LIGHT_KEYS.items():
            c = a.get_component_by_class(getattr(u, comp_cls))
            if c:
                row[comp_cls] = {k: P(c, k) for k in keys}
        if cls in ('PointLight', 'SpotLight', 'RectLight'):
            c = a.get_component_by_class(u.LightComponent)
            row['light'] = {k: P(c, k) for k in ('intensity', 'attenuation_radius', 'light_color', 'cast_shadows', 'visible')}
        if cls == 'PostProcessVolume':
            row['unbound'] = P(a, 'unbound'); row['priority'] = P(a, 'priority'); row['blend_weight'] = P(a, 'blend_weight'); row['enabled'] = P(a, 'enabled')
            st = a.get_editor_property('settings'); ov = {}
            for k in PP_KEYS:
                try:
                    if st.get_editor_property('override_' + k):
                        ov[k] = P(st, k)
                except Exception:
                    pass
            row['pp_overrides'] = ov
        res['look_actors'].append(row)
# structural meshes in use (actors + foliage)
KEYS = ('rock', 'stone', 'cliff', 'embank', 'root', 'log', 'trunk', 'stump', 'moss', 'litter', 'leaves', 'branch', 'debris', 'boulder', 'needle', 'twig', 'bark', 'mud', 'soil')
cnt = collections.Counter()
for a in A:
    for c in a.get_components_by_class(u.StaticMeshComponent):
        m = c.get_editor_property('static_mesh')
        if not m:
            continue
        n = m.get_path_name()
        if any(k in n.lower() for k in KEYS):
            cnt[n] += c.get_instance_count() if isinstance(c, u.InstancedStaticMeshComponent) else 1
res['structural_meshes'] = dict(cnt.most_common(80))
reg = u.AssetRegistryHelpers.get_asset_registry()
flt = u.ARFilter(package_paths=['/Game'], recursive_paths=True, class_paths=[u.TopLevelAssetPath('/Script/Engine', 'MaterialInstanceConstant'), u.TopLevelAssetPath('/Script/Engine', 'Material')])
for ad in reg.get_assets(flt):
    n = str(ad.package_name)
    if 'decal' in n.lower():
        res['decals'].append(n)
res['decals'] = sorted(res['decals'])[:200]
json.dump(res, open(os.path.join(PILOT, 'look_probe.json'), 'w'), indent=1, default=str)
print('LOOK_PROBE actors %d decals %d structural %d' % (len(res['look_actors']), len(res['decals']), len(res['structural_meshes'])))
for r in res['look_actors']:
    print(' ', r['class'], r['label'], r['level'], r['rot'], {k: v for k, v in r.items() if k in ('pp_overrides', 'unbound', 'priority', 'enabled', 'light')})
