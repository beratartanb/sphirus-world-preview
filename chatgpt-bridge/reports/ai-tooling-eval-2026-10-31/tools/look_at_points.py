"""look_at_points.py (measure job): editor-viewport inspection shots looking down (pitch -55, 3.2 m above, 3 m back) at the labelled
VMP_ trial actors given in builtins.LOOK_LABELS (substring match), for judging decal / mesh appearance. Viewport restored. Nothing edited.
Output: <VMP>/lookat/<label>.png"""
import unreal as u, os, json, math, time, builtins

VMP = r'C:\Users\berat\AppData\Local\Temp\claude\C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS\5f49a232-b001-47ad-8881-1eb04d9cb1c5\scratchpad\vmp'
OUT = os.path.join(VMP, 'lookat'); os.makedirs(OUT, exist_ok=True)
WANT = list(getattr(builtins, 'LOOK_LABELS'))
L = u.get_editor_subsystem(u.LevelEditorSubsystem)
acts = [a for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors() if a.get_actor_label().startswith('VMP_')]
targets = []
for w in WANT:
    m = [a for a in acts if w in a.get_actor_label()]
    if m:
        targets.append(m[0])
key = L.get_active_viewport_config_key(); pose0, fov0, gv0 = L.get_level_viewport_camera_info(key), L.get_level_viewport_fov(key), L.editor_get_game_view(key)
PLAN = []
for a in targets:
    p = a.get_actor_location(); yaw = a.get_actor_rotation().yaw
    cam = u.Vector(p.x - 300 * math.cos(math.radians(yaw + 30)), p.y - 300 * math.sin(math.radians(yaw + 30)), p.z + 320)
    PLAN += [('move', cam, u.Rotator(pitch=-55.0, yaw=yaw + 30, roll=0)), ('wait', 3.0), ('shot', a.get_actor_label())]
st = {'i': 0, 't': time.monotonic(), 'task': None}


def tick(dt):
    if st['i'] >= len(PLAN):
        u.unregister_slate_post_tick_callback(st['h'])
        L.set_level_viewport_camera_info(pose0[0], pose0[1], key); L.set_level_viewport_fov(fov0, key); L.editor_set_game_view(gv0, key)
        json.dump({'done': True, 'n': len(targets)}, open(os.path.join(OUT, 'status.json'), 'w')); return
    p, now = PLAN[st['i']], time.monotonic()
    if p[0] == 'move':
        L.editor_set_game_view(True, key); L.set_level_viewport_camera_info(p[1], p[2], key); L.set_level_viewport_fov(70.0, key); L.editor_invalidate_viewports()
        st['i'] += 1; st['t'] = now
    elif p[0] == 'wait':
        if now - st['t'] >= p[1]:
            st['i'] += 1; st['t'] = now
    else:
        if st['task'] is None:
            st['f'] = os.path.join(OUT, '%s.png' % p[1]); st['task'] = u.AutomationLibrary.take_high_res_screenshot(1280, 720, st['f'], delay=0.2, force_game_view=True); st['r'] = now
            u.ToolsetRegistry.execute_tool('EditorToolset.EditorAppToolset', 'CaptureViewport', '{"captureTransform":null,"annotations":null,"bShowUI":false}')
        elif st['task'].is_task_done() and os.path.exists(st['f']):
            st['task'] = None; st['i'] += 1; st['t'] = now
        elif now - st['r'] > 40:
            st['task'] = None; st['i'] += 1


st['h'] = u.register_slate_post_tick_callback(tick)
print('LOOKAT', [a.get_actor_label() for a in targets])
