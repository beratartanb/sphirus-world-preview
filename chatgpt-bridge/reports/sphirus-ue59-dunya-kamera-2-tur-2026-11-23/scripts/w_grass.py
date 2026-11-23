# w_grass.py (write, gated): muted ground-layer foliage colours (apply_grass.py), saved per instance.
import unreal as u, builtins
exec(open(u.Paths.project_dir()+'Tools/R2G2_20261123/apply_grass.py',encoding='utf8').read())
for mi in builtins.R2G_GRASS_ASSETS: print('SAVE',mi.get_name(),u.EditorAssetLibrary.save_loaded_asset(mi,False))
S=u.EditorLoadingAndSavingUtils; print('DIRTY_AFTER',[p.get_name() for p in S.get_dirty_map_packages()],[p.get_name() for p in S.get_dirty_content_packages()])
