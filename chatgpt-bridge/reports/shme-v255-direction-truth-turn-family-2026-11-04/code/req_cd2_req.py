import builtins
CM = '/Game/CoreMotion_Retargeted/AAMS/Walk/'
WK = '/Game/AAMS/AAMS/Animations/Locomotion/Walk/M_Neutral_Walk_'
builtins.CD255 = {'clips': [CM + 'af_Loco_%s_Start_Turn%s%s_%sfoot' % (g, s, a, s) for g in ('Run', 'Jog', 'Walk') for s in 'RL' for a in ('090', '135', '180')]
                  + [WK + 'Turn_%s_%s_%sfoot' % (s, a, f) for s in 'RL' for a in ('090', '180') for f in 'RL'] + [CM + 'af_Loco_Jog_Fwd', CM + 'af_Loco_Walk_Fwd', CM + 'af_Loco_Jog_Fwd_Stop', CM + 'af_Loco_Walk_Fwd_Stop', CM + 'af_Stand_Idle_TurnR180']}
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V255_20261104/clipdump255.py', encoding='utf8').read(), 'clipdump255.py', 'exec'))
