# w_sdb_revert.py (write, gated): revert the failed candidate PSD_Sph_SprintJog_Stops (Motion Matching still chose the sprint stop
# at 430, FS_E_s3): remove the SphS_Stops notify track from the four clips, delete the unreferenced database created by w_sdb.py.
import unreal as u
EA = u.EditorAssetLibrary; AL = u.AnimationLibrary
for p in ('/Game/Characters/UEFN_Mannequin/Animations/Sprint/M_Relaxed_Sprint_Stop_F_Lfoot', '/Game/Characters/UEFN_Mannequin/Animations/Sprint/M_Relaxed_Sprint_Stop_F_Rfoot',
          '/Game/Characters/UEFN_Mannequin/Animations/Run/M_Neutral_Run_Stop_F_Lfoot', '/Game/Characters/UEFN_Mannequin/Animations/Run/M_Neutral_Run_Stop_F_Rfoot'):
    a = u.load_asset(p); assert a
    if 'SphS_Stops' in [str(t) for t in AL.get_animation_notify_track_names(a)]: AL.remove_animation_notify_track(a, 'SphS_Stops')
    assert EA.save_loaded_asset(a, False); print('TRACKS', a.get_name(), [str(t) for t in AL.get_animation_notify_track_names(a)])
D = '/Game/Sphirus/Player/GASP/DB/PSD_Sph_SprintJog_Stops'
if EA.does_asset_exist(D):
    refs = [r for r in EA.find_package_referencers_for_asset(D, False)]; print('REFS', refs)
    if not refs: print('DELETED', EA.delete_asset(D))
print('EXISTS_AFTER', EA.does_asset_exist(D)); print('DONE')
