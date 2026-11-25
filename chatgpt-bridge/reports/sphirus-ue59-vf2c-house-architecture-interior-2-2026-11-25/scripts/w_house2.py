# w_house2.py (write, gated): build the four layered house materials on a clean session, re-parent the five instances, save exactly those.
import unreal as u, builtins
exec(open(u.Paths.project_dir() + 'Tools/VF2C_20261125/apply_house2.py', encoding='utf8').read())
mel = u.MaterialEditingLibrary
for t in builtins.VF2H2_TOUCHED: print('WH2 saved', t.get_name(), u.EditorAssetLibrary.save_loaded_asset(t, False))
S = u.EditorLoadingAndSavingUtils; print('WH2 dirty', [p.get_name() for p in S.get_dirty_content_packages()], [p.get_name() for p in S.get_dirty_map_packages()])
