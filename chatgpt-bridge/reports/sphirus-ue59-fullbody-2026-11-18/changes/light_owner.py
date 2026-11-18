# light_owner.py (read-only, PIE): every owner of the image at the player's spot - post process volumes (all overridden fields,
# bound/unbound, inside or not), camera components with post-process weight (player / view target / Black Eye cameras),
# directional / sky / local lights near the player, exposure-related cvars. -> Saved/UE59Work/probe/light_owner_<tag>.txt
import unreal as u, builtins
W = u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world()
pc = u.GameplayStatics.get_player_controller(W, 0); P = pc.get_controlled_pawn(); L = P.get_actor_location()
o = ['PAWN %s %s  view_target=%s' % (P.get_name(), L, pc.get_view_target().get_name())]
cm = u.GameplayStatics.get_player_camera_manager(W, 0); o.append('CAMMGR %s loc %s fov %.1f' % (cm.get_class().get_name(), cm.get_camera_location(), cm.get_fov_angle()))
def ovs(s):
    r = []
    for n in dir(s):
        if n.startswith('override_'):
            try:
                if s.get_editor_property(n): k = n[len('override_'):]; r.append('%s=%s' % (k, s.get_editor_property(k)))
            except Exception: pass
    return r
for v in u.GameplayStatics.get_all_actors_of_class(W, u.PostProcessVolume):
    s = v.get_editor_property('settings')
    inside = None
    try:
        b = v.get_components_bounding_box(True) if hasattr(v, 'get_components_bounding_box') else None
    except Exception: b = None
    try:
        org, ext = v.get_actor_bounds(False); inside = all(abs(getattr(L, a) - getattr(org, a)) <= getattr(ext, a) for a in 'xyz')
    except Exception: pass
    o.append('PPV %s label=%s unbound=%s enabled=%s prio=%s weight=%s blend_radius=%s inside_bounds=%s' % (v.get_name(), v.get_actor_label() if hasattr(v, 'get_actor_label') else '', v.get_editor_property('unbound'), v.get_editor_property('enabled'), v.get_editor_property('priority'), v.get_editor_property('blend_weight'), v.get_editor_property('blend_radius'), inside))
    for x in ovs(s): o.append('    ' + x[:200])
for a in [P, pc.get_view_target()] + list(u.GameplayStatics.get_all_actors_of_class(W, u.CameraActor)):
    for c in a.get_components_by_class(u.CameraComponent):
        try:
            o.append('CAMCOMP %s.%s active=%s pp_weight=%s' % (a.get_name(), c.get_name(), c.is_active(), c.get_editor_property('post_process_blend_weight')))
            for x in ovs(c.get_editor_property('post_process_settings')): o.append('    ' + x[:200])
        except Exception as e: o.append('CAMCOMP ERR %s' % e)
for a in u.GameplayStatics.get_all_actors_of_class(W, u.Actor):
    n = a.get_class().get_name()
    if 'BlackEye' in n or 'Camera_Ranger' in n or 'PCM_Ranger' in n: o.append('BLACKEYE_ACTOR %s [%s]' % (a.get_name(), n))
for a in u.GameplayStatics.get_all_actors_of_class(W, u.Actor):
    for c in a.get_components_by_class(u.LightComponentBase):
        isdir = isinstance(c, (u.DirectionalLightComponent, u.SkyLightComponent))
        try: d = (c.get_world_location() - L).length()
        except Exception: d = -1
        if isdir or d < 1200:
            r = []
            for n in ('intensity', 'light_color', 'temperature', 'use_temperature', 'cast_shadows', 'indirect_lighting_intensity', 'specular_scale', 'source_angle', 'source_radius', 'attenuation_radius', 'intensity_units', 'light_source_angle', 'atmosphere_sun_light'):
                try: r.append('%s=%s' % (n, c.get_editor_property(n)))
                except Exception: pass
            o.append('LIGHT %s.%s [%s] d=%.0f vis=%s rot=%s | %s' % (a.get_name(), c.get_name(), c.get_class().get_name(), d, c.is_visible(), a.get_actor_rotation() if isdir else '', ' '.join(r)))
for cv in ('r.DefaultFeature.AutoExposure', 'r.DefaultFeature.AutoExposure.Method', 'r.DefaultFeature.AutoExposure.ExtendDefaultLuminanceRange', 'r.EyeAdaptation.ExponentialTransitionDistance', 'r.LocalExposure', 'r.Tonemapper.Quality', 'r.TonemapperFilm', 'r.Lumen.DiffuseIndirect.Allow', 'r.DynamicGlobalIlluminationMethod'):
    try: o.append('CVAR %s = %s' % (cv, u.SystemLibrary.get_console_variable_float_value(cv)))
    except Exception as e: o.append('CVAR %s ?' % cv)
tag = getattr(builtins, 'LO_TAG', 'x')
open(u.Paths.project_dir() + 'Saved/UE59Work/probe/light_owner_%s.txt' % tag, 'w', encoding='utf8').write('\n'.join(o)); print('LIGHTOWNER', tag, len(o))
