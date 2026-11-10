exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
exec(open(u.Paths.project_dir()+'Tools/GASP_20261109/gdump.py',encoding='utf8').read())
bp=u.load_asset('/Game/Sphirus/Player/Motion/AC_Sph_Motion'); print('DUMP',gdump(B.get_graph(bp,'EventGraph'),u.Paths.project_dir()+'Tools/GASP_20261109/g_motion.txt'))
