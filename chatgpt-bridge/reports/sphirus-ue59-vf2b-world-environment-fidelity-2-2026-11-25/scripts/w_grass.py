# w_grass.py (write, gated): mute the ground-layer grass further (desat 0.62, gain 0.72 from the stored baseline) and save the 10 instances.
import unreal as u, builtins
builtins.R2G_GRASS = {'desat': 0.62, 'gain': 0.72}
exec(open(u.Paths.project_dir() + 'Tools/R2G2_20261123/apply_grass.py', encoding='utf8').read())
for m in builtins.R2G_GRASS_ASSETS: print('WG saved', m.get_name(), u.EditorAssetLibrary.save_loaded_asset(m, False))
S = u.EditorLoadingAndSavingUtils; print('WG dirty', [p.get_name() for p in S.get_dirty_content_packages()], [p.get_name() for p in S.get_dirty_map_packages()])
