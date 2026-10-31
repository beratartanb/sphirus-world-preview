"""Player-camera stills (pie job): start PIE with the existing game mode / pawn / GraceRanger camera, teleport the pawn to three
stations (house front, pond, forest; pawn placed on the ground at the T1 camera xy, facing the T1 view yaw), and for each station
set the control rotation to forward / left90 / right90 / lookback and take HighResShot 1920x1080 through the real player camera.
Runtime-only: pawn location and control rotation in the PIE world. No asset, ABP default, cvar, config or map is changed, nothing is saved.
NOTE: PIE runs whatever is loaded in memory (the two dirty ABPs hold V2.40 candidate knob values; see abp_inspect.json).
Output: <OUT>/pie/*.png, <OUT>/pie_log.json, <OUT>/pie_status.json
"""
import unreal as u, json, os, time, builtins

OUT = r'C:\Users\berat\AppData\Local\Temp\claude\C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS\5f49a232-b001-47ad-8881-1eb04d9cb1c5\scratchpad\t1b'
STATIONS = {  # xy and yaw from the T1 views (Bridge camera_plan 2026-09-25); pawn stands on the traced ground
    'house_front': (-1550, 2460, -36.830867829324454),
    'pond':        (1500, 2810, 130.80909247267473),
    'forest':      (2200, 1580, -77.14368743247138),
}
DIRS = [('forward', 0), ('left90', -90), ('right90', 90), ('lookback', 180)]
SETTLE_TP, SETTLE_DIR = 8.0, 4.0
if getattr(builtins, 'PIECAM_ACTIVE', None):
    raise RuntimeError('pie_cam already running')
os.makedirs(os.path.join(OUT, 'pie'), exist_ok=True)
E = u.get_editor_subsystem(u.UnrealEditorSubsystem)
L = u.get_editor_subsystem(u.LevelEditorSubsystem)
if E.get_game_world() is not None:
    raise RuntimeError('PIE already running')
S = u.EditorLoadingAndSavingUtils
dirty = lambda: sorted([p.get_name() for p in S.get_dirty_content_packages()] + [p.get_name() for p in S.get_dirty_map_packages()])
LOG = {'started': time.strftime('%Y-%m-%d %H:%M:%S'), 'stations': STATIONS, 'dirs': DIRS, 'dirty_before': dirty(), 'shots': [], 'errors': [], 'events': []}
PLAN = []
for s in STATIONS:
    PLAN.append(('tp', s))
    PLAN.append(('wait', SETTLE_TP))
    for d, off in DIRS:
        PLAN += [('rot', s, d, off), ('wait', SETTLE_DIR), ('shot', s, d)]


