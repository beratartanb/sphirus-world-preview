# cm_turn1.py (write): physical turn braking (SHME V2.55 direction-truth behaviour, rebuilt on the Core Motion pawn).
# Measured: with orient-to-movement at 260 deg/s the capsule keeps 180 / 500 cm/s through 90 and 180 degree direction
# changes (T_walk / T_jog), so the body slides around a 40 cm arc on strafe/turn clips - the "artificial turn".
# Rule: heading error = angle between the movement input direction and the actor forward; GR_TurnScale =
# clamp(1 - max(0, err-25)/110, 0.3, 1) eased at 8/s, multiplied into the max walk speed before it is applied.
# Sharp turns brake (walk 180 -> ~55, run 500 -> ~150), the motion-matching trajectory then predicts the brake and the
# stop/turn-start clips are chosen; once aligned the speed recovers with the normal acceleration (450).
# Also: GR_SteadyEnable default -> false (with the double-evaluation fixed, the full gait databases select the loops
# themselves: G_full.json Walk_Fwd 129/240 frames; the loop-only override and its database switches are not needed).
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
PP='/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'
_LF=open(u.Paths.project_dir()+'Saved/Codex/Day_20261107/turn_progress.txt','w')
def P(*a):
    print(*a); print(*a,file=_LF); _LF.flush()
bp0=u.load_asset(PP); have=[str(x) for x in B.list_variables(bp0)]
for n,t in (('GR_TurnScale','float'),('GR_HeadErr','float')):
    if n not in have: B.add_variable(bp0,n,t)
L.compile_blueprint(bp0); cdo=u.get_default_object(bp0.generated_class()); cdo.set_editor_property('GR_TurnScale',1.0); cdo.set_editor_property('GR_SteadyEnable',False); P('DEFAULTS steadyEnable',cdo.get_editor_property('GR_SteadyEnable'))
del bp0; gc.collect()
def pv(p,k):
    try: return str(B.get_pin_value([x for x in info(p).input_pins if str(x.name)==k][0].pin_id))
    except Exception: return None
def build(bp):
    g=Gr(bp); N=[pn(x) for x in B.find_nodes(g.g)]; tp=lambda p:str(info(p).type_id); ins=lambda p:[str(x.name) for x in info(p).input_pins]
    ticks=[p for p in N if 'Tick' in tp(p) and any('Delta' in str(x.name) for x in info(p).output_pins) and 'then' in [str(x.name) for x in info(p).output_pins]]; tick=ticks[0]; dtp=[str(x.name) for x in info(tick).output_pins if 'Delta' in str(x.name)][0]
    sms=[p for p in N if tp(p).endswith('SetMaxWalkSpeed')]; P('SetMaxWalkSpeed nodes',len(sms)); assert len(sms)>=1
    ss=[p for p in N if 'GR_Steady' in ins(p) and 'execute' in ins(p)]; assert len(ss)==1; ss=ss[0]
    outs=[(q,str(ip.name)) for q in N for ip in info(q).input_pins if (ss,'then') in src((q,str(ip.name)))]; assert outs
    inp=(g.fn('/Script/Engine.Pawn:GetLastMovementInputVector'),'ReturnValue'); inn=(g.fn(M+'Normal',A=inp),'ReturnValue')
    fwd=(g.fn('/Script/Engine.Actor:GetActorForwardVector'),'ReturnValue')
    err=(g.fn(M+'DegAcos',A=(g.fn(M+'FClamp',Value=(g.fn(M+'Dot_VectorVector',A=fwd,B=inn),'ReturnValue'),Min=-1.0,Max=1.0),'ReturnValue')),'ReturnValue')
    moving=(g.fn(M+'Greater_DoubleDouble',A=(g.fn(M+'VSize',A=inp),'ReturnValue'),B=0.1),'ReturnValue')
    err2=(g.fn(M+'SelectFloat',A=err,B=0.0,bPickA=moving),'ReturnValue')
    raw=(g.fn(M+'FClamp',Value=(g.fn(M+'Subtract_DoubleDouble',A=1.0,B=(g.fn(M+'Divide_DoubleDouble',A=(g.fn(M+'FMax',A=(g.fn(M+'Subtract_DoubleDouble',A=err2,B=25.0),'ReturnValue'),B=0.0),'ReturnValue'),B=110.0),'ReturnValue')),'ReturnValue'),Min=0.3,Max=1.0),'ReturnValue')
    sm=(g.fn(M+'FInterpTo',Current=g.get('GR_TurnScale'),Target=raw,DeltaTime=(tick,dtp),InterpSpeed=8.0),'ReturnValue')
    for d_ in outs: disconnect(d_)
    t=g.set('GR_HeadErr',err2,(ss,'then')); t=g.set('GR_TurnScale',sm,t)
    for d_ in outs: connect(t,d_)
    n=0
    for p in sms:
        s_=src((p,'MaxWalkSpeed')); assert len(s_)==1,s_
        disconnect((p,'MaxWalkSpeed')); m=g.fn(M+'Multiply_DoubleDouble',A=s_[0],B=g.get('GR_TurnScale')); connect((m,'ReturnValue'),(p,'MaxWalkSpeed')); n+=1
    P('TURN wired, speed setters scaled',n)
run(PP,build); P('DONE')
