# cm_camlag1.py (write): camera framing loss when moving left/right. Measured with the camera yaw fixed (CL_cam2.json):
# head normalized X idle 0.30, A (left) mean 0.05 min -0.06 (off screen), D 0.54, W+A 0.19, W+D 0.48. Cause: the spring
# arm's built-in position lag (7/s, max 45 cm) lets the pawn lead the camera laterally; 45 cm at 140 cm arm and 66 deg FOV
# is 0.25 of the screen width, added to the 0.30 shoulder composition. Fix: built-in lag off; a project-owned lag pivot
# (GR_LagPivot, VInterpTo 7/s) whose offset from the pawn is projected onto the camera forward axis (depth, +-45 cm) and
# up axis (+-15 cm) and written to the spring arm TargetOffset (world space). Lateral drift becomes zero, the weight feel
# (approach/recede along the view axis) stays.
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
PP='/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'
_LF=open(u.Paths.project_dir()+'Saved/Codex/Day_20261107/camlag_progress.txt','w')
def P(*a):
    print(*a); print(*a,file=_LF); _LF.flush()
bp0=u.load_asset(PP); have=[str(x) for x in B.list_variables(bp0)]
if 'GR_LagPivot' not in have: B.add_struct_variable(bp0,'GR_LagPivot',u.Vector.static_struct())
L.compile_blueprint(bp0); del bp0; gc.collect(); P('STEP var')
def build(bp):
    g=Gr(bp); N=[pn(x) for x in B.find_nodes(g.g)]; tp=lambda p:str(info(p).type_id); ins=lambda p:[str(x.name) for x in info(p).input_pins]
    ticks=[p for p in N if 'Tick' in tp(p) and any('Delta' in str(x.name) for x in info(p).output_pins) and 'then' in [str(x.name) for x in info(p).output_pins]]; tick=ticks[0]; dtp=[str(x.name) for x in info(tick).output_pins if 'Delta' in str(x.name)][0]
    ss=[p for p in N if 'GR_Steady' in ins(p) and 'execute' in ins(p)]; assert len(ss)==1,ss; ss=ss[0]
    outs=[(q,str(ip.name)) for q in N for ip in info(q).input_pins if (ss,'then') in src((q,str(ip.name)))]; assert outs
    loc=(g.fn('/Script/Engine.Actor:K2_GetActorLocation'),'ReturnValue')
    piv=(g.fn(M+'VInterpTo',Current=g.get('GR_LagPivot'),Target=loc,DeltaTime=(tick,dtp),InterpSpeed=7.0),'ReturnValue')
    for d_ in outs: disconnect(d_)
    t=g.set('GR_LagPivot',piv,(ss,'then'))
    diff=(g.fn(M+'Subtract_VectorVector',A=g.get('GR_LagPivot'),B=loc),'ReturnValue')
    yaw=(g.fn(M+'BreakRotator',InRot=(g.fn('/Script/Engine.Pawn:GetControlRotation'),'ReturnValue')),'Yaw')
    fwd=(g.fn(M+'GetForwardVector',InRot=(g.fn(M+'MakeRotator',Roll=0.0,Pitch=0.0,Yaw=yaw),'ReturnValue')),'ReturnValue')
    depth=(g.fn(M+'FClamp',Value=(g.fn(M+'Dot_VectorVector',A=diff,B=fwd),'ReturnValue'),Min=-45.0,Max=45.0),'ReturnValue')
    dz=(g.fn(M+'FClamp',Value=(g.fn(M+'BreakVector',InVec=diff),'Z'),Min=-15.0,Max=15.0),'ReturnValue')
    off=(g.fn(M+'Add_VectorVector',A=(g.fn(M+'Multiply_VectorVector',A=fwd,B=(g.fn(M+'MakeVector',X=depth,Y=depth,Z=depth),'ReturnValue')),'ReturnValue'),B=(g.fn(M+'MakeVector',X=0.0,Y=0.0,Z=dz),'ReturnValue')),'ReturnValue')
    # SpringArm.TargetOffset has no setter function: write the component property with a Set node
    setn=pn(g.e.add_set_member_variable_node('TargetOffset','/Script/Engine.SpringArmComponent')); assert setn; connect(g.get('SpringArm'),(setn,'self')); connect(off,(setn,'TargetOffset'))
    connect(t,(setn,'execute')); t=(setn,'then')
    for d_ in outs: connect(t,d_)
    P('GRAPH wired',len(outs))
run(PP,build); P('STEP graph saved')
bp=u.load_asset(PP); sds=u.get_engine_subsystem(u.SubobjectDataSubsystem); SB=u.SubobjectDataBlueprintFunctionLibrary
for h in sds.k2_gather_subobject_data_for_blueprint(bp):
    o=SB.get_object(SB.get_data(h))
    if o and isinstance(o,u.SpringArmComponent):
        c=SB.get_object_for_blueprint(SB.get_data(h),bp); c.set_editor_property('enable_camera_lag',False); P('ARM lag off; rotation lag',c.get_editor_property('enable_camera_rotation_lag'),c.get_editor_property('camera_rotation_lag_speed'))
L.compile_blueprint(bp); assert EA.save_loaded_asset(bp,False); P('DONE')
