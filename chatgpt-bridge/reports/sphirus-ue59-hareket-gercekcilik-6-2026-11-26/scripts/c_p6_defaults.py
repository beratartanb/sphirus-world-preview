# c_p6_defaults.py (control, in memory; re-appliable): pass-6 player values on top of pass 5. builtins.P6P overrides entries.
# Arms: relaxed abduction target 4 deg (spine frame), servo floor -24 (was a hard -14), arm-thigh clearance with the measured B13 thigh
# radius (9.3 cm at the hip -> 6.0 cm at the knee incl. shorts), 2 cm target gap, clearance fades 6 deg/s (was 1 deg/s: arms stayed open
# for up to 14 s after walking).
import unreal as u, builtins
exec(open(u.Paths.project_dir() + 'Tools/UE59_20261126/c_p5_defaults.py', encoding='utf8').read())
P6 = {'PS_AbdBase': 4.0, 'PS_DAMin': -24.0, 'CA_Rad0': 9.3, 'CA_Rad1': 6.0, 'CA_Tgt': 2.0, 'CA_Fall': 6.0,
      # real contact -> region reaction (m_contact6/7): thresholds, cooldown, side widths, gain, cap, step push, obstacle probe reach
      'RC_On': 1.0, 'RC_VMin': 120.0, 'RC_Cool': 0.5, 'RC_ShW': 11.0, 'RC_ArmW': 17.0, 'RC_K': 1.0, 'RC_Max': 650.0, 'RC_VStep': 280.0, 'RC_PushK': 0.35, 'RC_Reach': 45.0,
      # ledge catch / hang / climb (m_ledge6): reach, probe height, max snap, braced hand offsets (clip: hands 52 above capsule centre, 36 out from the wall)
      'LG_On': 1.0, 'LG_Reach': 65.0, 'LG_Up': 80.0, 'LG_Snap': 45.0, 'LG_HandUp': 52.0, 'LG_HandBack': 36.0,
      # falls (m_fall8): ground phase from pelvis/chest floor contact, time only as fallback; 6 alternating roll attempts
      'FL_GndMax': 1.6, 'FL_TryMax': 6.0,
      # knock-down by a real contact (m_contact13): normal relative speed above RC_FallV -> whole-body hit -> fall
      'RC_FallV': 700.0, 'RC_FallMax': 1600.0,
      # contact strength from the hit impulse (m_contact14): body mass for |NormalImpulse| -> velocity change
      'RC_Mass': 60.0,
      # get-up hand-over (m_fall10): montage blend from the held lying pose into the get-up clip
      'FL_GuBlend': 0.1}
P6.update(getattr(builtins, 'P6P', None) or {})
c = u.get_default_object(u.load_asset('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player').generated_class())
for k, v in P6.items(): c.set_editor_property(k, v)
print('P6DEF', {k: c.get_editor_property(k) for k in P6})
