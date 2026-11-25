# PIE only: face camera; one HighResShot with lids open, one at blink peak, one during a glance.
import unreal as u, time
exec(open(u.Paths.project_dir() + 'Tools/SF52_20261105/h.py', encoding='utf8').read())
fc = [c for c in PW.get_components_by_class(u.SkeletalMeshComponent) if c.get_name() == 'Face'][0]
hd = fc.get_socket_location('head'); f = PW.get_actor_forward_vector(); r = PW.get_actor_right_vector()
tg = u.Vector(hd.x, hd.y, hd.z + 6.0); loc = u.Vector(tg.x + f.x * 70 + r.x * 14, tg.y + f.y * 70 + r.y * 14, tg.z + 1)
cs = u.GameplayStatics.get_all_actors_of_class(W, u.CameraActor)
if not cs: cmd('summon CameraActor'); cs = u.GameplayStatics.get_all_actors_of_class(W, u.CameraActor)
cam = cs[0]; cam.root_component.set_mobility(u.ComponentMobility.MOVABLE); cam.set_actor_location_and_rotation(loc, u.MathLibrary.find_look_at_rotation(loc, tg), False, True)
cc = cam.get_component_by_class(u.CameraComponent); cc.set_editor_property('field_of_view', 22.0); cc.set_editor_property('constrain_aspect_ratio', False); cc.set_editor_property('post_process_blend_weight', 0.0)
PC.set_view_target_with_blend(cam, 0.0); cmd('r.DepthOfFieldQuality 0')
st = dict(h=None, done=set(), t0=time.time())
def tick(dt):
    try:
        if not u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world(): u.unregister_slate_post_tick_callback(st['h']); return
        a = fc.get_anim_instance(); b = a.get_curve_value('CTRL_expressions_eyeBlinkL'); l = max(a.get_curve_value('CTRL_expressions_eyeLookLeftL'), a.get_curve_value('CTRL_expressions_eyeLookRightL')); t = time.time() - st['t0']
        k = 'open' if (b < 0.01 and l < 0.005 and t > 1.0) else 'blink' if b > 0.93 else 'glance' if (l > 0.07 and b < 0.01) else None
        if k and k not in st['done'] and t - st.get('last', -9) > 0.8: st['done'].add(k); st['last'] = t; cmd('HighResShot 1280x720'); open(u.Paths.project_dir() + 'Saved/UE59Work/vf2c/_blink_order.txt', 'a').write(k + '\n')
        if len(st['done']) == 3 or t > 40: cmd('r.DepthOfFieldQuality 2'); open(u.Paths.project_dir() + 'Saved/UE59Work/vf2c/_blink_done.txt', 'w').write(str(sorted(st['done']))); u.unregister_slate_post_tick_callback(st['h'])
    except Exception as e: u.log_error('blink shot ' + str(e)); u.unregister_slate_post_tick_callback(st['h'])
st['h'] = u.register_slate_post_tick_callback(tick); print('BLINKSHOT armed')
