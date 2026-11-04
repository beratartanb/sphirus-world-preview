import builtins
CM = '/Game/CoreMotion_Retargeted/AAMS/Walk/'
S = dict(knee_align=0.8, swing_clear=8.0, arm_k=0.75, lean_cap=18.0, pelvis_k=0.5, pelvis_ref=86.0, a0=0.28, aJ=1.20, b0=0.25, b1=1.6, c_brake=1.3, c_turn=1.1, x_fade=0.28, s_brake=0.45, ang=180.0, v_lead=0.08, v_early=0.2, x_vel=0.75, v_center=0.2, land_reach=38.0, own_tail=0.25, block_t=0.27)
J = dict(knee_align=0.8, swing_clear=7.0, arm_k=0.3, a0=0.3, aJ=1.03, b0=0.35, b1=1.7, c_brake=1.15, c_turn=1.35, x_fade=0.26, s_brake=0.45, ang=180.0, v_lead=0.06, v_early=0.15, x_vel=0.65, v_center=0.18, land_reach=34.0, own_tail=0.25, block_t=0.42, v_scale_a=0.85, lean_cap=16.0, pelvis_ref=86.0, pelvis_k=0.3)
builtins.G255 = {'dry_run': DRY255, 'clips': [
    dict(S, name='SHM255_Sprint_R180', A=CM + 'af_Loco_Run_Fwd_Stop', B=CM + 'af_Loco_Run_Start_TurnR180_Rfoot', mirrorA=False, side=1.0),
    dict(S, name='SHM255_Sprint_L180', A=CM + 'af_Loco_Run_Fwd_Stop', B=CM + 'af_Loco_Run_Start_TurnL180_Lfoot', mirrorA=True, side=-1.0),
    dict(J, name='SHM255_Jog_R180', A=CM + 'af_Loco_Jog_Fwd_Stop', B=CM + 'af_Loco_Jog_Start_TurnR180_Rfoot', mirrorA=True, side=1.0),
    dict(J, name='SHM255_Jog_L180', A=CM + 'af_Loco_Jog_Fwd_Stop', B=CM + 'af_Loco_Jog_Start_TurnL180_Lfoot', mirrorA=False, side=-1.0),
]}
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V255_20261104/gen255_turn.py', encoding='utf8').read(), 'gen255_turn.py', 'exec'))
