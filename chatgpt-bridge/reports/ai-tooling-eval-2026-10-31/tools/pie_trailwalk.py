"""pie_trailwalk.py (pie job): BEFORE set for the rear-trail pilot, walking the AUTHORED trail curve (not a fixed yaw).

Trail = TRAIL of Tools/AAAPolishRear20260923/design_terrain.py; segment = arc [s0, s0 + 16.5 m], s0 = projection of (2960, -1730).
Steering: W held (Enhanced Input forced key, walk gait); each frame the control yaw turns toward a look-ahead point 2.5 m further along
the trail, rate-limited to 90 deg/s (like a player steering with the mouse); pitch -5.
  pass A  walk with MediaCapture frames (JPG, centre crop 1664x896, 30 FPS fixed-step game time = real speed)
  pass B  same walk, no capture, stock 'csvprofile' (no cvar changed)
  stations s = 2 / 8 / 14 m (approach / compression / release): forward (trail tangent), left90, right90, lookback (tangent + 180) and,
           at 14 m, 'house' (yaw toward the house content bounds centre) - HighResShot 1920x1080 through the real player camera
  pans     at 8 and 14 m: captured yaw sweep tangent-100 -> tangent+100 deg over 6 s (right/left camera turn in motion)
Also records the live camera rig (spring arm / camera component / CMC walkability) once.
Runtime only; nothing saved. PIE runs the in-memory state (2 dirty ABPs, see v4 report).
Output: <OUT>/frames, <OUT>/stills, <OUT>/trailwalk_log.json, <OUT>/trailwalk_status.json
"""
import unreal as u, json, os, time, builtins, math

OUT = getattr(builtins, 'TRAILWALK_OUT', r'C:\Users\berat\AppData\Local\Temp\claude\C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS\5f49a232-b001-47ad-8881-1eb04d9cb1c5\scratchpad\pilot\before')
TRAIL = [(1950, 2110), (2300, 1850), (2560, 1300), (2520, 750), (2580, 250), (2790, -250), (3010, -760), (2930, -1260),
         (3110, -1800), (3080, -2300), (2780, -2800), (2350, -3340)]
HOUSE_C = (760.0, 695.5)            # centre of the house content bounds (env_probe.json)
SEG, LOOK, YAW_RATE, CROP, SETTLE = 1650.0, 250.0, 90.0, (1664, 896), 6.0
STATIONS = [('approach', 200.0), ('compression', 800.0), ('release', 1400.0)]
if getattr(builtins, 'TRAILWALK_ACTIVE', None):
    raise RuntimeError('trailwalk already running')
for d in ('frames', 'stills'):
    os.makedirs(os.path.join(OUT, d), exist_ok=True)
for f in os.listdir(os.path.join(OUT, 'frames')):
    os.remove(os.path.join(OUT, 'frames', f))
seg = [0.0]
for a, b in zip(TRAIL, TRAIL[1:]):
    seg.append(seg[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))


def at(s):
    for i in range(len(TRAIL) - 1):
        if s <= seg[i + 1] or i == len(TRAIL) - 2:
            L = seg[i + 1] - seg[i]; t = (s - seg[i]) / L; a, b = TRAIL[i], TRAIL[i + 1]
            return a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]), math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))


def proj(x, y):
    best = (1e18, 0.0)
    for i in range(len(TRAIL) - 1):
        a, b = TRAIL[i], TRAIL[i + 1]; dx, dy = b[0] - a[0], b[1] - a[1]; L2 = dx * dx + dy * dy
        t = max(0.0, min(1.0, ((x - a[0]) * dx + (y - a[1]) * dy) / L2)); d2 = (a[0] + t * dx - x) ** 2 + (a[1] + t * dy - y) ** 2
        if d2 < best[0]:
            best = (d2, seg[i] + t * math.sqrt(L2))
    return best[1], math.sqrt(best[0])


S0 = proj(2960.0, -1730.0)[0]
E = u.get_editor_subsystem(u.UnrealEditorSubsystem)
L = u.get_editor_subsystem(u.LevelEditorSubsystem)
if E.get_game_world() is not None:
    raise RuntimeError('PIE already running')
