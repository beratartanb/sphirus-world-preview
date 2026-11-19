# w_r2w_window.py (write, gated, 2026-11-19 evening): run->walk transition selection window in PSD_Sph_N_Walk_F_Loops.
# The two Neutral Run_to_Walk clips are in the walk DB through the SphN_Walk_F_Loops PoseSearchBranchIn notify state (w_ndb.py,
# 2026-11-16) covering the whole clip (4.4 s). In game MM enters at clip start and stays 3.8 s: the clip root slows 500 -> 394 in
# 0.7 s while the capsule is already at walk speed (180) after 0.5 s, so the visible body keeps the run arm carriage (elbow 87-112)
# and then the large forward swing (hand 43 cm forward, 4 cm under chest level) at walk speed. The BranchIn window is cut to
# [0, END] so MM leaves the transition for the walk loop once the capsule has slowed. END from builtins-free constant below.
import unreal as u
END = 0.6
EA = u.EditorAssetLibrary; AL = u.AnimationLibrary
db = u.load_asset('/Game/Sphirus/Player/GASP/DB/PSD_Sph_N_Walk_F_Loops'); TR = 'SphN_Walk_F_Loops'
for side in ('Lfoot', 'Rfoot'):
    a = u.load_asset('/Game/Characters/UEFN_Mannequin/Animations/Walk/M_Neutral_Transition_Run_to_Walk_' + side)
    assert TR in [str(t) for t in AL.get_animation_notify_track_names(a)], side
    AL.remove_animation_notify_track(a, TR); AL.add_animation_notify_track(a, TR)
    st = AL.add_animation_notify_state_event(a, TR, 0.0, END, u.AnimNotifyState_PoseSearchBranchIn); st.set_editor_property('database', db)
    assert EA.save_loaded_asset(a, False)
    ev = [(round(e.get_editor_property('trigger_time_offset') if False else 0, 2)) for e in []]
    print('CLIP', side, a.get_play_length(), [str(t) for t in AL.get_animation_notify_track_names(a)])
assert EA.save_loaded_asset(db, False)
print('DB', sorted(db.get_animation_asset(i).get_name() for i in range(db.get_num_animation_assets()) if db.get_animation_asset(i)))
print('DONE')
