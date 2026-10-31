"""height_export.py (measure job, read-only): landscape heightmap -> <D>/<builtins.XR_HNAME>.u16 (1017x1017 LE). The export is issued
from a tick (after the editor has rendered) and read 30 s later; a readback of all-zero is retried up to 3 times (first recon run read zeros)."""
import unreal as u, pathlib, time, array, builtins
D = pathlib.Path(u.Paths.project_dir()) / 'Saved/Codex/ExteriorRedesign_20261031/recon'
NAME = getattr(builtins, 'XR_HNAME', 'height_before')
assert not (NAME == 'height_before' and (D / 'height_before.ok').exists()), 'height_before exists - never overwrite the restore source'
ed = u.get_editor_subsystem(u.UnrealEditorSubsystem); assert ed.get_game_world() is None, 'PIE running'
w = ed.get_editor_world()
land = next(a for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors() if isinstance(a, u.Landscape))
st = {'t': time.monotonic(), 'phase': 'export', 'try': 0}
builtins.XR_RT = u.RenderingLibrary.create_render_target2d(w, 1017, 1017, u.TextureRenderTargetFormat.RTF_RGBA32F, u.LinearColor(0, 0, 0, 1), False, False)


def tick(dt):
    now = time.monotonic()
    if st['phase'] == 'export' and now - st['t'] > 3:
        u.EditorLevelLibrary.editor_invalidate_viewports() if hasattr(u, 'EditorLevelLibrary') else None
        assert land.landscape_export_heightmap_to_render_target(builtins.XR_RT, False, True)
        st.update(phase='read', t=now); return
    if st['phase'] == 'read' and now - st['t'] > 30:
        vals = array.array('H', (round(c.r) for c in u.RenderingLibrary.read_render_target_raw(w, builtins.XR_RT, False)))
        if max(vals) == 0 and st['try'] < 3:
            st.update(phase='export', t=now, **{'try': st['try'] + 1}); return
        u.unregister_slate_post_tick_callback(builtins.XR_HT2)
        (D / (NAME + '.u16')).write_bytes(vals.tobytes()); (D / (NAME + '.ok')).write_text('%d %d try %d' % (min(vals), max(vals), st['try']))


builtins.XR_HT2 = u.register_slate_post_tick_callback(tick)
print('HEIGHT_EXPORT scheduled', NAME)
