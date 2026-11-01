# xr5_final.py: FINAL tuning on top of the L1 base (loaded by xr3_chain look5 before xr5_look.py). Judged on the x7 L1/L2/L3 sheets:
#  - L1 kept the rock / ground detail and the depth layers without crushing blacks, but its sun shafts still washed the pond views
#    (P1 from_veranda, P0 fwd) and the water stayed a bright sheet -> rays become an accent (vol scattering 1.6 -> 0.8, directional
#    inscatter 0.02 -> 0.012), sky a little lower (1.7 -> 1.45) so the water reflection stops reading as a white panel,
#    highlights compressed a touch harder (local exposure highlight 0.85 -> 0.78, highlight gain 0.97).
#  - v1 (xr5_FINAL_v1_overmist.json, views_id_x7_FINALv1): pond mist 0.08/0.14 was a lit wall across the pond -> the histogram exposure
#    adapted to the bright haze and crushed everything else (P0_fwd 19.9 % black, P3_fwd 12 %, house hidden from the glade).
#    v2: mist hugs the water (height extinction with a 350 cm falloff, 3-4x thinner), inlet thinner, shelf/glade bias milder.
import builtins
builtins.XR5_FINAL_SUN = {'intensity': 1300.0, 'volumetric_scattering_intensity': 0.8}
builtins.XR5_FINAL_SKY = {'intensity': 1.45}
builtins.XR5_FINAL_FOG = {'fog_density': 0.015, 'directional_inscattering_luminance': [0.012, 0.0135, 0.015], 'directional_inscattering_exponent': 8.0}
builtins.XR5_FINAL_PP = {'local_exposure_highlight_contrast_scale': 0.78, 'color_gain_highlights': [0.98, 0.975, 0.96, 1.0], 'film_shoulder': 0.26}
builtins.XR5_FINAL_REGIONS = [
    ('XR5_PPV_House', 'ppv', (900, 1300, 150), (55, 45, 25), {'priority': 2.0, 'blend_radius': 900.0, 'pp': {'auto_exposure_bias': 0.2, 'white_temp': -250, 'color_gain_midtones': [1.03, 1.0, 0.96, 1.0]}}),
    ('XR5_PPV_Shelf', 'ppv', (2900, 4900, 100), (22, 60, 25), {'priority': 2.0, 'blend_radius': 700.0, 'pp': {'auto_exposure_bias': -0.2, 'color_contrast': [1.05, 1.05, 1.05, 1.0], 'color_gain_shadows': [0.95, 1.0, 1.07, 1.0]}}),
    ('XR5_PPV_Glade', 'ppv', (-900, 8750, 150), (40, 40, 25), {'priority': 2.0, 'blend_radius': 900.0, 'pp': {'auto_exposure_bias': -0.1, 'color_saturation': [0.9, 0.9, 0.9, 1.0], 'local_exposure_highlight_contrast_scale': 0.75}}),
    ('XR5_Fog_Pond', 'fog', (-600, 5200, -110), (42, 38, 4), {'radial_fog_extinction': 0.004, 'height_fog_extinction': 0.05, 'height_fog_falloff': 350.0, 'fog_albedo': [0.76, 0.79, 0.82], 'fog_phase_g': 0.2}),
    ('XR5_Fog_Inlet', 'fog', (2300, 7300, -40), (14, 12, 3), {'radial_fog_extinction': 0.01, 'height_fog_extinction': 0.06, 'height_fog_falloff': 300.0, 'fog_albedo': [0.72, 0.77, 0.8], 'fog_phase_g': 0.2}),
]
