"""probe_vram.py (control job, read-only): write a full engine memory report (MemReport -full -> Saved/Profiling/MemReports/*.memreport)
so the texture / mesh / RHI budget of the loaded world can be ranked offline. Also records the texture streaming pool size and the GPU
adapter memory as the engine reports them. Output: Saved/Codex/PineForestRedesign_20261104/perf/vram_probe_<tag>.json"""
import unreal as u, json, pathlib, time, builtins, glob, os
PJ = pathlib.Path(u.Paths.project_dir()); TAG = getattr(builtins, 'PFR_VRAM_TAG', 'x'); OUT = PJ / 'Saved/Codex/PineForestRedesign_20261104/perf' / ('vram_probe_%s.json' % TAG)
w = u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
before = set(glob.glob(str(PJ / 'Saved/Profiling/MemReports/*.memreport')))
u.SystemLibrary.execute_console_command(w, 'MemReport -full')
res = {'tag': TAG, 'time': time.strftime('%Y-%m-%d %H:%M:%S'), 'pool_size_mb': None, 'memreport': None}
try:
    res['pool_size_mb'] = u.SystemLibrary.get_console_variable_int_value('r.Streaming.PoolSize')
except Exception as ex: res['pool_err'] = repr(ex)[:80]
st = {'t': time.monotonic()}


def tick(dt):
    new = set(glob.glob(str(PJ / 'Saved/Profiling/MemReports/*.memreport'))) - before
    if new or time.monotonic() - st['t'] > 60:
        u.unregister_slate_post_tick_callback(builtins.PFR_VRAM); res['memreport'] = sorted(new)[-1] if new else None
        OUT.write_text(json.dumps(res, indent=1)); print('PFR_VRAM', res)


builtins.PFR_VRAM = u.register_slate_post_tick_callback(tick)
print('PFR_VRAM scheduled', TAG)
