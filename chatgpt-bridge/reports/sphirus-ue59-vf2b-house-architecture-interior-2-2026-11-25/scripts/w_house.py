# w_house.py (write, gated): build the two VF2 house materials under their final names, re-parent the three instances, save exactly those assets.
import unreal as u, builtins
builtins.VF2H = {}
exec(open(u.Paths.project_dir() + 'Tools/VF2B_20261125/apply_house.py', encoding='utf8').read())
E = u.EditorAssetLibrary
for t in builtins.VF2H_TOUCHED: print('WH saved', t.get_name(), E.save_loaded_asset(t, False))
S = u.EditorLoadingAndSavingUtils; print('WH dirty', [p.get_name() for p in S.get_dirty_content_packages()], [p.get_name() for p in S.get_dirty_map_packages()])
