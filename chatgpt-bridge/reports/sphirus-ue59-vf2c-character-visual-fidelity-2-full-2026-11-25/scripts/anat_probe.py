# VF2C PIE-only, read-only: body proportions from the visible body's bones (idle), and 12 s of face curve / eye rotation samples (blink, gaze).
import unreal as u, json, time, builtins
exec(open(u.Paths.project_dir() + 'Tools/SF52_20261105/h.py', encoding='utf8').read())
C = {c.get_name(): c for c in PW.get_components_by_class(u.SkeletalMeshComponent)}; body = C['Manny']; face = C['Face']
B = ['root', 'pelvis', 'spine_01', 'spine_03', 'spine_05', 'neck_01', 'neck_02', 'head', 'clavicle_l', 'clavicle_r', 'upperarm_l', 'upperarm_r', 'lowerarm_l', 'lowerarm_r', 'hand_l', 'hand_r', 'middle_01_l', 'middle_03_l',
     'thigh_l', 'thigh_r', 'calf_l', 'calf_r', 'foot_l', 'foot_r', 'ball_l', 'ball_r']
P = {}
for b in B:
    l = body.get_socket_location(b); P[b] = [round(l.x, 2), round(l.y, 2), round(l.z, 2)]
fl = PW.get_actor_location(); cap = PW.get_component_by_class(u.CapsuleComponent); P['_floor_z'] = round(fl.z - cap.get_scaled_capsule_half_height(), 2)
for b in ('FACIAL_L_Eye', 'FACIAL_R_Eye', 'FACIAL_C_FacialRoot', 'head'):
    try: l = face.get_socket_location(b); P['face_' + b] = [round(l.x, 2), round(l.y, 2), round(l.z, 2)]
    except Exception: pass
bb = face.get_local_bounds() if hasattr(face, 'get_local_bounds') else None
o, e = face.get_owner().get_actor_bounds(True); P['_actor_top_z'] = round(o.z + e.z, 2)
ai = face.get_anim_instance(); P['_face_abp'] = ai.get_class().get_name() if ai else None; P['_body_abp'] = body.get_anim_instance().get_class().get_name()
names = [str(n) for n in ai.get_all_curve_names()] if ai and hasattr(ai, 'get_all_curve_names') else []
P['_face_curve_count'] = len(names); P['_blinkish'] = [n for n in names if 'blink' in n.lower()][:12]; P['_lookish'] = [n for n in names if 'look' in n.lower()][:12]
watch = ['CTRL_expressions_eyeBlinkL', 'CTRL_expressions_eyeLookLeftL', 'CTRL_expressions_eyeLookRightL'] + [n for n in names if 'blink' in n.lower()][:2] + [n for n in names if 'jawOpen' in n or 'browRaise' in n][:3]
st = dict(t0=time.time(), rows=[], h=None)
def tick(dt):
    try:
        t = time.time() - st['t0']
        if not u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world(): u.unregister_slate_post_tick_callback(st['h']); return
        a = face.get_anim_instance(); r = [round(t, 2)] + [round(a.get_curve_value(n), 3) for n in watch]
        try:
            le = face.get_socket_rotation('FACIAL_L_Eye'); hd = face.get_socket_rotation('head'); r += [round(le.yaw - hd.yaw, 2), round(le.pitch - hd.pitch, 2)]
        except Exception: pass
        for mt in ('head_lod0_mesh__eyeBlinkL', 'eyeBlinkL'): 
            try: r.append(round(face.get_morph_target(mt), 3))
            except Exception: pass
        st['rows'].append(r)
        if t > 12.0:
            P['_watch'] = watch; P['_samples'] = st['rows']; json.dump(P, open(u.Paths.project_dir() + 'Saved/UE59Work/vf2c/anat_probe.json', 'w')); u.unregister_slate_post_tick_callback(st['h'])
    except Exception as ex:
        P['_err'] = repr(ex)[:200]; json.dump(P, open(u.Paths.project_dir() + 'Saved/UE59Work/vf2c/anat_probe.json', 'w')); u.unregister_slate_post_tick_callback(st['h'])
st['h'] = u.register_slate_post_tick_callback(tick); print('ANAT armed', len(names), watch)
