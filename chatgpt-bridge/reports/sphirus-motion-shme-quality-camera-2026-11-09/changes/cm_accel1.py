# cm_accel1.py (write): acceleration per gait, calibrated to the Core Motion start clips (q_prof root profiles):
# Walk_Fwd_Start reaches 180 at ~1.05 s (~170 cm/s2), Jog_Fwd_Start 300 at ~1.2 s (~250), Run_Fwd_Start 489 at 1.9 s
# (~260). With MaxAcceleration 450 the capsule reached walk speed in 0.41 s while the body (true clip, P_phys_e seg 1)
# played Walk_Fwd_Start 0.20->0.97 in phase: for ~0.5 s the feet moved slower than the ground (slide). SHME start-load
# contract: the capsule accelerates like the source. walk 220 (0.82 s), jog 300 (1.0 s), run 330 (1.5 s); written each
# tick from the latched GR_GaitSel after the braking setter (cm_brake1).
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
PP='/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'
def build(bp):
    g=Gr(bp); N=[pn(x) for x in B.find_nodes(g.g)]; tp=lambda p:str(info(p).type_id); ins=lambda p:[str(x.name) for x in info(p).input_pins]
    bs=[p for p in N if 'BrakingDecelerationWalking' in ins(p) and 'execute' in ins(p)]; assert len(bs)==1,bs; bs=bs[0]
    cmc=src((bs,'self')); assert len(cmc)==1; cmc=cmc[0]
    outs=[(q,str(ip.name)) for q in N for ip in info(q).input_pins if (bs,'then') in src((q,str(ip.name)))]; assert outs
    is2=(g.fn(M+'EqualEqual_IntInt',A=g.get('GR_GaitSel'),B=2),'ReturnValue'); is1=(g.fn(M+'EqualEqual_IntInt',A=g.get('GR_GaitSel'),B=1),'ReturnValue')
    acc=(g.fn(M+'SelectFloat',A=330.0,B=(g.fn(M+'SelectFloat',A=300.0,B=220.0,bPickA=is1),'ReturnValue'),bPickA=is2),'ReturnValue')
    setn=pn(g.e.add_set_member_variable_node('MaxAcceleration','/Script/Engine.CharacterMovementComponent')); assert setn
    connect(cmc,(setn,'self')); connect(acc,(setn,'MaxAcceleration'))
    for d_ in outs: disconnect(d_)
    connect((bs,'then'),(setn,'execute'))
    for d_ in outs: connect((setn,'then'),d_)
    print('ACCEL wired',len(outs))
run(PP,build); print('DONE')
