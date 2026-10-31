"""Forest-station walk test (pie job): real pawn + GraceRanger camera, rear uphill trail (Bridge 14_uphill_path pose, P03/P04 zone).

  stills  at the start: forward / left90 / right90 (HighResShot 1920x1080); at the end of pass A: lookback (P05-type)
  pass A  12 s walk (forced key W through Enhanced Input 'Input.+key', walk gait = no gait action), frames captured with the existing
          MediaCapture path (FileMediaOutput JPG, centre crop 1664x896, 30 FPS fixed-step game time = real speed, unedited)
  pass B  same start + same 12 s walk without capture, 'csvprofile start/stop' (stock CSV profiler; no cvar changed) + per-tick wall time
Per tick: pawn location / speed, camera location / rotation / FOV, camera-to-pawn distance and whether a Visibility trace from the
camera to the pawn chest is blocked (foliage without collision is NOT detected by the trace; judged from the frames).
Runtime only: no asset, ABP default, cvar, config or map is changed; nothing is saved. PIE runs the in-memory state (2 dirty ABPs with
V2.40 candidate knob values, see abp_inspect.json).
Output: <OUT>/frames/fNNNNN.jpg, <OUT>/stills/*.png, <OUT>/walk_log.json, <OUT>/walk_status.json; CSV under Saved/Profiling/CSV.
"""
import unreal as u, json, os, time, builtins, math

OUT = r'C:\Users\berat\AppData\Local\Temp\claude\C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS\5f49a232-b001-47ad-8881-1eb04d9cb1c5\scratchpad\walk'
START = (2960.0, -1730.0, getattr(builtins, 'PIEWALK_YAW', -115.03070967737723))   # Bridge '14_uphill_path' (rear_trail) xy + yaw
WALK_S, SETTLE, CROP = getattr(builtins, 'PIEWALK_GAME_S', 12.0), 6.0, (1664, 896)   # WALK_S = GAME seconds (fixed-step 30 FPS)
OUT = getattr(builtins, 'PIEWALK_OUT', OUT)
if getattr(builtins, 'PIEWALK_ACTIVE', None):
    raise RuntimeError('pie_walk already running')
for d in ('frames', 'stills'):
    os.makedirs(os.path.join(OUT, d), exist_ok=True)
for f in os.listdir(os.path.join(OUT, 'frames')):
    os.remove(os.path.join(OUT, 'frames', f))
E = u.get_editor_subsystem(u.UnrealEditorSubsystem)
L = u.get_editor_subsystem(u.LevelEditorSubsystem)
if E.get_game_world() is not None:
    raise RuntimeError('PIE already running')
S = u.EditorLoadingAndSavingUtils
dirty = lambda: sorted([p.get_name() for p in S.get_dirty_content_packages()] + [p.get_name() for p in S.get_dirty_map_packages()])
LOG = {'started': time.strftime('%Y-%m-%d %H:%M:%S'), 'start': START, 'walk_s': WALK_S, 'crop': CROP, 'dirty_before': dirty(),
       'stills': [], 'passA': {'ticks': []}, 'passB': {'ticks': []}, 'errors': [], 'events': []}
PLAN = [('tp', 0), ('wait', SETTLE), ('still', 'start_forward', 0), ('rot', -90), ('wait', 3.0), ('still', 'start_left90', 0),
        ('rot', 90), ('wait', 3.0), ('still', 'start_right90', 0), ('rot', 0), ('wait', 3.0),
        ('cap_on',), ('walk', 'passA'), ('cap_off',), ('wait', 1.0), ('rot', 180), ('wait', 3.0), ('still', 'end_lookback', 0),
        ('tp', 0), ('wait', SETTLE), ('csv_on',), ('walk', 'passB'), ('csv_off',), ('wait', 2.0)]


