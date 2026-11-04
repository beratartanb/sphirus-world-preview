import builtins
CM = '/Game/CoreMotion_Retargeted/AAMS/Walk/'
W = dict(a0=1.35, aJ=2.30, b0=0.30, b1=1.7, c_brake=1.2, c_turn=1.2, x_fade=0.3, s_brake=1.7, ang=180.0, v_lead=0.05, v_early=0.1, x_vel=0.6, v_center=0.15, land_reach=46.0, own_tail=0.25, block_t=0.4, v_scale_a=VS255, v_scale_b=0.72, lean_cap=14.0, pelvis_ref=88.0, pelvis_k=0.0)
builtins.G255 = {'dry_run': DRY255, 'clips': [
    dict(W, name='SHM255_Walk_R180', A=CM + 'af_Loco_Walk_Fwd_Stop', B=CM + 'af_Loco_Walk_Start_TurnR180_Rfoot', mirrorA=True, side=1.0),
    dict(W, name='SHM255_Walk_L180', A=CM + 'af_Loco_Walk_Fwd_Stop', B=CM + 'af_Loco_Walk_Start_TurnL180_Lfoot', mirrorA=False, side=-1.0),
]}
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V255_20261104/gen255_turn.py', encoding='utf8').read(), 'gen255_turn.py', 'exec'))
