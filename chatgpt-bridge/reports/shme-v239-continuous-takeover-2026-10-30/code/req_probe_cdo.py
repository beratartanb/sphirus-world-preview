import unreal as u
for ap in ('/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase', '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatching'):
    b = u.load_asset(ap); c = u.get_default_object(b.generated_class())
    print('CDO', ap.rsplit('/', 1)[-1], [(k, str(c.get_editor_property(k))[-40:]) for k in ('SHM239_DB_Back', 'SHM239_DB_Opp', 'SHM239_Own')])
d = u.load_asset('/Game/GraceRanger/SHME/Animations/V239/PSD_SHM239_Tk_Opp'); print('OPPDB', d, d.get_num_animation_assets() if d else None)
