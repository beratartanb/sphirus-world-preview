# c1c_cal.py (write): effort calibration - a calm walk start (~600 cm/s2) or a walking reversal must not build effort:
# Acc/700 -> Acc/1500, TurnSev x0.9 -> x0.45, rise gain 1.4 -> 0.9.
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
def pv(p,k):
    try: return float(B.get_pin_value([x for x in info(p).input_pins if str(x.name)==k][0].pin_id))
    except Exception: return None
def build(bp):
    g=Gr(bp); ch={}
    for p in [pn(x) for x in B.find_nodes(g.g)]:
        t=str(info(p).type_id)
        if t.endswith('float/float') and pv(p,'B')==700.0: value((p,'B'),1500.0); ch['acc']=1
        if t.endswith('float*float') and pv(p,'B') is not None and abs(pv(p,'B')-0.9)<1e-6: value((p,'B'),0.45); ch['turn']=1
        if t.endswith('float*float') and pv(p,'B') is not None and abs(pv(p,'B')-1.4)<1e-6: value((p,'B'),0.9); ch['gain']=1
    print('CHANGED',ch); assert len(ch)==3
run('/Game/Sphirus/Player/Motion/AC_Sph_Motion',build); print('DONE')
