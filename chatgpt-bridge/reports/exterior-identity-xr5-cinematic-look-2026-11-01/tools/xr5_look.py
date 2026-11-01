"""xr5_look.py (WRITE job under the map manifest; NEVER saves): cinematic look variants on the EXISTING owners, in memory, with a
one-time backup and a full restore. builtins.XR5_LOOK in LOOKS or 'restore'.
Owners: EX_PostRain_Sun (DirectionalLight, actor rotation + component), EX_PostRain_Sky (SkyLight), EX_PostRain_Atmosphere
(SkyAtmosphere), EX_PostRain_Humidity (ExponentialHeightFog), EX_PostRain_NeutralExposure (PostProcessVolume: 'settings' struct with
override_<key> flags). Regional atmosphere = spawned XR5_* actors (PostProcessVolume boxes with blend radius, LocalFogVolume spheres)
destroyed on restore. The first call writes design/xr5_backup.json (every key any look touches: value + override flag); 'restore' writes
it back and clears the override flags it set. Output design/xr5_<look>.json.

Looks (all post-rain, same weather, same world):
  L1 "Gumus nem" (silver damp)        : west-south sun 1400 lx 5600 K, cool sky 1.7, grey-blue fog; WB 6200, contrast 1.08, sat 0.86,
                                         lifted cool shadows, desaturated highlights, film toe 0.6; bloom 0.25, vignette 0.3, grain 0.08
  L2 "Bakir isik" (copper light)      : low south sun 1600 lx 4600 K (XR4 A direction, less), cool sky 0.9, warm directional fog;
                                         WB 5300 (warm key), cool shadow gain, warm highlight gain, contrast 1.12, sat 0.92; bloom 0.4
                                         threshold 1.0, vignette 0.35, grain 0.12
  L3 "Kapali mavi saat" (overcast)    : soft sun 650 lx 7400 K angle 6, sky 2.5, dense low cool fog; WB 6900, contrast 1.18, gamma lift
                                         midtones, sat 0.8 with green-blue shadows; no bloom, vignette 0.4, grain 0.15
  FINAL                                : the chosen base (set after the comparison) + regional volumes (house warm/clear, forest
                                         transition darker and denser, pond mist + quieter highlights)
  RES                                  : FINAL + the 'resonance' delta (subtle: WB -300 K, sat 0.94, grain +0.08, shadow tint shift,
                                         vignette +0.1, fringe 0.35) - a preview of how the same place may read later in the story"""
import unreal as u, json, os, builtins, pathlib

PJ = pathlib.Path(u.Paths.project_dir()); D = PJ / 'Saved/Codex/ExteriorIdentity_XR3_20261031/design'
LOOK = builtins.XR5_LOOK
E = u.get_editor_subsystem(u.UnrealEditorSubsystem); assert E.get_game_world() is None, 'PIE running'
A = u.get_editor_subsystem(u.EditorActorSubsystem); ACT = {a.get_actor_label(): a for a in A.get_all_level_actors()}
sun_a, sky_a, atm_a, fog_a, pp_a = (ACT[k] for k in ('EX_PostRain_Sun', 'EX_PostRain_Sky', 'EX_PostRain_Atmosphere', 'EX_PostRain_Humidity', 'EX_PostRain_NeutralExposure'))
sun = sun_a.get_component_by_class(u.DirectionalLightComponent); sky = sky_a.get_component_by_class(u.SkyLightComponent)
atm = atm_a.get_component_by_class(u.SkyAtmosphereComponent); fog = fog_a.get_component_by_class(u.ExponentialHeightFogComponent)
LC = lambda c: u.LinearColor(c[0], c[1], c[2], c[3] if len(c) > 3 else 1.0)
V4 = lambda v: u.Vector4(v[0], v[1], v[2], v[3] if len(v) > 3 else 1.0)
COLOR_KEYS = ('fog_inscattering_luminance', 'directional_inscattering_luminance', 'lower_hemisphere_color')
V4_KEYS = ('color_saturation', 'color_contrast', 'color_gamma', 'color_gain', 'color_offset', 'color_saturation_shadows', 'color_contrast_shadows', 'color_gamma_shadows',
           'color_gain_shadows', 'color_offset_shadows', 'color_saturation_midtones', 'color_contrast_midtones', 'color_gamma_midtones', 'color_gain_midtones',
           'color_saturation_highlights', 'color_contrast_highlights', 'color_gamma_highlights', 'color_gain_highlights', 'color_offset_highlights')

