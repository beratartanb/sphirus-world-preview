"""showcase_cap.py (measure job): reference captures inside the loaded Pine Forest Pack showcase map with a transient CameraActor
(editor render, 1920x1080, no PIE). Spots = every CameraActor/CineCameraActor of the map (their own pose), every PlayerStart (4 yaws at
eye height 170 cm) and builtins.PFR_SPOTS [[x, y, yaw, pitch, name], ...] (eye height 170 cm above the traced ground).
Lighting variants: builtins.PFR_LIGHT_LEVELS = [sublevel package names]; for each, only that sublevel is made visible and the PlayerStart
set is captured again (<name>__<variant>.png). Everything is restored (sublevel visibility, camera destroyed). Nothing is saved.
Output: Saved/Codex/PineForestRedesign_20261104/ref/showcase/<name>.png + cap_log.json + cap_done"""
import unreal as u, json, pathlib, time, builtins, math

D = pathlib.Path(u.Paths.project_dir()) / 'Saved/Codex/PineForestRedesign_20261104/ref/showcase'; D.mkdir(parents=True, exist_ok=True)
E = u.get_editor_subsystem(u.UnrealEditorSubsystem); assert E.get_game_world() is None, 'PIE running'
w = E.get_editor_world(); assert 'PineForestPack' in w.get_path_name(), w.get_path_name()
A = u.get_editor_subsystem(u.EditorActorSubsystem); acts = A.get_all_level_actors()
ifa = [a for a in acts if isinstance(a, u.InstancedFoliageActor)]


def ground(x, y):
    hs = u.SystemLibrary.line_trace_multi(w, u.Vector(x, y, 20000), u.Vector(x, y, -20000), u.TraceTypeQuery.TRACE_TYPE_QUERY1, False, ifa, u.DrawDebugTrace.NONE, True)
    for h in (hs or []):
        t = h.to_tuple()
        if t[0] and (isinstance(t[9], u.Landscape) or isinstance(t[9], u.StaticMeshActor)):
            return t[4].z
    return None


plan = []
for a in acts:
    if isinstance(a, (u.CameraActor, u.CineCameraActor)):
        cc = a.get_component_by_class(u.CameraComponent); l = a.get_actor_location(); r = a.get_actor_rotation()
        plan.append({'name': 'cam_' + a.get_actor_label().replace(' ', '_'), 'loc': [l.x, l.y, l.z], 'rot': [r.pitch, r.yaw], 'fov': (cc.get_editor_property('field_of_view') if cc else 90.0), 'set': 'cam'})
ps = [a for a in acts if isinstance(a, u.PlayerStart)]
for k, a in enumerate(ps):
    l = a.get_actor_location(); r = a.get_actor_rotation(); gz = ground(l.x, l.y)
    z = (gz + 170) if gz is not None else l.z + 80
    for tag, off in (('fwd', 0), ('L90', -90), ('R90', 90), ('back', 180)):
        plan.append({'name': 'ps%d_%s' % (k, tag), 'loc': [l.x, l.y, z], 'rot': [-5.0, r.yaw + off], 'fov': 90.0, 'set': 'ps'})
for s in getattr(builtins, 'PFR_SPOTS', []):
    gz = ground(s[0], s[1])
    if gz is None: continue
    plan.append({'name': s[4], 'loc': [s[0], s[1], gz + 170], 'rot': [s[3], s[2]], 'fov': 90.0, 'set': 'spot'})
LIGHTS = list(getattr(builtins, 'PFR_LIGHT_LEVELS', []))
SL = {}
for lv in u.EditorLevelUtils.get_levels(w):
    try:
        nm = lv.get_outer().get_name(); SL[nm] = lv
    except Exception:
        pass