class PieCam:
    def __init__(self):
        self.i, self.t, self.phase, self.t0 = 0, time.monotonic(), 'start', time.monotonic()
        self.handle = u.register_slate_post_tick_callback(self.tick)
        builtins.PIECAM_ACTIVE = self
        L.editor_request_begin_play()

    def status(self, s):
        json.dump({'state': s, 'step': self.i, 'of': len(PLAN), 'shots': len(LOG['shots']), 'errors': LOG['errors']}, open(os.path.join(OUT, 'pie_status.json'), 'w'))

    def tick(self, dt):
        try:
            now = time.monotonic()
            gw = E.get_game_world()
            if self.phase == 'start':
                if gw is None:
                    if now - self.t0 > 60:
                        raise RuntimeError('PIE did not start')
                    return
                self.pawn = u.GameplayStatics.get_player_pawn(gw, 0); self.pc = u.GameplayStatics.get_player_controller(gw, 0)
                if not self.pawn:
                    return
                cm = u.GameplayStatics.get_player_camera_manager(gw, 0)
                LOG['pawn_class'] = self.pawn.get_class().get_path_name()
                LOG['camera_manager'] = cm.get_class().get_path_name() if cm else None
                LOG['view_target'] = self.pc.get_view_target().get_class().get_path_name() if self.pc.get_view_target() else None
                self.phase = 'run'; self.t = now; self.status('running')
                return
            if gw is None:
                raise RuntimeError('PIE ended early at step %d' % self.i)
            if self.i >= len(PLAN):
                return self.finish()
            st = PLAN[self.i]
            if st[0] == 'tp':
                x, y, yaw = STATIONS[st[1]]
                hit = u.SystemLibrary.line_trace_single(gw, u.Vector(x, y, 3000), u.Vector(x, y, -3000), u.TraceTypeQuery.TRACE_TYPE_QUERY1,
                                                        False, [self.pawn], u.DrawDebugTrace.NONE, True)
                hr = hit.to_tuple() if hit else None
                gz = hr[4].z if hr and hr[0] else 0.0
                cap = self.pawn.get_component_by_class(u.CapsuleComponent)
                hh = cap.get_scaled_capsule_half_height() if cap else 90.0
                ok = self.pawn.set_actor_location(u.Vector(x, y, gz + hh + 2), False, True)
                self.pc.set_control_rotation(u.Rotator(pitch=0, yaw=yaw, roll=0))
                LOG['events'].append({'station': st[1], 'ground_z': round(gz, 1), 'ground_hit_actor': (hr[9].get_actor_label() if hr and hr[0] and hr[9] else None),
                                      'capsule_half_height': hh, 'teleport_ok': bool(ok), 'session_s': round(now - self.t0, 2)})
                self.i += 1; self.t = now
            elif st[0] == 'rot':
                yaw = STATIONS[st[1]][2] + st[3]
                self.pc.set_control_rotation(u.Rotator(pitch=-5.0, yaw=yaw, roll=0))
                self.i += 1; self.t = now
            elif st[0] == 'wait':
                if now - self.t >= st[1]:
                    self.i += 1; self.t = now
            elif st[0] == 'shot':
                if not getattr(self, 'file', None):
                    self.file = os.path.join(OUT, 'pie', 'player_%s__%s.png' % (st[1], st[2]))
                    if os.path.exists(self.file):
                        os.remove(self.file)
                    u.SystemLibrary.execute_console_command(gw, 'HighResShot 1920x1080 filename=%s' % self.file.replace('\\', '/'))
                    self.req = now
                elif os.path.exists(self.file) and os.path.getsize(self.file) > 0 and now - self.req > 0.5:
                    cm = u.GameplayStatics.get_player_camera_manager(gw, 0)
                    pl = self.pawn.get_actor_location(); cl = cm.get_camera_location(); cr = cm.get_camera_rotation()
                    LOG['shots'].append({'station': st[1], 'dir': st[2], 'file': os.path.basename(self.file), 'session_s': round(now - self.t0, 2),
                                         'camera_fov': round(cm.get_fov_angle(), 2), 'camera_loc': [round(cl.x, 1), round(cl.y, 1), round(cl.z, 1)],
                                         'camera_rot_pyr': [round(cr.pitch, 2), round(cr.yaw, 2), round(cr.roll, 2)],
                                         'pawn_loc': [round(pl.x, 1), round(pl.y, 1), round(pl.z, 1)],
                                         'camera_to_pawn_cm': round(((cl.x - pl.x) ** 2 + (cl.y - pl.y) ** 2 + (cl.z - pl.z) ** 2) ** 0.5, 1),
                                         'pawn_speed': round(self.pawn.get_velocity().length(), 1)})
                    self.file = None; self.i += 1; self.t = now; self.status('running')
                elif now - self.req > 30:
                    raise RuntimeError('HighResShot timeout %s' % self.file)
        except Exception as ex:
            LOG['errors'].append(repr(ex)); self.finish()

    def finish(self):
        u.unregister_slate_post_tick_callback(self.handle)
        builtins.PIECAM_ACTIVE = None
        if E.get_game_world() is not None:
            L.editor_request_end_play()
        LOG['dirty_after_pie_request_end'] = dirty()
        LOG['finished'] = time.strftime('%Y-%m-%d %H:%M:%S')
        json.dump(LOG, open(os.path.join(OUT, 'pie_log.json'), 'w'), indent=1, default=str)
        self.status('done' if not LOG['errors'] else 'error')


PieCam()
print('PIECAM started, steps', len(PLAN))
