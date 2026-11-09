# cm_gait2.py (write): gait latch while coasting. Measured (P_phys_a seg 7): on key release at 500 cm/s the gait selector
# fell to Walk 0.18 s into the stop (Shift released -> GR_Gait 0, run AND false), so the driver switched to the Walk
# database mid-stop and Run_Fwd_Stop (only in PSD_Sph_Run) could never be chosen; the body jumped between start-turn
# clips. SHME contract: the stop belongs to the gait you were in. GR_GaitSel keeps its previous value while there is no
# movement input and the capsule is still moving (> 30 cm/s); any new input or a full stop releases the latch.
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
PP='/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'
def build(bp):
    g=Gr(bp); N=[pn(x) for x in B.find_nodes(g.g)]; tp=lambda p:str(info(p).type_id); ins=lambda p:[str(x.name) for x in info(p).input_pins]
    sg=[p for p in N if 'GR_GaitSel' in ins(p) and 'execute' in ins(p)]; assert len(sg)==1,sg; sg=sg[0]
    sel=src((sg,'GR_GaitSel')); assert len(sel)==1; sel=sel[0]; print('SEL src',tp(sel[0])[-30:])
    inp=(g.fn(M+'VSize',A=(g.fn('/Script/Engine.Pawn:GetLastMovementInputVector'),'ReturnValue')),'ReturnValue')
    spd=(g.fn(M+'VSizeXY',A=(g.fn('/Script/Engine.Actor:GetVelocity'),'ReturnValue')),'ReturnValue')
    hold=(g.fn(M+'BooleanAND',A=(g.fn(M+'Less_DoubleDouble',A=inp,B=0.1),'ReturnValue'),B=(g.fn(M+'Greater_DoubleDouble',A=spd,B=30.0),'ReturnValue')),'ReturnValue')
    disconnect((sg,'GR_GaitSel'))
    latched=(g.fn(M+'SelectInt',A=g.get('GR_GaitSel'),B=sel,bPickA=hold),'ReturnValue'); connect(latched,(sg,'GR_GaitSel')); print('LATCH wired')
run(PP,build); print('DONE')
