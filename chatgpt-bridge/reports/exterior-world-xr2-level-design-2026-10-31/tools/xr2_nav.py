"""xr2_nav.py: player-view navigation test (no guide line, no auto-steering, no markers).
A PIE session stays open; each control job queues ONE command and returns; the tick executes it and writes nav_status.json.
  builtins.XR2_NAV_CMD = ('start', x, y, yaw)     pie job: begin PIE, place the pawn (setup), face yaw
  builtins.XR2_NAV_CMD = ('look', tag)            three player-camera stills at the current spot: yaw-55 / yaw / yaw+55 (what a player
                                                  sees when glancing around), 1600x900, plus the pawn state
  builtins.XR2_NAV_CMD = ('go', yaw, metres)      hold W along a chosen heading (the decision is made from the stills only), with the
                                                  same intent-preserving local avoidance as xr2_probe.py (+-35/70/105 deg at a trunk);
                                                  ends at the distance, on BLOCKED or on timeout; the camera then faces the heading
  builtins.XR2_NAV_CMD = ('turn', yaw)            rotate the view only
  builtins.XR2_NAV_CMD = ('cmd', 'viewmode lightingonly')  console command in the running PIE
  builtins.XR2_NAV_CMD = ('stop',)                end PIE
Log: <OUT>/nav_log.json (every command, pawn path, results). Global time dilation 3 during 'go' only."""
import unreal as u, json, os, time, builtins, math

OUT = builtins.XR2_NAV_OUT
os.makedirs(OUT, exist_ok=True)
E = u.get_editor_subsystem(u.UnrealEditorSubsystem); L = u.get_editor_subsystem(u.LevelEditorSubsystem)


