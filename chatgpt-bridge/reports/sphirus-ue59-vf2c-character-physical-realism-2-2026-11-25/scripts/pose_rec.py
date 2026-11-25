# VF2C PIE-only, read-only: drive the real player through a movement matrix with movement input and record the visible body's
# component-space bone transforms at fixed moments (for an offline skinning / penetration check), plus one still per phase.
import unreal as u, json, time, math
exec(open(u.Paths.project_dir() + 'Tools/SF52_20261105/h.py', encoding='utf8').read())
C = {c.get_name(): c for c in PW.get_components_by_class(u.SkeletalMeshComponent)}; body = C['Manny']
names = [str(body.get_bone_name(i)) for i in range(body.get_num_bones())]
def snap():
    o = {}
    for n in names:
        t = body.get_socket_transform(n, u.RelativeTransformSpace.RTS_COMPONENT); l = t.translation; q = t.rotation; s = t.scale3d
        o[n] = [round(l.x, 4), round(l.y, 4), round(l.z, 4), round(q.x, 6), round(q.y, 6), round(q.z, 6), round(q.w, 6), round(s.x, 4)]
    return o
ref = {}
try:
    rp = u.AnimPoseExtensions.get_reference_pose(body.get_skeletal_mesh_asset().skeleton)
    for n in names:
        try:
            t = u.AnimPoseExtensions.get_bone_pose(rp, n, u.AnimPoseSpaces.WORLD); l = t.translation; q = t.rotation
            ref[n] = [round(l.x, 4), round(l.y, 4), round(l.z, 4), round(q.x, 6), round(q.y, 6), round(q.z, 6), round(q.w, 6), 1.0]
        except Exception: pass
except Exception as e: print('POSEREC ref err', repr(e)[:160])
# 3/4 body camera attached to the pawn
hd = body.get_socket_location('head'); f = PW.get_actor_forward_vector(); r = PW.get_actor_right_vector()
tg = u.Vector(hd.x, hd.y, hd.z - 62.0); loc = u.Vector(tg.x + f.x * 300 + r.x * 170, tg.y + f.y * 300 + r.y * 170, tg.z + 10)
cs = u.GameplayStatics.get_all_actors_of_class(W, u.CameraActor)
if not cs: cmd('summon CameraActor'); cs = u.GameplayStatics.get_all_actors_of_class(W, u.CameraActor)
cam = cs[0]; cam.root_component.set_mobility(u.ComponentMobility.MOVABLE); cam.set_actor_location_and_rotation(loc, u.MathLibrary.find_look_at_rotation(loc, tg), False, True)
cc = cam.get_component_by_class(u.CameraComponent); cc.set_editor_property('field_of_view', 40.0); cc.set_editor_property('constrain_aspect_ratio', False); cc.set_editor_property('post_process_blend_weight', 0.0)
cam.attach_to_actor(PW, '', u.AttachmentRule.KEEP_WORLD, u.AttachmentRule.KEEP_WORLD, u.AttachmentRule.KEEP_WORLD, False); PC.set_view_target_with_blend(cam, 0.0); cmd('r.DepthOfFieldQuality 0')
F = (0.0, 1.0); Bk = (0.0, -1.0); R = (-1.0, 0.0)      # world directions (pawn starts facing +Y)
# (label, duration, move dir, scale, extra action at start, sample offsets from phase start)
SEQ = [('idle', 1.6, None, 0, None, [1.2]), ('walk', 2.4, F, 0.45, None, [1.2, 1.4, 1.6, 1.8, 2.0]), ('run', 2.2, F, 1.0, None, [1.2, 1.35, 1.5, 1.65, 1.8]), ('stop', 1.2, None, 0, None, [0.15, 0.4, 1.0]),
       ('turn180_run', 2.0, Bk, 1.0, None, [0.2, 0.4, 0.6, 1.4, 1.6]), ('sprint', 2.2, Bk, 1.0, 'sprint', [1.2, 1.35, 1.5, 1.65]), ('stop2', 1.2, None, 0, 'unsprint', [0.2, 1.0]),
       ('strafe_turn90', 1.8, R, 1.0, None, [0.2, 0.45, 1.2, 1.4]), ('backstep', 1.6, F, 0.4, None, [0.3, 1.0]), ('crouch', 2.0, None, 0, 'crouch', [0.4, 1.6]), ('crouch_walk', 1.8, Bk, 0.5, None, [1.0, 1.3]),
       ('stand', 1.2, None, 0, 'uncrouch', [0.3, 1.0]), ('jump', 1.6, F, 0.6, 'jump', [0.25, 0.5, 0.8, 1.2]), ('settle', 1.5, None, 0, None, [1.2])]
st = dict(t0=time.time(), i=-1, ph0=0.0, k=0, out=[], h=None, shot=False)
def start(i):
    st['i'] = i; st['ph0'] = time.time(); st['k'] = 0; st['shot'] = False; a = SEQ[i][4]
    if a == 'crouch': PW.crouch()
    elif a == 'uncrouch': PW.un_crouch()
    elif a == 'jump': PW.jump()
    elif a == 'sprint': cmd('Input.+key LeftShift true')
    elif a == 'unsprint': cmd('Input.-key LeftShift')
def tick(dt):
    try:
        if not u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world(): u.unregister_slate_post_tick_callback(st['h']); return
        if st['i'] < 0: start(0)
        lab, dur, d, sc, act, offs = SEQ[st['i']]; t = time.time() - st['ph0']
        if d: PW.add_movement_input(u.Vector(d[0], d[1], 0.0), sc, False)
        if st['k'] < len(offs) and t >= offs[st['k']]:
            v = PW.get_velocity(); st['out'].append({'label': lab, 'k': st['k'], 't': round(t, 3), 'speed': round((v.x * v.x + v.y * v.y) ** 0.5, 1), 'vz': round(v.z, 1), 'crouched': bool(PW.is_crouched) if hasattr(PW, 'is_crouched') else None, 'bones': snap()}); st['k'] += 1
            if st['k'] == max(1, len(offs) // 2 + 1) and not st['shot']: st['shot'] = True; cmd('HighResShot 960x720'); open(u.Paths.project_dir() + 'Saved/UE59Work/vf2c/_pose_order.txt', 'a').write(lab + '\n')
        if t >= dur:
            if st['i'] + 1 < len(SEQ): start(st['i'] + 1)
            else:
                cmd('Input.-key LeftShift'); cmd('r.DepthOfFieldQuality 2')
                json.dump({'names': names, 'ref': ref, 'samples': st['out']}, open(u.Paths.project_dir() + 'Saved/UE59Work/vf2c/pose_rec.json', 'w')); u.unregister_slate_post_tick_callback(st['h'])
    except Exception as e:
        u.log_error('POSEREC ' + str(e)); open(u.Paths.project_dir() + 'Saved/UE59Work/vf2c/pose_rec_err.txt', 'w').write(repr(e)); u.unregister_slate_post_tick_callback(st['h'])
st['h'] = u.register_slate_post_tick_callback(tick); print('POSEREC armed bones', len(names), 'ref', len(ref))
