"""weight_export.py (measure job, read-only): render each landscape paint layer's final weightmap over the whole landscape into a
1017x1017 RGBA32F render target (issued from a tick, read 20 s later) -> <recon>/weight_<layer>.u8 (row = y, col = x) + stats.
builtins.XR2_WNAME suffix (default 'before'); used as the restore source of the path-paint trial."""
import unreal as u, pathlib, time, array, builtins, json
P = pathlib.Path(u.Paths.project_dir()) / 'Saved/Codex/ExteriorWorld_XR2_20261031/recon'
SUF = getattr(builtins, 'XR2_WNAME', 'before')
E = u.get_editor_subsystem(u.UnrealEditorSubsystem); assert E.get_game_world() is None
w = E.get_editor_world()
land = next(a for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors() if isinstance(a, u.Landscape))
LAY = ['layer1', 'layer2', 'Layer3', 'NoGrass']
st = {'k': 0, 'phase': 'render', 't': time.monotonic(), 'out': {}}
builtins.XR2_WRT = [u.RenderingLibrary.create_render_target2d(w, 1017, 1017, u.TextureRenderTargetFormat.RTF_RGBA32F, u.LinearColor(0, 0, 0, 1), False, False) for _ in LAY]


def tick(dt):
    now = time.monotonic()
    try:
        if st['phase'] == 'render' and now - st['t'] > 2:
            for i, l in enumerate(LAY):
                st['out'][l] = {'ok': bool(land.render_weightmap(land.get_actor_transform(), u.Box2D(u.Vector2D(0, 0), u.Vector2D(0, 0)), l, builtins.XR2_WRT[i]))}
            st.update(phase='read', t=now); return
        if st['phase'] == 'read' and now - st['t'] > 20:
            for i, l in enumerate(LAY):
                px = u.RenderingLibrary.read_render_target_raw(w, builtins.XR2_WRT[i], False)
                v = array.array('B', (max(0, min(255, round(c.r * 255))) for c in px))
                (P / ('weight_%s_%s.u8' % (l, SUF))).write_bytes(v.tobytes())
                st['out'][l].update({'n': len(v), 'max': max(v), 'mean': round(sum(v) / len(v), 2), 'g_max': round(max(c.g for c in px), 3)})
            (P / ('weight_%s.json' % SUF)).write_text(json.dumps(st['out'], indent=1))
            u.unregister_slate_post_tick_callback(builtins.XR2_WH); print('WEIGHT', st['out'])
    except Exception as ex:
        (P / ('weight_%s.json' % SUF)).write_text(json.dumps({'error': repr(ex)})); u.unregister_slate_post_tick_callback(builtins.XR2_WH)


builtins.XR2_WH = u.register_slate_post_tick_callback(tick)
print('WEIGHT_EXPORT scheduled', SUF)