SL = u.EditorLoadingAndSavingUtils
dirty = lambda: sorted([p.get_name() for p in SL.get_dirty_content_packages()] + [p.get_name() for p in SL.get_dirty_map_packages()])
LOG = {'started': time.strftime('%Y-%m-%d %H:%M:%S'), 's0_cm': S0, 'segment_cm': SEG, 'lookahead_cm': LOOK, 'yaw_rate_dps': YAW_RATE,
       'dirty_before': dirty(), 'stills': [], 'passA': {'ticks': []}, 'passB': {'ticks': []}, 'errors': [], 'events': []}
PLAN = [('tp', 0.0, 0.0), ('wait', SETTLE), ('cap_on',), ('walk', 'passA'), ('cap_off',),
        ('tp', 0.0, 0.0), ('wait', SETTLE), ('csv_on',), ('walk', 'passB'), ('csv_off',)]
for name, s in STATIONS:
    PLAN += [('tp', s, 0.0), ('wait', 5.0)]
    dirs = [('forward', 0.0), ('left90', -90.0), ('right90', 90.0), ('lookback', 180.0)] + ([('house', 'house')] if name == 'release' else [])
    for dn, off in dirs:
        PLAN += [('rot', s, off), ('wait', 3.0), ('still', '%s_%s' % (name, dn))]
    if name in ('compression', 'release'):   # right/left camera turn in motion: yaw sweep tangent-100 -> tangent+100 over 6 s, captured
        PLAN += [('rot', s, -100.0), ('wait', 2.0), ('cap_on', 'frames_pan_' + name), ('pan', s, -100.0, 100.0, 6.0), ('cap_off',)]


