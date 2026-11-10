# s1b_fix.py (write) on AC_Sph_Motion: restore two literal A pins wiped by the promotable-operator trap
#   (1 - BrakeEffortK*EUse) had A=0 -> brake decel ~0 (no stop at all);  (2 * SettleZ * SettleW) had A=0 -> undamped settle spring.
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
exec(open(u.Paths.project_dir()+'Tools/GASP_20261109/gdump.py',encoding='utf8').read())
P='/Game/Sphirus/Player/Motion/AC_Sph_Motion'
def build(bp):
    g=B.get_graph(bp,'EventGraph'); N=[pn(n) for n in B.find_nodes(g)]; tp=lambda p:str(info(p).type_id)
    def srcname(p,pin):
        s=src((p,pin)); return [str(info(a).type_id) for a,b in s]+[b for a,b in s]
    done=0
    for p in N:
        t=tp(p)
        if t.endswith('float-float') and not src((p,'A')):
            bs=src((p,'B'))
            if bs and tp(bs[0][0]).endswith('float*float') and any('BrakeEffortK' in x for x in srcname(bs[0][0],'A')):
                value((p,'A'),1.0); done+=1; print('FIX 1-kE',p)
        if t.endswith('float*float') and not src((p,'A')):
            if any('SettleZ' in x for x in srcname(p,'B')): value((p,'A'),2.0); done+=1; print('FIX 2*zeta',p)
    assert done==2,done
run(P,build)
a=u.load_asset(P); n=gdump(B.get_graph(a,'EventGraph'),u.Paths.project_dir()+'Tools/GASP_20261109/g_motion3.txt'); print('DUMP',n,'DONE')
