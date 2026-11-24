# VF2B motion recorder (PIE only): timed input in GAME time under a global time dilation, one HighResShot per 1/FPS of game time,
# from a camera attached to the pawn. Nothing is saved. builtins.VF2B_REC = dict(cam=(dist,right,up,fov,tz), seq=[(t,'+W')...], dur, fps, dil, res)
# Frames land in Saved/Screenshots/WindowsEditor/HighresScreenshot*.png in order; a done-file marks the end.
import unreal as u, builtins, time
exec(open(u.Paths.project_dir() + 'Tools/SF52_20261105/h.py', encoding='utf8').read())
R = getattr(builtins, 'VF2B_REC', {})
D_, RT, UP, FOV, TZ = R.get('cam', (120.0, 34.0, 2.0, 30.0, 0.0)); FPS = R.get('fps', 30.0); DIL = R.get('dil', 0.2); DUR = R.get('dur', 9.0); RES = R.get('res', '960x540')
SEQ = sorted(R.get('seq', [(1.0, '+W'), (1.0, '+LeftShift'), (3.0, '-W'), (3.0, '-LeftShift'), (5.2, '+A'), (5.2, '+LeftShift'), (6.0, '-A'), (6.0, '+D'), (6.8, '-D'), (6.8, '-LeftShift')]))
fc = [c for c in PW.get_components_by_class(u.SkeletalMeshComponent) if c.get_name() == 'Face'][0]
hd = fc.get_socket_location('head'); f = PW.get_actor_forward_vector(); r = PW.get_actor_right_vector()
tg = u.Vector(hd.x, hd.y, hd.z + TZ); loc = u.Vector(tg.x + f.x * D_ + r.x * RT, tg.y + f.y * D_ + r.y * RT, tg.z + UP)
cs = u.GameplayStatics.get_all_actors_of_class(W, u.CameraActor)
if not cs:
    cmd('summon CameraActor'); cs = u.GameplayStatics.get_all_actors_of_class(W, u.CameraActor)
cam = cs[0]
try: cam.root_component.set_mobility(u.ComponentMobility.MOVABLE)
except Exception as e: print('mob', e)
cam.detach_from_actor(u.DetachmentRule.KEEP_WORLD, u.DetachmentRule.KEEP_WORLD, u.DetachmentRule.KEEP_WORLD)
cam.set_actor_location_and_rotation(loc, u.MathLibrary.find_look_at_rotation(loc, tg), False, True)
cc = cam.get_component_by_class(u.CameraComponent); cc.set_editor_property('field_of_view', FOV); cc.set_editor_property('constrain_aspect_ratio', False); cc.set_editor_property('post_process_blend_weight', 0.0)
cam.attach_to_actor(PW, '', u.AttachmentRule.KEEP_WORLD, u.AttachmentRule.KEEP_WORLD, u.AttachmentRule.KEEP_WORLD, False)
PC.set_view_target_with_blend(cam, 0.0)
u.GameplayStatics.set_global_time_dilation(W, DIL)
st = dict(t0=u.GameplayStatics.get_time_seconds(W), i=0, n=0, h=None, rows=[])
def tick(dt):
    try:
        w = u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world()
        if not w: u.unregister_slate_post_tick_callback(st['h']); return
        now = u.GameplayStatics.get_time_seconds(w) - st['t0']
        while st['i'] < len(SEQ) and now >= SEQ[st['i']][0]:
            a = SEQ[st['i']][1]; st['i'] += 1
            if a[0] == '+': cmd('Input.+key ' + a[1:] + ' true')
            elif a[0] == '-': cmd('Input.-key ' + a[1:])
        if now >= st['n'] / FPS and now < DUR:
            cmd(R.get('shot', 'Shot')); st['n'] += 1
            v = PW.get_velocity(); st['rows'].append('%d %.3f %.1f' % (st['n'], now, (v.x * v.x + v.y * v.y) ** 0.5))
        if now >= DUR:
            for k in ('W', 'A', 'S', 'D', 'LeftShift'): cmd('Input.-key ' + k)
            u.GameplayStatics.set_global_time_dilation(w, 1.0)
            open(u.Paths.project_dir() + 'Saved/UE59Work/vf2b/_rec_done.txt', 'w').write('\n'.join(st['rows']))
            u.unregister_slate_post_tick_callback(st['h'])
    except Exception as e:
        u.log_error('VF2B rec tick ' + str(e)); u.unregister_slate_post_tick_callback(st['h'])
st['h'] = u.register_slate_post_tick_callback(tick)
print('VF2BREC armed', len(SEQ), 'dil', DIL, 'fps', FPS, 'dur', DUR)
