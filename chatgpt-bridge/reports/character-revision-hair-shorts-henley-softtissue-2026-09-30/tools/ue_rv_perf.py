"""GPU cost evidence (editor, RTX machine, not a shipping build): points the level viewport at the QA character (gameplay-like
distance), waits for the view to settle, then runs ProfileGPU (hierarchical per-pass timings written to the editor log).
Toggles the grooms off for a second profile so the hair cost can be read as a difference. Parse with parse_rv_perf.py."""
import unreal as u, builtins, time, json, pathlib
Q = builtins.SPH_RV_QA; R = pathlib.Path(u.Paths.project_dir()).resolve(); O = R/'Saved/Codex/CharacterRevision_20260930'
ues = u.get_editor_subsystem(u.UnrealEditorSubsystem)
ues.set_level_viewport_camera_info(u.Vector(-160, 260, 150), u.Rotator(yaw=-58, pitch=-6, roll=0))
b = Q['components']['Body']; b.play_animation(u.load_asset('/MetaHumanCharacter/Optional/Animation/UEFNAnimPreset/Locomotion/AS_MH_Neutral_Walk_Loop_F'), True); b.set_play_rate(1.0)
for part, c in Q['components'].items(): c.set_forced_lod(0)
for g, c in Q['garments'].items(): c.set_forced_lod(0)
st = {'n': 0, 'phase': 0, 'marks': []}
cap = Q['capture']; cc = Q['cc']; cap.set_actor_location(u.Vector(-230, 330, 150), False, False); cap.set_actor_rotation(u.Rotator(yaw=-55, pitch=-8, roll=0), False); cc.set_editor_property('fov_angle', 40.0)
for gc in Q['grooms'].values(): gc.set_visibility(True, False)
for g, c in Q['garments'].items(): c.set_visibility(True, False)
def tick(dt):
    st['n'] += 1; w = ues.get_editor_world()
    if st['n'] in (60, 210): cc.capture_scene()
    if st['n'] == 90: st['marks'].append(('hair_on', time.time())); u.SystemLibrary.execute_console_command(w, 'ProfileGPU'); cc.capture_scene()
    if st['n'] == 150:
        for gc in Q['grooms'].values(): gc.set_visibility(False, False)
    if st['n'] == 240: st['marks'].append(('hair_off', time.time())); u.SystemLibrary.execute_console_command(w, 'ProfileGPU'); cc.capture_scene()
    if st['n'] == 300:
        for gc in Q['grooms'].values(): gc.set_visibility(True, False)
        b.set_play_rate(0.0); u.unregister_slate_post_tick_callback(h); (O/'perf_marks.json').write_text(json.dumps(st['marks']))
h = u.register_slate_post_tick_callback(tick); print('PERF_STARTED')
