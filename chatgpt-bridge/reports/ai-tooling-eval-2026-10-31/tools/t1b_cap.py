"""T1b (measure job): 5-frame median capture sets + REAL reversible scene changes, editor viewport, same poses as T1.

Per view:
  warm   move, settle 12 s, one discarded shot
  S1     5 consecutive shots
  (revisit) move to the next view's pose and back, settle 12 s
  S2     5 shots                                   -> S1 vs S2 = revisit noise, median and single frame
  hide SMALL actor (set_is_temporarily_hidden_in_editor: transient editor visibility, not a property edit), wait 5 s
  S3     5 shots                                   -> S2/S5 vs S3 = a real small change
  unhide SMALL, hide MEDIUM actor, wait 5 s
  S4     5 shots                                   -> S2/S5 vs S4 = a real medium change
  unhide MEDIUM, wait 5 s
  S5     5 shots                                   -> S2 vs S5 = static noise after a restore (scene identical)
Actors are chosen automatically: StaticMeshActor-like, line-of-sight from the camera, projected centre inside the central 70 %,
4-30 m away; SMALL = largest bounds half-extent 25-80 cm, MEDIUM = 90-250 cm. Their projected screen boxes are logged.
Every hidden actor is unhidden in finish() even on error; dirty packages and the actor transform hash are compared before/after.
Output: <OUT>/shots/*.png, <OUT>/t1b_log.json, <OUT>/t1b_status.json
"""
import unreal as u, json, time, os, math, builtins, hashlib

OUT = r'C:\Users\berat\AppData\Local\Temp\claude\C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS\5f49a232-b001-47ad-8881-1eb04d9cb1c5\scratchpad\t1b'
VIEWS = {
    'house_front': ([-1550, 2460, 92.3320484161377], [4.045882564505467, -36.830867829324454, 0], 68),
    'pond':        ([1500, 2810, 152.16795921325684], [-6.110206786658776, 130.80909247267473, 0], 75),
    'forest':      ([2200, 1580, 319.35779571533203], [3.696050782488103, -77.14368743247138, 0], 70),
}
ORDER = list(VIEWS)
W_, H_ = 1920, 1080
SETTLE, CHANGE_WAIT, NSHOT = 12.0, 5.0, 5
SKIP_CLASSES = ('InstancedFoliageActor', 'Landscape', 'LandscapeProxy', 'LandscapeStreamingProxy', 'WaterBodyCustom', 'WaterBodyLake',
                'DirectionalLight', 'SkyLight', 'SkyAtmosphere', 'ExponentialHeightFog', 'PostProcessVolume', 'VolumetricCloud', 'WorldSettings')

if getattr(builtins, 'T1B_ACTIVE', None):
    raise RuntimeError('T1b already running')
os.makedirs(os.path.join(OUT, 'shots'), exist_ok=True)
A = u.get_editor_subsystem(u.EditorActorSubsystem)
E = u.get_editor_subsystem(u.UnrealEditorSubsystem)
L = u.get_editor_subsystem(u.LevelEditorSubsystem)
if L.is_in_play_in_editor():
    raise RuntimeError('PIE is running')
world = E.get_editor_world()
key = L.get_active_viewport_config_key()
pose0, fov0, gv0 = L.get_level_viewport_camera_info(key), L.get_level_viewport_fov(key), L.editor_get_game_view(key)


def dirty():
    S = u.EditorLoadingAndSavingUtils
    return sorted([p.get_name() for p in S.get_dirty_content_packages()] + [p.get_name() for p in S.get_dirty_map_packages()])


def xform_hash():
    h = hashlib.sha1()
    for a in sorted(A.get_all_level_actors(), key=lambda a: a.get_path_name()):
        t = a.get_actor_transform()
        h.update(('%s %.3f %.3f %.3f\n' % (a.get_path_name(), t.translation.x, t.translation.y, t.translation.z)).encode())
    return h.hexdigest()


def project(p, cam, rot, fov):
    F, R, U = u.MathLibrary.get_forward_vector(rot), u.MathLibrary.get_right_vector(rot), u.MathLibrary.get_up_vector(rot)
    d = p - cam
    dot = u.MathLibrary.dot_vector_vector
    x, y, z = dot(d, F), dot(d, R), dot(d, U)
    if x <= 1:
        return None
    k = (W_ / 2) / math.tan(math.radians(fov) / 2)
    return (W_ / 2 + y / x * k, H_ / 2 - z / x * k, x)


