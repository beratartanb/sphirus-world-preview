# w_biascopies.py (write, gated, manifest ue59_m19_bias, NEW assets only): Sphirus test copies of the Relaxed sprint stop database
# with a higher base cost bias (vendor original untouched). Not saved: runtime A/B only (CM_ADD remap Relaxed sprint stops -> copy).
import unreal as u
AT = u.AssetToolsHelpers.get_asset_tools(); EAL = u.EditorAssetLibrary
src = u.load_asset('/Game/Characters/UEFN_Mannequin/Animations/MotionMatchingData/Databases/Relaxed/PSD_Relaxed_Stand_Sprint_Stops')
D = '/Game/Sphirus/Player/GASP/DB/Test'
for tag, b in (('B05', 0.5), ('B15', 1.5), ('B40', 4.0)):
    n = 'PSD_Sph_R_Sprint_Stops_' + tag
    a = u.load_asset(D + '/' + n) if EAL.does_asset_exist(D + '/' + n) else AT.duplicate_asset(n, D, src)
    a.set_editor_property('base_cost_bias', b); print('COPY', a.get_path_name(), a.get_editor_property('base_cost_bias'))
print('DONE')
