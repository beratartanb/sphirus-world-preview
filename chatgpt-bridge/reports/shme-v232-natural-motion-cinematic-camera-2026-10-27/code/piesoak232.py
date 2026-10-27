"""piesoak232.py (editor job) - V2.32 automation item: GameViewport.IsUnique() assertion study (SLevelViewport::EndPlayInEditorSession,
check that the level viewport holds the ONLY shared reference to the PIE FSceneViewport). Bare PIE cycles on the production map with NONE of
the QA harness work (no input injection, no console commands, no captures, no telemetry, no state record): begin play -> wait SOAK_HOLD
game seconds (default 3) -> end play from a Slate post-tick callback -> next cycle. Mode 'harness_end' adds exactly the QA end-path calls
(Input.-action / t.MaxFPS 0 / mcap_stop-equivalent no-op) before the end request, to separate the engine path from the harness end path.
builtins.SOAK232 = {'cycles': 60, 'hold': 3.0, 'mode': 'bare' | 'harness_end'}. Writes a progress line per cycle (SOAK232 n=..) to the log;
a crash ends the editor (the driver counts completed cycles from the log). Prints SOAK232_DONE {...} when all cycles finished."""
import unreal as u, builtins, json, time
cfg = getattr(builtins, 'SOAK232', {}); N = int(cfg.get('cycles', 60)); HOLD = float(cfg.get('hold', 3.0)); MODE = cfg.get('mode', 'bare')
les = u.get_editor_subsystem(u.LevelEditorSubsystem); ues = u.get_editor_subsystem(u.UnrealEditorSubsystem)
st = {'n': 0, 'phase': 'start', 't0': time.time(), 'gt0': None, 'wait': 0}
IA_LOOK = '/Game/AAMS/Demo/MotionMatching/Input/IA_Look.IA_Look'
def tick(dt):
    gw = ues.get_game_world()
    if st['phase'] == 'start':
        if gw is None:
            les.editor_request_begin_play(); st['phase'] = 'starting'; st['wait'] = 0
        return
    if st['phase'] == 'starting':
        st['wait'] += 1
        if gw is not None: st['phase'] = 'run'; st['gt0'] = u.GameplayStatics.get_time_seconds(gw)
        elif st['wait'] > 3000: u.log_error('SOAK232 PIE did not start'); finish('nostart')
        return
    if st['phase'] == 'run':
        if gw is None: st['phase'] = 'start'; return
        if u.GameplayStatics.get_time_seconds(gw) - st['gt0'] >= HOLD:
            if MODE == 'harness_end':
                u.SystemLibrary.execute_console_command(gw, 'Input.-action ' + IA_LOOK)
                u.SystemLibrary.execute_console_command(ues.get_editor_world(), 't.MaxFPS 0')
            les.editor_request_end_play(); st['phase'] = 'ending'; st['wait'] = 0
        return
    if st['phase'] == 'ending':
        st['wait'] += 1
        if gw is None:
            st['n'] += 1; u.log('SOAK232 n=%d mode=%s t=%.0f' % (st['n'], MODE, time.time() - st['t0']))
            if st['n'] >= N: finish('ok')
            else: st['phase'] = 'start'
        elif st['wait'] > 3000: u.log_error('SOAK232 PIE did not end'); finish('noend')
def finish(why):
    u.unregister_slate_post_tick_callback(st['h'])
    print('SOAK232_DONE ' + json.dumps({'cycles': st['n'], 'mode': MODE, 'hold': HOLD, 'why': why, 'wall_s': round(time.time() - st['t0'])}))
    u.log('SOAK232_DONE cycles=%d why=%s' % (st['n'], why))
st['h'] = u.register_slate_post_tick_callback(tick)
print('SOAK232_STARTED ' + json.dumps({'cycles': N, 'mode': MODE, 'hold': HOLD}))
