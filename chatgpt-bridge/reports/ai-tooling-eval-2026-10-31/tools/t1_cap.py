"""T1 capture repeatability (same editor session), read-only measure job.

Starts a slate post-tick state machine that, for 3 fixed views (house front, pond, forest; poses from the
2026-09-25 Bridge camera_plan.json), takes engine renders with the same call the Bridge exporter uses
(AutomationLibrary.take_high_res_screenshot 1920x1080, force_game_view) and records exact timing and settings.

  Phase A  per view: move once, shots at 0.5 / 2.5 / 6 / 10 / 12 / 14 s after the move (settle curve; the
           10/12/14 s shots are the static repeats with the camera untouched).
  Phase B  2 more rounds over all views: move away + back, settle 10 s, shot (revisit repeats).
           In round 2 the MCP tool function EditorAppToolset.CaptureViewport is also called in-process through
           ToolsetRegistry.ExecuteTool (no MCP server) and its PNG saved.
The viewport pose / FOV / game view are restored at the end. Nothing is spawned, edited or saved; dirty
packages and actor transforms are recorded before and after.
Output: <OUT>/shots/*.png, <OUT>/t1_status.json (progress), <OUT>/t1_log.json (final).
"""
import unreal as u, json, time, os, base64, builtins, hashlib

OUT = r'C:\Users\berat\AppData\Local\Temp\claude\C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS\5f49a232-b001-47ad-8881-1eb04d9cb1c5\scratchpad\t1'
VIEWS = {  # Bridge camera_plan.json (run 2026-09-25_071602): 06_house_exterior, 17_shoreline_gameplay, 09_house_to_forest
    'house_front': ([-1550, 2460, 92.3320484161377], [4.045882564505467, -36.830867829324454, 0], 68),
    'pond':        ([1500, 2810, 152.16795921325684], [-6.110206786658776, 130.80909247267473, 0], 75),
    'forest':      ([2200, 1580, 319.35779571533203], [3.696050782488103, -77.14368743247138, 0], 70),
}
SWEEP = [0.5, 2.5, 6.0, 10.0, 12.0, 14.0]
SETTLE_B = 10.0

if getattr(builtins, 'T1_CAP_ACTIVE', None):
    raise RuntimeError('T1 capture already running')
os.makedirs(os.path.join(OUT, 'shots'), exist_ok=True)

A = u.get_editor_subsystem(u.EditorActorSubsystem)
E = u.get_editor_subsystem(u.UnrealEditorSubsystem)
L = u.get_editor_subsystem(u.LevelEditorSubsystem)
if L.is_in_play_in_editor():
    raise RuntimeError('PIE is running; T1 needs the editor world')
world = E.get_editor_world()
key = L.get_active_viewport_config_key()
pose0 = L.get_level_viewport_camera_info(key)
fov0 = L.get_level_viewport_fov(key)
gv0 = L.editor_get_game_view(key)
size0 = E.get_level_viewport_size()


def prop(obj, key, default=None):  # same accessor as Content/Python/chatgpt_bridge.py
    try:
        return obj.get_editor_property(key)
    except Exception:
        try:
            return obj.get_editor_property(''.join(p[:1].upper() + p[1:] for p in key.split('_')))
        except Exception:
            return default


def dirty():
    S = u.EditorLoadingAndSavingUtils
    return sorted([p.get_name() for p in S.get_dirty_content_packages()] + [p.get_name() for p in S.get_dirty_map_packages()])


def xform_hash():
    h = hashlib.sha1()
    for a in sorted(A.get_all_level_actors(), key=lambda a: a.get_path_name()):
        t = a.get_actor_transform()
        h.update(('%s %.3f %.3f %.3f %.3f %.3f %.3f\n' % (a.get_path_name(), t.translation.x, t.translation.y, t.translation.z,
                                                          t.rotation.x, t.rotation.y, t.rotation.z)).encode())
    return h.hexdigest()


def cv(name):
    try:
        return u.SystemLibrary.get_console_variable_float_value(name)
    except Exception as ex:
        return 'ERR %s' % ex


