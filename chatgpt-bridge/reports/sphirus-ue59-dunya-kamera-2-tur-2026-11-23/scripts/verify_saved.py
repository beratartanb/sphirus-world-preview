# verify_saved.py (measure, read-only): readback of this pass's saved values from the reopened editor -> Saved/UE59Work/r2g2/verify_saved.txt
import unreal as u
O=[]
acts={a.get_actor_label():a for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors()}
s=acts['EX_PostRain_Sun']; r=s.get_actor_rotation(); c=s.light_component
O.append('SUN pitch %.1f yaw %.1f intensity %.0f source_angle %.2f specular %.2f'%(r.pitch,r.yaw,c.intensity,c.light_source_angle,c.specular_scale))
O.append('SKY intensity %.2f'%acts['EX_PostRain_Sky'].light_component.intensity)
lc=acts['EX_Pond_CalmSurface'].static_mesh_component.get_editor_property('lighting_channels'); O.append('WATER channels %s %s %s'%(lc.channel0,lc.channel1,lc.channel2))
for lb in ('KitchenPendant','LivingPendantLight','WorkshopPendant','HearthGlow'):
    l=acts[lb].light_component; O.append('LAMP %s temp %.0f int %.1f indirect %.2f'%(lb,l.temperature,l.intensity,l.indirect_lighting_intensity))
p=acts.get('EX_Look_PPV_Interior')
if p:
    o,e=p.get_actor_bounds(False); st=p.settings; O.append('INT_PPV bounds c(%d %d %d) e(%d %d %d) bias %.2f wb %.0f prio %.1f blend %.0f unbound %s lvl %s'%(o.x,o.y,o.z,e.x,e.y,e.z,st.auto_exposure_bias,st.white_temp,p.priority,p.blend_radius,p.unbound,p.get_outer().get_outermost().get_name().split('/')[-1]))
else: O.append('INT_PPV MISSING')
a=u.load_asset('/Game/Sphirus/Player/Camera/AC_Sph_Camera'); d=u.get_default_object(a.generated_class())
O.append('CAM '+' '.join('%s=%.2f'%(k,d.get_editor_property(k)) for k in ('HeadX','HeadXTight','HeadY','OutD','OutDTight','HomeD','HomeDTight','TightRaise','YKeep')))
for lb in sorted(acts):
    if lb.startswith('R2G_'):
        x=acts[lb]; l=x.get_actor_location(); O.append('NEW %s | %s | %d %d %d | lvl %s'%(lb,x.get_class().get_name(),l.x,l.y,l.z,x.get_outer().get_outermost().get_name().split('/')[-1]))
S=u.EditorLoadingAndSavingUtils; O.append('DIRTY %s %s'%([p.get_name() for p in S.get_dirty_map_packages()],[p.get_name() for p in S.get_dirty_content_packages()]))
open(u.Paths.project_dir()+'Saved/UE59Work/r2g2/verify_saved.txt','w',encoding='utf8').write('\n'.join(O)); print('VERIFY',len(O))
