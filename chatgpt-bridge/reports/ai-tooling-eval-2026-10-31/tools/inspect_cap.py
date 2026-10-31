"""inspect_cap.py (measure job): fixed editor-viewport inspection shots of the P1 move ORIGINS (where instances are taken from -> holes?)
and TARGETS (compression bank, release tread edges -> crown overlap, ground contact), identical poses for BEFORE / AFTER.
Pose = cluster centroid seen from 8 m on the trail side, eye 2.5 m above the landscape, looking at the centroid ground + 0.8 m.
Same capture call as T1 (take_high_res_screenshot 1920x1080, game view); viewport restored afterwards. Nothing edited or saved.
builtins.INSPECT_TAG selects the output sub-folder. Output: <PILOT>/inspect/<tag>/*.png + inspect_<tag>.json
"""
import unreal as u, json, os, math, time, builtins

PILOT = r'C:\Users\berat\AppData\Local\Temp\claude\C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS\5f49a232-b001-47ad-8881-1eb04d9cb1c5\scratchpad\pilot'
TAG = getattr(builtins, 'INSPECT_TAG', 'before')
OUT = os.path.join(PILOT, 'inspect', TAG); os.makedirs(OUT, exist_ok=True)
VIEWS = {   # name: (cluster centroid xy, camera side point xy)
    'origin_east_uphill': ((3450.0, -3320.0), (2980.0, -2980.0)),
    'origin_west_downhill': ((2116.0, -2557.0), (2700.0, -2650.0)),
    'target_compression_bank': ((3237.0, -2637.0), (2930.0, -2560.0)),
    'target_release_tread': ((2641.0, -2968.0), (2985.0, -2560.0)),
}
if getattr(builtins, 'INSPECT_ACTIVE', None):
    raise RuntimeError('inspect already running')
E = u.get_editor_subsystem(u.UnrealEditorSubsystem); L = u.get_editor_subsystem(u.LevelEditorSubsystem)
if L.is_in_play_in_editor():
    raise RuntimeError('PIE running')
world = E.get_editor_world()
IFA = [a for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors() if a.get_class().get_name() == 'InstancedFoliageActor']


def ground(x, y):
    ign = list(IFA)
    for _ in range(10):
        t = u.SystemLibrary.line_trace_single(world, u.Vector(x, y, 6000), u.Vector(x, y, -3000), u.TraceTypeQuery.TRACE_TYPE_QUERY1, True, ign, u.DrawDebugTrace.NONE, True).to_tuple()
        if not t[0] or t[9] is None:
            return 400.0
        if t[9].get_class().get_name() == 'Landscape':
            return t[4].z
        ign.append(t[9])
    return 400.0


key = L.get_active_viewport_config_key(); pose0, fov0, gv0 = L.get_level_viewport_camera_info(key), L.get_level_viewport_fov(key), L.editor_get_game_view(key)
POSES = {}
for n, (c, side) in VIEWS.items():
    dx, dy = side[0] - c[0], side[1] - c[1]; d = math.hypot(dx, dy); cam = (c[0] + dx / d * 800, c[1] + dy / d * 800)
    cz = ground(*cam) + 250; tz = ground(*c) + 80
    yaw = math.degrees(math.atan2(c[1] - cam[1], c[0] - cam[0])); pitch = math.degrees(math.atan2(tz - cz, 800))
    POSES[n] = ([cam[0], cam[1], cz], [pitch, yaw, 0.0], 75.0)
LOG = {'tag': TAG, 'poses': POSES, 'shots': [], 'errors': []}
PLAN = []
for n in POSES:
    PLAN += [('move', n), ('wait', 6.0), ('shot', n)]


class Insp:
    def __init__(self):
        self.i, self.t, self.task = 0, time.monotonic(), None
        self.handle = u.register_slate_post_tick_callback(self.tick); builtins.INSPECT_ACTIVE = self

    def tick(self, dt):
        try:
            if self.i >= len(PLAN):
                return self.finish()
            st, now = PLAN[self.i], time.monotonic()
            if st[0] == 'move':
                p, r, fov = POSES[st[1]]
                L.editor_set_game_view(True, key); L.set_level_viewport_camera_info(u.Vector(*p), u.Rotator(pitch=r[0], yaw=r[1], roll=0), key)
                L.set_level_viewport_fov(fov, key); L.editor_invalidate_viewports(); self.i += 1; self.t = now
            elif st[0] == 'wait':
                if now - self.t >= st[1]:
                    self.i += 1; self.t = now
            elif st[0] == 'shot':
                if self.task is None:
                    self.file = os.path.join(OUT, '%s.png' % st[1]); self.req = now
                    self.task = u.AutomationLibrary.take_high_res_screenshot(1920, 1080, self.file, delay=0.2, force_game_view=True); self.redraw = None
                elif self.redraw is None and now - self.req > 0.5:
                    self.redraw = u.ToolsetRegistry.execute_tool('EditorToolset.EditorAppToolset', 'CaptureViewport', '{"captureTransform":null,"annotations":null,"bShowUI":false}')
                elif self.task.is_task_done() and os.path.exists(self.file) and os.path.getsize(self.file) > 0:
                    LOG['shots'].append(st[1]); self.task = None; self.i += 1; self.t = now
                elif now - self.req > 45:
                    raise RuntimeError('shot timeout')
        except Exception as ex:
            LOG['errors'].append(repr(ex)); self.finish()

    def finish(self):
        u.unregister_slate_post_tick_callback(self.handle); builtins.INSPECT_ACTIVE = None
        L.set_level_viewport_camera_info(pose0[0], pose0[1], key); L.set_level_viewport_fov(fov0, key); L.editor_set_game_view(gv0, key); L.editor_invalidate_viewports()
        S = u.EditorLoadingAndSavingUtils
        LOG['dirty_after'] = sorted([p.get_name() for p in S.get_dirty_content_packages()] + [p.get_name() for p in S.get_dirty_map_packages()])
        json.dump(LOG, open(os.path.join(PILOT, 'inspect', 'inspect_%s.json' % TAG), 'w'), indent=1)
        json.dump({'state': 'done' if not LOG['errors'] else 'error'}, open(os.path.join(PILOT, 'inspect', 'status_%s.json' % TAG), 'w'))


Insp()
print('INSPECT started', TAG, json.dumps(POSES))
