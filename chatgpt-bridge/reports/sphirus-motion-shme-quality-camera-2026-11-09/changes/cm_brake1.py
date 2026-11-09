# cm_brake1.py (write): braking deceleration per gait, calibrated to the Core Motion stop clips (root profiles q_prof):
# Walk_Fwd_Stop 207->0 over ~1.5 s (~140 cm/s2), Jog_Fwd_Stop 374->0 over ~0.6 s (~550), Run_Fwd_Stop 512->0 over 1.3 s
# (~400). A single 650 stopped the walk in 0.31 s / 25 cm, 4-5x faster than the walk stop clip, so the trajectory never
# resembled the stop clip. New: walk 300 (180->0 in 0.6 s / 54 cm; the play-rate window 0.7-1.25 covers the rest),
# jog 500 (300->0 in 0.6 s / 90 cm), run 420 (500->0 in 1.2 s / 3 m, as the run stop clip). Written each tick from the
# latched GR_GaitSel into CharacterMovement.BrakingDecelerationWalking (same CMC reference as the SetMaxWalkSpeed node).
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
PP='/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'
def build(bp):
    g=Gr(bp); N=[pn(x) for x in B.find_nodes(g.g)]; tp=lambda p:str(info(p).type_id); ins=lambda p:[str(x.name) for x in info(p).input_pins]
    sg=[p for p in N if 'GR_GaitSel' in ins(p) and 'execute' in ins(p)]; assert len(sg)==1,sg; sg=sg[0]
    sms=[p for p in N if tp(p).endswith('SetMaxWalkSpeed')]; assert len(sms)==1; cmc=src((sms[0],'self')); assert len(cmc)==1,cmc; cmc=cmc[0]; print('CMC src',tp(cmc[0])[-40:])
    outs=[(q,str(ip.name)) for q in N for ip in info(q).input_pins if (sg,'then') in src((q,str(ip.name)))]; assert outs
    gs=g.get('GR_GaitSel')
    is2=(g.fn(M+'EqualEqual_IntInt',A=gs,B=2),'ReturnValue'); is1=(g.fn(M+'EqualEqual_IntInt',A=g.get('GR_GaitSel'),B=1),'ReturnValue')
    br=(g.fn(M+'SelectFloat',A=420.0,B=(g.fn(M+'SelectFloat',A=500.0,B=300.0,bPickA=is1),'ReturnValue'),bPickA=is2),'ReturnValue')
    setn=pn(g.e.add_set_member_variable_node('BrakingDecelerationWalking','/Script/Engine.CharacterMovementComponent')); assert setn
    connect(cmc,(setn,'self')); connect(br,(setn,'BrakingDecelerationWalking'))
    for d_ in outs: disconnect(d_)
    connect((sg,'then'),(setn,'execute'))
    for d_ in outs: connect((setn,'then'),d_)
    print('BRAKE wired',len(outs))
run(PP,build); print('DONE')