LOOKS = {
 'L1': {'sun_rot': [-24.0, -62.0], 'sun': {'intensity': 1400.0, 'temperature': 5600.0, 'light_source_angle': 1.6, 'volumetric_scattering_intensity': 1.6},
        'sky': {'intensity': 1.7}, 'atm': {'mie_scattering_scale': 0.02, 'mie_anisotropy': 0.7},
        'fog': {'fog_density': 0.016, 'fog_height_falloff': 0.22, 'start_distance': 300.0, 'fog_max_opacity': 0.55, 'fog_inscattering_luminance': [0.050, 0.058, 0.066],
                'directional_inscattering_luminance': [0.02, 0.022, 0.024], 'directional_inscattering_exponent': 6.0, 'volumetric_fog_extinction_scale': 1.5, 'volumetric_fog_albedo': [200, 210, 220, 255]},
        'pp': {'white_temp': 6200.0, 'white_tint': 0.0, 'color_contrast': [1.08, 1.08, 1.08, 1.0], 'color_saturation': [0.86, 0.86, 0.86, 1.0],
               'color_gain_shadows': [0.96, 1.0, 1.06, 1.0], 'color_offset_shadows': [0.006, 0.008, 0.012, 0.0], 'color_saturation_highlights': [0.8, 0.8, 0.8, 1.0],
               'color_gain_highlights': [1.0, 0.99, 0.97, 1.0], 'film_slope': 0.86, 'film_toe': 0.6, 'film_shoulder': 0.28, 'film_white_clip': 0.03,
               'bloom_intensity': 0.25, 'bloom_threshold': 0.5, 'vignette_intensity': 0.3, 'film_grain_intensity': 0.08, 'auto_exposure_bias': -0.75,
               'auto_exposure_min_brightness': -1.0, 'auto_exposure_max_brightness': 10.0, 'local_exposure_highlight_contrast_scale': 0.85, 'local_exposure_shadow_contrast_scale': 0.9}},
 'L2': {'sun_rot': [-10.0, -95.0], 'sun': {'intensity': 1600.0, 'temperature': 4600.0, 'light_source_angle': 1.0, 'volumetric_scattering_intensity': 2.2},
        'sky': {'intensity': 0.9}, 'atm': {'mie_scattering_scale': 0.018, 'mie_anisotropy': 0.75},
        'fog': {'fog_density': 0.022, 'fog_height_falloff': 0.3, 'start_distance': 0.0, 'fog_max_opacity': 0.65, 'fog_inscattering_luminance': [0.040, 0.046, 0.054],
                'directional_inscattering_luminance': [0.085, 0.06, 0.035], 'directional_inscattering_exponent': 7.0, 'volumetric_fog_extinction_scale': 1.8, 'volumetric_fog_albedo': [230, 215, 195, 255]},
        'pp': {'white_temp': 5300.0, 'white_tint': 0.0, 'color_contrast': [1.12, 1.12, 1.12, 1.0], 'color_saturation': [0.92, 0.92, 0.92, 1.0],
               'color_gain_shadows': [0.94, 0.98, 1.08, 1.0], 'color_gain_highlights': [1.05, 1.0, 0.92, 1.0], 'color_saturation_highlights': [0.9, 0.9, 0.9, 1.0],
               'film_slope': 0.9, 'film_toe': 0.52, 'film_shoulder': 0.3, 'film_white_clip': 0.04,
               'bloom_intensity': 0.4, 'bloom_threshold': 1.0, 'vignette_intensity': 0.35, 'film_grain_intensity': 0.12, 'auto_exposure_bias': -0.9,
               'auto_exposure_min_brightness': -1.0, 'auto_exposure_max_brightness': 10.0, 'local_exposure_highlight_contrast_scale': 0.8, 'local_exposure_shadow_contrast_scale': 0.9}},
 'L3': {'sun_rot': [-34.0, -75.0], 'sun': {'intensity': 650.0, 'temperature': 7400.0, 'light_source_angle': 6.0, 'volumetric_scattering_intensity': 0.8},
        'sky': {'intensity': 2.5}, 'atm': {'mie_scattering_scale': 0.03, 'mie_anisotropy': 0.5},
        'fog': {'fog_density': 0.026, 'fog_height_falloff': 0.16, 'start_distance': 0.0, 'fog_max_opacity': 0.6, 'fog_inscattering_luminance': [0.052, 0.062, 0.072],
                'directional_inscattering_luminance': [0.0, 0.0, 0.0], 'directional_inscattering_exponent': 4.0, 'volumetric_fog_extinction_scale': 1.4, 'volumetric_fog_albedo': [190, 205, 215, 255]},
        'pp': {'white_temp': 6900.0, 'white_tint': 0.08, 'color_contrast': [1.18, 1.18, 1.18, 1.0], 'color_saturation': [0.8, 0.8, 0.8, 1.0],
               'color_gamma_midtones': [1.06, 1.06, 1.06, 1.0], 'color_gain_shadows': [0.92, 1.0, 1.04, 1.0], 'color_saturation_shadows': [0.9, 0.9, 0.9, 1.0],
               'film_slope': 0.84, 'film_toe': 0.62, 'film_shoulder': 0.24, 'film_white_clip': 0.03,
               'bloom_intensity': 0.0, 'bloom_threshold': -1.0, 'vignette_intensity': 0.4, 'film_grain_intensity': 0.15, 'auto_exposure_bias': -0.5,
               'auto_exposure_min_brightness': -1.0, 'auto_exposure_max_brightness': 8.0, 'local_exposure_highlight_contrast_scale': 0.8, 'local_exposure_shadow_contrast_scale': 0.85}},
}
# regional volumes: (label, kind, location, scale, settings)
REGIONS = [
    ('XR5_PPV_House', 'ppv', (900, 1300, 150), (55, 45, 25), {'priority': 2.0, 'blend_radius': 900.0, 'pp': {'auto_exposure_bias': 0.25, 'white_temp': -250, 'color_gain_midtones': [1.03, 1.0, 0.96, 1.0]}}),
    ('XR5_PPV_Shelf', 'ppv', (2900, 4900, 100), (22, 60, 25), {'priority': 2.0, 'blend_radius': 700.0, 'pp': {'auto_exposure_bias': -0.35, 'color_contrast': [1.06, 1.06, 1.06, 1.0], 'color_gain_shadows': [0.95, 1.0, 1.07, 1.0]}}),
    ('XR5_PPV_Glade', 'ppv', (-900, 8750, 150), (40, 40, 25), {'priority': 2.0, 'blend_radius': 900.0, 'pp': {'auto_exposure_bias': -0.15, 'color_saturation': [0.9, 0.9, 0.9, 1.0], 'local_exposure_highlight_contrast_scale': 0.75}}),
    ('XR5_Fog_Pond', 'fog', (-600, 5200, -60), (42, 38, 6), {'radial_fog_extinction': 0.08, 'height_fog_extinction': 0.14, 'height_fog_falloff': 900.0, 'fog_albedo': [0.72, 0.78, 0.84], 'fog_phase_g': 0.3}),
    ('XR5_Fog_Inlet', 'fog', (2300, 7300, 0), (14, 12, 5), {'radial_fog_extinction': 0.14, 'height_fog_extinction': 0.2, 'height_fog_falloff': 500.0, 'fog_albedo': [0.7, 0.76, 0.8], 'fog_phase_g': 0.3}),
]
RES_DELTA = {'white_temp': -300, 'color_saturation': [0.94, 0.94, 0.94, 1.0], 'film_grain_intensity': 0.08, 'vignette_intensity': 0.1, 'scene_fringe_intensity': 0.35,
             'color_gain_shadows': [0.98, 0.96, 1.04, 1.0]}
