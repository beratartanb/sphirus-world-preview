"""showcase_load.py (measure job): load the Pine Forest Pack showcase map (reference), record its lighting recipe and candidate
camera spots. builtins.PFR_LEVEL (default /Game/PineForestPack/Levels/L_Showcase). Nothing is saved. The caller must bring the
production map back afterwards (showcase_cap.py / load_production.py). Writes Saved/Codex/PineForestRedesign_20261104/ref/showcase_info.json"""
import unreal as u, json, pathlib, time, builtins, math

D = pathlib.Path(u.Paths.project_dir()) / 'Saved/Codex/PineForestRedesign_20261104/ref'; D.mkdir(parents=True, exist_ok=True)
LVL = getattr(builtins, 'PFR_LEVEL', '/Game/PineForestPack/Levels/L_Showcase')
E = u.get_editor_subsystem(u.UnrealEditorSubsystem); assert E.get_game_world() is None, 'PIE running'
S = u.EditorLoadingAndSavingUtils
dirty = sorted([p.get_name() for p in S.get_dirty_content_packages()] + [p.get_name() for p in S.get_dirty_map_packages()])
assert not dirty, 'dirty packages before level switch: %s' % dirty[:5]
L = u.get_editor_subsystem(u.LevelEditorSubsystem)
t0 = time.monotonic()
# 2026-11-04: load_level from inside a runner job crashed the editor (EXCEPTION_ACCESS_VIOLATION in python311 during the world switch);
# the showcase editor is now launched directly on the map and this job only reads it (PFR_NOLOAD).
if getattr(builtins, 'PFR_NOLOAD', True):
    ok = True
else:
    ok = L.load_level(LVL)
w = E.get_editor_world(); assert 'PineForestPack' in w.get_path_name(), 'not the showcase world: ' + w.get_path_name()
info = {'level': LVL, 'load_ok': bool(ok), 'load_s': round(time.monotonic() - t0, 1), 'world': w.get_path_name(), 'sublevels': [], 'lights': {}, 'cameras': [], 'player_starts': [], 'pp': []}
for sl in u.EditorLevelUtils.get_levels(w):
    try:
        pkg = sl.get_outer().get_name(); vis = sl.get_editor_property('b_is_visible') if False else None
    except Exception:
        pkg = str(sl)
    info['sublevels'].append({'package': pkg, 'visible': u.EditorLevelUtils.get_level_visibility if False else None})
try:
    info['streaming'] = [{'package': str(s.get_editor_property('world_asset').get_path_name() if s.get_editor_property('world_asset') else s.get_world_asset_package_name()), 'should_be_visible': s.get_editor_property('should_be_visible'), 'loaded': s.is_level_loaded(), 'visible': s.is_level_visible()} for s in w.get_editor_property('streaming_levels')]
except Exception as ex:
    info['streaming'] = 'n/a ' + repr(ex)[:200]
