# cm_turn2.py (write): repair of cm_turn1. Two faults found by the chain dump (q_speedchain.py) and a live probe:
#  1. the speed setter's source was FInterpTo(Current=GetMaxWalkSpeed, Target=select) and the turn scale was multiplied
#     into its OUTPUT -> feedback loop (max speed x0.3 every frame -> 7.5 cm/s). Now the scale multiplies the TARGET.
#  2. GR_TurnScale sat at 0.3 with heading error 0 -> the hand-built 1-(err-25)/110 chain did not evaluate as intended.
#     Replaced by one MapRangeClamped(err, 25..135 -> 1.0..0.3) node.
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
PP='/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'
def pv(p,k):
    try: return str(B.get_pin_value([x for x in info(p).input_pins if str(x.name)==k][0].pin_id))
    except Exception: return None
def build(bp):
    g=Gr(bp); N=[pn(x) for x in B.find_nodes(g.g)]; tp=lambda p:str(info(p).type_id); ins=lambda p:[str(x.name) for x in info(p).input_pins]
    sms=[p for p in N if tp(p).endswith('SetMaxWalkSpeed')]; assert len(sms)==1; sm=sms[0]
    mul=src((sm,'MaxWalkSpeed'))[0][0]; assert 'float*float' in tp(mul) or 'Multiply' in tp(mul),tp(mul)
    fi=src((mul,'A'))[0][0]; assert tp(fi).endswith('FInterpTo'),tp(fi)
    tgt=src((fi,'Target'))[0]; print('TARGET src',tp(tgt[0])[-30:])
    # 1. setter <- FInterpTo directly; FInterpTo.Target <- select * GR_TurnScale
    disconnect((sm,'MaxWalkSpeed')); connect((fi,'ReturnValue'),(sm,'MaxWalkSpeed'))
    disconnect((fi,'Target')); m2=g.fn(M+'Multiply_DoubleDouble',A=tgt,B=g.get('GR_TurnScale')); connect((m2,'ReturnValue'),(fi,'Target')); print('STEP speed target scaled')
    # 2. GR_TurnScale target <- MapRangeClamped(err)
    sts=[p for p in N if 'GR_TurnScale' in ins(p) and 'execute' in ins(p)]; assert len(sts)==1; st=sts[0]
    fi2=src((st,'GR_TurnScale'))[0][0]; assert tp(fi2).endswith('FInterpTo'),tp(fi2)
    she=[p for p in N if 'GR_HeadErr' in ins(p) and 'execute' in ins(p)]; assert len(she)==1; err=src((she[0],'GR_HeadErr'))[0]
    disconnect((fi2,'Target')); mr=g.fn(M+'MapRangeClamped',Value=err,InRangeA=25.0,InRangeB=135.0,OutRangeA=1.0,OutRangeB=0.3); connect((mr,'ReturnValue'),(fi2,'Target'))
    print('MAPRANGE pins',{k:pv(mr,k) for k in ('InRangeA','InRangeB','OutRangeA','OutRangeB')}); print('STEP scale formula replaced')
run(PP,build); print('DONE')
