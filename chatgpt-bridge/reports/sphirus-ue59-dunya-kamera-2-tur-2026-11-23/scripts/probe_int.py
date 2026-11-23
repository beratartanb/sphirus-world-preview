# probe_int.py (measure, read-only): interior lights, emissive lamp meshes and the levels that own light/atmosphere actors.
import unreal as u
O=[]
for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors():
    cn=a.get_class().get_name(); lb=a.get_actor_label(); lv=a.get_outer().get_outermost().get_name().split('/')[-1]
    if cn in ('PointLight','SpotLight','RectLight'):
        c=a.light_component; l=a.get_actor_location()
        if lb.startswith('ReviewOnly'): continue
        O.append('LIGHT %s | %s | lvl %s | loc %d %d %d | int %.1f units %s | temp %s use %s | col %s | rad %.0f | shadows %s | vis %s | srcR %.0f | indirect %.2f | vol %.2f'%(cn,lb,lv,l.x,l.y,l.z,c.intensity,str(c.get_editor_property('intensity_units')).split('.')[-1] if cn!='DirectionalLight' else '',c.temperature,c.use_temperature,(c.light_color.r,c.light_color.g,c.light_color.b),c.attenuation_radius,c.cast_shadows,c.is_visible(),getattr(c,'source_radius',0) if cn=='PointLight' else 0,c.indirect_lighting_intensity,c.volumetric_scattering_intensity))
    if cn in ('DirectionalLight','SkyLight','ExponentialHeightFog','SkyAtmosphere','PostProcessVolume','LocalFogVolume') or lb=='EX_Pond_CalmSurface':
        O.append('OWNER %s | %s | lvl %s'%(cn,lb,lv))
    if cn=='PostProcessVolume' and lb in ('EX_Look_PPV_House','EX_PostRain_NeutralExposure'):
        s=a.settings
        for k in ('white_temp','white_tint','auto_exposure_bias','auto_exposure_min_brightness','auto_exposure_max_brightness','color_saturation','color_gain','color_gamma','film_slope','film_toe','lumen_final_gather_quality','lumen_scene_lighting_quality','indirect_lighting_intensity','indirect_lighting_color','local_exposure_highlight_contrast_scale','local_exposure_shadow_contrast_scale','local_exposure_method'):
            try: O.append('  PP %s %s = %s (ov %s)'%(lb,k,s.get_editor_property(k),s.get_editor_property('override_'+k)))
            except Exception as e: O.append('  PP_ERR %s %s'%(k,repr(e)[:80]))
open(u.Paths.project_dir()+'Saved/UE59Work/r2g2/probe_int.txt','w',encoding='utf8').write('\n'.join(O)); print('PROBE',len(O))
