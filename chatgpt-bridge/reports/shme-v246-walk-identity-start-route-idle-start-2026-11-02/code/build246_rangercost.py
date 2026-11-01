"""build246_rangercost.py (editor job, write manifest = the clip): V2.46 walk identity - the project-integrated Ranger forward walk loop
(M_Ranger_Walk_Loop_F_PureForward_CWF, CharacterWorldFinal integration 2026-09-04, a 206 cm/s loop played at 0.64x) wins the first ~1.5 s
after every walk start (CWF start pose continuity) and hands over to the LB loop (SHM245_Walk_Fwd) later: two walk identities in sequence.
A full-window PoseSearchModifyCost (cost_addend, default +2.0) on that loop lets the LB family loop win from the first search while a
large pose mismatch (> addend) can still pick it. builtins.V246_RC = {'clip', 'cost_addend', 'remove'}. Prints RCOST246 {...}."""
import unreal as u, json, builtins
L = u.AnimationLibrary; EAL = u.EditorAssetLibrary
c = dict(getattr(builtins, 'V246_RC', {})); CLIP = c.get('clip', '/Game/ActionAdventureMovementS/Animations/Locomotion/CoreMotionAAMS/Integrated/CharacterWorldFinal/WalkLoops/M_Ranger_Walk_Loop_F_PureForward_CWF')
ADD = float(c.get('cost_addend', 2.0)); REMOVE = bool(c.get('remove', False)); tr = 'SHME_V246_Cost'
s = u.load_asset(CLIP); assert s, CLIP
names = [str(t) for t in L.get_animation_notify_track_names(s)]; out = {'clip': CLIP, 'tracks_before': names, 'remove': REMOVE}
if tr in names: L.remove_animation_notify_events_by_track(s, tr); L.remove_animation_notify_track(s, tr)
if not REMOVE:
    ln = float(s.get_play_length()); L.add_animation_notify_track(s, tr)
    mc = L.add_animation_notify_state_event(s, tr, 0.0, ln, u.AnimNotifyState_PoseSearchModifyCost); mc.set_editor_property('cost_addend', ADD); out['cost_addend'] = ADD
out['saved'] = EAL.save_asset(CLIP, False); out['tracks_after'] = [str(t) for t in L.get_animation_notify_track_names(s)]
out['dirty'] = [q.get_name() for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('RCOST246 ' + json.dumps(out, default=str))
