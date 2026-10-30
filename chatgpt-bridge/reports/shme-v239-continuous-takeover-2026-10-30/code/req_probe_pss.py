import unreal as u
d = u.load_asset('/Game/GraceRanger/SHME/Animations/V238/PSD_SHM238_JogCut'); s = d.get_editor_property('schema'); print('SCHEMA', s.get_path_name())
for k in ('channels', 'sample_rate', 'data_preprocessor', 'add_data_padding'):
    try: v = s.get_editor_property(k); print(k, v if k != 'channels' else len(v))
    except Exception as e: print(k, 'ERR', str(e)[:80])
for c in s.get_editor_property('channels'):
    props = {}
    for k in ('weight', 'sample_role', 'debug_color', 'sampled_bones', 'samples', 'bone', 'sample_time_offset', 'channel_name'):
        try: v = c.get_editor_property(k); props[k] = (len(v) if isinstance(v, (list, u.Array)) else str(v)[:40])
        except Exception: pass
    print('CH', c.get_class().get_name(), props)
    for k in ('sampled_bones', 'samples'):
        try:
            for x in c.get_editor_property(k)[:8]: print('    ', str(x.to_tuple() if hasattr(x, 'to_tuple') else x)[:200])
        except Exception: pass
