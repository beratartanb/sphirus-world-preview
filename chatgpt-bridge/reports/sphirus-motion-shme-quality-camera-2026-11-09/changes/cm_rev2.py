# cm_rev2.py (write): roll back the reversal database set (SHME step E). Same protocol, true-clip telemetry: the walk
# reversal spent 1.21 s in blends with the set (P_phys_l seg 4) against 0.75 s without it (P_phys_j2): a third database
# stage (Loop -> Rev -> Full -> Loop) forces one more re-search/blend, and the 180 start-turn clips still cannot hold
# because their history is "standing" while the capsule's is "walking" (the pack has no moving pivot with root yaw).
# The state is disabled by thresholds no heading error can reach (100 -> 9999, 30 -> 9999); databases and graph stay for
# a later clip-authoring pass.
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
PP='/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'
def pv(p,k):
    try: return str(B.get_pin_value([x for x in info(p).input_pins if str(x.name)==k][0].pin_id))
    except Exception: return None
def build(bp):
    g=Gr(bp); N=[pn(x) for x in B.find_nodes(g.g)]; tp=lambda p:str(info(p).type_id); ins=lambda p:[str(x.name) for x in info(p).input_pins]; n=0
    sr=[p for p in N if 'GR_Reverse' in ins(p) and 'execute' in ins(p)]; assert len(sr)==1
    # walk the boolean chain feeding the setter and raise every Greater(GR_HeadErr, 100/30) threshold
    seen=set(); stack=[src((sr[0],'GR_Reverse'))[0][0]]
    while stack:
        p=stack.pop()
        if str(p) in seen: continue
        seen.add(str(p))
        if 'Greater' in tp(p) or '>' in tp(p):
            b=pv(p,'B')
            try: bv=float(b)
            except (TypeError,ValueError): bv=None
            if bv in (100.0,30.0): value((p,'B'),9999.0); n+=1; print('RAISED',b)
        for ip in info(p).input_pins:
            try: stack+=[q[0] for q in src((p,str(ip.name)))]
            except Exception: pass
    print('CHANGED',n); assert n==2,n
run(PP,build)
bp=u.load_asset(PP); cdo=u.get_default_object(bp.generated_class()); cdo.set_editor_property('GR_Reverse',False); L.compile_blueprint(bp); assert EA.save_loaded_asset(bp,False); print('DONE')
