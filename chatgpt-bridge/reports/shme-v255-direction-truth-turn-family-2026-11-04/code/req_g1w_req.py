import builtins
CM = '/Game/CoreMotion_Retargeted/AAMS/Walk/'
K = dict(a0=0.0, aJ=1.20, b0=0.25, b1=1.6, c_brake=1.3, c_turn=1.1, x_fade=0.28, s_brake=0.45, ang=180.0, v_lead=0.12, x_vel=0.4, v_center=0.12, land_reach=38.0)
builtins.G255 = {'dry_run': False, 'block_t': 0.5, 'clips': [
    dict(K, name='SHM255_Sprint_R180', A=CM + 'af_Loco_Run_Fwd_Stop', B=CM + 'af_Loco_Run_Start_TurnR180_Rfoot', mirrorA=False, side=1.0),
    dict(K, name='SHM255_Sprint_L180', A=CM + 'af_Loco_Run_Fwd_Stop', B=CM + 'af_Loco_Run_Start_TurnL180_Lfoot', mirrorA=True, side=-1.0),
]}
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V255_20261104/gen255_turn.py', encoding='utf8').read(), 'gen255_turn.py', 'exec'))
