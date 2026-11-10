# c1_motion.py (write): /Game/Sphirus/Player/Motion/AC_Sph_Motion - project-owned movement-physics state component
# (independent of GASP / Core Motion / AAMS). Per tick, from the owner's real velocity and CMC input acceleration:
#   Acc        smoothed horizontal acceleration magnitude (cm/s2)
#   TurnSev    smoothed request-vs-velocity opposition (0 straight .. 1 reversal) x speed share
#   Demand     physical demand = Acc/700 + 0.9 TurnSev + 0.5 * speed above 300
#   E          accumulated effort, dE/dt = 1.4 Demand (1-E) - (E/5) clamp(1-2 Demand)   (rest ~5 s recovery; SHME V2.29)
#   EUse       low-passed effort (0.8/s) - the only value the consumers read (a maneuver never slows itself)
#   ReqLoad    momentary load latched on a request-direction change (>60 deg at >100 cm/s), decays 1.2/s
#   SpeedScale max-speed multiplier: drops toward 0.05 when the request opposes a fast velocity (brake -> plant -> push
#              instead of a constant-speed arc), asymmetric smoothing (fall 15/s, rise 3/s)
#   AccScale   acceleration multiplier 1 -> 0.75 with EUse (tired = slower re-acceleration)
# Switches: Enabled (whole layer), EffortEnabled (effort only) - for the A/B tests.
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
P='/Game/Sphirus/Player/Motion/AC_Sph_Motion'
bp=u.load_asset(P) if EA.does_asset_exist(P) else L.create_blueprint_asset_with_parent(P,u.ActorComponent); assert bp
have=[str(v) for v in B.list_variables(bp)]
for n,t in [('Enabled','bool'),('EffortEnabled','bool'),('PrevVel','Vector'),('PrevIn','Vector'),('Acc','float'),('TurnSev','float'),('Demand','float'),('E','float'),('EUse','float'),('ReqLoad','float'),('SpeedScale','float'),('AccScale','float'),('SpeedNow','float')]:
    if n not in have: B.add_variable(bp,n,t)
