# cm_camkick1.py (write): camera mass response (SHME V2.53-style damped signal, independent rebuild). The arm length was
# FInterpTo(TargetArmLength -> base target, 2.2/s): a monotone ease with no acceleration content ("donuk"). New:
#   GR_Accel   = FInterpTo(GR_Accel, (speed - GR_PrevSpeed)/dt, dt, 8)          (smoothed forward acceleration, cm/s2)
#   GR_CamKick = GR_CamKick + (GR_Accel * 0.05 - 3 * GR_CamKick) * dt            (leaky integrator: ~+5 cm on a 450 start,
#                                                                                  ~-6 cm on a 650 brake, decays in ~0.7 s)
#   GR_ArmBase = FInterpTo(GR_ArmBase, base target, dt, 2.2)                     (the old ease, now on its own variable)
#   TargetArmLength = GR_ArmBase + clamp(GR_CamKick, -8, 8)
# Nothing else in the camera chain changes (shoulder, Z, FOV, depth lag pivot, collision).
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
PP='/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'
bp0=u.load_asset(PP); have=[str(x) for x in B.list_variables(bp0)]
for v in ('GR_Accel','GR_PrevSpeed','GR_CamKick','GR_ArmBase'):
    if v not in have: B.add_variable(bp0,v,'float')
L.compile_blueprint(bp0); del bp0; gc.collect(); print('STEP vars')
def pv(p,k):
    try: return str(B.get_pin_value([x for x in info(p).input_pins if str(x.name)==k][0].pin_id))
    except Exception: return None
def build(bp):
    g=Gr(bp); N=[pn(x) for x in B.find_nodes(g.g)]; tp=lambda p:str(info(p).type_id); ins=lambda p:[str(x.name) for x in info(p).input_pins]
    ticks=[p for p in N if 'Tick' in tp(p) and any('Delta' in str(x.name) for x in info(p).output_pins) and 'then' in [str(x.name) for x in info(p).output_pins]]; tick=ticks[0]; dtp=[str(x.name) for x in info(tick).output_pins if 'Delta' in str(x.name)][0]
    ar=[p for p in N if 'TargetArmLength' in ins(p) and 'execute' in ins(p) and src((p,'execute'))]; assert len(ar)==1,ar; ar=ar[0]
    fi=src((ar,'TargetArmLength'))[0][0]; assert tp(fi).endswith('FInterpTo'),tp(fi); print('ARM interp',pv(fi,'InterpSpeed'))
    pre=src((ar,'execute')); assert len(pre)==1
    # 1. the ease runs on GR_ArmBase: Current <- GR_ArmBase, result -> Set GR_ArmBase (inserted before the arm setter)
    disconnect((fi,'Current')); connect(g.get('GR_ArmBase'),(fi,'Current'))
    disconnect((ar,'execute')); t=g.set('GR_ArmBase',(fi,'ReturnValue'),pre[0])
    # 2. acceleration + kick
    spd=(g.fn(M+'VSizeXY',A=(g.fn('/Script/Engine.Actor:GetVelocity'),'ReturnValue')),'ReturnValue')
    araw=(g.fn(M+'Divide_DoubleDouble',A=(g.fn(M+'Subtract_DoubleDouble',A=spd,B=g.get('GR_PrevSpeed')),'ReturnValue'),B=(g.fn(M+'FMax',A=(tick,dtp),B=0.004),'ReturnValue')),'ReturnValue')
    t=g.set('GR_PrevSpeed',spd,t)
    t=g.set('GR_Accel',(g.fn(M+'FInterpTo',Current=g.get('GR_Accel'),Target=araw,DeltaTime=(tick,dtp),InterpSpeed=8.0),'ReturnValue'),t)
    dk=(g.fn(M+'Subtract_DoubleDouble',A=(g.fn(M+'Multiply_DoubleDouble',A=g.get('GR_Accel'),B=0.05),'ReturnValue'),B=(g.fn(M+'Multiply_DoubleDouble',A=g.get('GR_CamKick'),B=3.0),'ReturnValue')),'ReturnValue')
    kick=(g.fn(M+'Add_DoubleDouble',A=g.get('GR_CamKick'),B=(g.fn(M+'Multiply_DoubleDouble',A=dk,B=(tick,dtp)),'ReturnValue')),'ReturnValue')
    t=g.set('GR_CamKick',kick,t)
    # 3. arm = base + clamp(kick)
    disconnect((ar,'TargetArmLength'))
    arm=(g.fn(M+'Add_DoubleDouble',A=g.get('GR_ArmBase'),B=(g.fn(M+'FClamp',Value=g.get('GR_CamKick'),Min=-8.0,Max=8.0),'ReturnValue')),'ReturnValue')
    connect(arm,(ar,'TargetArmLength')); connect(t,(ar,'execute')); print('GRAPH wired')
run(PP,build)
# GR_ArmBase default = outdoor idle arm so the first frames do not ease from 0
bp=u.load_asset(PP); B.set_variable_default(bp,'GR_ArmBase','140.0') if hasattr(B,'set_variable_default') else None
L.compile_blueprint(bp); assert EA.save_loaded_asset(bp,False); print('DONE')
