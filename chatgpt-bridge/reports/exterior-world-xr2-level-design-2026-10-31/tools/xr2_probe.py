"""xr2_probe.py (pie job, runtime only, nothing saved): free-movement permeability probes for the XR2 exterior level-design test.

Every probe is real player input, no steering: the pawn is placed at a start point (setup teleport, ground trace that ignores foliage),
the control yaw is set ONCE to a fixed heading, then W is held through the player's mapping context (Input.+key W -> IA_Move, walk gait)
and nothing corrects the direction. The capsule slides along whatever it meets exactly as a player holding forward would.
A probe ends when the pawn is `dist` metres from its start (ESCAPED / reached), when it stalls (horizontal speed < 25 cm/s for 0.8 s of
game time after a 1.2 s start), or on a game-time timeout. At a stall the blocker is identified with forward capsule-height sweeps
(knee 40 cm / chest 120 cm above the feet: actor label + component + mesh) and the slope under the pawn.
Global time dilation XR2_DIL (default 3) only speeds the test up; the movement is the production walk.

builtins:
  XR2_PROBES  [{'name', 'start': [x_cm, y_cm], 'yaw': deg (0 = +X east, 90 = +Y south), 'dist': m, 'set': 'boundary'|'lateral'|...}]
  XR2_OUT     output directory (probe_log.json, probe_status.json)
  XR2_CMDS    console commands run once when the pawn exists
Output per probe: start/end, straight distance from start, path length, game time, mean speed, result, blocker, path (every 0.25 s)."""
import unreal as u, json, os, time, builtins, math

OUT = builtins.XR2_OUT
PROBES = list(builtins.XR2_PROBES)
CMDS = list(getattr(builtins, 'XR2_CMDS', []))
DIL = float(getattr(builtins, 'XR2_DIL', 3.0))
os.makedirs(OUT, exist_ok=True)
E = u.get_editor_subsystem(u.UnrealEditorSubsystem)
L = u.get_editor_subsystem(u.LevelEditorSubsystem)
if E.get_game_world() is not None:
    raise RuntimeError('PIE already running')
if getattr(builtins, 'XR2_PROBE_ACTIVE', None):
    raise RuntimeError('probe already running')
SL = u.EditorLoadingAndSavingUtils
dirty = lambda: sorted([p.get_name() for p in SL.get_dirty_content_packages()] + [p.get_name() for p in SL.get_dirty_map_packages()])
LOG = {'started': time.strftime('%Y-%m-%d %H:%M:%S'), 'dilation': DIL, 'dirty_before': dirty(), 'probes': [], 'errors': []}


