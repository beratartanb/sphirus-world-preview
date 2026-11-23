# apply_light.py: the lighting change set of this pass, idempotent. Used in memory for candidates (control) and by the gated write job.
# builtins.R2G_LIGHT may override keys of CFG. Touches: EX_PostRain_Sun, EX_PostRain_Sky, EX_Pond_CalmSurface (L_GR_SphirusHouse),
# interior lamps (L_GR_CurrentHouseContent), and creates/updates EX_Look_PPV_Interior (duplicate of EX_Look_PPV_House, L_GR_SphirusHouse).
import unreal as u, builtins
CFG={'sun_rot':(-30.0,-60.0,0.0),'sun_int':900.0,'sun_angle':2.5,'sky_int':2.8,'water_off_sun':True,
     'lamp_temp':3600.0,'lamp_mul':0.8,'lamp_indirect':1.3,
     'int_ppv':True,'int_bias':0.35,'int_wb':5300.0,'int_center':(760.0,570.0,580.0),'int_half':(748.0,558.0,440.0),'int_blend':90.0}
CFG.update(getattr(builtins,'R2G_LIGHT',None) or {})
LAMPS={'LivingLamp':252,'KitchenPendant':275,'WorkshopPendant':237.5,'HallSconce':240,'LivingPendantLight':300,'R05_LivingFloorLampLight':187.5,'R05_MainStairWallLampLight':330,'LowerWCLight':180,'LowerStoreLight':132,'ReadingLamp':107.5,'BathLamp':300,'R05_BedsideLampRightLight':270,'AtticServiceLight':275}
EAS=u.get_editor_subsystem(u.EditorActorSubsystem)
acts={a.get_actor_label():a for a in EAS.get_all_level_actors()}
def P(*a): print('LIGHT',*a)
s=acts['EX_PostRain_Sun']; s.set_actor_rotation(u.Rotator(pitch=CFG['sun_rot'][0],yaw=CFG['sun_rot'][1],roll=0),False)
c=s.light_component; c.set_editor_property('intensity',CFG['sun_int']); c.set_editor_property('light_source_angle',CFG['sun_angle'])
k=acts['EX_PostRain_Sky'].light_component; k.set_editor_property('intensity',CFG['sky_int'])
w=acts['EX_Pond_CalmSurface'].static_mesh_component
w.set_editor_property('lighting_channels',u.LightingChannels(channel0=not CFG['water_off_sun'],channel1=bool(CFG['water_off_sun']),channel2=False))
for lb,base in LAMPS.items():
    lc=acts[lb].light_component; lc.set_editor_property('temperature',CFG['lamp_temp']); lc.set_editor_property('intensity',round(base*CFG['lamp_mul'],1)); lc.set_editor_property('indirect_lighting_intensity',CFG['lamp_indirect'])
p=acts.get('EX_Look_PPV_Interior')
if CFG['int_ppv']:
    src=acts['EX_Look_PPV_House']
    if not p:
        p=EAS.duplicate_actor(src); p.set_actor_label('EX_Look_PPV_Interior'); p.set_folder_path('EX_PostRain_Look')
    o,e=src.get_actor_bounds(False); sc=src.get_actor_scale3d()
    ux,uy,uz=e.x/sc.x,e.y/sc.y,e.z/sc.z   # half extent of the brush at scale 1
    p.set_actor_location(u.Vector(*CFG['int_center']),False,False)
    p.set_actor_scale3d(u.Vector(CFG['int_half'][0]/ux,CFG['int_half'][1]/uy,CFG['int_half'][2]/uz))
    p.set_editor_property('unbound',False); p.set_editor_property('priority',2.5); p.set_editor_property('blend_radius',CFG['int_blend']); p.set_editor_property('enabled',True)
    st=p.settings
    st.set_editor_property('override_auto_exposure_bias',True); st.set_editor_property('auto_exposure_bias',CFG['int_bias'])
    st.set_editor_property('override_white_temp',True); st.set_editor_property('white_temp',CFG['int_wb'])
    p.set_editor_property('settings',st)
    o2,e2=p.get_actor_bounds(False); P('INT_PPV bounds',(round(o2.x),round(o2.y),round(o2.z)),(round(e2.x),round(e2.y),round(e2.z)),'lvl',p.get_outer().get_outermost().get_name().split('/')[-1])
elif p:
    EAS.destroy_actor(p); P('INT_PPV removed')
r=s.get_actor_rotation(); P('SUN',round(r.pitch,1),round(r.yaw,1),c.intensity,c.light_source_angle,'SKY',k.intensity,'WATERCH',w.get_editor_property('lighting_channels').channel0,'LAMP',acts['KitchenPendant'].light_component.temperature,acts['KitchenPendant'].light_component.intensity)
