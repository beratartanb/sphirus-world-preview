# s1_settle.py (write) on AC_Sph_Motion: SHME visible-body drivers (one owner; consumed by ABP_Sph_Body_GASP).
#   AccL      signed longitudinal acceleration (speed derivative, smoothed 8/s)
#   SetX/SetV damped spring (omega SettleW, zeta SettleZ) driven by braking u = clamp(-AccL/700,0,1.2)*SettleDeg
#             -> chest carried forward late in the brake, small overshoot, settles (SHME V2.53 brake settle)
#   ChestLead signed angle input-vs-velocity * 0.12, clamped +-LeadMax, only above 80 cm/s, smoothed 6/s (turn preparation)
#   EffLean   EffLeanDeg * EUse above 250 cm/s (effort posture), smoothed 2/s
#   BodyOn    master switch (default OFF until promoted)
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
P='/Game/Sphirus/Player/Motion/AC_Sph_Motion'
bp=u.load_asset(P); have=[str(v) for v in B.list_variables(bp)]; assert 'SetX' not in have
V=(('BodyOn','bool'),('SpPrev','float'),('AccL','float'),('SetX','float'),('SetV','float'),('SettleDeg','float'),('SettleW','float'),('SettleZ','float'),('ChestLead','float'),('LeadMax','float'),('EffLean','float'),('EffLeanDeg','float'))
for n,t in V: B.add_variable(bp,n,t)
L.compile_blueprint(bp)
def build(bp):
    g=Gr(bp); N=[pn(x) for x in B.find_nodes(g.g)]; tp=lambda p:str(info(p).type_id); ins=lambda p:[str(x.name) for x in info(p).input_pins]
    def consumers(ep): return [(q,str(ip.name)) for q in N for ip in info(q).input_pins if ep in src((q,str(ip.name)))]
    bf=[p for p in N if 'BrakeFriction' in ins(p) and 'execute' in ins(p)]; assert len(bf)==1; bf=bf[0]
    T=consumers((bf,'then')); assert len(T)==1,T; disconnect(T[0])
    cst=[p for p in N if tp(p).endswith('CastToCharacter')][0]; asc=(cst,'AsCharacter')
    tk=[p for p in N if 'DeltaSeconds' in [str(x.name) for x in info(p).output_pins]][0]; dt=(tk,'DeltaSeconds')
    F=lambda name,**k:(g.fn(M+name,**k),'ReturnValue')
    v=(g.fn('/Script/Engine.Actor:GetVelocity',self=asc),'ReturnValue'); sp=F('VSizeXY',A=v)
    inv=(g.fn('/Script/Engine.Pawn:GetLastMovementInputVector',self=asc),'ReturnValue')
    hasIn=F('Greater_DoubleDouble',A=F('VSizeXY',A=inv),B=0.1)
    on=g.get('BodyOn'); t=(bf,'then')
    aRaw=F('Divide_DoubleDouble',A=F('Subtract_DoubleDouble',A=sp,B=g.get('SpPrev')),B=F('FMax',A=dt,B=0.001))
    t=g.set('AccL',F('FInterpTo',Current=g.get('AccL'),Target=aRaw,DeltaTime=dt,InterpSpeed=8.0),t)
    t=g.set('SpPrev',sp,t)
    uu=F('Multiply_DoubleDouble',A=F('FClamp',Value=F('Divide_DoubleDouble',A=g.get('AccL'),B=-700.0),Min=0.0,Max=1.2),B=g.get('SettleDeg'))
    acc=F('Subtract_DoubleDouble',A=F('Multiply_DoubleDouble',A=F('Multiply_DoubleDouble',A=g.get('SettleW'),B=g.get('SettleW')),B=F('Subtract_DoubleDouble',A=uu,B=g.get('SetX'))),
          B=F('Multiply_DoubleDouble',A=F('Multiply_DoubleDouble',A=F('Multiply_DoubleDouble',A=2.0,B=g.get('SettleZ')),B=g.get('SettleW')),B=g.get('SetV')))
    t=g.set('SetV',F('SelectFloat',A=F('Add_DoubleDouble',A=g.get('SetV'),B=F('Multiply_DoubleDouble',A=acc,B=F('FMin',A=dt,B=0.05))),B=0.0,bPickA=on),t)
    t=g.set('SetX',F('SelectFloat',A=F('Add_DoubleDouble',A=g.get('SetX'),B=F('Multiply_DoubleDouble',A=g.get('SetV'),B=F('FMin',A=dt,B=0.05))),B=0.0,bPickA=on),t)
    inN=F('Vector_Normal2D',A=inv); vN=F('Vector_Normal2D',A=v)
    cz=(g.fn(M+'BreakVector',InVec=F('Cross_VectorVector',A=vN,B=inN)),'Z')
    ang=F('DegAtan2',Y=cz,X=F('Dot_VectorVector',A=inN,B=vN))
    neg=F('Multiply_DoubleDouble',A=g.get('LeadMax'),B=-1.0)
    gate=F('BooleanAND',A=F('BooleanAND',A=hasIn,B=on),B=F('Greater_DoubleDouble',A=sp,B=80.0))
    lt=F('SelectFloat',A=F('FClamp',Value=F('Multiply_DoubleDouble',A=ang,B=0.12),Min=neg,Max=g.get('LeadMax')),B=0.0,bPickA=gate)
    t=g.set('ChestLead',F('FInterpTo',Current=g.get('ChestLead'),Target=lt,DeltaTime=dt,InterpSpeed=6.0),t)
    el=F('SelectFloat',A=F('Multiply_DoubleDouble',A=g.get('EffLeanDeg'),B=g.get('EUse')),B=0.0,bPickA=F('BooleanAND',A=on,B=F('Greater_DoubleDouble',A=sp,B=250.0)))
    t=g.set('EffLean',F('FInterpTo',Current=g.get('EffLean'),Target=el,DeltaTime=dt,InterpSpeed=2.0),t)
    connect(t,T[0]); print('SETTLE chain built')
run(P,build)
bp=u.load_asset(P); cdo=u.get_default_object(bp.generated_class())
for k,v in (('BodyOn',False),('SettleDeg',3.0),('SettleW',9.0),('SettleZ',0.45),('LeadMax',9.0),('EffLeanDeg',2.0)): cdo.set_editor_property(k,v)
for k in ('BodyOn','SettleDeg','SettleW','SettleZ','LeadMax','EffLeanDeg','IdleNext','Idle0','Idle1','Idle2','Idle3','Idle4'): B.set_variable_instance_editable(bp,k,True)
L.compile_blueprint(bp); e=errs(bp); print('ERR',e); assert not e; assert EA.save_loaded_asset(bp,False)
print('CDO',{k:cdo.get_editor_property(k) for k in ('BodyOn','SettleDeg','SettleW','SettleZ','LeadMax','EffLeanDeg')}); print('DONE')