def scene_settings():
    s = {'cvars': {n: cv(n) for n in ['r.AntiAliasingMethod', 'r.DynamicGlobalIlluminationMethod', 'r.ReflectionMethod',
                                      'r.Shadow.Virtual.Enable', 'r.ScreenPercentage', 'r.Lumen.HardwareRayTracing',
                                      'r.EyeAdaptationQuality', 'r.MotionBlurQuality', 'sg.ViewDistanceQuality',
                                      'sg.ShadowQuality', 'sg.GlobalIlluminationQuality', 'sg.ReflectionQuality',
                                      'sg.PostProcessQuality', 'sg.TextureQuality', 'sg.EffectsQuality',
                                      'sg.FoliageQuality', 'sg.ShadingQuality', 't.MaxFPS']}}
    lights = []
    for a in A.get_all_level_actors():
        c = a.get_class().get_name()
        if c in ('DirectionalLight', 'SkyLight', 'ExponentialHeightFog', 'SkyAtmosphere', 'PostProcessVolume', 'VolumetricCloud'):
            r = a.get_actor_rotation()
            row = {'class': c, 'name': a.get_actor_label(), 'rotation': [r.pitch, r.yaw, r.roll]}
            if c == 'PostProcessVolume':
                try:
                    st = a.get_editor_property('settings')
                    row['unbound'] = a.get_editor_property('unbound')
                    row['auto_exposure_method'] = str(st.get_editor_property('auto_exposure_method')) if st.get_editor_property('override_auto_exposure_method') else 'not overridden'
                    row['exposure_bias'] = st.get_editor_property('auto_exposure_bias') if st.get_editor_property('override_auto_exposure_bias') else 'not overridden'
                    row['min_max_ev100'] = [st.get_editor_property('auto_exposure_min_brightness') if st.get_editor_property('override_auto_exposure_min_brightness') else None,
                                            st.get_editor_property('auto_exposure_max_brightness') if st.get_editor_property('override_auto_exposure_max_brightness') else None]
                except Exception as ex:
                    row['err'] = str(ex)
            lights.append(row)
    s['scene_actors'] = lights
    return s


LOG = {'started': time.strftime('%Y-%m-%d %H:%M:%S'), 'engine': u.SystemLibrary.get_engine_version(),
       'world': world.get_path_name(), 'viewport_key': str(key), 'viewport_size': [size0.x, size0.y] if size0 else None,
       'pose0': [[pose0[0].x, pose0[0].y, pose0[0].z], [pose0[1].pitch, pose0[1].yaw, pose0[1].roll]], 'fov0': fov0,
       'game_view0': gv0, 'views': VIEWS, 'sweep_s': SWEEP, 'settle_b_s': SETTLE_B,
       'capture_call': 'AutomationLibrary.take_high_res_screenshot(1920,1080,file,delay=0.2,force_game_view=True)',
       'dirty_before': dirty(), 'xform_before': xform_hash(), 'settings_before': scene_settings(), 'shots': [], 'errors': []}

# plan: list of steps ('move', view) / ('shot', view, tag, t_after_move) / ('mcp', view, tag)
PLAN = []
for v in VIEWS:
    PLAN.append(('move', v))
    for t in SWEEP:
        PLAN.append(('shot', v, 'A_t%04.1f' % t, t))
for rnd in (2, 3):
    for v in VIEWS:
        PLAN.append(('move', v))
        PLAN.append(('shot', v, 'B_round%d' % rnd, SETTLE_B))
        if rnd == 2:
            PLAN.append(('mcp', v, 'B_round2_captureviewport'))


