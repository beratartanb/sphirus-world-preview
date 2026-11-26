# c_p5_defaults.py (control, in memory; re-appliable; runs after every pass-5 compile): pass-5 player values on top of pass 4.
# Shoulder girdle: target shoulder height PS_ShL 5.7 -> 6.9 cm and forward offset PS_ShF -0.7 -> -1.6 cm (more level, slightly open
# shoulders on the B5 body; the clavicle feedback owner is unchanged). builtins.P5P overrides entries.
import unreal as u, builtins
exec(open(u.Paths.project_dir() + 'Tools/UE59_20261125/c_p4_defaults.py', encoding='utf8').read())
P5 = {'PS_ShL': 6.9, 'PS_ShF': -1.6, 'TR_PkDecay': 450.0, 'PS_B3': -5.0,
      # region impact (m_impact*_mcp): physics blend peak, fade time, PhysicalAnimation motor strengths, capsule push (0 = none)
      'IMP_W0': 0.85, 'IMP_Dur': 0.6, 'IMP_OS': 250.0, 'IMP_AVS': 25.0, 'IMP_Push': 0.0, 'IMP_FatK': 0.5,
      # physical fall + face-down get-up (m_fall_mcp): tone, settle test, roll-over impulse, get-up length (clip 8 s - blend-out)
      'FL_TryMax': 4.0, 'FL_Len': 7.6, 'FL_Fade': 0.75, 'FL_StillV': 25.0, 'FL_TMax': 4.0, 'FL_OS': 1800.0, 'FL_AVS': 180.0, 'FL_Roll': 280.0, 'FL_LandV': -1100.0, 'FL_LandK': 250.0,
      # active ragdoll (m_fall4_mcp): joint-space motors toward protective / on-ground poses, fatigue weakens, severity -> time down
      'FL_FatK': 0.55, 'FL_VelK': 1.0, 'FL_SevV': 900.0, 'FL_DazeK': 1.2, 'FL_GndT': 0.8, 'FL_GndK': 0.35, 'FL_ImpMin': 600.0, 'FL_ImpK': 0.45, 'FL_ProneMin': 0.0, 'FL_RollW': 260.0, 'FL_RollK': 0.15}; P5.update(getattr(builtins, 'P5P', None) or {})
c = u.get_default_object(u.load_asset('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player').generated_class())
for k, v in P5.items(): c.set_editor_property(k, v)
print('P5DEF', {k: c.get_editor_property(k) for k in P5})
