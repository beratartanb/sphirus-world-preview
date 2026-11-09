# cm_turn3.py (write): tighten the turn brake measured in R_rev3 (speed still 115-134 cm/s at 0.5-0.75 s while the
# body had not finished the 180 turn): MapRangeClamped floor 0.3 -> 0.15 and the GR_TurnScale ease 8 -> 12/s.
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
PP='/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'
def pv(p,k):
    try: return str(B.get_pin_value([x for x in info(p).input_pins if str(x.name)==k][0].pin_id))
    except Exception: return None
def build(bp):
    g=Gr(bp); N=[pn(x) for x in B.find_nodes(g.g)]; tp=lambda p:str(info(p).type_id); ins=lambda p:[str(x.name) for x in info(p).input_pins]; n=0
    for p in N:
        if tp(p).endswith('MapRangeClamped') and pv(p,'InRangeA')=='25.0' and pv(p,'InRangeB')=='135.0': value((p,'OutRangeB'),0.15); n+=1
    sts=[p for p in N if 'GR_TurnScale' in ins(p) and 'execute' in ins(p)]; assert len(sts)==1
    fi=src((sts[0],'GR_TurnScale'))[0][0]; assert tp(fi).endswith('FInterpTo'); value((fi,'InterpSpeed'),12.0); n+=1
    print('CHANGED',n); assert n==2
run(PP,build); print('DONE')