class T1:
    def __init__(self):
        self.i, self.moved, self.task, self.file, self.res, self.t0 = 0, 0.0, None, None, None, time.monotonic()
        self.handle = u.register_slate_post_tick_callback(self.tick)
        builtins.T1_CAP_ACTIVE = self

    def status(self, state):
        with open(os.path.join(OUT, 't1_status.json'), 'w') as f:
            json.dump({'state': state, 'step': self.i, 'of': len(PLAN), 'shots': len(LOG['shots']), 'errors': LOG['errors']}, f)

    def tick(self, dt):
        try:
            if L.is_in_play_in_editor() or E.get_editor_world().get_path_name() != LOG['world']:
                raise RuntimeError('PIE started or world changed')
            if time.monotonic() - self.t0 > 900:
                raise RuntimeError('T1 overall timeout')
            if self.i >= len(PLAN):
                return self.finish()
            st = PLAN[self.i]
            now = time.monotonic()
            if st[0] == 'move':
                p, r, fov = VIEWS[st[1]]
                L.editor_set_game_view(True, key)
                L.set_level_viewport_camera_info(u.Vector(*p), u.Rotator(pitch=r[0], yaw=r[1], roll=r[2]), key)
                L.set_level_viewport_fov(fov, key)
                L.editor_invalidate_viewports()
                self.moved = now
                self.i += 1
                self.status('running')
            elif st[0] == 'shot':
                if self.task is None:
                    if now - self.moved < st[3]:
                        return
                    self.file = os.path.join(OUT, 'shots', '%s__%s.png' % (st[1], st[2]))
                    if os.path.exists(self.file):
                        os.remove(self.file)
                    self.req = now
                    self.task = u.AutomationLibrary.take_high_res_screenshot(1920, 1080, self.file, delay=0.2, force_game_view=True)
                    self.redraw = None
                elif self.redraw is None and now - self.req > 0.5:
                    # same as the Bridge exporter: synchronous viewport draw so the request is served with realtime off
                    self.redraw = u.ToolsetRegistry.execute_tool('EditorToolset.EditorAppToolset', 'CaptureViewport',
                                                                 '{"captureTransform":null,"annotations":null,"bShowUI":false}')
                elif self.task.is_task_done() and os.path.exists(self.file) and os.path.getsize(self.file) > 0:
                    LOG['shots'].append({'view': st[1], 'tag': st[2], 'file': os.path.basename(self.file),
                                         'requested_after_move_s': round(self.req - self.moved, 3),
                                         'done_after_move_s': round(now - self.moved, 3),
                                         'session_s': round(now - self.t0, 3), 'bytes': os.path.getsize(self.file)})
                    self.task = None
                    self.i += 1
                    self.status('running')
                elif now - self.req > 45:
                    raise RuntimeError('screenshot timeout %s' % self.file)
            elif st[0] == 'mcp':
                if self.res is None:
                    self.req = now
                    self.res = u.ToolsetRegistry.execute_tool('EditorToolset.EditorAppToolset', 'CaptureViewport',
                                                              '{"captureTransform":null,"annotations":null,"bShowUI":false}')
                elif prop(self.res, 'is_complete'):
                    row = {'view': st[1], 'tag': st[2], 'call': 'ToolsetRegistry.execute_tool(EditorToolset.EditorAppToolset, CaptureViewport)'}
                    err = prop(self.res, 'error')
                    if err:
                        row['error'] = str(err)
                    else:
                        val = json.loads(prop(self.res, 'value'))
                        img = val.get('Image') or val.get('image') or {}
                        b64 = img.get('Data') or img.get('data') or img.get('Base64') or img.get('base64')
                        row['keys'] = list(val.keys())
                        row['image_keys'] = list(img.keys()) if isinstance(img, dict) else str(type(img))
                        for k in ('CameraLocation', 'CameraRotation', 'FieldOfView', 'cameraLocation', 'cameraRotation', 'fieldOfView'):
                            if k in val:
                                row[k] = val[k]
                        if b64:
                            fn = os.path.join(OUT, 'shots', '%s__%s.png' % (st[1], st[2]))
                            with open(fn, 'wb') as f:
                                f.write(base64.b64decode(b64))
                            row['file'] = os.path.basename(fn)
                            row['bytes'] = os.path.getsize(fn)
                    row['done_s'] = round(now - self.req, 3)
                    LOG['shots'].append(row)
                    self.res = None
                    self.i += 1
                    self.status('running')
                elif now - self.req > 30:
                    raise RuntimeError('CaptureViewport timeout')
        except Exception as ex:
            LOG['errors'].append(repr(ex))
            self.finish()

    def finish(self):
        u.unregister_slate_post_tick_callback(self.handle)
        builtins.T1_CAP_ACTIVE = None
        try:
            L.set_level_viewport_camera_info(pose0[0], pose0[1], key)
            L.set_level_viewport_fov(fov0, key)
            L.editor_set_game_view(gv0, key)
            L.editor_invalidate_viewports()
            p1 = L.get_level_viewport_camera_info(key)
            LOG['restored'] = {'pose': [[p1[0].x, p1[0].y, p1[0].z], [p1[1].pitch, p1[1].yaw, p1[1].roll]],
                               'fov': L.get_level_viewport_fov(key), 'game_view': L.editor_get_game_view(key)}
        except Exception as ex:
            LOG['errors'].append('restore ' + repr(ex))
        LOG['dirty_after'] = dirty()
        LOG['xform_after'] = xform_hash()
        LOG['xform_unchanged'] = LOG['xform_after'] == LOG['xform_before']
        LOG['finished'] = time.strftime('%Y-%m-%d %H:%M:%S')
        with open(os.path.join(OUT, 't1_log.json'), 'w') as f:
            json.dump(LOG, f, indent=1, default=str)
        self.status('done' if not LOG['errors'] else 'error')


T1()
print('T1_CAP started, steps', len(PLAN), 'world', LOG['world'], 'viewport', LOG['viewport_size'], 'dirty_before', len(LOG['dirty_before']))