BASE_FOR_FINAL = getattr(builtins, 'XR5_BASE', 'L1')
if LOOK in ('FINAL', 'RES'):
    import copy
    spec = copy.deepcopy(LOOKS[BASE_FOR_FINAL]); spec['regions'] = getattr(builtins, 'XR5_FINAL_REGIONS', REGIONS)
    spec['pp'].update(getattr(builtins, 'XR5_FINAL_PP', {})); spec['sun'].update(getattr(builtins, 'XR5_FINAL_SUN', {})); spec['fog'].update(getattr(builtins, 'XR5_FINAL_FOG', {})); spec['sky'].update(getattr(builtins, 'XR5_FINAL_SKY', {})); spec['atm'].update(getattr(builtins, 'XR5_FINAL_ATM', {}))
    if 'XR5_FINAL_SUNROT' in dir(builtins): spec['sun_rot'] = builtins.XR5_FINAL_SUNROT
    if LOOK == 'RES':
        for k, v in RES_DELTA.items():
            spec['pp'][k] = (spec['pp'].get(k, 0) + v) if isinstance(v, (int, float)) and k != 'scene_fringe_intensity' else v
    LOOKS[LOOK] = spec
KEYS = {'sun': set(), 'sky': set(), 'atm': set(), 'fog': set(), 'pp': set()}
for lk in LOOKS.values():
    for g in KEYS: KEYS[g] |= set(lk.get(g, {}))
