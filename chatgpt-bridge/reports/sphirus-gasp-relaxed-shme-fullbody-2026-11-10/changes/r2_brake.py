# r2_brake.py (write) on AC_Sph_Motion: physical brake owner (default PhysBrake OFF = GASP 2000 / friction 3 unchanged).
#   BrakeLatchSpeed = speed while there is input (held after release)
#   BrakeDecel = PhysBrake ? MapRangeClamped(BrakeLatchSpeed,165,585,BrakeDecelLow,BrakeDecelHigh) * (1 - BrakeEffortK*EUse) : 2000
#   BrakeFriction = PhysBrake ? 0 : 3        (constant deceleration -> stop time ~ v/decel like the Relaxed stop clips)
# Inserted right after SetAccScale (before the idle-break chain).
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
P='/Game/Sphirus/Player/Motion/AC_Sph_Motion'
bp=u.load_asset(P); have=[str(v) for v in B.list_variables(bp)]; assert 'BrakeDecel' not in have
for n,t in (('PhysBrake','bool'),('BrakeLatchSpeed','float'),('BrakeDecel','float'),('BrakeFriction','float'),('BrakeDecelLow','float'),('BrakeDecelHigh','float'),('BrakeEffortK','float')): B.add_variable(bp,n,t)
L.compile_blueprint(bp)
def build(bp):
    g=Gr(bp); N=[pn(x) for x in B.find_nodes(g.g)]; tp=lambda p:str(info(p).type_id); ins=lambda p:[str(x.name) for x in info(p).input_pins]
    def consumers(ep): return [(q,str(ip.name)) for q in N for ip in info(q).input_pins if ep in src((q,str(ip.name)))]
    acc=[p for p in N if 'AccScale' in ins(p) and 'execute' in ins(p)]; assert len(acc)==1; acc=acc[0]
    T=consumers((acc,'then')); print('after AccScale',T); assert len(T)==1
    disconnect(T[0])
    cst=[p for p in N if tp(p).endswith('CastToCharacter')][0]; asc=(cst,'AsCharacter')
    F=lambda name,**k:(g.fn(M+name,**k),'ReturnValue')
    sp=F('VSizeXY',A=(g.fn('/Script/Engine.Actor:GetVelocity',self=asc),'ReturnValue'))
    hasIn=F('Greater_DoubleDouble',A=F('VSizeXY',A=(g.fn('/Script/Engine.Pawn:GetLastMovementInputVector',self=asc),'ReturnValue')),B=0.1)
    t=(acc,'then')
    t=g.set('BrakeLatchSpeed',F('SelectFloat',A=sp,B=g.get('BrakeLatchSpeed'),bPickA=hasIn),t)
    mr=g.fn(M+'MapRangeClamped',Value=g.get('BrakeLatchSpeed'),OutRangeA=g.get('BrakeDecelLow'),OutRangeB=g.get('BrakeDecelHigh')); value((mr,'InRangeA'),165.0); value((mr,'InRangeB'),585.0)
    eff=F('Subtract_DoubleDouble',A=1.0,B=F('Multiply_DoubleDouble',A=g.get('BrakeEffortK'),B=g.get('EUse')))
    phys=F('Multiply_DoubleDouble',A=(mr,'ReturnValue'),B=eff)
    sel=g.fn(M+'SelectFloat',A=phys,bPickA=g.get('PhysBrake')); value((sel,'B'),2000.0)
    t=g.set('BrakeDecel',(sel,'ReturnValue'),t)
    sf=g.fn(M+'SelectFloat',bPickA=g.get('PhysBrake')); value((sf,'A'),0.0); value((sf,'B'),3.0)
    t=g.set('BrakeFriction',(sf,'ReturnValue'),t)
    connect(t,T[0]); print('BRAKE chain built')
run(P,build)
bp=u.load_asset(P); cdo=u.get_default_object(bp.generated_class())
for k,v in (('PhysBrake',False),('BrakeDecel',2000.0),('BrakeFriction',3.0),('BrakeDecelLow',380.0),('BrakeDecelHigh',780.0),('BrakeEffortK',0.15)): cdo.set_editor_property(k,v)
B.set_variable_instance_editable(bp,'PhysBrake',True)
for k in ('BrakeDecelLow','BrakeDecelHigh','BrakeEffortK'): B.set_variable_instance_editable(bp,k,True)
L.compile_blueprint(bp); e=errs(bp); print('ERR',e); assert not e; assert EA.save_loaded_asset(bp,False)
print('CDO',{k:cdo.get_editor_property(k) for k in ('PhysBrake','BrakeDecel','BrakeFriction','BrakeDecelLow','BrakeDecelHigh','BrakeEffortK')}); print('DONE')
