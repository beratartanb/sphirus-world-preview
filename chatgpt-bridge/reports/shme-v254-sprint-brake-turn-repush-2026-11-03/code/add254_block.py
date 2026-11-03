"""add254_block.py (dry = measure job, write = manifest of the SHM254 clips): V2.54 the planned turn-around / cut clips can only be ENTERED
near their start. Measured (v254d60 s54_lr rvc, sprint L/R spam): Motion Matching entered SHM254_Cut mid-clip (1.37 s, mid-transfer) - a
brake/plant/transfer is only physically valid from its own beginning. PoseSearch 'Block Transition' notify state (track SHME_V254_Block)
from ENTRY (0.12 s) to the clip end (the V2.10 / V2.51 method; continuing playback stays a candidate).
builtins.V254_BL = {'dry': bool, 'entry': 0.12}. Prints BLOCK254 {...}."""
import unreal as u, json, builtins
L = u.AnimationLibrary; EAL = u.EditorAssetLibrary; AR = u.AssetRegistryHelpers.get_asset_registry()
cfg = dict(getattr(builtins, 'V254_BL', {})); DRY = bool(cfg.get('dry', True)); ENTRY = float(cfg.get('entry', 0.12))
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
V = '/Game/GraceRanger/SHME/Animations/V254'; TR = 'SHME_V254_Block'
out = {'dry': DRY, 'entry': ENTRY, 'clips': {}, 'saved': 0}
for a in sorted(AR.get_assets_by_path(V, False), key=lambda x: str(x.asset_name)):
    if str(a.asset_class_path.asset_name) != 'AnimSequence': continue
    p = str(a.package_name); seq = u.load_asset(p); ln = seq.get_play_length()
    tracks = [str(t) for t in L.get_animation_notify_track_names(seq)]; rec = {'len': round(ln, 3), 'had_track': TR in tracks}
    if not DRY:
        if TR in tracks: L.remove_animation_notify_events_by_track(seq, TR)
        else: L.add_animation_notify_track(seq, TR)
        L.add_animation_notify_state_event(seq, TR, ENTRY, ln - ENTRY, u.AnimNotifyState_PoseSearchBlockTransition)
        assert EAL.save_asset(p, False), p; out['saved'] += 1
    out['clips'][p.split('/')[-1]] = rec
out['dirty'] = [q.get_name().split('/')[-1] for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('BLOCK254 ' + json.dumps(out, default=str))
