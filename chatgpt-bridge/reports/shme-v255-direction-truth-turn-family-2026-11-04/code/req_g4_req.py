import builtins
CM = '/Game/CoreMotion_Retargeted/AAMS/Walk/'
SC = dict(knee_align=0.8, swing_clear=8.0, arm_k=0.75, lean_cap=18.0, pelvis_k=0.5, pelvis_ref=86.0, v_floor=220.0, a0=0.15, aJ=0.88, b0=0.12, b1=1.5, c_brake=1.25, c_turn=1.1, x_fade=0.24, s_brake=0.3, ang=90.0, v_lead=0.0, x_vel=1.1, v_center=0.1, land_reach=40.0, own_tail=0.25, block_t=0.45)
JC = dict(knee_align=0.8, swing_clear=7.0, arm_k=0.3, v_floor=150.0, a0=0.2, aJ=0.67, b0=0.18, b1=1.7, c_brake=1.15, c_turn=1.25, x_fade=0.24, s_brake=0.45, ang=90.0, v_lead=0.0, x_vel=0.85, v_center=0.1, land_reach=34.0, own_tail=0.25, block_t=0.45, v_scale_a=0.85, lean_cap=18.0, pelvis_ref=86.0, pelvis_k=0.3)
builtins.G255 = {'dry_run': DRY255, 'clips': [
    dict(SC, name='SHM255_Sprint_R090', A=CM + 'af_Loco_Run_Fwd_Stop', B=CM + 'af_Loco_Run_Start_TurnR090_Rfoot', mirrorA=True, side=1.0),
    dict(SC, name='SHM255_Sprint_L090', A=CM + 'af_Loco_Run_Fwd_Stop', B=CM + 'af_Loco_Run_Start_TurnL090_Lfoot', mirrorA=False, side=-1.0),
    dict(JC, name='SHM255_Jog_R090', A=CM + 'af_Loco_Jog_Fwd_Stop', B=CM + 'af_Loco_Jog_Start_TurnR090_Rfoot', mirrorA=False, side=1.0),
    dict(JC, b0=0.25, name='SHM255_Jog_L090', A=CM + 'af_Loco_Jog_Fwd_Stop', B=CM + 'af_Loco_Jog_Start_TurnL090_Lfoot', mirrorA=True, side=-1.0),
]}
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V255_20261104/gen255_turn.py', encoding='utf8').read(), 'gen255_turn.py', 'exec'))
