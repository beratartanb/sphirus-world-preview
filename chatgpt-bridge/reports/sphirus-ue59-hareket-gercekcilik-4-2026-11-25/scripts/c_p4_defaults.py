# c_p4_defaults.py (control, in memory; re-appliable; runs after every pass-4 compile) - movement pass 4 (2026-11-25).
# builtins.P4P / P4M / P4B override entries for the player / AC_Sph_Motion / ABP_Sph_Body_GASP class defaults (A/B tests).
import unreal as u, builtins
P = {'CS_DecSlope': 900.0, 'CS_SlopeTan': 0.36, 'CS_V5': 1.0, 'CS_StepUp': 25.0,
     'SH_On': 0.0, 'SH_Rest': 0.15, 'SH_MaxFwd': 40.0, 'SH_MinLat': 8.0, 'SH_MaxLat': 45.0, 'SH_In': 10.0, 'SH_Out': 6.0, 'SH_VStill': 6.0,
     'ATH_On': 0.0, 'ATH_K': 0.9, 'ATH_Rel': 300.0, 'ATH_Max': 45.0, 'ATH_Air': 50.0, 'ATH_VMin': 40.0,
     'AW_On': 1.0, 'AW_In': 32.0, 'AW_Out': 45.0, 'AW_Min': 8.0, 'AW_RIn': 5.0, 'AW_ROut': 2.5, 'AW_Arm': 6.0, 'AW_Yaw': 7.0, 'AW_Head': 8.0, 'TR_On': 1.0,
     'PS_AbdBwd': 9.0, 'PS_AbdFwdJog': 4.0, 'PS_AbdRate': 6.0, 'CA_RadP': 0.0, 'CA_Max': 14.0, 'CA_Rise': 80.0}
P.update(getattr(builtins, 'P4P', None) or {})
M = {'AL_Deg': 5.0, 'AL_DegB': 3.0, 'AL_Ref': 700.0, 'AL_RefB': 900.0, 'AL_Rate': 6.0}; M.update(getattr(builtins, 'P4M', None) or {})
c = u.get_default_object(u.load_asset('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player').generated_class())
m = u.get_default_object(u.load_asset('/Game/Sphirus/Player/Motion/AC_Sph_Motion').generated_class())
miss = []
for o, D in ((c, P), (m, M)):
    for k, v in D.items():
        try: o.set_editor_property(k, v)
        except Exception: miss.append(k)
print('P4DEF', {k: c.get_editor_property(k) for k in P if k not in miss}, {k: m.get_editor_property(k) for k in M if k not in miss}, 'missing', miss)
