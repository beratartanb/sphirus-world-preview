import unreal as u
for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors():
    if isinstance(a, (u.RectLight, u.PointLight, u.DirectionalLight, u.SkyLight)):
        c = a.light_component; l = a.get_actor_location(); r = a.get_actor_rotation()
        ex = ''
        if isinstance(a, u.RectLight): ex = 'src %dx%d barn %s' % (c.source_width, c.source_height, round(c.barn_door_angle))
        print('LG %-34s %-9s int %9.1f units %-12s att %6.0f vis %s hidden_game %s affects %s shadows %s temp %s col %s at %s rot %s %s' % (a.get_actor_label()[:34], a.get_class().get_name()[:9], c.intensity,
              str(getattr(c, 'intensity_units', '')).split('.')[-1][:12], getattr(c, 'attenuation_radius', 0), c.get_editor_property('visible'), a.is_hidden_ed() if hasattr(a, 'is_hidden_ed') else '?', c.get_editor_property('affects_world'), c.cast_shadows,
              (round(c.temperature) if getattr(c, 'use_temperature', False) else '-'), (c.light_color.r, c.light_color.g, c.light_color.b), [round(l.x), round(l.y), round(l.z)], [round(r.pitch), round(r.yaw)], ex))
