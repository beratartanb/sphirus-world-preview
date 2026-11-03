import unreal as u, json
AL = u.AnimationLibrary; out = {}
for p in ['/Game/GraceRanger/SHME/Animations/V237/SHM237_JogStop_Bl_P16', '/Game/GraceRanger/SHME/Animations/V253/SHM253_JogStop_Bl_P16', '/Game/GraceRanger/SHME/Animations/V252/SHM252_StartTransfer_FR_Rfoot_APA']:
    s = u.load_asset(p); r = []
    for ev in AL.get_animation_notify_events(s):
        st = ev.get_editor_property('notify_state_class'); nt = ev.get_editor_property('notify')
        o = st or nt; d = {}
        for k in ('database', 'cost_addend', 'continuing_pose_cost_addend'):
            try: d[k] = str(o.get_editor_property(k)).split('.')[-1][:40]
            except Exception: pass
        r.append([o.get_class().get_name() if o else None, round(float(ev.get_editor_property('trigger_time_offset')), 3) if False else None, round(AL.get_animation_notify_event_trigger_time(s, ev), 3) if hasattr(AL, 'get_animation_notify_event_trigger_time') else None, d])
    try: r.append(['link', [round(float(ev.get_editor_property('duration')), 3) for ev in AL.get_animation_notify_events(s)]])
    except Exception as e: r.append(['dur_err', str(e)[:80]])
    out[p.split('/')[-1]] = {'tracks': [str(t) for t in AL.get_animation_notify_track_names(s)], 'ev': r, 'len': s.get_play_length()}
print('NOTIF253 ' + json.dumps(out, default=str))
