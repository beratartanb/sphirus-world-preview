# PIE only: run forward 2.2 s then stop; sample the cloth parameter collection every tick and take side stills at start / steady / stop.
import unreal as u, json, time
exec(open(u.Paths.project_dir() + 'Tools/SF52_20261105/h.py', encoding='utf8').read())
mpc = u.load_asset('/Game/Sphirus/CharacterLab/VF2_20261124/Garments/MPC_Sph_Cloth'); KM = u.MaterialLibrary
body = [c for c in PW.get_components_by_class(u.SkeletalMeshComponent) if c.get_name() == 'Manny'][0]
hd = body.get_socket_location('spine_03'); f = PW.get_actor_forward_vector(); r = PW.get_actor_right_vector()
tg = u.Vector(hd.x, hd.y, hd.z - 12.0); loc = u.Vector(tg.x - f.x * 60 + r.x * 150, tg.y - f.y * 60 + r.y * 150, tg.z + 5)
cs = u.GameplayStatics.get_all_actors_of_class(W, u.CameraActor)
if not cs: cmd('summon CameraActor'); cs = u.GameplayStatics.get_all_actors_of_class(W, u.CameraActor)
cam = cs[0]; cam.root_component.set_mobility(u.ComponentMobility.MOVABLE); cam.set_actor_location_and_rotation(loc, u.MathLibrary.find_look_at_rotation(loc, tg), False, True)
cc = cam.get_component_by_class(u.CameraComponent); cc.set_editor_property('field_of_view', 34.0); cc.set_editor_property('constrain_aspect_ratio', False); cc.set_editor_property('post_process_blend_weight', 0.0)
cam.attach_to_actor(PW, '', u.AttachmentRule.KEEP_WORLD, u.AttachmentRule.KEEP_WORLD, u.AttachmentRule.KEEP_WORLD, False); PC.set_view_target_with_blend(cam, 0.0); cmd('r.DepthOfFieldQuality 0')
st = dict(t0=time.time(), rows=[], h=None, shots=[(0.9, 'standing'), (1.75, 'accelerating'), (3.3, 'steady_run'), (4.45, 'stopping'), (6.2, 'settled')])
def tick(dt):
    try:
        if not u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world(): u.unregister_slate_post_tick_callback(st['h']); return
        t = time.time() - st['t0']
        if 1.5 <= t < 4.2: cmd('Input.+key LeftShift true') if not st.get('s') else None; st['s'] = 1; PW.add_movement_input(u.Vector(0, 1, 0), 1.0, False)
        elif st.get('s') == 1: cmd('Input.-key LeftShift'); st['s'] = 2
        v = KM.get_vector_parameter_value(W, mpc, 'Vel'); s = KM.get_vector_parameter_value(W, mpc, 'VelSmooth'); a = PW.get_velocity()
        st['rows'].append([round(t, 3), round(a.y, 1), round(v.g, 1), round(s.g, 1)])
        if st['shots'] and t >= st['shots'][0][0]: k = st['shots'].pop(0); cmd('HighResShot 960x720'); open(u.Paths.project_dir() + 'Saved/UE59Work/vf2c/_mpc_order.txt', 'a').write(k[1] + '\n')
        if t > 7.0: cmd('r.DepthOfFieldQuality 2'); json.dump(st['rows'], open(u.Paths.project_dir() + 'Saved/UE59Work/vf2c/mpc_probe.json', 'w')); u.unregister_slate_post_tick_callback(st['h'])
    except Exception as e: open(u.Paths.project_dir() + 'Saved/UE59Work/vf2c/mpc_probe_err.txt', 'w').write(repr(e)); u.unregister_slate_post_tick_callback(st['h'])
st['h'] = u.register_slate_post_tick_callback(tick); print('MPCPROBE armed')