def screen_box(a, cam, rot, fov):
    o, e = a.get_actor_bounds(False)
    pts = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            for sz in (-1, 1):
                q = project(u.Vector(o.x + sx * e.x, o.y + sy * e.y, o.z + sz * e.z), cam, rot, fov)
                if q:
                    pts.append(q)
    if len(pts) < 8:
        return None
    xs, ys = [q[0] for q in pts], [q[1] for q in pts]
    return [max(0, min(xs)), max(0, min(ys)), min(W_, max(xs)), min(H_, max(ys))]


def pick(view):
    p, r, fov = VIEWS[view]
    cam, rot = u.Vector(*p), u.Rotator(pitch=r[0], yaw=r[1], roll=r[2])
    cands = {'small': [], 'medium': []}
    for a in A.get_all_level_actors():
        c = a.get_class().get_name()
        if c in SKIP_CLASSES:
            continue
        if not a.get_components_by_class(u.StaticMeshComponent) or a.get_components_by_class(u.InstancedStaticMeshComponent):
            continue
        o, e = a.get_actor_bounds(False)
        ext = max(e.x, e.y, e.z)
        cls = 'small' if 25 <= ext <= 80 else 'medium' if 90 <= ext <= 250 else None
        if not cls:
            continue
        q = project(o, cam, rot, fov)
        if not q or not (0.15 * W_ < q[0] < 0.85 * W_ and 0.15 * H_ < q[1] < 0.85 * H_) or not (400 < q[2] < 3000):
            continue
        hit = u.SystemLibrary.line_trace_single(world, cam, o, u.TraceTypeQuery.TRACE_TYPE_QUERY1, False, [], u.DrawDebugTrace.NONE, True)
        hr = hit.to_tuple() if hit else None
        hit_actor = hr[9] if hr and len(hr) > 9 else None
        if hit_actor is not None and hit_actor != a:
            continue
        box = screen_box(a, cam, rot, fov)
        if not box:
            continue
        cands[cls].append((math.hypot(q[0] - W_ / 2, q[1] - H_ / 2), a, ext, box, q[2]))
    out = {}
    for cls in cands:
        cands[cls].sort(key=lambda t: t[0])
        if cands[cls]:
            _, a, ext, box, dist = cands[cls][0]
            out[cls] = {'actor': a, 'label': a.get_actor_label(), 'path': a.get_path_name(), 'class': a.get_class().get_name(),
                        'max_half_extent_cm': round(ext, 1), 'distance_cm': round(dist, 1), 'screen_box_1920x1080': [round(v) for v in box],
                        'n_candidates': len(cands[cls])}
    return out


LOG = {'started': time.strftime('%Y-%m-%d %H:%M:%S'), 'world': world.get_path_name(), 'views': VIEWS, 'settle_s': SETTLE,
       'change_wait_s': CHANGE_WAIT, 'nshot': NSHOT, 'dirty_before': dirty(), 'xform_before': xform_hash(), 'picks': {}, 'shots': [],
       'hide_events': [], 'errors': []}
PICKS = {}
for v in ORDER:
    PICKS[v] = pick(v)
    LOG['picks'][v] = {k: {kk: vv for kk, vv in d.items() if kk != 'actor'} for k, d in PICKS[v].items()}

PLAN = []
for i, v in enumerate(ORDER):
    other = ORDER[(i + 1) % len(ORDER)]
    PLAN += [('move', v), ('wait', SETTLE), ('shot', v, 'warm', 0)]
    PLAN += [('shot', v, 'S1', k) for k in range(NSHOT)]
    PLAN += [('move', other), ('wait', 2.0), ('move', v), ('wait', SETTLE)]
    PLAN += [('shot', v, 'S2', k) for k in range(NSHOT)]
    if 'small' in PICKS[v]:
        PLAN += [('hide', v, 'small', True), ('wait', CHANGE_WAIT)] + [('shot', v, 'S3small', k) for k in range(NSHOT)] + [('hide', v, 'small', False)]
    if 'medium' in PICKS[v]:
        PLAN += [('hide', v, 'medium', True), ('wait', CHANGE_WAIT)] + [('shot', v, 'S4medium', k) for k in range(NSHOT)] + [('hide', v, 'medium', False)]
    PLAN += [('wait', CHANGE_WAIT)] + [('shot', v, 'S5', k) for k in range(NSHOT)]


