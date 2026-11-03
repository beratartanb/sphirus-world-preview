"""add251_cropblock.py (dry = measure job, write = manifest of the 6 crops): V2.51 the turning-start crops can only be ENTERED at their start.
Measured (v251 b60/c60 jstart, every variant incl. the continuing-pose bias and the exit release): the last 0.30 s of a crop is not a
candidate, so Motion Matching must leave it 0.30 s before its end; inside the held T2 database it then hops for single frames into the MIDDLE
of other crops (TurnR135 @0.83, TurnR090 @0.63) before a run start -> three blend-stack entries in three frames -> shoulder 77-80 m/s2 at
60 FPS. A turning start is only physically valid from its own beginning (planted feet, body at rest).
Patch: PoseSearch 'Block Transition' notify state (track SHME_V251_Block) from SHM251_ENTRY (0.25 s) to the clip end on each crop (the
V2.10 cut-clip method): entering the crop from its first 0.25 s stays possible, entering mid-turn is not; the exit then goes straight to a
run start / loop. builtins.V251_BL = {'dry': bool, 'entry': 0.25}. Prints CROPBLOCK251 {...}."""
import unreal as u, json, builtins
L = u.AnimationLibrary; EAL = u.EditorAssetLibrary
cfg = dict(getattr(builtins, 'V251_BL', {})); DRY = bool(cfg.get('dry', True)); ENTRY = float(cfg.get('entry', 0.25))
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
V = '/Game/GraceRanger/SHME/Animations/V248/'; TR = 'SHME_V251_Block'
out = {'dry': DRY, 'entry': ENTRY, 'clips': {}, 'saved': 0}
for s in 'LR':
    for d in ('090', '135', '180'):
        p = V + 'SHM248_Jog_Start_Turn%s%s_crop' % (s, d); seq = u.load_asset(p); ln = seq.get_play_length()
        tracks = [str(t) for t in L.get_animation_notify_track_names(seq)]; rec = {'len': round(ln, 3), 'had_track': TR in tracks, 'tracks': tracks}
        if not DRY:
            if TR in tracks: L.remove_animation_notify_events_by_track(seq, TR)
            else: L.add_animation_notify_track(seq, TR)
            L.add_animation_notify_state_event(seq, TR, ENTRY, ln - ENTRY, u.AnimNotifyState_PoseSearchBlockTransition)
            assert EAL.save_asset(p, False), p; out['saved'] += 1
        out['clips'][p.split('/')[-1]] = rec
out['dirty'] = [q.get_name().split('/')[-1] for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('CROPBLOCK251 ' + json.dumps(out, default=str))
