# c_fireview.py (control, editor world, nothing saved): place the editor viewport in front of the hearth, print fire actor state.
import unreal as u, builtins
ue=u.get_editor_subsystem(u.UnrealEditorSubsystem); cam=getattr(builtins,'FV_CAM',(1330.0,905.0,215.0,-8.0,0.0))
ue.set_level_viewport_camera_info(u.Vector(cam[0],cam[1],cam[2]),u.Rotator(0.0,cam[3],cam[4]))
for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors():
    l=a.get_actor_label()
    if l.startswith('GR_Day_FireFX') or l in ('GR_Day_Flame','GR_Day_FireSmoke','GR_Day_FireLight','HearthGlow','GR_DayHub'):
        if l=='GR_DayHub':
            print('HUB FireOn',[x.get_actor_label() if x else None for x in a.get_editor_property('GR_FireOn')],'Laid',[x.get_actor_label() if x else None for x in a.get_editor_property('GR_FireLaid')]); continue
        for c in a.get_components_by_class(u.NiagaraComponent):
            s=c.get_asset(); print('FX',l,s.get_path_name() if s else None,'auto',c.get_editor_property('auto_activate'),'scale',a.get_actor_scale3d().x)
        for c in a.get_components_by_class(u.PointLightComponent): print('LIGHT',l,c.intensity,c.get_editor_property('intensity_units'),'radius',c.attenuation_radius,'color',c.get_light_color().to_tuple(),'temp',c.temperature,c.use_temperature)
        for c in a.get_components_by_class(u.StaticMeshComponent): print('MESH',l,c.static_mesh.get_name() if c.static_mesh else None,[m.get_name() if m else None for m in c.get_materials()])
