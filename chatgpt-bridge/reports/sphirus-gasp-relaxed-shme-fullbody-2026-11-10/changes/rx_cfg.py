# rx_cfg.py (exec'd in a PIE prelude after the pawn exists, PW = player pawn): apply a locomotion candidate to the live pawn.
#   rxcfg(1) = GASP Relaxed family + Relaxed clip speeds + physical brake + relaxed idle breaks;  rxcfg(0) = production values.
def rxcfg(on,speeds=None):
    N=u.PropertyAccessChangeNotifyMode.NEVER
    ai=PW.get_editor_property('mesh').get_anim_instance(); ai.set_editor_property('SphRelaxed',bool(on),N)
    sp=speeds or ({'WalkSpeeds':(165,165,165),'RunSpeeds':(375,375,375),'SprintSpeeds':(585,585,585)} if on else {'WalkSpeeds':(200,180,150),'RunSpeeds':(500,350,300),'SprintSpeeds':(700,700,700)})
    for k,v in sp.items(): PW.set_editor_property(k,u.Vector(*v),N)
    c=[x for x in PW.get_components_by_class(u.ActorComponent) if x.get_name()=='SphMotion'][0]
    if on:
        try:
            for i,n in enumerate((1,2,3,5,7)): c.set_editor_property('Idle%d'%i,u.load_asset('/Game/Characters/UEFN_Mannequin/Animations/Idle/M_Relaxed_Stand_Idle_Break_v0%d'%n),N)
        except Exception as e: print('RXCFG idle clips not set',str(e)[:80])
    print('RXCFG',on,ai.get_editor_property('SphRelaxed'),PW.get_editor_property('RunSpeeds'))
