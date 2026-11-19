exec(open(__import__('unreal').Paths.project_dir()+'Tools/UE59_20261119/b59.py',encoding='utf8').read())
# p3_relax.py (write, gated) on ABP_Sph_Body_GASP: shoulder/arm RELAX terms appended to the posture layer (2026-11-19).
# Diagnosis (an_shoulder.py, seqA/B): steady walk upper-arm abduction 15.6 deg (idle 10.8), shoulder joints 1.3 cm higher and
# 1.5 cm behind the chest joint; after jog->walk the Neutral Run_to_Walk transition clip keeps the run arm carriage
# (abduction 28 deg) for ~1 s in the driver itself. The posture layer had no walk-only or slow-down channel.
#   MoveA = FInterpTo(clamp(speed/150, 0, 1), 4/s)                         (0 standing, 1 walking or faster)
#   RelA  = FInterpTo(target, RelUp if rising else RelDown), target = clamp((prevSpeed - speed)/dt / RelDecel, 0, 1) x clamp((speed-40)/60, 0, 1)
#   P<bone> += (VW_<bone> x MoveA + VD_<bone> x RelA) x ArmW              (ArmW = 0 while a montage plays: interactions untouched)
# for ClavL, ClavR, ArmL, ArmR, Spine5. All new vectors default 0 (inert) - values are stored separately after runtime screening.
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
P='/Game/Sphirus/Player/GASP/ABP_Sph_Body_GASP'
a=u.load_asset(P); have=[str(v) for v in B.list_variables(a)]; assert 'MoveA' not in have,'already built'
BN=('ClavL','ClavR','ArmL','ArmR','Spine5')
for n in ('MoveA','RelA','SpPrev','RelDecel','RelUp','RelDown'): B.add_variable(a,n,'float')
for nm in BN:
    for t in 'WD': B.add_variable(a,'V%s_%s'%(t,nm),'Vector')
L.compile_blueprint(a)
for n in ['MoveA','RelA','SpPrev','RelDecel','RelUp','RelDown']+['V%s_%s'%(t,nm) for nm in BN for t in 'WD']:
    try: B.set_variable_instance_editable(a,n,True)
    except Exception as e: print('IE?',n,e)
def build(a):
    g=Gr(a); N=[pn(x) for x in B.find_nodes(g.g)]; tp=lambda p:str(info(p).type_id); ins=lambda p:[str(x.name) for x in info(p).input_pins]
    def consumers(ep): return [(q,str(ip.name)) for q in N for ip in info(q).input_pins if ep in src((q,str(ip.name)))]
    F=lambda name,**k:(g.fn(M+name,**k),'ReturnValue')
    ev=[p for p in N if tp(p).endswith('OlayBlueprintUpdateAnimation')]; assert len(ev)==1; dt=(ev[0],[str(x.name) for x in info(ev[0]).output_pins if 'Delta' in str(x.name)][0])
    last=[p for p in N if 'PHandR' in ins(p) and 'execute' in ins(p)]; assert len(last)==1,last; last=last[0]
    T=consumers((last,'then')); print('after PHandR',T)
    for x in T: disconnect(x)
    t=(last,'then')
    pawn=(g.fn('/Script/Engine.AnimInstance:TryGetPawnOwner'),'ReturnValue')
    sp=F('VSizeXY',A=(g.fn('/Script/Engine.Actor:GetVelocity',self=pawn),'ReturnValue'))
    t=g.set('MoveA',F('FInterpTo',Current=g.get('MoveA'),Target=F('FClamp',Value=F('Divide_DoubleDouble',A=sp,B=150.0),Min=0.0,Max=1.0),DeltaTime=dt,InterpSpeed=4.0),t)
    dec=F('Divide_DoubleDouble',A=F('Subtract_DoubleDouble',A=g.get('SpPrev'),B=sp),B=F('FMax',A=dt,B=0.001))
    rt=F('Multiply_DoubleDouble',A=F('FClamp',Value=F('Divide_DoubleDouble',A=dec,B=F('FMax',A=g.get('RelDecel'),B=1.0)),Min=0.0,Max=1.0),
         B=F('FClamp',Value=F('Divide_DoubleDouble',A=F('Subtract_DoubleDouble',A=sp,B=40.0),B=60.0),Min=0.0,Max=1.0))
    rs=F('SelectFloat',A=g.get('RelUp'),B=g.get('RelDown'),bPickA=F('Greater_DoubleDouble',A=rt,B=g.get('RelA')))
    t=g.set('RelA',F('FInterpTo',Current=g.get('RelA'),Target=rt,DeltaTime=dt,InterpSpeed=rs),t)
    t=g.set('SpPrev',sp,t)
    for nm in BN:
        r=g.fn(M+'BreakRotator',InRot=g.get('P'+nm))
        base=F('MakeVector',X=(r,'Roll'),Y=(r,'Pitch'),Z=(r,'Yaw'))
        add=F('Multiply_VectorFloat',A=F('Add_VectorVector',A=F('Multiply_VectorFloat',A=g.get('VW_'+nm),B=g.get('MoveA')),B=F('Multiply_VectorFloat',A=g.get('VD_'+nm),B=g.get('RelA'))),B=g.get('ArmW'))
        v=F('Add_VectorVector',A=base,B=add); br=g.fn(M+'BreakVector',InVec=v)
        t=g.set('P'+nm,(g.fn(M+'MakeRotator',Roll=(br,'X'),Pitch=(br,'Y'),Yaw=(br,'Z')),'ReturnValue'),t)
    for x in T: connect(t,x)
    print('RELAX chain built', len(BN))
run(P,build)
a=u.load_asset(P); d=u.get_default_object(a.generated_class())
print('CHECK', [str(v) for v in B.list_variables(a) if str(v).startswith(('VW_','VD_','MoveA','RelA'))])
for k,v in (('RelDecel',300.0),('RelUp',8.0),('RelDown',1.2)): d.set_editor_property(k,v)
L.compile_blueprint(a); assert EA.save_loaded_asset(a,False); print('DEFAULTS', [(k,d.get_editor_property(k)) for k in ('RelDecel','RelUp','RelDown')]); print('DONE')