class PR:
    def __init__(self):
        self.k, self.phase, self.t0 = 0, 'start', time.monotonic()
        self.handle = u.register_slate_post_tick_callback(self.tick)
        builtins.XR2_PROBE_ACTIVE = self
        L.editor_request_begin_play()

    def status(self, s):
        json.dump({'state': s, 'probe': self.k, 'of': len(PROBES), 'errors': LOG['errors']}, open(os.path.join(OUT, 'probe_status.json'), 'w'))

    def cmd(self, c):
        u.SystemLibrary.execute_console_command(self.gw, c)

    def ground(self, x, y):
        ifa = [a for a in u.GameplayStatics.get_all_actors_of_class(self.gw, u.Actor) if a.get_class().get_name() == 'InstancedFoliageActor']
        h = u.SystemLibrary.line_trace_single(self.gw, u.Vector(x, y, 6000), u.Vector(x, y, -3000), u.TraceTypeQuery.TRACE_TYPE_QUERY1, True,
                                              [self.pawn] + ifa, u.DrawDebugTrace.NONE, True)
        t = h.to_tuple() if h else None
        return t[4].z if t and t[0] else None

    def blocker(self):
        p = self.pawn.get_actor_location(); yaw = math.radians(self.yaw); out = {}
        for nm, dz in (('knee', -self.hh + 40), ('chest', -self.hh + 120)):
            a = u.Vector(p.x, p.y, p.z + dz); b = u.Vector(p.x + math.cos(yaw) * 120, p.y + math.sin(yaw) * 120, p.z + dz)
            h = u.SystemLibrary.sphere_trace_single(self.gw, a, b, 20.0, u.TraceTypeQuery.TRACE_TYPE_QUERY1, False, [self.pawn], u.DrawDebugTrace.NONE, True)
            t = h.to_tuple() if h else None
            if t and t[0]:
                act, comp = t[9], t[10]
                mesh = None
                try:
                    mesh = comp.static_mesh.get_name() if comp and hasattr(comp, 'static_mesh') and comp.static_mesh else None
                except Exception:
                    pass
                out[nm] = {'dist': round(t[3], 1), 'actor': act.get_actor_label() if act else None, 'comp': comp.get_name() if comp else None,
                           'mesh': mesh, 'normal_z': round(t[7].z, 3)}
        g = [self.ground(p.x + dx, p.y + dy) for dx, dy in ((60, 0), (-60, 0), (0, 60), (0, -60))]
        if None not in g:
            out['slope_deg'] = round(math.degrees(math.atan(math.hypot(g[0] - g[1], g[2] - g[3]) / 120.0)), 1)
        return out

    def tick(self, dt):
        try:
            now = time.monotonic(); self.gw = E.get_game_world(); gw = self.gw
            if self.phase == 'start':
                if gw is None:
                    if now - self.t0 > 60:
                        raise RuntimeError('PIE did not start')
                    return
                self.pawn = u.GameplayStatics.get_player_pawn(gw, 0); self.pc = u.GameplayStatics.get_player_controller(gw, 0)
                if not self.pawn:
                    return
                cap = self.pawn.get_component_by_class(u.CapsuleComponent)
                self.hh = cap.get_scaled_capsule_half_height() if cap else 90.0
                LOG['capsule'] = [cap.get_scaled_capsule_radius(), self.hh] if cap else None
                for c in CMDS:
                    self.cmd(c)
                u.GameplayStatics.set_global_time_dilation(gw, DIL)
                self.phase = 'place'; self.status('running'); return
            if gw is None:
                raise RuntimeError('PIE ended early at probe %d' % self.k)
            if self.k >= len(PROBES):
                return self.finish()
            pr = PROBES[self.k]; g = u.GameplayStatics.get_time_seconds(gw)
            if self.phase == 'place':
                x, y = pr['start']; gz = self.ground(x, y)
                self.pawn.set_actor_location(u.Vector(x, y, (gz if gz is not None else 300) + self.hh + 3), False, True)
                self.yaw = float(pr['yaw'])
                self.pawn.set_actor_rotation(u.Rotator(pitch=0, yaw=self.yaw, roll=0), True)
                self.pc.set_control_rotation(u.Rotator(pitch=-8.0, yaw=self.yaw, roll=0))
                self.g0 = g; self.phase = 'settle'; return
            if self.phase == 'settle':
                if g - self.g0 >= 1.0 * DIL:
                    p = self.pawn.get_actor_location()
                    self.rec = {'name': pr['name'], 'set': pr.get('set'), 'start': [round(p.x), round(p.y), round(p.z)], 'yaw': self.yaw, 'dist_target_m': pr['dist'],
                                'path': [], 'plen_cm': 0.0}
                    self.last = (p.x, p.y); self.gs = g; self.lastrec = -1.0
                    self.hist = [(g, 0.0)]; self.avoid = None; self.enc = None; self.rec['avoids'] = 0; self.best = 0.0
                    self.pc.set_control_rotation(u.Rotator(pitch=-8.0, yaw=self.yaw, roll=0))
                    self.cmd('Input.+key W true'); self.phase = 'move'
                return
            if self.phase == 'move':
                # intent-preserving local avoidance (what a player holding one direction does at a trunk or rock): when progress
                # along the intended heading stalls (< 15 cm in 0.6 s game), deflect +-35 / +-70 / +-105 deg for 1.2 s, then resume the
                # heading. BLOCKED = the whole deflection cycle of one encounter gains < 50 cm along the heading.
                p = self.pawn.get_actor_location(); v = self.pawn.get_velocity(); hs = math.hypot(v.x, v.y); t = g - self.gs
                self.rec['plen_cm'] += math.hypot(p.x - self.last[0], p.y - self.last[1]); self.last = (p.x, p.y)
                if t - self.lastrec >= 0.25:
                    self.rec['path'].append([round(p.x), round(p.y), round(p.z), round(hs)]); self.lastrec = t
                hx, hy = math.cos(math.radians(self.yaw)), math.sin(math.radians(self.yaw))
                along = (p.x - self.rec['start'][0]) * hx + (p.y - self.rec['start'][1]) * hy; self.best = max(self.best, along)
                d = math.hypot(p.x - self.rec['start'][0], p.y - self.rec['start'][1])
                self.hist.append((g, along)); self.hist = [h for h in self.hist if g - h[0] <= 0.9]
                res = None
                if self.avoid and g >= self.avoid[1]:
                    self.avoid = None; self.pc.set_control_rotation(u.Rotator(pitch=-8.0, yaw=self.yaw, roll=0))
                elif not self.avoid and t > 1.2 and g - self.hist[0][0] >= 0.55 and along - self.hist[0][1] < 15:
                    if self.enc is None or along - self.enc[0] > 120:
                        self.enc = [along, 0]          # new obstacle encounter
                    DEF = (35, -35, 70, -70, 105, -105)
                    if self.enc[1] >= len(DEF):
                        res = 'BLOCKED'
                    else:
                        a = DEF[self.enc[1]]; self.enc[1] += 1; self.rec['avoids'] += 1
                        self.avoid = (a, g + 1.2); self.hist = [(g, along)]
                        self.pc.set_control_rotation(u.Rotator(pitch=-8.0, yaw=self.yaw + a, roll=0))
                if res:
                    pass
                elif along >= pr['dist'] * 100:
                    res = 'REACHED'
                elif t > pr['dist'] / 0.9 + 20:
                    res = 'TIMEOUT'
                elif p.z < self.rec['start'][2] - 3000:
                    res = 'FELL'
                if res:
                    self.rec.update({'result': res, 'end': [round(p.x), round(p.y), round(p.z)], 'straight_m': round(d / 100, 2), 'path_m': round(self.rec['plen_cm'] / 100, 2),
                                     'progress_m': round(self.best / 100, 2), 'game_s': round(t, 2), 'mean_speed': round(self.rec['plen_cm'] / max(t, 0.01), 1)})
                    if res != 'REACHED':
                        self.rec['blocker'] = self.blocker()
                    self.cmd('Input.-key W'); LOG['probes'].append(self.rec); self.k += 1; self.phase = 'place'
                    json.dump(LOG, open(os.path.join(OUT, 'probe_log.json'), 'w'), default=str); self.status('running')
        except Exception as ex:
            LOG['errors'].append(repr(ex)); self.finish()

    def finish(self):
        u.unregister_slate_post_tick_callback(self.handle)
        builtins.XR2_PROBE_ACTIVE = None
        gw = E.get_game_world()
        try:
            if gw:
                u.SystemLibrary.execute_console_command(gw, 'Input.-key W')
                u.GameplayStatics.set_global_time_dilation(gw, 1.0)
        except Exception as ex:
            LOG['errors'].append('cleanup ' + repr(ex))
        if gw is not None:
            L.editor_request_end_play()
        LOG['dirty_after'] = dirty(); LOG['finished'] = time.strftime('%Y-%m-%d %H:%M:%S')
        json.dump(LOG, open(os.path.join(OUT, 'probe_log.json'), 'w'), indent=1, default=str)
        self.status('done' if not LOG['errors'] else 'error')


PR()
print('XR2_PROBE started', len(PROBES))
