"""T3-lite (read-only measure job): the MCP tool function EditorAppToolset.CaptureViewport called in-process through
ToolsetRegistry.ExecuteTool (the same dispatch the MCP server uses, but without starting the server), from the same fixed
poses as T1. Saves the returned PNG plus the metadata layout, then restores the viewport. Nothing is spawned, edited or saved.
Output: <OUT>/cv/*.png, <OUT>/t3_log.json, <OUT>/t3_status.json.
"""
import unreal as u, json, time, os, base64, builtins

OUT = r'C:\Users\berat\AppData\Local\Temp\claude\C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS\5f49a232-b001-47ad-8881-1eb04d9cb1c5\scratchpad\t1'
VIEWS = {
    'house_front': ([-1550, 2460, 92.3320484161377], [4.045882564505467, -36.830867829324454, 0], 68),
    'pond':        ([1500, 2810, 152.16795921325684], [-6.110206786658776, 130.80909247267473, 0], 75),
    'forest':      ([2200, 1580, 319.35779571533203], [3.696050782488103, -77.14368743247138, 0], 70),
}
SETTLE = 10.0
if getattr(builtins, 'T3_CV_ACTIVE', None):
    raise RuntimeError('T3 already running')
os.makedirs(os.path.join(OUT, 'cv'), exist_ok=True)
E = u.get_editor_subsystem(u.UnrealEditorSubsystem)
L = u.get_editor_subsystem(u.LevelEditorSubsystem)
if L.is_in_play_in_editor():
    raise RuntimeError('PIE is running')
key = L.get_active_viewport_config_key()
pose0, fov0, gv0 = L.get_level_viewport_camera_info(key), L.get_level_viewport_fov(key), L.editor_get_game_view(key)


def prop(obj, k, default=None):
    try:
        return obj.get_editor_property(k)
    except Exception:
        try:
            return obj.get_editor_property(''.join(p[:1].upper() + p[1:] for p in k.split('_')))
        except Exception:
            return default


def shape(o, depth=0):  # JSON layout with long strings elided
    if isinstance(o, dict):
        return {k: shape(v, depth + 1) for k, v in o.items()}
    if isinstance(o, list):
        return [shape(v, depth + 1) for v in o[:3]]
    if isinstance(o, str) and len(o) > 80:
        return '<str len %d>' % len(o)
    return o


def find_b64(o):
    if isinstance(o, dict):
        for v in o.values():
            r = find_b64(v)
            if r:
                return r
    if isinstance(o, str) and len(o) > 1000:
        return o
    return None


LOG = {'started': time.strftime('%Y-%m-%d %H:%M:%S'), 'views': VIEWS, 'settle_s': SETTLE, 'rows': [], 'errors': []}
PLAN = [(v, s) for v in VIEWS for s in ('move', 'cv')]


class T3:
    def __init__(self):
        self.i, self.res, self.moved = 0, None, 0.0
        self.handle = u.register_slate_post_tick_callback(self.tick)
        builtins.T3_CV_ACTIVE = self

    def tick(self, dt):
        try:
            if L.is_in_play_in_editor():
                raise RuntimeError('PIE started')
            if self.i >= len(PLAN):
                return self.finish()
            v, s = PLAN[self.i]
            now = time.monotonic()
            if s == 'move':
                p, r, fov = VIEWS[v]
                L.editor_set_game_view(True, key)
                L.set_level_viewport_camera_info(u.Vector(*p), u.Rotator(pitch=r[0], yaw=r[1], roll=r[2]), key)
                L.set_level_viewport_fov(fov, key)
                L.editor_invalidate_viewports()
                self.moved = now; self.i += 1
            elif self.res is None:
                if now - self.moved < SETTLE:
                    return
                self.req = now
                self.res = u.ToolsetRegistry.execute_tool('EditorToolset.EditorAppToolset', 'CaptureViewport',
                                                          '{"captureTransform":null,"annotations":null,"bShowUI":false}')
            elif prop(self.res, 'is_complete'):
                row = {'view': v, 'call_s': round(now - self.req, 3)}
                err = prop(self.res, 'error')
                if err:
                    row['error'] = str(err)
                else:
                    val = json.loads(prop(self.res, 'value'))
                    row['layout'] = shape(val)
                    b64 = find_b64(val)
                    if b64:
                        fn = os.path.join(OUT, 'cv', '%s__captureviewport.png' % v)
                        with open(fn, 'wb') as f:
                            f.write(base64.b64decode(b64))
                        row['file'], row['bytes'] = os.path.basename(fn), os.path.getsize(fn)
                LOG['rows'].append(row)
                self.res = None; self.i += 1
            elif now - self.req > 30:
                raise RuntimeError('CaptureViewport timeout')
        except Exception as ex:
            LOG['errors'].append(repr(ex)); self.finish()

    def finish(self):
        u.unregister_slate_post_tick_callback(self.handle)
        builtins.T3_CV_ACTIVE = None
        L.set_level_viewport_camera_info(pose0[0], pose0[1], key)
        L.set_level_viewport_fov(fov0, key)
        L.editor_set_game_view(gv0, key)
        L.editor_invalidate_viewports()
        S = u.EditorLoadingAndSavingUtils
        LOG['dirty_after'] = sorted([p.get_name() for p in S.get_dirty_content_packages()] + [p.get_name() for p in S.get_dirty_map_packages()])
        LOG['finished'] = time.strftime('%Y-%m-%d %H:%M:%S')
        with open(os.path.join(OUT, 't3_log.json'), 'w') as f:
            json.dump(LOG, f, indent=1, default=str)
        with open(os.path.join(OUT, 't3_status.json'), 'w') as f:
            json.dump({'state': 'done' if not LOG['errors'] else 'error'}, f)


T3()
print('T3_CV started')
