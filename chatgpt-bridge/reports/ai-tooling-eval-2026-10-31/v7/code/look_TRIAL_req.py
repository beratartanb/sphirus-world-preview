import builtins
# TRIAL look = V1 key/fill structure (form, light hierarchy) cooled toward the Sphirus palette + a little of V3's moist depth.
builtins.LOOK_TRIAL_SPEC = {
    'sun_rot': [-36.0, -38.0],
    'sun': {'intensity': 3000.0, 'temperature': 6100.0, 'light_source_angle': 1.0, 'volumetric_scattering_intensity': 1.8},
    'sky': {'intensity': 1.3},
    'fog': {'fog_density': 0.010, 'start_distance': 900.0, 'fog_height_falloff': 0.15, 'fog_max_opacity': 0.45, 'fog_inscattering_luminance': [0.052, 0.060, 0.068]},
}
builtins.LOOK_VARIANT = 'TRIAL'
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/AIToolingEval_20261031/look_variant.py', encoding='utf-8').read(), 'look_variant.py', 'exec'), {'__name__': '__job__'})
