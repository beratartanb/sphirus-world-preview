# probe_light.py (measure): sun / sky / fog / PPV / water read-out for the atmosphere pass -> Saved/UE59Work/r2g/probe_light.txt
import unreal as u
O=[]
def P(*a): O.append(' '.join(str(x) for x in a))
acts=u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors()
def g(o,k):
    try: return o.get_editor_property(k)
    except Exception as e: return 'ERR'
for a in acts:
    cn=a.get_class().get_name(); lb=a.get_actor_label()
    if cn=='DirectionalLight':
        c=a.light_component; P('SUN',lb,a.get_actor_rotation(),{k:g(c,k) for k in ('intensity','light_color','temperature','use_temperature','light_source_angle','light_source_soft_angle','specular_scale','diffuse_scale','indirect_lighting_intensity','volumetric_scattering_intensity','enable_light_shaft_bloom','bloom_scale','bloom_threshold','light_shaft_override_direction','cast_cloud_shadows','atmosphere_sun_light','shadow_amount','dynamic_shadow_distance_movable_light','cascade_distribution_exponent')})
    elif cn=='SkyLight':
        c=a.light_component; P('SKY',lb,{k:g(c,k) for k in ('intensity','light_color','real_time_capture','source_type','indirect_lighting_intensity','volumetric_scattering_intensity','lower_hemisphere_is_black','cubemap','sky_distance_threshold')})
    elif cn=='ExponentialHeightFog':
        c=a.component; P('FOG',lb,a.get_actor_location(),{k:g(c,k) for k in ('fog_density','fog_height_falloff','fog_inscattering_luminance','fog_inscattering_color','directional_inscattering_luminance','directional_inscattering_exponent','directional_inscattering_start_distance','fog_max_opacity','start_distance','enable_volumetric_fog','volumetric_fog_scattering_distribution','volumetric_fog_albedo','volumetric_fog_extinction_scale','volumetric_fog_distance','volumetric_fog_emissive','sky_atmosphere_ambient_contribution_color_scale')})
    elif cn=='SkyAtmosphere':
        c=a.get_component_by_class(u.SkyAtmosphereComponent); P('ATMO',lb,{k:g(c,k) for k in ('rayleigh_scattering_scale','mie_scattering_scale','mie_absorption_scale','multi_scattering_factor','aerial_pespective_view_distance_scale','height_fog_contribution','sky_luminance_factor')})
    elif cn=='LocalFogVolume':
        c=a.get_component_by_class(u.LocalFogVolumeComponent); P('LFV',lb,a.get_actor_location(),a.get_actor_scale3d(),'hid',a.is_hidden_ed(),{k:g(c,k) for k in ('radial_fog_extinction','height_fog_extinction','height_fog_falloff','height_fog_offset','fog_phase_g','fog_albedo','fog_emissive','visible')})
    elif cn=='PostProcessVolume':
        s=a.settings; ov=[n for n in dir(s) if n.startswith('override_') and g(s,n)==True]
        P('PPV',lb,'unbound',g(a,'unbound'),'enabled',g(a,'enabled'),'prio',g(a,'priority'),'blendw',g(a,'blend_weight'),'radius',g(a,'blend_radius'),a.get_actor_location(),a.get_actor_scale3d())
        P('   OV',{n[9:]:g(s,n[9:]) for n in ov if not n[9:].startswith('weighted')})
        try: P('   BLENDABLES',[ (w.object.get_path_name() if w.object else None, w.weight) for w in s.weighted_blendables.array])
        except Exception as e: P('   BL_ERR',e)
    elif cn in ('RectLight','PointLight') and lb.startswith('ReviewOnly'):
        c=a.light_component; P('REVIEW',lb,{k:g(c,k) for k in ('intensity','visible','cast_shadows','source_width','source_height','attenuation_radius','affects_world')},'hid',a.is_hidden_ed())
# water: static mesh actors whose material name mentions water
for a in acts:
    if a.get_class().get_name()!='StaticMeshActor': continue
    c=a.static_mesh_component
    try: ms=c.get_materials()
    except Exception: continue
    for m in ms:
        if m and any(k in m.get_name().lower() for k in ('water','pond','lake')):
            P('WATER',a.get_actor_label(),a.get_actor_location(),a.get_actor_scale3d(),'mesh',c.static_mesh.get_name() if c.static_mesh else None,'mat',m.get_path_name(),'class',m.get_class().get_name())
            if isinstance(m,u.MaterialInstance):
                P('   PARENT',m.get_editor_property('parent').get_path_name() if m.get_editor_property('parent') else None)
                P('   SCALARS',{str(p.parameter_info.name):round(p.parameter_value,4) for p in m.get_editor_property('scalar_parameter_values')})
                P('   VECTORS',{str(p.parameter_info.name):(round(p.parameter_value.r,3),round(p.parameter_value.g,3),round(p.parameter_value.b,3),round(p.parameter_value.a,3)) for p in m.get_editor_property('vector_parameter_values')})
            break
open(u.Paths.project_dir()+'Saved/UE59Work/r2g/probe_light.txt','w',encoding='utf8').write('\n'.join(O)); print('PROBE_LIGHT',len(O))
