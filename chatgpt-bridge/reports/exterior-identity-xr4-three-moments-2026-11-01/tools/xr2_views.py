"""xr2_views.py (pie job, runtime only): player-camera stills at the XR2 decision points (same poses BEFORE / AFTER, clay / lit).
Each view places the pawn (setup teleport onto the ground, foliage ignored by the trace), sets the control rotation, waits for the
GraceRanger camera to settle and takes HighResShot 1920x1080 through the real player camera (FOV / boom / collision as in game).
builtins: XR2_VIEWS [{'name', 'pawn': [x, y], 'yaw', 'pitch'}], XR2_OUT (stills dir, no spaces), XR2_CMDS (console commands once the pawn
exists, e.g. 'viewmode lightingonly'; 'viewmode lit' is restored at the end). Output: <OUT>/<name>.png, <OUT>/views_log.json, views_status.json"""
import unreal as u, json, os, time, builtins, math

OUT = builtins.XR2_OUT; VIEWS = list(builtins.XR2_VIEWS); CMDS = list(getattr(builtins, 'XR2_CMDS', []))
os.makedirs(OUT, exist_ok=True)
E = u.get_editor_subsystem(u.UnrealEditorSubsystem); L = u.get_editor_subsystem(u.LevelEditorSubsystem)
if E.get_game_world() is not None:
    raise RuntimeError('PIE already running')
LOG = {'started': time.strftime('%Y-%m-%d %H:%M:%S'), 'views': [], 'errors': [], 'cmds': CMDS}


class VW:
    def __init__(self):
        self.k, self.phase, self.t0, self.file = 0, 'start', time.monotonic(), None
        self.h = u.register_slate_post_tick_callback(self.tick); L.editor_request_begin_play()

    def status(self, s):
        json.dump({'state': s, 'view': self.k, 'of': len(VIEWS), 'errors': LOG['errors']}, open(os.path.join(OUT, 'views_status.json'), 'w'))

    def tick(self, dt):
        try:
            now = time.monotonic(); gw = E.get_game_world()
            if self.phase == 'start':
                if gw is None:
                    if now - self.t0 > 60: raise RuntimeError('PIE did not start')
                    return
                self.pawn = u.GameplayStatics.get_player_pawn(gw, 0); self.pc = u.GameplayStatics.get_player_controller(gw, 0)
                if not self.pawn: return
                cap = self.pawn.get_component_by_class(u.CapsuleComponent); self.hh = cap.get_scaled_capsule_half_height() if cap else 90.0
                for c in CMDS: u.SystemLibrary.execute_console_command(gw, c)
                self.phase = 'place'; self.t = now; self.status('running'); return
            if gw is None: raise RuntimeError('PIE ended early')
            if self.k >= len(VIEWS): return self.finish()
            v = VIEWS[self.k]
            if self.phase == 'place':
                if now - self.t < 1.0: return
                x, y = v['pawn']
                ifa = [a for a in u.GameplayStatics.get_all_actors_of_class(gw, u.Actor) if a.get_class().get_name() == 'InstancedFoliageActor']
                # ground = the first hit that is not a spawned tree / plant / prop (XR3/XR4 pine swaps and spruces are actors, not foliage):
                # rocks and ledges count as ground, so a station on a ledge block stands on it
                hs = u.SystemLibrary.line_trace_multi(gw, u.Vector(x, y, 6000), u.Vector(x, y, -3000), u.TraceTypeQuery.TRACE_TYPE_QUERY1, True, [self.pawn] + ifa, u.DrawDebugTrace.NONE, True)
                gz = 300.0
                for h in (hs or []):
                    t = h.to_tuple()
                    if not t[0]: continue
                    lab = t[9].get_actor_label() if t[9] else ''
                    if lab.startswith(('XR2_Dress', 'XR3_', 'XR4_')) and not any(k in lab for k in ('Ledge', 'Talus', 'Rock', 'Stone', 'Outcrop', 'Bank', 'Arc')):
                        continue
                    gz = t[4].z; break
                self.pawn.set_actor_location(u.Vector(x, y, gz + self.hh + 3), False, True)
                self.pawn.set_actor_rotation(u.Rotator(pitch=0, yaw=v['yaw'], roll=0), True)
                self.pc.set_control_rotation(u.Rotator(pitch=v.get('pitch', -6.0), yaw=v['yaw'], roll=0))
                self.phase = 'wait'; self.t = now; return
            if self.phase == 'wait':
                self.pc.set_control_rotation(u.Rotator(pitch=v.get('pitch', -6.0), yaw=v['yaw'], roll=0))
                if now - self.t >= 3.0: self.phase = 'shot'
                return
            if self.phase == 'shot':
                if not self.file:
                    self.file = os.path.join(OUT, v['name'] + '.png')
                    if os.path.exists(self.file): os.remove(self.file)
                    u.SystemLibrary.execute_console_command(gw, 'HighResShot 1920x1080 filename=%s' % self.file.replace('\\', '/')); self.req = now
                elif os.path.exists(self.file) and os.path.getsize(self.file) > 0 and now - self.req > 0.5:
                    cm = u.GameplayStatics.get_player_camera_manager(gw, 0); c = cm.get_camera_location(); r = cm.get_camera_rotation(); p = self.pawn.get_actor_location()
                    LOG['views'].append({'name': v['name'], 'cam': [round(c.x), round(c.y), round(c.z)], 'cam_rot': [round(r.pitch, 1), round(r.yaw, 1)],
                                         'pawn': [round(p.x), round(p.y), round(p.z)], 'fov': round(cm.get_fov_angle(), 1)})
                    self.file = None; self.k += 1; self.phase = 'place'; self.t = now; self.status('running')
                elif now - self.req > 30:
                    raise RuntimeError('HighResShot timeout ' + v['name'])
        except Exception as ex:
            LOG['errors'].append(repr(ex)); self.finish()

    def finish(self):
        u.unregister_slate_post_tick_callback(self.h); gw = E.get_game_world()
        try:
            if gw and CMDS: u.SystemLibrary.execute_console_command(gw, 'viewmode lit')
        except Exception as ex:
            LOG['errors'].append('cleanup ' + repr(ex))
        if gw is not None: L.editor_request_end_play()
        LOG['finished'] = time.strftime('%Y-%m-%d %H:%M:%S')
        json.dump(LOG, open(os.path.join(OUT, 'views_log.json'), 'w'), indent=1); self.status('done' if not LOG['errors'] else 'error')


VW()
print('XR2_VIEWS started', len(VIEWS))
