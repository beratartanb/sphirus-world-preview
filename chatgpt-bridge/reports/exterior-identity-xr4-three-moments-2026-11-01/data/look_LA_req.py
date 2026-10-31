import builtins
# XR4 look A "alcak guney gunesi, nemli": sun low in the SOUTH (yaw -95: the light travels north) so the shelf and the inlet are BACKLIT
# (rim light + shafts in the release) and the house is FRONTLIT from the far shore; warm directional in-scatter, dense low fog.
builtins.LOOK_TRIAL_SPEC = {'sun_rot': [-11.0, -95.0], 'sun': {'intensity': 2200.0, 'temperature': 5000.0, 'light_source_angle': 1.0, 'volumetric_scattering_intensity': 2.6},
    'sky': {'intensity': 0.9},
    'fog': {'fog_density': 0.028, 'start_distance': 0.0, 'fog_height_falloff': 0.35, 'fog_max_opacity': 0.7, 'fog_inscattering_luminance': [0.045, 0.05, 0.056],
            'directional_inscattering_luminance': [0.10, 0.075, 0.045], 'directional_inscattering_exponent': 6.0}}
builtins.LOOK_VARIANT = 'TRIAL'
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/AIToolingEval_20261031/look_variant.py', encoding='utf-8').read(), 'look_variant.py', 'exec'), {'__name__': '__job__'})
