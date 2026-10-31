"""pie_stations.py (pie job): real player camera (BP_PBI_Player + BP_PCM_GR_Camera) stills at fixed world stations, for the
Environment Visual Master Pass. builtins.STATIONS_OUT = output dir; builtins.STATIONS_DIRS = list of (name, yaw offset) (default forward/left90/right90).
Pawn placed on the landscape (foliage and other meshes ignored in the ground trace) facing the station yaw; pitch -5; 6 s settle after a
teleport, 3 s per direction (Lumen / exposure). At 'trail_compression' a 6 s stock csvprofile is recorded facing forward.
Runtime only. Output: <OUT>/stills/<station>_<dir>.png, <OUT>/stations_log.json, <OUT>/stations_status.json"""
import unreal as u, json, os, time, builtins, math

OUT = getattr(builtins, 'STATIONS_OUT')
DIRS = getattr(builtins, 'STATIONS_DIRS', [('forward', 0.0), ('left90', -90.0), ('right90', 90.0)])
STATIONS = [   # name, x, y, yaw (deg)
    ('house_front', -1550.0, 2460.0, -36.83),
    ('pond_shore', 1500.0, 2810.0, 130.81),
    ('trail_house_side', 2540.0, 1000.0, -94.2),
    ('trail_rear_entry', 2700.0, -20.0, -66.0),
    ('trail_compression', 2984.7, -2458.9, -121.0),
    ('trail_release', 2654.1, -2958.1, -128.5),
    ('uphill_lookback', 1600.0, -4900.0, 97.0),
]
os.makedirs(os.path.join(OUT, 'stills'), exist_ok=True)
if getattr(builtins, 'STATIONS_ACTIVE', None):
    raise RuntimeError('stations already running')
E = u.get_editor_subsystem(u.UnrealEditorSubsystem); L = u.get_editor_subsystem(u.LevelEditorSubsystem)
if E.get_game_world() is not None:
    raise RuntimeError('PIE already running')
LOG = {'started': time.strftime('%Y-%m-%d %H:%M:%S'), 'stations': STATIONS, 'dirs': DIRS, 'stills': [], 'errors': [], 'events': []}
PLAN = []
for st in STATIONS:
    PLAN += [('tp', st), ('wait', 6.0)]
    for dn, off in DIRS:
        PLAN += [('rot', st, off), ('wait', 3.0), ('still', st[0], dn)]
    if st[0] == 'trail_compression':
        PLAN += [('rot', st, 0.0), ('wait', 2.0), ('csv', 'csvprofile start'), ('wait', 6.0), ('csv', 'csvprofile stop')]


class PS:
    def __init__(self):
        self.i, self.t, self.phase, self.t0, self.file = 0, time.monotonic(), 'start', time.monotonic(), None
        self.handle = u.register_slate_post_tick_callback(self.tick); builtins.STATIONS_ACTIVE = self
        L.editor_request_begin_play()

    def status(self, s):
        json.dump({'state': s, 'step': self.i, 'of': len(PLAN), 'errors': LOG['errors']}, open(os.path.join(OUT, 'stations_status.json'), 'w'))

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
                self.ifa = [a for a in u.GameplayStatics.get_all_actors_of_class(gw, u.Actor) if a.get_class().get_name() == 'InstancedFoliageActor']
                self.phase = 'run'; self.t = now; self.status('running'); return
            if gw is None:
                raise RuntimeError('PIE ended early at step %d' % self.i)
            if self.i >= len(PLAN):
                return self.finish()
            st = PLAN[self.i]
            if st[0] == 'tp':
                n, x, y, yaw = st[1]; ign = [self.pawn] + self.ifa; gz = None
                for _ in range(10):
                    t = u.SystemLibrary.line_trace_single(gw, u.Vector(x, y, 6000), u.Vector(x, y, -3000), u.TraceTypeQuery.TRACE_TYPE_QUERY1, True, ign, u.DrawDebugTrace.NONE, True).to_tuple()
                    if not t[0] or t[9] is None:
                        break
                    if t[9].get_class().get_name() == 'Landscape':
                        gz = t[4].z; break
                    ign.append(t[9])
                gz = 400.0 if gz is None else gz
                cap = self.pawn.get_component_by_class(u.CapsuleComponent); hh = cap.get_scaled_capsule_half_height() if cap else 86.0
                self.pawn.set_actor_location(u.Vector(x, y, gz + hh + 2), False, True); self.pawn.set_actor_rotation(u.Rotator(pitch=0, yaw=yaw, roll=0), True)
                self.pc.set_control_rotation(u.Rotator(pitch=-5.0, yaw=yaw, roll=0))
                LOG['events'].append({'station': n, 'ground_z': round(gz, 1)}); self.i += 1; self.t = now
            elif st[0] == 'rot':
                self.pc.set_control_rotation(u.Rotator(pitch=-5.0, yaw=st[1][3] + st[2], roll=0)); self.i += 1; self.t = now
            elif st[0] == 'wait':
                if now - self.t >= st[1]:
                    self.i += 1; self.t = now
            elif st[0] == 'csv':
                u.SystemLibrary.execute_console_command(gw, st[1]); LOG.setdefault('csv', []).append([st[1], time.strftime('%H:%M:%S')]); self.i += 1; self.t = now
            elif st[0] == 'still':
                if not self.file:
                    self.file = os.path.join(OUT, 'stills', '%s_%s.png' % (st[1], st[2]))
                    if os.path.exists(self.file):
                        os.remove(self.file)
                    u.SystemLibrary.execute_console_command(gw, 'HighResShot 1920x1080 filename=%s' % self.file.replace('\\', '/')); self.req = now
                elif os.path.exists(self.file) and os.path.getsize(self.file) > 0 and now - self.req > 0.5:
                    cm = u.GameplayStatics.get_player_camera_manager(gw, 0); c = cm.get_camera_location(); r = cm.get_camera_rotation()
                    LOG['stills'].append({'name': '%s_%s' % (st[1], st[2]), 'cam': [round(c.x, 1), round(c.y, 1), round(c.z, 1)], 'rot': [round(r.pitch, 2), round(r.yaw, 2)]})
                    self.file = None; self.i += 1; self.t = now; self.status('running')
                elif now - self.req > 30:
                    raise RuntimeError('HighResShot timeout')
        except Exception as ex:
            LOG['errors'].append(repr(ex)); self.finish()

    def finish(self):
        u.unregister_slate_post_tick_callback(self.handle); builtins.STATIONS_ACTIVE = None
        if E.get_game_world() is not None:
            L.editor_request_end_play()
        SL = u.EditorLoadingAndSavingUtils
        LOG['dirty_after'] = sorted([p.get_name() for p in SL.get_dirty_content_packages()] + [p.get_name() for p in SL.get_dirty_map_packages()])
        LOG['finished'] = time.strftime('%Y-%m-%d %H:%M:%S')
        json.dump(LOG, open(os.path.join(OUT, 'stations_log.json'), 'w'), indent=1, default=str)
        self.status('done' if not LOG['errors'] else 'error')


PS()
print('STATIONS started', OUT, len(PLAN))
