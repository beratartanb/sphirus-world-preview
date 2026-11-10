# k1_idle.py (write) on AC_Sph_Motion: rare GASP idle breaks for the CMC/Motion-Matching path (GASP plays them only in its
# experimental state machine, which Sphirus keeps off). Owner = SphMotion tick, after AccScale:
#   still = speed<3 & no input & on ground & no montage & IdleEnabled  -> IdleTime += dt, else 0
#   IdleTime > IdleNext -> IdleIdx = rand 0..4 -> DefaultSlot dynamic montage of Idle0..Idle4 (blend 0.5/0.6), IdleNext = rand 14..26 s
#   while IdleOn: our clip no longer playing -> IdleOn off; input -> StopSlotAnimation(0.3) only if our clip still plays.
# Clips: GASP M_Neutral_Stand_Idle_Break_v01-04,v06 (UEFN driver skeleton, same pose family as the MM idle loop).
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
P='/Game/Sphirus/Player/Motion/AC_Sph_Motion'; AI_='/Script/Engine.AnimInstance:'
CL=['/Game/Characters/UEFN_Mannequin/Animations/Idle/M_Neutral_Stand_Idle_Break_v0%d'%i for i in (1,2,3,4,6)]
bp=u.load_asset(P); have=[str(v) for v in B.list_variables(bp)]
assert 'IdleOn' not in have,'already built'
for n,t in (('IdleEnabled','bool'),('IdleOn','bool'),('IdleTime','float'),('IdleNext','float'),('IdleIdx','int')): B.add_variable(bp,n,t)
for i in range(5): B.add_object_variable(bp,'Idle%d'%i,u.AnimSequenceBase.static_class())
B.add_object_variable(bp,'IdleClip',u.AnimSequenceBase.static_class())
L.compile_blueprint(bp)
def build(bp):
    g=Gr(bp); N=[pn(x) for x in B.find_nodes(g.g)]; tp=lambda p:str(info(p).type_id)
    ins=lambda p:[str(x.name) for x in info(p).input_pins]; outs=lambda p:[str(x.name) for x in info(p).output_pins]
    def consumers(ep): return [(q,str(ip.name)) for q in N for ip in info(q).input_pins if ep in src((q,str(ip.name)))]
    last=[p for p in N if 'AccScale' in ins(p) and 'execute' in ins(p)]; assert len(last)==1,last; last=last[0]
    assert not consumers((last,'then')),'tail not free'
    cst=[p for p in N if tp(p).endswith('CastToCharacter')]; assert len(cst)==1; cst=cst[0]; asc=(cst,'AsCharacter')
    tk=[p for p in N if 'DeltaSeconds' in outs(p)]; assert len(tk)==1; dt=(tk[0],'DeltaSeconds')
    F=lambda name,**k:(g.fn(M+name,**k),'ReturnValue')
    def X(path,tail,**a):   # call node; chained on exec when impure
        p=g.fn(path,**a)
        if 'execute' in ins(p): connect(tail,(p,'execute')); return p,(p,'then')
        return p,tail
    mesh=g.pos(g.e.add_get_member_variable_node('Mesh','/Script/Engine.Character')); assert mesh; connect(asc,(mesh,'self'))
    ai=(g.fn('/Script/Engine.SkeletalMeshComponent:GetAnimInstance',self=(mesh,'Mesh')),'ReturnValue')
    sp=F('VSizeXY',A=(g.fn('/Script/Engine.Actor:GetVelocity',self=asc),'ReturnValue'))
    hasIn=F('Greater_DoubleDouble',A=F('VSizeXY',A=(g.fn('/Script/Engine.Pawn:GetLastMovementInputVector',self=asc),'ReturnValue')),B=0.1)
    ground=(g.fn('/Script/Engine.NavMovementComponent:IsMovingOnGround',self=(g.fn('/Script/Engine.Pawn:GetMovementComponent',self=asc),'ReturnValue')),'ReturnValue')
    t=(last,'then')
    pm,t=X(AI_+'IsAnyMontagePlaying',t,self=ai); busy=(pm,'ReturnValue')
    ps,t=X(AI_+'IsPlayingSlotAnimation',t,self=ai,Asset=g.get('IdleClip')); value((ps,'SlotNodeName'),'DefaultSlot'); ours=(ps,'ReturnValue')
    on_t,on_f=g.br(g.get('IdleOn'),t)
    # IdleOn: leave on input or when the clip ended / was replaced by another montage
    leave_t,_=g.br(F('BooleanOR',A=hasIn,B=F('Not_PreBool',A=ours)),on_t)
    st_t,st_f=g.br(ours,leave_t)
    sp_,st_end=X(AI_+'StopSlotAnimation',st_t,self=ai); value((sp_,'InBlendOutTime'),0.3); value((sp_,'SlotNodeName'),'DefaultSlot')
    s1=g.pos(g.e.add_set_member_variable_node('IdleOn','')); value((s1,'IdleOn'),False); connect(st_end,(s1,'execute')); connect(st_f,(s1,'execute'))
    g.set('IdleTime',0.0,(s1,'then'))
    # not on: accumulate still time
    still=F('BooleanAND',A=F('BooleanAND',A=F('Less_DoubleDouble',A=sp,B=3.0),B=F('Not_PreBool',A=hasIn)),B=F('BooleanAND',A=ground,B=F('BooleanAND',A=F('Not_PreBool',A=busy),B=g.get('IdleEnabled'))))
    tt=g.set('IdleTime',F('SelectFloat',A=F('Add_DoubleDouble',A=g.get('IdleTime'),B=dt),B=0.0,bPickA=still),on_f)
    go,_=g.br(F('Greater_DoubleDouble',A=g.get('IdleTime'),B=g.get('IdleNext')),tt)
    rnd=g.fn(M+'RandomIntegerInRange'); value((rnd,'Min'),0); value((rnd,'Max'),4)
    tt=g.set('IdleIdx',(rnd,'ReturnValue'),go)
    ends=[]
    for i in range(5):
        if i<4:
            yes,no=g.br(F('EqualEqual_IntInt',A=g.get('IdleIdx'),B=i),tt)
        else: yes=tt
        a=g.set('IdleClip',g.get('Idle%d'%i),yes)
        pl,a=X(AI_+'PlaySlotAnimationAsDynamicMontage',a,self=ai,Asset=g.get('Idle%d'%i))
        for k,v in (('SlotNodeName','DefaultSlot'),('BlendInTime',0.5),('BlendOutTime',0.6),('InPlayRate',1.0),('LoopCount',1),('BlendOutTriggerTime',-1.0),('InTimeToStartMontageAt',0.0)): value((pl,k),v)
        ends.append(a)
        if i<4: tt=no
    s2=g.pos(g.e.add_set_member_variable_node('IdleOn','')); value((s2,'IdleOn'),True)
    for a in ends: connect(a,(s2,'execute'))
    a=g.set('IdleTime',0.0,(s2,'then'))
    rf=g.fn(M+'RandomFloatInRange'); value((rf,'Min'),14.0); value((rf,'Max'),26.0)
    g.set('IdleNext',(rf,'ReturnValue'),a)
    print('IDLE chain built')
run(P,build)
bp=u.load_asset(P); cdo=u.get_default_object(bp.generated_class())
cdo.set_editor_property('IdleEnabled',True); cdo.set_editor_property('IdleNext',16.0)
for i,c in enumerate(CL): a=u.load_asset(c); assert a,c; cdo.set_editor_property('Idle%d'%i,a)
B.set_variable_instance_editable(bp,'IdleEnabled',True)
L.compile_blueprint(bp); e=errs(bp); print('ERR',e); assert not e; assert EA.save_loaded_asset(bp,False)
print('CDO',cdo.get_editor_property('IdleEnabled'),cdo.get_editor_property('IdleNext'),[cdo.get_editor_property('Idle%d'%i).get_name() for i in range(5)]); print('DONE')