class TW:
    def __init__(self):
        self.i, self.t, self.phase, self.t0, self.cap, self.file, self.walking = 0, time.monotonic(), 'start', time.monotonic(), None, None, False
        self.handle = u.register_slate_post_tick_callback(self.tick)
        builtins.TRAILWALK_ACTIVE = self
        L.editor_request_begin_play()

    def status(self, s):
        json.dump({'state': s, 'step': self.i, 'of': len(PLAN), 'errors': LOG['errors']}, open(os.path.join(OUT, 'trailwalk_status.json'), 'w'))

    def cmd(self, gw, c):
        u.SystemLibrary.execute_console_command(gw, c)

    def rig(self):
        r = {}
        try:
            sa = self.pawn.get_component_by_class(u.SpringArmComponent)
            if sa:
                for k in ('target_arm_length', 'do_collision_test', 'probe_size', 'probe_channel', 'enable_camera_lag', 'camera_lag_speed',
                          'enable_camera_rotation_lag', 'socket_offset', 'target_offset', 'use_pawn_control_rotation'):
                    try:
                        r['spring_arm.' + k] = str(sa.get_editor_property(k))
                    except Exception as ex:
                        r['spring_arm.' + k] = 'n/a'
            cc = self.pawn.get_component_by_class(u.CameraComponent)
            if cc:
                r['camera.field_of_view'] = cc.get_editor_property('field_of_view')
            cm = self.pawn.get_component_by_class(u.CharacterMovementComponent)
            if cm:
                for k in ('walkable_floor_angle', 'max_step_height', 'max_walk_speed'):
                    r['cmc.' + k] = cm.get_editor_property(k)
        except Exception as ex:
            r['err'] = repr(ex)
        LOG['camera_rig'] = r

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
                self.rig(); self.phase = 'run'; self.t = now; self.status('running'); return
            if gw is None:
                raise RuntimeError('PIE ended early at step %d' % self.i)
            if self.i >= len(PLAN):
                return self.finish()
            st = PLAN[self.i]
            if st[0] == 'tp':
                x, y, yaw = at(S0 + st[1])
                ifa = [a for a in u.GameplayStatics.get_all_actors_of_class(gw, u.Actor) if a.get_class().get_name() == 'InstancedFoliageActor']
                h = u.SystemLibrary.line_trace_single(gw, u.Vector(x, y, 5000), u.Vector(x, y, -3000), u.TraceTypeQuery.TRACE_TYPE_QUERY1, True,
                                                      [self.pawn] + ifa, u.DrawDebugTrace.NONE, True)   # foliage ignored: tree canopies blocked complex traces
                ht = h.to_tuple() if h else None
                gz = ht[4].z if ht and ht[0] else 400.0
                cap = self.pawn.get_component_by_class(u.CapsuleComponent)
                hh = cap.get_scaled_capsule_half_height() if cap else 86.0
                self.pawn.set_actor_location(u.Vector(x, y, gz + hh + 2), False, True)
                self.pawn.set_actor_rotation(u.Rotator(pitch=0, yaw=yaw, roll=0), True)
                self.pc.set_control_rotation(u.Rotator(pitch=-5.0, yaw=yaw, roll=0))
                LOG['events'].append({'tp_s_cm': st[1], 'xy': [round(x, 1), round(y, 1)], 'ground_z': round(gz, 1), 'yaw': round(yaw, 1), 'wall': round(now - self.t0, 2)})
                self.i += 1; self.t = now
            elif st[0] == 'rot':
                x, y, yaw = at(S0 + st[1])
                if st[2] == 'house':
                    p = self.pawn.get_actor_location(); yaw = math.degrees(math.atan2(HOUSE_C[1] - p.y, HOUSE_C[0] - p.x))
                else:
                    yaw = yaw + st[2]
                self.pc.set_control_rotation(u.Rotator(pitch=-5.0, yaw=yaw, roll=0))
                self.i += 1; self.t = now
            elif st[0] == 'wait':
                if now - self.t >= st[1]:
                    self.i += 1; self.t = now
            elif st[0] == 'still':
                if not self.file:
                    self.file = os.path.join(OUT, 'stills', '%s.png' % st[1])
                    if os.path.exists(self.file):
                        os.remove(self.file)
                    self.cmd(gw, 'HighResShot 1920x1080 filename=%s' % self.file.replace('\\', '/')); self.req = now
                elif os.path.exists(self.file) and os.path.getsize(self.file) > 0 and now - self.req > 0.5:
                    cm = u.GameplayStatics.get_player_camera_manager(gw, 0); c = cm.get_camera_location(); r = cm.get_camera_rotation(); p = self.pawn.get_actor_location()
                    LOG['stills'].append({'name': st[1], 'cam': [round(c.x, 1), round(c.y, 1), round(c.z, 1)], 'cam_rot': [round(r.pitch, 2), round(r.yaw, 2)],
                                          'pawn': [round(p.x, 1), round(p.y, 1), round(p.z, 1)], 'fov': round(cm.get_fov_angle(), 2)})
                    self.file = None; self.i += 1; self.t = now
                elif now - self.req > 30:
                    raise RuntimeError('HighResShot timeout')
            elif st[0] == 'cap_on':
                vs = u.WidgetLayoutLibrary.get_viewport_size(gw); vw, vh = int(round(vs.x)), int(round(vs.y))
                fd = os.path.join(OUT, st[1] if len(st) > 1 else 'frames'); os.makedirs(fd, exist_ok=True)
                for f_ in os.listdir(fd):
                    os.remove(os.path.join(fd, f_))
                if vw >= CROP[0] and vh >= CROP[1]:
                    out = u.FileMediaOutput(); out.set_editor_property('file_path', u.DirectoryPath(path=fd))
                    out.set_editor_property('base_file_name', 'f')
                    wo = out.get_editor_property('write_options'); wo.set_editor_property('format', u.DesiredImageFormat.JPG)
                    wo.set_editor_property('compression_quality', 90); wo.set_editor_property('async_', True); out.set_editor_property('write_options', wo)
                    out.set_editor_property('override_desired_size', True); out.set_editor_property('desired_size', u.IntPoint(CROP[0], CROP[1]))
                    self.cap = out.create_media_capture(); opts = u.MediaCaptureOptions(); opts.set_editor_property('crop', u.MediaCaptureCroppingType.CENTER)
                    LOG.setdefault('captures', []).append({'dir': os.path.basename(fd), 'ok': bool(self.cap.capture_active_scene_viewport(opts)), 'viewport': [vw, vh]})
                else:
                    LOG['capture'] = {'refused': [vw, vh]}
                self.i += 1; self.t = now
            elif st[0] == 'cap_off':
                if self.cap:
                    self.cap.stop_capture(True); self.cap = None
                self.i += 1; self.t = now
            elif st[0] == 'pan':
                g = u.GameplayStatics.get_time_seconds(gw)
                if not getattr(self, 'pan_g0', None):
                    self.pan_g0 = g
                f = min(1.0, (g - self.pan_g0) / st[4]); x, y, yaw = at(S0 + st[1])
                self.pc.set_control_rotation(u.Rotator(pitch=-5.0, yaw=yaw + st[2] + f * (st[3] - st[2]), roll=0))
                if f >= 1.0:
                    self.pan_g0 = None; self.i += 1; self.t = now
            elif st[0] in ('csv_on', 'csv_off'):
                self.cmd(gw, 'csvprofile start' if st[0] == 'csv_on' else 'csvprofile stop'); LOG[st[0]] = time.strftime('%H:%M:%S'); self.i += 1; self.t = now
            elif st[0] == 'walk':
                key = st[1]; g = u.GameplayStatics.get_time_seconds(gw); p = self.pawn.get_actor_location()
                sp, off = proj(p.x, p.y)
                if not self.walking:
                    self.walking = True; self.wg = g; self.lg = g; self.yaw = self.pc.get_control_rotation().yaw; self.cmd(gw, 'Input.+key W true')
                tx, ty, _ = at(sp + LOOK); want = math.degrees(math.atan2(ty - p.y, tx - p.x))
                d = (want - self.yaw + 540) % 360 - 180; step = YAW_RATE * max(g - self.lg, 0.0)
                self.yaw += max(-step, min(step, d)); self.lg = g
                self.pc.set_control_rotation(u.Rotator(pitch=-5.0, yaw=self.yaw, roll=0))
                cm = u.GameplayStatics.get_player_camera_manager(gw, 0); c = cm.get_camera_location(); r = cm.get_camera_rotation()
                LOG[key]['ticks'].append({'game': round(g - self.wg, 4), 'wall': round(now - self.t0, 4), 's_cm': round(sp - S0, 1), 'offtrail_cm': round(off, 1),
                                          'pawn': [round(p.x, 1), round(p.y, 1), round(p.z, 1)], 'speed': round(self.pawn.get_velocity().length(), 1),
                                          'ctrl_yaw': round(self.yaw, 2), 'cam': [round(c.x, 1), round(c.y, 1), round(c.z, 1)], 'cam_rot': [round(r.pitch, 2), round(r.yaw, 2)]})
                if sp - S0 >= SEG or g - self.wg > 18.0:
                    self.cmd(gw, 'Input.-key W'); self.walking = False; self.i += 1; self.t = now
        except Exception as ex:
            LOG['errors'].append(repr(ex)); self.finish()

    def finish(self):
        u.unregister_slate_post_tick_callback(self.handle)
        builtins.TRAILWALK_ACTIVE = None
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
        LOG['frames_written'] = {d: len([f for f in os.listdir(os.path.join(OUT, d)) if f.endswith('.jpg')]) for d in os.listdir(OUT) if d.startswith('frames') and os.path.isdir(os.path.join(OUT, d))}
        LOG['dirty_after'] = dirty(); LOG['finished'] = time.strftime('%Y-%m-%d %H:%M:%S')
        json.dump(LOG, open(os.path.join(OUT, 'trailwalk_log.json'), 'w'), indent=1, default=str)
        self.status('done' if not LOG['errors'] else 'error')


TW()
print('TRAILWALK started, s0 %.0f, steps %d' % (S0, len(PLAN)))
