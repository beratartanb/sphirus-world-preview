import unreal as u
o=[]; F=u.Vector(1405,905,205)
for a in u.EditorLevelLibrary.get_all_level_actors():
    l=a.get_actor_location()
    if ((l.x-F.x)**2+(l.y-F.y)**2)**0.5>330 or abs(l.z-F.z)>260: continue
    for c in a.get_components_by_class(u.LightComponent):
        e={}
        for k in ('intensity','attenuation_radius','source_radius','soft_source_radius','intensity_units','light_color','temperature','use_temperature','cast_shadows','volumetric_scattering_intensity','indirect_lighting_intensity','specular_scale'):
            try: e[k]=str(c.get_editor_property(k))[:46]
            except Exception: pass
        o.append('%s | %s | loc (%.0f,%.0f,%.0f) vis %s hidden %s | %s'%(a.get_actor_label(),c.get_class().get_name(),l.x,l.y,l.z,c.is_visible(),a.is_hidden_ed(),e))
    if 'Fire' in a.get_actor_label() or 'Ember' in a.get_actor_label():
        if not a.get_components_by_class(u.LightComponent): o.append('%s | %s | loc (%.0f,%.0f,%.0f) hidden %s'%(a.get_actor_label(),a.get_class().get_name(),l.x,l.y,l.z,a.is_hidden_ed()))
print('FIRELIGHTS\n'+'\n'.join(o))