class NAV:
    def __init__(self):
        self.log = json.load(open(os.path.join(OUT, 'nav_log.json'))) if os.path.exists(os.path.join(OUT, 'nav_log.json')) else {'steps': []}
        self.cmd = None; self.phase = None; self.h = u.register_slate_post_tick_callback(self.tick); self.yaw = 0.0; self.n = len(self.log['steps'])

    def status(self, s, extra=None):
        d = {'state': s, 'n': self.n, 'cmd': list(self.cmd) if self.cmd else None}
        if extra: d.update(extra)
        json.dump(d, open(os.path.join(OUT, 'nav_status.json'), 'w'))

    def save(self):
        json.dump(self.log, open(os.path.join(OUT, 'nav_log.json'), 'w'), indent=1)

    def queue(self, c):
        self.cmd = c; self.phase = 'begin'; self.t = time.monotonic(); self.status('busy')

    def c(self, s):
        u.SystemLibrary.execute_console_command(self.gw, s)

    def ground(self, x, y):
        ifa = [a for a in u.GameplayStatics.get_all_actors_of_class(self.gw, u.Actor) if a.get_class().get_name() == 'InstancedFoliageActor']
        h = u.SystemLibrary.line_trace_single(self.gw, u.Vector(x, y, 6000), u.Vector(x, y, -3000), u.TraceTypeQuery.TRACE_TYPE_QUERY1, True, [self.pawn] + ifa, u.DrawDebugTrace.NONE, True)
        t = h.to_tuple() if h else None
        return t[4].z if t and t[0] else 300.0

    def done(self, rec):
        self.n += 1; rec['k'] = self.n; self.log['steps'].append(rec); self.save(); self.cmd = None; self.status('ready', {'last': rec})

    def tick(self, dt):
        if not self.cmd:
            return
        try:
            now = time.monotonic(); self.gw = E.get_game_world(); k = self.cmd[0]
            if k == 'start':
                if self.phase == 'begin':
                    if self.gw is None:
                        L.editor_request_begin_play(); self.phase = 'wait'; return
                    self.phase = 'wait'
                if self.gw is None:
                    if now - self.t > 60: raise RuntimeError('PIE did not start')
                    return
                self.pawn = u.GameplayStatics.get_player_pawn(self.gw, 0); self.pc = u.GameplayStatics.get_player_controller(self.gw, 0)
                if not self.pawn: return
                if self.phase == 'wait':
                    cap = self.pawn.get_component_by_class(u.CapsuleComponent); self.hh = cap.get_scaled_capsule_half_height()
                    x, y, yaw = self.cmd[1:4]; self.yaw = yaw
                    self.pawn.set_actor_location(u.Vector(x, y, self.ground(x, y) + self.hh + 3), False, True)
                    self.pawn.set_actor_rotation(u.Rotator(pitch=0, yaw=yaw, roll=0), True); self.pc.set_control_rotation(u.Rotator(pitch=-8, yaw=yaw, roll=0))
                    self.phase = 'settle'; self.t = now; return
                if now - self.t > 3.0:
                    p = self.pawn.get_actor_location(); self.done({'cmd': 'start', 'pawn': [round(p.x), round(p.y), round(p.z)], 'yaw': self.yaw})
                return
            if self.gw is None:
                raise RuntimeError('PIE not running')
            if k == 'cmd':
                self.c(self.cmd[1]); return self.done({'cmd': 'cmd', 'console': self.cmd[1]})
            if k == 'turn':
                self.yaw = float(self.cmd[1]); self.pc.set_control_rotation(u.Rotator(pitch=-8, yaw=self.yaw, roll=0))
                if self.phase == 'begin': self.phase = 'w'; self.t = now; return
                if now - self.t > 1.5:
                    self.done({'cmd': 'turn', 'yaw': self.yaw})
                return
            if k == 'look':
                if self.phase == 'begin':
                    self.shots = [(-55, 'L'), (0, 'C'), (55, 'R')]; self.si = 0; self.phase = 'aim'; self.file = None; self.files = []; return
                if self.phase == 'aim':
                    if self.si >= len(self.shots):
                        self.pc.set_control_rotation(u.Rotator(pitch=-8, yaw=self.yaw, roll=0))
                        p = self.pawn.get_actor_location()
                        return self.done({'cmd': 'look', 'tag': self.cmd[1], 'pawn': [round(p.x), round(p.y), round(p.z)], 'yaw': self.yaw, 'files': self.files})
                    off, nm = self.shots[self.si]; self.pc.set_control_rotation(u.Rotator(pitch=-8, yaw=self.yaw + off, roll=0))
                    self.phase = 'hold'; self.t = now; return
                if self.phase == 'hold':
                    off, nm = self.shots[self.si]; self.pc.set_control_rotation(u.Rotator(pitch=-8, yaw=self.yaw + off, roll=0))
                    if now - self.t < 2.0: return
                    if not self.file:
                        self.file = os.path.join(OUT, 'nav%02d_%s_%s.png' % (self.n + 1, self.cmd[1], nm))
                        if os.path.exists(self.file): os.remove(self.file)
                        self.c('HighResShot 1600x900 filename=%s' % self.file.replace('\\', '/')); self.req = now; return
                    if os.path.exists(self.file) and os.path.getsize(self.file) > 0 and now - self.req > 0.5:
                        self.files.append(os.path.basename(self.file)); self.file = None; self.si += 1; self.phase = 'aim'
                    elif now - self.req > 30:
                        raise RuntimeError('HighResShot timeout')
                return
            if k == 'go':
                g = u.GameplayStatics.get_time_seconds(self.gw)
                if self.phase == 'begin':
                    self.yaw = float(self.cmd[1]); p = self.pawn.get_actor_location(); self.s0 = (p.x, p.y, p.z)
                    self.pc.set_control_rotation(u.Rotator(pitch=-8, yaw=self.yaw, roll=0)); u.GameplayStatics.set_global_time_dilation(self.gw, 3.0)
                    self.c('Input.+key W true'); self.g0 = g; self.hist = [(g, 0.0)]; self.avoid = None; self.enc = None; self.av = 0; self.path = []; self.best = 0.0
                    self.phase = 'move'; self.lr = -1; return
                p = self.pawn.get_actor_location(); t = g - self.g0
                hx, hy = math.cos(math.radians(self.yaw)), math.sin(math.radians(self.yaw))
                along = (p.x - self.s0[0]) * hx + (p.y - self.s0[1]) * hy; self.best = max(self.best, along)
                if t - self.lr >= 0.25: self.path.append([round(p.x), round(p.y), round(p.z)]); self.lr = t
                self.hist.append((g, along)); self.hist = [h_ for h_ in self.hist if g - h_[0] <= 0.9]
                res = None
                if self.avoid and g >= self.avoid[1]:
                    self.avoid = None; self.pc.set_control_rotation(u.Rotator(pitch=-8, yaw=self.yaw, roll=0))
                elif not self.avoid and t > 1.2 and g - self.hist[0][0] >= 0.55 and along - self.hist[0][1] < 15:
                    if self.enc is None or along - self.enc[0] > 120: self.enc = [along, 0]
                    DEF = (35, -35, 70, -70, 105, -105)
                    if self.enc[1] >= len(DEF): res = 'BLOCKED'
                    else:
                        a = DEF[self.enc[1]]; self.enc[1] += 1; self.av += 1; self.avoid = (a, g + 1.2); self.hist = [(g, along)]
                        self.pc.set_control_rotation(u.Rotator(pitch=-8, yaw=self.yaw + a, roll=0))
                if not res and along >= self.cmd[2] * 100: res = 'REACHED'
                if not res and t > self.cmd[2] / 0.9 + 15: res = 'TIMEOUT'
                if res:
                    self.c('Input.-key W'); u.GameplayStatics.set_global_time_dilation(self.gw, 1.0)
                    self.pc.set_control_rotation(u.Rotator(pitch=-8, yaw=self.yaw, roll=0))
                    self.done({'cmd': 'go', 'yaw': self.yaw, 'want_m': self.cmd[2], 'result': res, 'progress_m': round(self.best / 100, 1), 'avoids': self.av,
                               'start': [round(v) for v in self.s0], 'end': [round(p.x), round(p.y), round(p.z)], 'game_s': round(t, 1), 'path': self.path})
                return
            if k == 'stop':
                L.editor_request_end_play(); u.unregister_slate_post_tick_callback(self.h); builtins.XR2_NAV = None
                self.n += 1; self.log['steps'].append({'cmd': 'stop', 'k': self.n}); self.save(); self.cmd = None; self.status('stopped'); return
        except Exception as ex:
            self.log.setdefault('errors', []).append(repr(ex)); self.save(); self.cmd = None; self.status('error', {'err': repr(ex)})


if getattr(builtins, 'XR2_NAV', None) is None:
    builtins.XR2_NAV = NAV()
builtins.XR2_NAV.queue(tuple(builtins.XR2_NAV_CMD))
print('XR2_NAV queued', builtins.XR2_NAV_CMD)