KEYS['pp'] |= set(RES_DELTA)
for r in list(REGIONS) + list(getattr(builtins, 'XR5_FINAL_REGIONS', [])):
    if r[1] == 'ppv': KEYS['pp'] |= set(r[4]['pp'])
COMP = {'sun': sun, 'sky': sky, 'atm': atm, 'fog': fog}


def rd(c, k):
    v = c.get_editor_property(k)
    if k in COLOR_KEYS: return [v.r, v.g, v.b, v.a]
    if k == 'volumetric_fog_albedo': return [v.r, v.g, v.b, v.a]
    return v


def wr(c, k, v):
    if k in COLOR_KEYS: v = LC(v)
    elif k == 'volumetric_fog_albedo': v = u.Color(r=int(v[0]), g=int(v[1]), b=int(v[2]), a=int(v[3]))
    c.set_editor_property(k, v)


def pp_read(settings, k):
    v = settings.get_editor_property(k)
    if k in V4_KEYS: v = [v.x, v.y, v.z, v.w]
    return [v, bool(settings.get_editor_property('override_' + k))]


def pp_write(settings, k, v, override=True):
    settings.set_editor_property(k, V4(v) if k in V4_KEYS else v); settings.set_editor_property('override_' + k, override)


bk_path = D / 'xr5_backup.json'
if not bk_path.exists():
    s0 = pp_a.get_editor_property('settings')
    bk = {'sun_rot': [sun_a.get_actor_rotation().pitch, sun_a.get_actor_rotation().yaw, sun_a.get_actor_rotation().roll],
          'comp': {g: {k: rd(COMP[g], k) for k in sorted(KEYS[g])} for g in COMP}, 'pp': {}}
    for k in sorted(KEYS['pp']):
        try: bk['pp'][k] = pp_read(s0, k)
        except Exception as ex: bk['pp'][k] = ['ERR ' + str(ex)[:80], False]
    bk_path.write_text(json.dumps(bk, indent=1, default=str))
