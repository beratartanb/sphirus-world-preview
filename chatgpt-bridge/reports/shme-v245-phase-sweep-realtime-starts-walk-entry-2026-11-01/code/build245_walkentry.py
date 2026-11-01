"""build245_walkentry.py (editor job, write manifest = SHM245_Walk_Fwd (+ PSD_LB_WalkLoops backup)): make the V2.45 walk candidate a PERMANENT,
testable entry of the PROJECT walk-loop database PSD_LB_WalkLoops (a GraceRanger asset; the chooser CHT_PBI_PlayerDense selects it and its
rows are not reachable from Python) WITHOUT touching the vendor clips: the project clip SHM245_Walk_Fwd gets a full-window BranchIn
(track SHME_V245_Walk -> PSD_LB_WalkLoops) and a full-window PoseSearchModifyCost (cost_addend, default -1.0) so that, with feet and
trajectory identical to A_LB_Walk_Fwd, the candidate wins the tie. Rollback = builtins.V245_WE['remove'] (tracks removed; the clip must
then be deleted and the editor restarted: removal leaves a stale entry, see memory). Prints WENTRY245 {...}."""
import unreal as u, json, builtins
L = u.AnimationLibrary; EAL = u.EditorAssetLibrary
c = dict(getattr(builtins, 'V245_WE', {})); CLIP = c.get('clip', '/Game/GraceRanger/SHME/Animations/V245/SHM245_Walk_Fwd'); DB = '/Game/GraceRanger/Animations/LocomotionBehavior/PSD_LB_WalkLoops'
ADD = float(c.get('cost_addend', -1.0)); REMOVE = bool(c.get('remove', False)); tr = 'SHME_V245_Walk'; tr2 = 'SHME_V245_WalkCost'
s = u.load_asset(CLIP); db = u.load_asset(DB); assert s and db
names = [str(t) for t in L.get_animation_notify_track_names(s)]; out = {'clip': CLIP, 'db': DB, 'tracks_before': names}
for t_ in (tr, tr2):
    if t_ in names: L.remove_animation_notify_events_by_track(s, t_); L.remove_animation_notify_track(s, t_)
if not REMOVE:
    ln = float(s.get_play_length())
    L.add_animation_notify_track(s, tr); st = L.add_animation_notify_state_event(s, tr, 0.0, ln, u.AnimNotifyState_PoseSearchBranchIn); st.set_editor_property('database', db)
    try:
        L.add_animation_notify_track(s, tr2); mc = L.add_animation_notify_state_event(s, tr2, 0.0, ln, u.AnimNotifyState_PoseSearchModifyCost); mc.set_editor_property('cost_addend', ADD); out['modify_cost'] = ADD
    except Exception as ex: out['modify_cost_err'] = str(ex)[:120]
    try: s.set_editor_property('loop', True)
    except Exception: pass
out['saved'] = EAL.save_asset(CLIP, False)
try: out['entries'] = [db.get_animation_asset(i).get_name() for i in range(db.get_num_animation_assets())]
except Exception as ex: out['entries_err'] = str(ex)[:80]
out['dirty'] = [q.get_name() for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('WENTRY245 ' + json.dumps(out, default=str))
