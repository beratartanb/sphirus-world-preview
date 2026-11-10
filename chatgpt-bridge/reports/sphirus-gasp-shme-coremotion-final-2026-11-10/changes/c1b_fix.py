# c1b_fix.py (write): AC_Sph_Motion '1 - x' subtract nodes lost their literal A=1.0 (promotable float-float operator:
# a literal set on A is reset when B is connected afterwards). Re-set A on every float-float node whose A is unlinked.
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
def build(bp):
    g=Gr(bp); n=0
    for p in [pn(x) for x in B.find_nodes(g.g)]:
        if str(info(p).type_id).endswith('float-float') and not src((p,'A')): value((p,'A'),1.0); n+=1
    print('FIXED',n); assert n==3
run('/Game/Sphirus/Player/Motion/AC_Sph_Motion',build)
exec(open(u.Paths.project_dir()+'Tools/GASP_20261109/gdump.py',encoding='utf8').read())
gdump(B.get_graph(u.load_asset('/Game/Sphirus/Player/Motion/AC_Sph_Motion'),'EventGraph'),u.Paths.project_dir()+'Tools/GASP_20261109/g_motion.txt'); print('DONE')
