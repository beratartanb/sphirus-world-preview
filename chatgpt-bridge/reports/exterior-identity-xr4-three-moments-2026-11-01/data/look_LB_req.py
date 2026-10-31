import builtins
# XR4 look B "kapali, nemli, alcak kontrast": weak soft sun, cool dominant sky, moist haze; value hierarchy must then come from masses alone.
builtins.LOOK_TRIAL_SPEC = {'sun_rot': [-32.0, -70.0], 'sun': {'intensity': 380.0, 'temperature': 7000.0, 'light_source_angle': 8.0, 'volumetric_scattering_intensity': 1.0},
    'sky': {'intensity': 2.1},
    'fog': {'fog_density': 0.02, 'start_distance': 0.0, 'fog_height_falloff': 0.2, 'fog_max_opacity': 0.6, 'fog_inscattering_luminance': [0.06, 0.068, 0.076],
            'directional_inscattering_luminance': [0.0, 0.0, 0.0], 'directional_inscattering_exponent': 4.0}}
builtins.LOOK_VARIANT = 'TRIAL'
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/AIToolingEval_20261031/look_variant.py', encoding='utf-8').read(), 'look_variant.py', 'exec'), {'__name__': '__job__'})
