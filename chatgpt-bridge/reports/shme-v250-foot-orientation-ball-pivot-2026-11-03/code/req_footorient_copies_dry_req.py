import builtins
J = '/Game/GraceRanger/SHME/Animations/Starts/Jog/'; RTG = '/Game/CoreMotion_Retargeted/AAMS/Walk/'
names = ['Bwd_Start', 'Fwd_Start', 'Left_Start', 'Right_Start'] 
clips = {}
for n in names:
    clips[J + 'SHM_JogQ_af_Loco_Jog_%s_AAMS' % n] = RTG + 'af_Loco_Jog_%s' % n
    clips[J + 'SHM232_IS_af_Loco_Jog_%s_AAMS' % n] = RTG + 'af_Loco_Jog_%s' % n
for s in 'LR':
    for d in ('045', '090', '135', '180'):
        clips[J + 'SHM_JogQ_af_Loco_Jog_Start_Turn%s%s_%sfoot_AAMS' % (s, d, s)] = RTG + 'af_Loco_Jog_Start_Turn%s%s_%sfoot' % (s, d, s)
builtins.V250_FO = {'dry': not bool(getattr(builtins, 'V250_FO_WRITE', False)), 'clips': clips}
exec(compile(open(r"C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V250_20261103/fix250_footorient.py", encoding="utf-8").read(), "fix250_footorient.py", "exec"), {"__name__": "__job__"})