class T1B:
    def __init__(self):
        self.i, self.t, self.task, self.t0 = 0, time.monotonic(), None, time.monotonic()
        self.hidden = []
        self.handle = u.register_slate_post_tick_callback(self.tick)
        builtins.T1B_ACTIVE = self

    def status(self, s):
        json.dump({'state': s, 'step': self.i, 'of': len(PLAN), 'shots': len(LOG['shots']), 'errors': LOG['errors']},
                  open(os.path.join(OUT, 't1b_status.json'), 'w'))

    def tick(self, dt):
        try:
            if L.is_in_play_in_editor():
                raise RuntimeError('PIE started')
            if time.monotonic() - self.t0 > 1500:
                raise RuntimeError('T1b overall timeout')
            if self.i >= len(PLAN):
                return self.finish()
            st, now = PLAN[self.i], time.monotonic()
            if st[0] == 'move':
                p, r, fov = VIEWS[st[1]]
                L.editor_set_game_view(True, key)
                L.set_level_viewport_camera_info(u.Vector(*p), u.Rotator(pitch=r[0], yaw=r[1], roll=r[2]), key)
                L.set_level_viewport_fov(fov, key)
                L.editor_invalidate_viewports()
                self.i += 1; self.t = now
            elif st[0] == 'wait':
                if now - self.t >= st[1]:
                    self.i += 1; self.t = now
            elif st[0] == 'hide':
                a = PICKS[st[1]][st[2]]['actor']
                a.set_is_temporarily_hidden_in_editor(st[3])
                L.editor_invalidate_viewports()
                if st[3]:
                    self.hidden.append(a)
                elif a in self.hidden:
                    self.hidden.remove(a)
                LOG['hide_events'].append({'view': st[1], 'size': st[2], 'hidden': st[3], 'session_s': round(now - self.t0, 2),
                                           'is_temporarily_hidden': a.is_temporarily_hidden_in_editor(), 'dirty': dirty()})
                self.i += 1; self.t = now
            elif st[0] == 'shot':
                if self.task is None:
                    self.file = os.path.join(OUT, 'shots', '%s__%s_f%d.png' % (st[1], st[2], st[3]))
                    if os.path.exists(self.file):
                        os.remove(self.file)
                    self.req = now
                    self.task = u.AutomationLibrary.take_high_res_screenshot(W_, H_, self.file, delay=0.2, force_game_view=True)
                    self.redraw = None
                elif self.redraw is None and now - self.req > 0.5:
                    self.redraw = u.ToolsetRegistry.execute_tool('EditorToolset.EditorAppToolset', 'CaptureViewport',
                                                                 '{"captureTransform":null,"annotations":null,"bShowUI":false}')
                elif self.task.is_task_done() and os.path.exists(self.file) and os.path.getsize(self.file) > 0:
                    LOG['shots'].append({'view': st[1], 'set': st[2], 'k': st[3], 'file': os.path.basename(self.file),
                                         'session_s': round(now - self.t0, 3), 'took_s': round(now - self.req, 3)})
                    self.task = None; self.i += 1; self.t = now
                    self.status('running')
                elif now - self.req > 45:
                    raise RuntimeError('screenshot timeout %s' % self.file)
        except Exception as ex:
            LOG['errors'].append(repr(ex))
            self.finish()

    def finish(self):
        u.unregister_slate_post_tick_callback(self.handle)
        builtins.T1B_ACTIVE = None
        for a in list(self.hidden):
            try:
                a.set_is_temporarily_hidden_in_editor(False)
            except Exception as ex:
                LOG['errors'].append('unhide ' + repr(ex))
        try:
            L.set_level_viewport_camera_info(pose0[0], pose0[1], key)
            L.set_level_viewport_fov(fov0, key)
            L.editor_set_game_view(gv0, key)
            L.editor_invalidate_viewports()
        except Exception as ex:
            LOG['errors'].append('restore ' + repr(ex))
        LOG['any_still_hidden'] = [d['label'] for v in PICKS.values() for d in v.values() if d['actor'].is_temporarily_hidden_in_editor()]
        LOG['dirty_after'] = dirty()
        LOG['xform_after'] = xform_hash()
        LOG['xform_unchanged'] = LOG['xform_after'] == LOG['xform_before']
        LOG['finished'] = time.strftime('%Y-%m-%d %H:%M:%S')
        json.dump(LOG, open(os.path.join(OUT, 't1b_log.json'), 'w'), indent=1, default=str)
        self.status('done' if not LOG['errors'] else 'error')


T1B()
print('T1B started steps', len(PLAN), 'picks', json.dumps(LOG['picks'], default=str))
