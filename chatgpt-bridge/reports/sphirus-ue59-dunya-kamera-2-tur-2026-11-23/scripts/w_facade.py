# w_facade.py (write, gated): facade material overrides (ground walls lime, gable ends aged boards), saved explicitly per touched level package.
import unreal as u, builtins
builtins.R2G_FACADE={'ground':'lime','gables':'cladding'}
exec(open(u.Paths.project_dir()+'Tools/R2G2_20261123/apply_facade.py',encoding='utf8').read())
S=u.EditorLoadingAndSavingUtils
print('DIRTY_BEFORE',[p.get_name() for p in S.get_dirty_map_packages()])
print('SAVE_PKGS',S.save_packages(builtins.R2G_FACADE_PKGS,False) if builtins.R2G_FACADE_PKGS else 'nothing touched')
print('DIRTY_AFTER',[p.get_name() for p in S.get_dirty_map_packages()],[p.get_name() for p in S.get_dirty_content_packages()])