L.compile_blueprint(bp)
def build(bp):
    g=Gr(bp); ev=B.add_event(bp,'ReceiveTick'); evp=pn(ev); print('TICK pins',[str(x.name) for x in info(evp).output_pins])
    dt=(evp,'DeltaSeconds'); F=lambda name,**k:(g.fn(M+name,**k),'ReturnValue')
    own=(g.fn('/Script/Engine.ActorComponent:GetOwner'),'ReturnValue')
    cst=g.pos(B.create_node(g.g,'İşlevsellikler|Casting|CastToCharacter',(0,0))); co=[str(x.name) for x in info(cst).output_pins]; print('CAST outs',co)
    connect(own,(cst,'Object')); connect((evp,'then'),(cst,'execute'))
    asc=(cst,[x for x in co if x not in ('then','CastFailed','bSuccess')][0])
    v=(g.fn('/Script/Engine.Actor:GetVelocity',self=asc),'ReturnValue')
    acc=(g.fn('/Script/Engine.Pawn:GetLastMovementInputVector',self=asc),'ReturnValue')
    sp=F('VSizeXY',A=v)
    aRaw=F('Divide_DoubleDouble',A=F('VSizeXY',A=F('Subtract_VectorVector',A=v,B=g.get('PrevVel'))),B=F('FMax',A=dt,B=0.001))
    hasIn=F('Greater_DoubleDouble',A=F('VSizeXY',A=acc),B=0.1)
    inN=F('Vector_Normal2D',A=acc); vN=F('Vector_Normal2D',A=v)
    dIV=F('Dot_VectorVector',A=inN,B=vN)
    turnRaw=F('SelectFloat',A=F('Multiply_DoubleDouble',A=F('MapRangeClamped',Value=dIV,InRangeA=0.8,InRangeB=-0.9,OutRangeA=0.0,OutRangeB=1.0),B=F('MapRangeClamped',Value=sp,InRangeA=0.0,InRangeB=400.0,OutRangeA=0.0,OutRangeB=1.0)),B=0.0,bPickA=hasIn)
    t=(cst,'then')
    t=g.set('Acc',F('FInterpTo',Current=g.get('Acc'),Target=aRaw,DeltaTime=dt,InterpSpeed=6.0),t)
    t=g.set('PrevVel',v,t)
    t=g.set('SpeedNow',sp,t)
    t=g.set('TurnSev',F('FInterpTo',Current=g.get('TurnSev'),Target=turnRaw,DeltaTime=dt,InterpSpeed=10.0),t)
    dem=F('FClamp',Value=F('Add_DoubleDouble',A=F('Add_DoubleDouble',A=F('Divide_DoubleDouble',A=g.get('Acc'),B=700.0),B=F('Multiply_DoubleDouble',A=g.get('TurnSev'),B=0.9)),B=F('MapRangeClamped',Value=sp,InRangeA=300.0,InRangeB=700.0,OutRangeA=0.0,OutRangeB=0.5)),Min=0.0,Max=1.5)
    t=g.set('Demand',dem,t)
    E=g.get('E'); Dm=g.get('Demand')
    rise=F('Multiply_DoubleDouble',A=F('Multiply_DoubleDouble',A=Dm,B=1.4),B=F('Subtract_DoubleDouble',A=1.0,B=E))
    rec=F('Multiply_DoubleDouble',A=F('Divide_DoubleDouble',A=g.get('E'),B=5.0),B=F('FClamp',Value=F('Subtract_DoubleDouble',A=1.0,B=F('Multiply_DoubleDouble',A=g.get('Demand'),B=2.0)),Min=0.0,Max=1.0))
    En=F('FClamp',Value=F('Add_DoubleDouble',A=g.get('E'),B=F('Multiply_DoubleDouble',A=dt,B=F('Subtract_DoubleDouble',A=rise,B=rec))),Min=0.0,Max=1.0)
    effOn=F('BooleanAND',A=g.get('EffortEnabled'),B=g.get('Enabled'))
    t=g.set('E',F('SelectFloat',A=En,B=0.0,bPickA=effOn),t)
    t=g.set('EUse',F('FInterpTo',Current=g.get('EUse'),Target=g.get('E'),DeltaTime=dt,InterpSpeed=0.8),t)
    dirCh=F('BooleanAND',A=F('BooleanAND',A=hasIn,B=F('Less_DoubleDouble',A=F('Dot_VectorVector',A=inN,B=g.get('PrevIn')),B=0.5)),B=F('Greater_DoubleDouble',A=sp,B=100.0))
    t=g.set('ReqLoad',F('FMax',A=F('FInterpTo',Current=g.get('ReqLoad'),Target=0.0,DeltaTime=dt,InterpSpeed=1.2),B=F('SelectFloat',A=F('MapRangeClamped',Value=sp,InRangeA=100.0,InRangeB=600.0,OutRangeA=0.2,OutRangeB=1.0),B=0.0,bPickA=dirCh)),t)
    t=g.set('PrevIn',F('SelectVector',A=inN,B=g.get('PrevIn'),bPickA=hasIn),t)
    sev=F('SelectFloat',A=F('Multiply_DoubleDouble',A=F('MapRangeClamped',Value=dIV,InRangeA=0.6,InRangeB=-0.8,OutRangeA=0.0,OutRangeB=1.0),B=F('MapRangeClamped',Value=sp,InRangeA=120.0,InRangeB=450.0,OutRangeA=0.25,OutRangeB=1.0)),B=0.0,bPickA=hasIn)
    tgt=F('Subtract_DoubleDouble',A=1.0,B=F('Multiply_DoubleDouble',A=sev,B=0.95))
    rate=F('SelectFloat',A=15.0,B=3.0,bPickA=F('Less_DoubleDouble',A=tgt,B=g.get('SpeedScale')))
    t=g.set('SpeedScale',F('SelectFloat',A=F('FInterpTo',Current=g.get('SpeedScale'),Target=tgt,DeltaTime=dt,InterpSpeed=rate),B=1.0,bPickA=g.get('Enabled')),t)
    t=g.set('AccScale',F('SelectFloat',A=F('Lerp',A=1.0,B=0.75,Alpha=g.get('EUse')),B=1.0,bPickA=effOn),t)
    print('CHAIN built')
run(P,build)
bp=u.load_asset(P); cdo=u.get_default_object(bp.generated_class())
for k,vv in (('Enabled',True),('EffortEnabled',True),('SpeedScale',1.0),('AccScale',1.0)): cdo.set_editor_property(k,vv)
cdo.set_editor_property('primary_component_tick',cdo.get_editor_property('primary_component_tick'))
L.compile_blueprint(bp); print('ERR',errs(bp)); assert EA.save_loaded_asset(bp,False); print('CDO',{k:cdo.get_editor_property(k) for k in ('Enabled','EffortEnabled','SpeedScale','AccScale')}); print('DONE')