A = u.get_editor_subsystem(u.EditorActorSubsystem)
for a in A.get_all_level_actors():
    cls = a.get_class().get_name(); lab = a.get_actor_label(); lvl = a.get_level().get_outer().get_name()
    try:
        if isinstance(a, u.DirectionalLight):
            c = a.get_component_by_class(u.DirectionalLightComponent)
            info['lights'][lab] = {'class': cls, 'level': lvl, 'rot': [round(v, 2) for v in a.get_actor_rotation().to_tuple()], 'intensity': c.get_editor_property('intensity'), 'temp': c.get_editor_property('temperature'), 'use_temp': c.get_editor_property('use_temperature'),
                                   'color': [round(v, 3) for v in c.get_editor_property('light_color').to_tuple()], 'angle': c.get_editor_property('light_source_angle'), 'vol': c.get_editor_property('volumetric_scattering_intensity'), 'atmos_sun': c.get_editor_property('atmosphere_sun_light'), 'mobility': str(c.get_editor_property('mobility'))}
        elif isinstance(a, u.SkyLight):
            c = a.get_component_by_class(u.SkyLightComponent)
            info['lights'][lab] = {'class': cls, 'level': lvl, 'intensity': c.get_editor_property('intensity'), 'real_time': c.get_editor_property('real_time_capture'), 'source': str(c.get_editor_property('source_type')), 'lower_hemi': c.get_editor_property('lower_hemisphere_is_black'), 'vol': c.get_editor_property('volumetric_scattering_intensity')}
        elif isinstance(a, u.ExponentialHeightFog):
            c = a.get_component_by_class(u.ExponentialHeightFogComponent)
            info['lights'][lab] = {'class': cls, 'level': lvl, 'loc': [round(v) for v in a.get_actor_location().to_tuple()], 'density': c.get_editor_property('fog_density'), 'falloff': c.get_editor_property('fog_height_falloff'), 'start': c.get_editor_property('start_distance'), 'opacity': c.get_editor_property('fog_max_opacity'),
                                   'inscatter': [round(v, 4) for v in c.get_editor_property('fog_inscattering_luminance').to_tuple()], 'dir_inscatter': [round(v, 4) for v in c.get_editor_property('directional_inscattering_luminance').to_tuple()], 'dir_exp': c.get_editor_property('directional_inscattering_exponent'),
                                   'vol_fog': c.get_editor_property('volumetric_fog'), 'vol_ext': c.get_editor_property('volumetric_fog_extinction_scale'), 'vol_dist': c.get_editor_property('volumetric_fog_distance'), 'vol_albedo': [round(v, 3) for v in c.get_editor_property('volumetric_fog_albedo').to_tuple()] if hasattr(c.get_editor_property('volumetric_fog_albedo'), 'to_tuple') else str(c.get_editor_property('volumetric_fog_albedo')),
                                   'second_density': c.get_editor_property('second_fog_data').get_editor_property('fog_density'), 'second_falloff': c.get_editor_property('second_fog_data').get_editor_property('fog_height_falloff'), 'second_offset': c.get_editor_property('second_fog_data').get_editor_property('fog_height_offset')}
        elif isinstance(a, u.SkyAtmosphere):
            c = a.get_component_by_class(u.SkyAtmosphereComponent)
            info['lights'][lab] = {'class': cls, 'level': lvl, 'mie_scale': c.get_editor_property('mie_scattering_scale'), 'mie_aniso': c.get_editor_property('mie_anisotropy'), 'rayleigh': c.get_editor_property('rayleigh_scattering_scale'), 'aerial_scale': c.get_editor_property('aerial_pespective_view_distance_scale'), 'height_fog_contrib': c.get_editor_property('height_fog_contribution')}
        elif isinstance(a, u.VolumetricCloud):
            info['lights'][lab] = {'class': cls, 'level': lvl}
        elif isinstance(a, u.PostProcessVolume):
            s = a.get_editor_property('settings'); d = {'class': cls, 'level': lvl, 'unbound': a.get_editor_property('unbound'), 'priority': a.get_editor_property('priority'), 'blend': a.get_editor_property('blend_weight')}
            for k in ('auto_exposure_method', 'auto_exposure_bias', 'auto_exposure_min_brightness', 'auto_exposure_max_brightness', 'white_temp', 'white_tint', 'color_saturation', 'color_contrast', 'color_gamma', 'color_gain', 'film_slope', 'film_toe', 'film_shoulder', 'film_black_clip', 'film_white_clip',
                      'bloom_intensity', 'bloom_threshold', 'vignette_intensity', 'film_grain_intensity', 'ambient_occlusion_intensity', 'lumen_scene_lighting_quality', 'lumen_final_gather_quality', 'reflection_method', 'dynamic_global_illumination_method', 'local_exposure_highlight_contrast_scale', 'local_exposure_shadow_contrast_scale', 'color_grading_lut', 'color_grading_intensity', 'scene_fringe_intensity', 'indirect_lighting_intensity', 'auto_exposure_apply_physical_camera_exposure', 'camera_iso', 'camera_shutter_speed', 'depth_of_field_fstop'):
                try:
                    if s.get_editor_property('override_' + k):
                        v = s.get_editor_property(k); d[k] = [round(x, 3) for x in v.to_tuple()] if hasattr(v, 'to_tuple') else (v.get_path_name() if hasattr(v, 'get_path_name') else (str(v) if not isinstance(v, (int, float, bool)) else v))
                except Exception:
                    pass
            info['pp'].append({lab: d})
        elif isinstance(a, (u.CameraActor, u.CineCameraActor)):
            cc = a.get_component_by_class(u.CameraComponent)
            info['cameras'].append({'label': lab, 'class': cls, 'loc': [round(v) for v in a.get_actor_location().to_tuple()], 'rot': [round(v, 1) for v in a.get_actor_rotation().to_tuple()], 'fov': cc.get_editor_property('field_of_view') if cc else None})
        elif isinstance(a, u.PlayerStart):
            info['player_starts'].append({'label': lab, 'loc': [round(v) for v in a.get_actor_location().to_tuple()], 'rot': [round(v, 1) for v in a.get_actor_rotation().to_tuple()]})
    except Exception as ex:
        info.setdefault('errors', []).append(lab + ': ' + repr(ex)[:160])
# world bounds of static geometry + landscape (for a view grid)
try:
    land = [a for a in A.get_all_level_actors() if isinstance(a, u.Landscape)]
    info['landscape'] = [{'label': l.get_actor_label(), 'material': str(l.get_editor_property('landscape_material')), 'bounds': [[round(v) for v in l.get_actor_bounds(False)[0].to_tuple()], [round(v) for v in l.get_actor_bounds(False)[1].to_tuple()]], 'target_layers': [str(x) for x in l.get_target_layer_names(False)]} for l in land]
    import collections
    cnt = collections.Counter(a.get_class().get_name() for a in A.get_all_level_actors()); info['actor_classes'] = cnt.most_common(30)
    info['n_actors'] = sum(cnt.values())
    ifa = [a for a in A.get_all_level_actors() if isinstance(a, u.InstancedFoliageActor)]; fol = collections.Counter()
    for a in ifa:
        for c in a.get_components_by_class(u.InstancedStaticMeshComponent):
            if c.static_mesh: fol[c.static_mesh.get_name()] += c.get_instance_count()
    info['foliage_meshes'] = fol.most_common(60)
    info['rvt_volumes'] = [a.get_actor_label() for a in A.get_all_level_actors() if a.get_class().get_name() == 'RuntimeVirtualTextureVolume']
    info['world_settings_gamemode'] = str(w.get_world_settings().get_editor_property('default_game_mode')) if w.get_world_settings() else None
except Exception as ex:
    info['bounds_err'] = repr(ex)[:200]
(D / 'showcase_info.json').write_text(json.dumps(info, indent=1, default=str))
print('SHOWCASE_LOAD', json.dumps({k: info[k] for k in ('level', 'load_ok', 'load_s', 'world', 'n_actors', 'player_starts', 'cameras', 'rvt_volumes')}, default=str)[:1500])
