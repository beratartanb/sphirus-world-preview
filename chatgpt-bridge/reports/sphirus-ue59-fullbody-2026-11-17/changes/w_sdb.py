# w_sdb.py (write, gated runner + manifest): PSD_Sph_SprintJog_Stops = Relaxed sprint stops + Neutral forward run stops.
# Why: with the curated jog speed (430) the stop chooser selects the Sprint_Stops database, so a jog stop plays the sprint stop
# (pelvis drop 32 cm, FS_P_s1) where production A at 375 played a run stop (14.5 cm, FS_A_s2). The combined database lets Motion
# Matching pick by velocity. Populated through one extra BranchIn notify track (SphS_Stops) on four clips. No ABP change here.
import unreal as u, json
EA = u.EditorAssetLibrary; AL = u.AnimationLibrary; AT = u.AssetToolsHelpers.get_asset_tools()
B = '/Game/Characters/UEFN_Mannequin/Animations/MotionMatchingData/Databases/'; D = '/Game/Sphirus/Player/GASP/DB'; name = 'PSD_Sph_SprintJog_Stops'
s = u.load_asset(B + 'Relaxed/PSD_Relaxed_Stand_Sprint_Stops'); r = u.load_asset(B + 'Dense/PSD_Dense_Stand_Run_Stops'); assert s and r
print('SCHEMA sprint', s.get_editor_property('schema').get_name(), 'run', r.get_editor_property('schema').get_name(), 'tags', s.get_editor_property('tags'), r.get_editor_property('tags'))
clips = [s.get_animation_asset(i) for i in range(s.get_num_animation_assets())]
clips += [c for c in (r.get_animation_asset(i) for i in range(r.get_num_animation_assets())) if c and c.get_name() in ('M_Neutral_Run_Stop_F_Lfoot', 'M_Neutral_Run_Stop_F_Rfoot')]
assert len(clips) == 4, [c.get_name() for c in clips]
f = u.DataAssetFactory(); f.set_editor_property('data_asset_class', u.PoseSearchDatabase)
db = u.load_asset(D + '/' + name) if EA.does_asset_exist(D + '/' + name) else AT.create_asset(name, D, u.PoseSearchDatabase, f)
for k in ('schema', 'continuing_pose_cost_bias', 'base_cost_bias', 'looping_cost_bias', 'tags', 'normalization_set', 'pose_search_mode'):
    try: db.set_editor_property(k, s.get_editor_property(k))
    except Exception as e: print('PROP', k, str(e)[:100])
assert EA.save_loaded_asset(db, False)
for a in clips:
    if 'SphS_Stops' in [str(t) for t in AL.get_animation_notify_track_names(a)]: AL.remove_animation_notify_track(a, 'SphS_Stops')
    AL.add_animation_notify_track(a, 'SphS_Stops'); st = AL.add_animation_notify_state_event(a, 'SphS_Stops', 0.0, float(a.get_play_length()), u.AnimNotifyState_PoseSearchBranchIn)
    st.set_editor_property('database', db); assert EA.save_loaded_asset(a, False)
assert EA.save_loaded_asset(db, False)
got = sorted(db.get_animation_asset(i).get_name() for i in range(db.get_num_animation_assets()) if db.get_animation_asset(i))
print('GOT', got, 'PATHS', [c.get_path_name() for c in clips]); print('ALL_OK', got == sorted(c.get_name() for c in clips)); print('DONE')