class Walk:
    def __init__(self):
        self.i, self.t, self.phase, self.t0 = 0, time.monotonic(), 'start', time.monotonic()
        self.cap = None
        self.handle = u.register_slate_post_tick_callback(self.tick)
        builtins.PIEWALK_ACTIVE = self
        L.editor_request_begin_play()

    def status(self, s):
        json.dump({'state': s, 'step': self.i, 'of': len(PLAN), 'errors': LOG['errors']}, open(os.path.join(OUT, 'walk_status.json'), 'w'))

    def cmd(self, gw, c):
        u.SystemLibrary.execute_console_command(gw, c)

    def sample(self, gw, key, now):
        cm = u.GameplayStatics.get_player_camera_manager(gw, 0)
        p = self.pawn.get_actor_location(); c = cm.get_camera_location(); r = cm.get_camera_rotation()
        hit = u.SystemLibrary.line_trace_single(gw, c, u.Vector(p.x, p.y, p.z + 40), u.TraceTypeQuery.TRACE_TYPE_QUERY1, False, [self.pawn],
                                                u.DrawDebugTrace.NONE, True)
        hr = hit.to_tuple() if hit else None
        LOG[key]['ticks'].append({'wall': round(now - self.t0, 4), 'game': round(u.GameplayStatics.get_time_seconds(gw), 4),
                                  'pawn': [round(p.x, 1), round(p.y, 1), round(p.z, 1)], 'speed': round(self.pawn.get_velocity().length(), 1),
                                  'cam': [round(c.x, 1), round(c.y, 1), round(c.z, 1)], 'cam_rot': [round(r.pitch, 2), round(r.yaw, 2)],
                                  'fov': round(cm.get_fov_angle(), 2),
                                  'cam_pawn_cm': round(math.sqrt((c.x - p.x) ** 2 + (c.y - p.y) ** 2 + (c.z - p.z) ** 2), 1),
                                  'blocked_by': (hr[9].get_actor_label() if hr and hr[0] and hr[9] else None)})

    def tick(self, dt):
        try:
            now = time.monotonic(); gw = E.get_game_world()
            if self.phase == 'start':
                if gw is None:
                    if now - self.t0 > 60:
                        raise RuntimeError('PIE did not start')
                    return
                self.pawn = u.GameplayStatics.get_player_pawn(gw, 0); self.pc = u.GameplayStatics.get_player_controller(gw, 0)
                if not self.pawn:
                    return
                try:
                    vs = u.WidgetLayoutLibrary.get_viewport_size(gw); LOG['viewport'] = [vs.x, vs.y]
                except Exception as ex:
                    LOG['viewport'] = str(ex)
                self.phase = 'run'; self.t = now; self.status('running'); return
            if gw is None:
                raise RuntimeError('PIE ended early at step %d' % self.i)
            if self.i >= len(PLAN):
                return self.finish()
            st = PLAN[self.i]
            if st[0] == 'tp':
                x, y, yaw = START
                hit = u.SystemLibrary.line_trace_single(gw, u.Vector(x, y, 4000), u.Vector(x, y, -4000), u.TraceTypeQuery.TRACE_TYPE_QUERY1, False,
                                                        [self.pawn], u.DrawDebugTrace.NONE, True)
                hr = hit.to_tuple() if hit else None
                gz = hr[4].z if hr and hr[0] else 0.0
                cap = self.pawn.get_component_by_class(u.CapsuleComponent)
                hh = cap.get_scaled_capsule_half_height() if cap else 90.0
                self.pawn.set_actor_location(u.Vector(x, y, gz + hh + 2), False, True)
                self.pawn.set_actor_rotation(u.Rotator(pitch=0, yaw=yaw, roll=0), True)
                self.pc.set_control_rotation(u.Rotator(pitch=-5.0, yaw=yaw, roll=0))
                LOG['events'].append({'tp_ground_z': round(gz, 1), 'ground_actor': (hr[9].get_actor_label() if hr and hr[0] and hr[9] else None), 'wall': round(now - self.t0, 2)})
                self.i += 1; self.t = now
            elif st[0] == 'rot':
                yaw = self.yaw_now = (self.pawn.get_actor_rotation().yaw if st[1] == 180 else START[2]) + st[1]
                self.pc.set_control_rotation(u.Rotator(pitch=-5.0, yaw=yaw, roll=0))
                self.i += 1; self.t = now
            elif st[0] == 'wait':
                if now - self.t >= st[1]:
                    self.i += 1; self.t = now
            elif st[0] == 'still':
                if not getattr(self, 'file', None):
                    self.file = os.path.join(OUT, 'stills', '%s.png' % st[1])
                    if os.path.exists(self.file):
                        os.remove(self.file)
                    self.cmd(gw, 'HighResShot 1920x1080 filename=%s' % self.file.replace('\\', '/')); self.req = now
                elif os.path.exists(self.file) and os.path.getsize(self.file) > 0 and now - self.req > 0.5:
                    cm = u.GameplayStatics.get_player_camera_manager(gw, 0); c = cm.get_camera_location(); p = self.pawn.get_actor_location()
                    LOG['stills'].append({'name': st[1], 'cam': [round(c.x, 1), round(c.y, 1), round(c.z, 1)], 'pawn': [round(p.x, 1), round(p.y, 1), round(p.z, 1)],
                                          'cam_rot': [round(cm.get_camera_rotation().pitch, 2), round(cm.get_camera_rotation().yaw, 2)], 'fov': round(cm.get_fov_angle(), 2)})
                    self.file = None; self.i += 1; self.t = now
                elif now - self.req > 30:
                    raise RuntimeError('HighResShot timeout')
            elif st[0] == 'cap_on':
                vs = u.WidgetLayoutLibrary.get_viewport_size(gw); vw, vh = int(round(vs.x)), int(round(vs.y))
                if vw < CROP[0] or vh < CROP[1]:
                    LOG['capture'] = {'refused': 'viewport %dx%d smaller than crop %s' % (vw, vh, CROP)}
                else:
                    out = u.FileMediaOutput(); out.set_editor_property('file_path', u.DirectoryPath(path=os.path.join(OUT, 'frames')))
                    out.set_editor_property('base_file_name', 'f')
                    wo = out.get_editor_property('write_options'); wo.set_editor_property('format', u.DesiredImageFormat.JPG)
                    wo.set_editor_property('compression_quality', 90); wo.set_editor_property('async_', True); out.set_editor_property('write_options', wo)
                    out.set_editor_property('override_desired_size', True); out.set_editor_property('desired_size', u.IntPoint(CROP[0], CROP[1]))
                    self.cap = out.create_media_capture(); opts = u.MediaCaptureOptions()
                    opts.set_editor_property('crop', u.MediaCaptureCroppingType.CENTER)
                    ok = self.cap.capture_active_scene_viewport(opts)
                    LOG['capture'] = {'ok': bool(ok), 'viewport': [vw, vh], 'game_t0': u.GameplayStatics.get_time_seconds(gw), 'wall_t0': round(now - self.t0, 3)}
                self.i += 1; self.t = now
            elif st[0] == 'cap_off':
                if self.cap:
                    self.cap.stop_capture(True); self.cap = None
                    LOG['capture']['game_t1'] = u.GameplayStatics.get_time_seconds(gw); LOG['capture']['wall_t1'] = round(now - self.t0, 3)
                self.i += 1; self.t = now
            elif st[0] == 'csv_on':
                self.cmd(gw, 'csvprofile start'); LOG['csv_start_wall'] = time.strftime('%H:%M:%S'); self.i += 1; self.t = now
            elif st[0] == 'csv_off':
                self.cmd(gw, 'csvprofile stop'); LOG['csv_stop_wall'] = time.strftime('%H:%M:%S'); self.i += 1; self.t = now
            elif st[0] == 'walk':
                key = st[1]
                gnow = u.GameplayStatics.get_time_seconds(gw)
                if not getattr(self, 'walking', False):
                    self.walking = True; self.wt = gnow; self.cmd(gw, 'Input.+key W true')
                self.sample(gw, key, now)
                if gnow - self.wt >= WALK_S:
                    self.cmd(gw, 'Input.-key W'); self.walking = False; self.i += 1; self.t = now
        except Exception as ex:
            LOG['errors'].append(repr(ex)); self.finish()

    def finish(self):
        u.unregister_slate_post_tick_callback(self.handle)
        builtins.PIEWALK_ACTIVE = None
        gw = E.get_game_world()
        try:
            if self.cap:
                self.cap.stop_capture(True)
            if gw:
                self.cmd(gw, 'Input.-key W')
        except Exception as ex:
            LOG['errors'].append('cleanup ' + repr(ex))
        if gw is not None:
            L.editor_request_end_play()
        LOG['frames_written'] = len([f for f in os.listdir(os.path.join(OUT, 'frames')) if f.endswith('.jpg')])
        LOG['dirty_after'] = dirty()
        LOG['finished'] = time.strftime('%Y-%m-%d %H:%M:%S')
        json.dump(LOG, open(os.path.join(OUT, 'walk_log.json'), 'w'), indent=1, default=str)
        self.status('done' if not LOG['errors'] else 'error')


Walk()
print('PIEWALK started steps', len(PLAN))