vis0 = {nm: bool(lv.get_editor_property('b_is_visible')) if False else None for nm, lv in SL.items()}
variants = [None] + [l for l in LIGHTS if l in SL]
# fog recipe (property names differ per engine version): record every fog-ish property that reads
fogp = {}
for a in acts:
    if isinstance(a, u.ExponentialHeightFog):
        c = a.get_component_by_class(u.ExponentialHeightFogComponent); d = {'level': a.get_level().get_outer().get_name(), 'loc': [round(v) for v in a.get_actor_location().to_tuple()]}
        for k in ('fog_density', 'fog_height_falloff', 'fog_max_opacity', 'start_distance', 'end_distance', 'fog_cutoff_distance', 'fog_inscattering_luminance', 'directional_inscattering_luminance', 'directional_inscattering_exponent',
                  'directional_inscattering_start_distance', 'enable_volumetric_fog', 'volumetric_fog', 'b_enable_volumetric_fog', 'volumetric_fog_scattering_distribution', 'volumetric_fog_albedo', 'volumetric_fog_emissive', 'volumetric_fog_extinction_scale',
                  'volumetric_fog_distance', 'volumetric_fog_start_distance', 'volumetric_fog_near_fade_in_distance', 'volumetric_fog_static_lighting_scattering_intensity', 'inscattering_color_cubemap', 'sky_atmosphere_ambient_contribution_color_scale'):
            try:
                v = c.get_editor_property(k); d[k] = [round(x, 4) for x in v.to_tuple()] if hasattr(v, 'to_tuple') else (v if isinstance(v, (int, float, bool, str)) else str(v)[:80])
            except Exception:
                pass
        try:
            sf = c.get_editor_property('second_fog_data'); d['second'] = {k: sf.get_editor_property(k) for k in ('fog_density', 'fog_height_falloff', 'fog_height_offset')}
        except Exception:
            pass
        fogp[a.get_actor_label()] = d
(D / 'fog_probe.json').write_text(json.dumps({'fog': fogp, 'levels': list(SL)}, indent=1, default=str))
cam = A.spawn_actor_from_class(u.CameraActor, u.Vector(0, 0, 0)); cc = cam.camera_component; cc.set_editor_property('constrain_aspect_ratio', False)
LOG = {'world': w.get_path_name(), 'plan': plan, 'variants': variants, 'vis0': vis0, 'shots': [], 'errors': []}
st = {'v': 0, 'i': 0, 'phase': 'variant', 't': time.monotonic(), 'task': None}


def shots_for(v):
    return plan if v is None else [p for p in plan if p['set'] == 'ps']


def set_variant(v):
    for nm, lv in SL.items():
        if nm in LIGHTS:
            want = (nm == v) if v is not None else (nm == LIGHTS[0] if LIGHTS else True)   # default = the first listed (the shipped Morning)
            u.EditorLevelUtils.set_level_visibility(lv, want, False)


def tick(dt):
    try:
        now = time.monotonic()
        if st['v'] >= len(variants):
            set_variant(None); A.destroy_actor(cam); u.unregister_slate_post_tick_callback(builtins.PFR_CAP)
            LOG['finished'] = time.strftime('%H:%M:%S'); (D / 'cap_log.json').write_text(json.dumps(LOG, indent=1, default=str)); (D / 'cap_done').write_text('ok'); return
        v = variants[st['v']]; S = shots_for(v)
        if st['phase'] == 'variant':
            set_variant(v); st.update(phase='pos', t=now, i=0); return
        if st['i'] >= len(S):
            st.update(v=st['v'] + 1, phase='variant', t=now); return
        s = S[st['i']]; fn = D / ((s['name'] + ('' if v is None else '__' + v.split('/')[-1])) + '.png')
        if st['phase'] == 'pos':
            cam.set_actor_location_and_rotation(u.Vector(*s['loc']), u.Rotator(pitch=s['rot'][0], yaw=s['rot'][1], roll=0), False, True)
            cc.set_editor_property('field_of_view', s['fov']); st.update(phase='warm', t=now)
        elif st['phase'] == 'warm' and now - st['t'] > (12.0 if st['i'] == 0 else 1.5):
            if fn.exists(): fn.unlink()
            st['task'] = u.AutomationLibrary.take_high_res_screenshot(1920, 1080, str(fn), camera=cam, delay=0.5); st.update(phase='shoot', t=now)
        elif st['phase'] == 'shoot' and ((fn.exists() and fn.stat().st_size > 0 and now - st['t'] > 2.0) or now - st['t'] > 60):
            LOG['shots'].append({'file': fn.name, 'ok': fn.exists(), 'loc': s['loc'], 'rot': s['rot'], 'fov': s['fov'], 'variant': v})
            st.update(i=st['i'] + 1, phase='pos', t=now)
    except Exception as ex:
        LOG['errors'].append(repr(ex)[:300]); u.unregister_slate_post_tick_callback(builtins.PFR_CAP)
        try: A.destroy_actor(cam)
        except Exception: pass
        (D / 'cap_log.json').write_text(json.dumps(LOG, indent=1, default=str)); (D / 'cap_done').write_text('error')


builtins.PFR_CAP = u.register_slate_post_tick_callback(tick)
print('SHOWCASE_CAP scheduled', len(plan), 'shots x variants', len(variants), 'streaming', list(SL))
