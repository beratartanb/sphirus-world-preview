"""topview_pfr.py (measure job): diagnostic top-down + oblique captures of the play area with a transient CameraActor (editor render,
no PIE). builtins.PFR_TOP_TAG (folder suffix). Output: Saved/Codex/PineForestRedesign_20261104/cap/top_<tag>/{top,top_close,oblique_SE,oblique_NW}.png"""
import unreal as u, pathlib, builtins, time, json
TAG = getattr(builtins, 'PFR_TOP_TAG', 'x'); D = pathlib.Path(u.Paths.project_dir()) / 'Saved/Codex/PineForestRedesign_20261104/cap' / ('top_' + TAG); D.mkdir(parents=True, exist_ok=True)
E = u.get_editor_subsystem(u.UnrealEditorSubsystem); assert E.get_game_world() is None
A = u.get_editor_subsystem(u.EditorActorSubsystem)
SHOTS = [('top', [0, 1000, 21000], [-90.0, 90.0], 60.0), ('top_close', [600, 2600, 11000], [-90.0, 90.0], 60.0), ('oblique_SE', [9500, -8500, 7500], [-30.0, 130.0], 60.0), ('oblique_NW', [-9000, 11000, 7500], [-30.0, -43.0], 60.0)]
cam = A.spawn_actor_from_class(u.CameraActor, u.Vector(0, 0, 0)); cam.set_actor_label('PFR_TopCam'); cc = cam.camera_component; cc.set_editor_property('constrain_aspect_ratio', False)
st = {'i': 0, 'phase': 'pos', 't': time.monotonic()}; log = []


def tick(dt):
    try:
        now = time.monotonic()
        if st['i'] >= len(SHOTS):
            A.destroy_actor(cam); u.unregister_slate_post_tick_callback(builtins.PFR_TOP_H); (D / 'done.json').write_text(json.dumps(log)); return
        n, loc, rot, fov = SHOTS[st['i']]; fn = D / (n + '.png')
        if st['phase'] == 'pos':
            cam.set_actor_location_and_rotation(u.Vector(*loc), u.Rotator(pitch=rot[0], yaw=rot[1], roll=0), False, True); cc.set_editor_property('field_of_view', fov); st.update(phase='warm', t=now)
        elif st['phase'] == 'warm' and now - st['t'] > (8.0 if st['i'] == 0 else 3.0):
            if fn.exists(): fn.unlink()
            u.AutomationLibrary.take_high_res_screenshot(2560, 1440, str(fn), camera=cam, delay=0.5); st.update(phase='shoot', t=now)
        elif st['phase'] == 'shoot' and ((fn.exists() and fn.stat().st_size > 0 and now - st['t'] > 2.0) or now - st['t'] > 60):
            log.append({'name': n, 'ok': fn.exists(), 'loc': loc, 'rot': rot, 'fov': fov}); st.update(i=st['i'] + 1, phase='pos', t=now)
    except Exception as ex:
        u.unregister_slate_post_tick_callback(builtins.PFR_TOP_H); (D / 'done.json').write_text(json.dumps({'error': repr(ex)[:200]}))
        try: A.destroy_actor(cam)
        except Exception: pass


if (D / 'done.json').exists(): (D / 'done.json').unlink()
builtins.PFR_TOP_H = u.register_slate_post_tick_callback(tick); print('TOPVIEW scheduled', TAG)
