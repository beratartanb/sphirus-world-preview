"""look_variant.py (WRITE job under a manifest; NEVER saves): apply one of three physically based light/atmosphere approaches to the
EXISTING look owners (EX_PostRain_Sun / _Sky / _Humidity, all in L_GR_SphirusHouse) in memory, or restore them.
builtins.LOOK_VARIANT in {'V1', 'V2', 'V3', 'TRIAL', 'restore'}. The first call records every touched property to
<VMP>/look_original.json; 'restore' writes those values back. The SkyLight (captured scene, no real-time capture) is recaptured after
every change. No LUT, colour-grade, bloom or vignette change (AGENTS: no orange/teal grade, restrained PP; the neutral exposure PPV is kept).

  V1 'filtered daylight'  Requiem-like grounded daylight: higher, stronger sun vs. weaker sky fill (value separation, canopy dapples),
                          cleaner middle distance (less, later fog)
  V2 'low morning damp'   low sun as back/side light for the trail views, fog hugging low ground, gentle directional glow toward the
                          sun, volumetric shafts
  V3 'overcast wet cool'  TLOU2/PNW-like: very soft weak sun, dominant cool sky, moist distance haze
  TRIAL                   the variant chosen after comparison (defined in TRIAL_FROM; may be refined below)
"""
import unreal as u, json, os, builtins

VMP = r'C:\Users\berat\AppData\Local\Temp\claude\C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS\5f49a232-b001-47ad-8881-1eb04d9cb1c5\scratchpad\vmp'
V = getattr(builtins, 'LOOK_VARIANT')
A = {a.get_actor_label(): a for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors()}
sun_a, sky_a, fog_a = A['EX_PostRain_Sun'], A['EX_PostRain_Sky'], A['EX_PostRain_Humidity']
sun = sun_a.get_component_by_class(u.DirectionalLightComponent); sky = sky_a.get_component_by_class(u.SkyLightComponent); fog = fog_a.get_component_by_class(u.ExponentialHeightFogComponent)
LC = lambda c: u.LinearColor(c[0], c[1], c[2], 1.0)
VARIANTS = {
    'V1': {'sun_rot': [-38.0, -38.0], 'sun': {'intensity': 3200.0, 'temperature': 5600.0, 'light_source_angle': 1.0, 'volumetric_scattering_intensity': 1.5},
           'sky': {'intensity': 1.1},
           'fog': {'fog_density': 0.008, 'start_distance': 1200.0, 'fog_height_falloff': 0.15, 'fog_max_opacity': 0.4, 'fog_inscattering_luminance': [0.05, 0.058, 0.064]}},
    'V2': {'sun_rot': [-14.0, 59.0], 'sun': {'intensity': 2400.0, 'temperature': 4900.0, 'light_source_angle': 1.5, 'volumetric_scattering_intensity': 3.0},
           'sky': {'intensity': 1.3},
           'fog': {'fog_density': 0.02, 'start_distance': 300.0, 'fog_height_falloff': 0.4, 'fog_max_opacity': 0.6, 'fog_inscattering_luminance': [0.058, 0.064, 0.068],
                   'directional_inscattering_luminance': [0.03, 0.025, 0.018], 'directional_inscattering_exponent': 8.0}},
    'V3': {'sun_rot': [-45.0, -38.0], 'sun': {'intensity': 450.0, 'temperature': 6800.0, 'light_source_angle': 10.0, 'volumetric_scattering_intensity': 1.0},
           'sky': {'intensity': 2.4},
           'fog': {'fog_density': 0.016, 'start_distance': 500.0, 'fog_height_falloff': 0.12, 'fog_max_opacity': 0.55, 'fog_inscattering_luminance': [0.06, 0.068, 0.074]}},
}
VARIANTS['TRIAL'] = getattr(builtins, 'LOOK_TRIAL_SPEC', None)
COLOR_KEYS = ('fog_inscattering_luminance', 'directional_inscattering_luminance')
orig_path = os.path.join(VMP, 'look_original.json')
os.makedirs(VMP, exist_ok=True)


def rd(c, k):
    v = c.get_editor_property(k)
    return [v.r, v.g, v.b] if k in COLOR_KEYS else v


if not os.path.exists(orig_path):
    keys = {'sun': sorted({k for s in VARIANTS.values() if s for k in s['sun']}), 'sky': ['intensity'],
            'fog': sorted({k for s in VARIANTS.values() if s for k in s['fog']})}
    o = {'sun_rot': [sun_a.get_actor_rotation().pitch, sun_a.get_actor_rotation().yaw, sun_a.get_actor_rotation().roll],
         'sun': {k: rd(sun, k) for k in keys['sun']}, 'sky': {k: rd(sky, k) for k in keys['sky']}, 'fog': {k: rd(fog, k) for k in keys['fog']}}
    json.dump(o, open(orig_path, 'w'), indent=1)
orig = json.load(open(orig_path))


def apply(spec, full_rot=None):
    if full_rot:
        sun_a.set_actor_rotation(u.Rotator(pitch=full_rot[0], yaw=full_rot[1], roll=full_rot[2] if len(full_rot) > 2 else 0.0), False)
    for k, v in spec.get('sun', {}).items():
        sun.set_editor_property(k, v)
    for k, v in spec.get('sky', {}).items():
        sky.set_editor_property(k, v)
    for k, v in spec.get('fog', {}).items():
        fog.set_editor_property(k, LC(v) if k in COLOR_KEYS else v)


with u.ScopedEditorTransaction('VMP look %s (unsaved test)' % V):
    if V == 'restore':
        apply(orig, orig['sun_rot'])
    else:
        spec = VARIANTS[V]; assert spec, 'no spec for %s' % V
        apply(orig, orig['sun_rot'])     # always start from the original so variants do not stack
        apply(spec, spec.get('sun_rot'))
sun.mark_render_state_dirty() if hasattr(sun, 'mark_render_state_dirty') else None
sky.recapture_sky()
now = {'sun_rot': [sun_a.get_actor_rotation().pitch, sun_a.get_actor_rotation().yaw], 'sun': {k: rd(sun, k) for k in orig['sun']},
       'sky': {k: rd(sky, k) for k in orig['sky']}, 'fog': {k: rd(fog, k) for k in orig['fog']}}
S = u.EditorLoadingAndSavingUtils
dirty = sorted([p.get_name() for p in S.get_dirty_content_packages()] + [p.get_name() for p in S.get_dirty_map_packages()])
json.dump({'variant': V, 'now': now, 'dirty': dirty}, open(os.path.join(VMP, 'look_applied_%s.json' % V), 'w'), indent=1, default=str)
print('LOOK_%s' % V, json.dumps(now, default=str)[:700], 'dirty', dirty)
