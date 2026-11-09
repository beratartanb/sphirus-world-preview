# cm_camlat1.py (write): lateral body-mass framing. Fixed-camera run labs (CS_run_kick): moving left the head sits at
# normalized X 0.20-0.25, moving right 0.45-0.49 (band 0.28-0.43), walking 0.20-0.29 / 0.27-0.39: the capsule is composed
# at ~0.33 and the body leans/offsets up to ~0.1 of the width into its travel direction; the depth-only lag pivot
# (cm_camlag1) cannot see that. The camera now reads the body's mass position: the visible pelvis offset from the capsule
# projected on the camera right axis, smoothed 4/s and clamped +-30 cm, added to the spring arm TargetOffset (world).
# Walking head sway (+-3 cm, 1 s) is attenuated by the 4/s ease to ~1 cm; no effect at idle or when the mesh is centred.
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
PP='/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'
bp0=u.load_asset(PP)
if 'GR_LatOff' not in [str(x) for x in B.list_variables(bp0)]: B.add_variable(bp0,'GR_LatOff','float')
L.compile_blueprint(bp0); del bp0; gc.collect(); print('STEP var')
def build(bp):
    g=Gr(bp); N=[pn(x) for x in B.find_nodes(g.g)]; tp=lambda p:str(info(p).type_id); ins=lambda p:[str(x.name) for x in info(p).input_pins]
    ticks=[p for p in N if 'Tick' in tp(p) and any('Delta' in str(x.name) for x in info(p).output_pins) and 'then' in [str(x.name) for x in info(p).output_pins]]; tick=ticks[0]; dtp=[str(x.name) for x in info(tick).output_pins if 'Delta' in str(x.name)][0]
    to=[p for p in N if 'TargetOffset' in ins(p) and 'execute' in ins(p) and src((p,'execute'))]; assert len(to)==1,to; to=to[0]
    add=src((to,'TargetOffset')); assert len(add)==1; add=add[0]; print('OFF src',tp(add[0])[-30:]); pre=src((to,'execute'))[0]
    yaw=(g.fn(M+'BreakRotator',InRot=(g.fn('/Script/Engine.Pawn:GetControlRotation'),'ReturnValue')),'Yaw')
    right=(g.fn(M+'GetRightVector',InRot=(g.fn(M+'MakeRotator',Roll=0.0,Pitch=0.0,Yaw=yaw),'ReturnValue')),'ReturnValue')
    pel=(g.fn('/Script/Engine.SceneComponent:GetSocketLocation',self=g.get('Manny'),InSocketName='pelvis'),'ReturnValue')
    diff=(g.fn(M+'Subtract_VectorVector',A=pel,B=(g.fn('/Script/Engine.Actor:K2_GetActorLocation'),'ReturnValue')),'ReturnValue')
    lat=(g.fn(M+'FClamp',Value=(g.fn(M+'Dot_VectorVector',A=diff,B=right),'ReturnValue'),Min=-30.0,Max=30.0),'ReturnValue')
    disconnect((to,'execute')); t=g.set('GR_LatOff',(g.fn(M+'FInterpTo',Current=g.get('GR_LatOff'),Target=lat,DeltaTime=(tick,dtp),InterpSpeed=4.0),'ReturnValue'),pre); connect(t,(to,'execute'))
    disconnect((to,'TargetOffset'))
    k=g.get('GR_LatOff'); off2=(g.fn(M+'Add_VectorVector',A=add,B=(g.fn(M+'Multiply_VectorVector',A=right,B=(g.fn(M+'MakeVector',X=k,Y=k,Z=k),'ReturnValue')),'ReturnValue')),'ReturnValue')
    connect(off2,(to,'TargetOffset')); print('LAT wired')
run(PP,build); print('DONE')
