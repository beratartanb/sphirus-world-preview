"""xr3_board.py (pie job, runtime only, NOTHING touches the map): asset lineup board for art-direction decisions.
Candidate meshes are spawned IN THE GAME WORLD (they vanish with PIE) on a flat plate high above the map (same sun / sky as the level,
no local shadows) and photographed with the real player camera, groups of up to 4 meshes per frame, each group framed by its tallest
member. builtins:
  XR3_GROUPS  [{'name', 'items': [[mesh_path, label, scale], ...]}]   XR3_OUT  stills dir   XR3_CMDS  console commands (e.g. clay)
Output: <OUT>/<group>.png + board_log.json (bounds measured at runtime per mesh)."""
import unreal as u, json, os, time, builtins, math

OUT = builtins.XR3_OUT; GROUPS = list(builtins.XR3_GROUPS); CMDS = list(getattr(builtins, 'XR3_CMDS', []))
os.makedirs(OUT, exist_ok=True)
E = u.get_editor_subsystem(u.UnrealEditorSubsystem); L = u.get_editor_subsystem(u.LevelEditorSubsystem)
if E.get_game_world() is not None:
    raise RuntimeError('PIE already running')
BX, BY, BZ = -20000.0, 20000.0, 6000.0          # plate centre (cm), far outside the play area, above the map
LOG = {'started': time.strftime('%Y-%m-%d %H:%M:%S'), 'groups': [], 'errors': [], 'cmds': CMDS}


class BD:
    def __init__(self):
        self.k, self.phase, self.t0, self.file, self.actors = 0, 'start', time.monotonic(), None, []
        self.h = u.register_slate_post_tick_callback(self.tick); L.editor_request_begin_play()

    def status(self, s):
        json.dump({'state': s, 'group': self.k, 'of': len(GROUPS), 'errors': LOG['errors']}, open(os.path.join(OUT, 'board_status.json'), 'w'))

    def tick(self, dt):
        try:
            now = time.monotonic(); gw = E.get_game_world()
            if self.phase == 'start':
                if gw is None:
                    if now - self.t0 > 60: raise RuntimeError('PIE did not start')
                    return
                self.gw = gw; self.pawn = u.GameplayStatics.get_player_pawn(gw, 0); self.pc = u.GameplayStatics.get_player_controller(gw, 0)
                if not self.pawn: return
                cap = self.pawn.get_component_by_class(u.CapsuleComponent); self.hh = cap.get_scaled_capsule_half_height() if cap else 90.0
                # the plate: a 120 x 40 m cube top at BZ
                cube = u.load_asset('/Engine/BasicShapes/Cube')
                self.plate = self.spawn_sm(cube, u.Vector(BX, BY, BZ - 50), 0, u.Vector(120, 40, 1))
                for c in CMDS: u.SystemLibrary.execute_console_command(gw, c)
                self.phase = 'place'; self.t = now + 1.0; self.status('running'); return
            if gw is None: raise RuntimeError('PIE ended early')
            if self.k >= len(GROUPS): return self.finish()
            g = GROUPS[self.k]
            if self.phase == 'place':
                if now < self.t: return
                for a in self.actors:
                    a.destroy_actor()
                self.actors = []; xs = []; hmax = 100.0; x = BX - 1500.0; rec = {'name': g['name'], 'items': []}
                for mesh, label, sc in g['items']:
                    m = u.load_asset(mesh)
                    if not m:
                        rec['items'].append({'mesh': mesh, 'label': label, 'missing': True}); continue
                    b = m.get_bounds(); w = max(b.box_extent.x, b.box_extent.y) * sc; h = b.box_extent.z * 2 * sc
                    x += w + 150.0
                    a = self.spawn_sm(m, u.Vector(x, BY, BZ - (b.origin.z - b.box_extent.z) * sc), 0.0, u.Vector(sc, sc, sc))
                    self.actors.append(a); xs.append(x); hmax = max(hmax, h); x += w
                    rec['items'].append({'mesh': mesh, 'label': label, 'scale': sc, 'w_m': round(2 * w / 100, 1), 'h_m': round(h / 100, 1), 'x': round(x)})
                if not xs:
                    LOG['groups'].append(rec); self.k += 1; return
                cx = (min(xs) + max(xs)) / 2; span = max(xs) - min(xs) + 400
                dist = max(span / (2 * math.tan(math.radians(30))), hmax / (2 * math.tan(math.radians(20))) , 400.0) + 300.0
                self.pawn.set_actor_location(u.Vector(cx, BY + dist, BZ + self.hh + 2), False, True)
                self.pawn.set_actor_rotation(u.Rotator(pitch=0, yaw=-90, roll=0), True)
                pitch = -math.degrees(math.atan2(hmax * 0.45 - 150, dist))
                self.pc.set_control_rotation(u.Rotator(pitch=max(-25, min(10, pitch + 2)), yaw=-90, roll=0)); self.rot = u.Rotator(pitch=max(-25, min(10, pitch + 2)), yaw=-90, roll=0)
                rec.update({'dist_m': round(dist / 100, 1), 'hmax_m': round(hmax / 100, 1)}); self.rec = rec
                self.phase = 'wait'; self.t = now; return
            if self.phase == 'wait':
                self.pc.set_control_rotation(self.rot)
                if now - self.t >= 2.5: self.phase = 'shot'
                return
            if self.phase == 'shot':
                if not self.file:
                    self.file = os.path.join(OUT, g['name'] + '.png')
                    if os.path.exists(self.file): os.remove(self.file)
                    u.SystemLibrary.execute_console_command(gw, 'HighResShot 1920x1080 filename=%s' % self.file.replace('\\', '/')); self.req = now
                elif os.path.exists(self.file) and os.path.getsize(self.file) > 0 and now - self.req > 0.5:
                    LOG['groups'].append(self.rec); self.file = None; self.k += 1; self.phase = 'place'; self.t = now; self.status('running')
                elif now - self.req > 30:
                    raise RuntimeError('HighResShot timeout ' + g['name'])
        except Exception as ex:
            LOG['errors'].append(repr(ex)); self.finish()

    def spawn_sm(self, mesh, loc, yaw, scale):
        # runtime spawn in the PIE world through the editor actor subsystem (it targets the game world while PIE runs)
        a = u.get_editor_subsystem(u.EditorActorSubsystem).spawn_actor_from_class(u.StaticMeshActor, loc, u.Rotator(pitch=0, yaw=yaw, roll=0))
        if a.get_world() != self.gw:
            raise RuntimeError('spawned into the editor world, not PIE')
        a.set_mobility(u.ComponentMobility.MOVABLE); a.static_mesh_component.set_static_mesh(mesh); a.set_actor_scale3d(scale)
        return a

    def finish(self):
        u.unregister_slate_post_tick_callback(self.h); gw = E.get_game_world()
        try:
            if gw and CMDS: u.SystemLibrary.execute_console_command(gw, 'viewmode lit')
        except Exception as ex:
            LOG['errors'].append('cleanup ' + repr(ex))
        if gw is not None: L.editor_request_end_play()
        LOG['finished'] = time.strftime('%Y-%m-%d %H:%M:%S')
        json.dump(LOG, open(os.path.join(OUT, 'board_log.json'), 'w'), indent=1); self.status('done' if not LOG['errors'] else 'error')


BD()
print('XR3_BOARD started', len(GROUPS))
