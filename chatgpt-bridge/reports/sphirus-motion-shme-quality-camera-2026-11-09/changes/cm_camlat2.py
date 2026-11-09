# cm_camlat2.py (write): lateral framing tracks the HEAD, not the pelvis. CS_run_lat (corridor, camera fixed): pelvis
# tracking centred the pelvis (A 0.33 / D 0.34) but the head still sat at 0.21 (A, run) / 0.46 (D, run) because the
# body leans ~0.13 of the width into its travel direction at run speed; the user reads the head as "the character".
# Same chain (cm_camlat1), only the socket of the GetSocketLocation node changes: pelvis -> head.
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
PP='/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'
def pv(p,k):
    try: return str(B.get_pin_value([x for x in info(p).input_pins if str(x.name)==k][0].pin_id))
    except Exception: return None
def build(bp):
    g=Gr(bp); N=[pn(x) for x in B.find_nodes(g.g)]; tp=lambda p:str(info(p).type_id); n=0
    for p in N:
        if tp(p).endswith('GetSocketLocation') and pv(p,'InSocketName')=='pelvis': value((p,'InSocketName'),'head'); n+=1
    print('CHANGED',n); assert n==1,n
run(PP,build); print('DONE')