bk = json.loads(bk_path.read_text())
res = {'look': LOOK, 'problems': [], 'regions': []}


def apply_base(spec):
    sr = spec.get('sun_rot', bk['sun_rot']); sun_a.set_actor_rotation(u.Rotator(pitch=sr[0], yaw=sr[1], roll=0.0), False)
    for g in COMP:                                           # always start from the backup so looks never stack
        for k, v in bk['comp'][g].items():
            try: wr(COMP[g], k, v)
            except Exception as ex: res['problems'].append('restore %s.%s %s' % (g, k, ex))
        for k, v in spec.get(g, {}).items():
            try: wr(COMP[g], k, v)
            except Exception as ex: res['problems'].append('%s.%s %s' % (g, k, ex))
    s = pp_a.get_editor_property('settings')
    for k, (v, ov) in bk['pp'].items():
        if isinstance(v, str) and v.startswith('ERR'): continue
        try: pp_write(s, k, v, ov)
        except Exception as ex: res['problems'].append('pp restore %s %s' % (k, ex))
    for k, v in spec.get('pp', {}).items():
        try: pp_write(s, k, v, True)
        except Exception as ex: res['problems'].append('pp %s %s' % (k, ex))
    pp_a.set_editor_property('settings', s)


def destroy_regions():
    n = 0
    for a in A.get_all_level_actors():
        if a.get_actor_label().startswith('XR5_'): A.destroy_actor(a); n += 1
    return n


def spawn_regions(regs):
    for lab, kind, loc, sc, cfg in regs:
        try:
            if kind == 'ppv':
                a = A.spawn_actor_from_class(u.PostProcessVolume, u.Vector(*loc), u.Rotator(0, 0, 0)); a.set_actor_scale3d(u.Vector(*sc))
                a.set_editor_property('unbound', False); a.set_editor_property('priority', cfg['priority']); a.set_editor_property('blend_radius', cfg['blend_radius'])
                s = a.get_editor_property('settings'); base = pp_a.get_editor_property('settings')
                for k, v in cfg['pp'].items():
                    if k in ('white_temp', 'auto_exposure_bias'):        # deltas on the base look
                        v = base.get_editor_property(k) + v
                    pp_write(s, k, v, True)
                a.set_editor_property('settings', s)
            else:
                a = A.spawn_actor_from_class(u.LocalFogVolume, u.Vector(*loc), u.Rotator(0, 0, 0)); a.set_actor_scale3d(u.Vector(*sc))
                c = a.get_component_by_class(u.LocalFogVolumeComponent)
                for k, v in cfg.items():
                    c.set_editor_property(k, LC(v) if k == 'fog_albedo' else v)
            a.set_actor_label(lab); a.set_folder_path('XR5_Look')
            o, e = a.get_actor_bounds(False); res['regions'].append({'label': lab, 'bounds_m': [round(e.x / 50), round(e.y / 50), round(e.z / 50)]})
        except Exception as ex:
            res['problems'].append('region %s %s' % (lab, repr(ex)[:160]))


with u.ScopedEditorTransaction('XR5 look %s (unsaved test)' % LOOK):
    res['regions_destroyed'] = destroy_regions()
    if LOOK == 'restore':
        apply_base({})
    else:
        spec = LOOKS[LOOK]; apply_base(spec)
        if spec.get('regions'): spawn_regions(spec['regions'])
sky.recapture_sky()
S = u.EditorLoadingAndSavingUtils
res['dirty'] = sorted([p.get_name() for p in S.get_dirty_content_packages()] + [p.get_name() for p in S.get_dirty_map_packages()])
res['sun_rot'] = [sun_a.get_actor_rotation().pitch, sun_a.get_actor_rotation().yaw]
(D / ('xr5_%s.json' % LOOK)).write_text(json.dumps(res, indent=1, default=str))
print('XR5_LOOK', LOOK, 'problems', res['problems'][:4], 'regions', len(res['regions']), 'destroyed', res['regions_destroyed'])
