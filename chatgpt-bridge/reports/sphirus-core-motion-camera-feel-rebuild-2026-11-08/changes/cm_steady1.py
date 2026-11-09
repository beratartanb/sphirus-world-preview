# cm_steady1.py (write): steady-state loop databases. The search keeps cycling inside the start-clip acceleration
# windows at steady speed (body never reaches the Walk_Fwd / Jog_Fwd / Run_Fwd loops) whatever the schema/history
# tuning. Architecture answer: a state-driven database choice.
#   PSD_Sph_WalkLoop (Walk_Fwd, FwdLeft, FwdRight), PSD_Sph_JogLoop (Jog_*), PSD_Sph_RunLoop (Run_Fwd)
#   Pawn: GR_Steady = speed within 15 % of the movement component's max speed, velocity within ~12 deg of the facing,
#         moving, for >= 0.35 s (GR_SteadyT accumulator, reset otherwise).
#   Driver: Steady copied from the pawn; while Steady the gait's loop database replaces the full gait database, so the
#         search can only pick loop poses (phase-matched to the current pose, 0.3 s blend). Starts, stops and turns
#         still come from the full databases; ForceLegacy path untouched.
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
_LF=open(u.Paths.project_dir()+'Saved/Codex/Day_20261107/steady_progress.txt','w')
def P(*a):
    print(*a); print(*a,file=_LF); _LF.flush()
AT=u.AssetToolsHelpers.get_asset_tools(); AL=u.AnimationLibrary; D='/Game/Sphirus/Player/MM'; C='/Game/Sphirus/Player/Anim/Core/'
PP='/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; PAWNC=PP+'.BP_HybridA_Player_C'
SETS={'PSD_Sph_WalkLoop':['af_Loco_Walk_Fwd','af_Loco_Walk_FwdLeft','af_Loco_Walk_FwdRight'],'PSD_Sph_JogLoop':['af_Loco_Jog_Fwd','af_Loco_Jog_FwdLeft','af_Loco_Jog_FwdRight'],'PSD_Sph_RunLoop':['af_Loco_Run_Fwd']}
f=u.DataAssetFactory(); f.set_editor_property('data_asset_class',u.PoseSearchDatabase)
for name,clips in SETS.items():
    db=u.load_asset(D+'/'+name) if EA.does_asset_exist(D+'/'+name) else AT.create_asset(name,D,u.PoseSearchDatabase,f)
    db.set_editor_property('schema',u.load_asset(D+'/PSS_Sph_Loco')); db.set_editor_property('continuing_pose_cost_bias',-0.12); db.set_editor_property('looping_cost_bias',-0.15); assert EA.save_loaded_asset(db,False)
    for n in clips:
        a=u.load_asset(C+n); assert a,n; tr='SphDB_'+name.split('_')[-1]
        if tr in [str(t) for t in AL.get_animation_notify_track_names(a)]: AL.remove_animation_notify_track(a,tr)
        AL.add_animation_notify_track(a,tr); st=AL.add_animation_notify_state_event(a,tr,0.0,float(a.get_play_length()),u.AnimNotifyState_PoseSearchBranchIn); st.set_editor_property('database',db); assert EA.save_loaded_asset(a,False)
    assert EA.save_loaded_asset(db,False); P('DB',name,db.get_num_animation_assets())
# ---- pawn: GR_Steady
bp0=u.load_asset(PP); have=[str(x) for x in B.list_variables(bp0)]
if 'GR_SteadyT' not in have: B.add_variable(bp0,'GR_SteadyT','float')
if 'GR_Steady' not in have: B.add_variable(bp0,'GR_Steady','bool')
L.compile_blueprint(bp0); del bp0; gc.collect(); P('STEP pawn vars')
def pv(p,k):
    try: return str(B.get_pin_value([x for x in info(p).input_pins if str(x.name)==k][0].pin_id))
    except Exception: return None
def build_pawn(bp):
    g=Gr(bp); N=[pn(x) for x in B.find_nodes(g.g)]; tp=lambda p:str(info(p).type_id); ins=lambda p:[str(x.name) for x in info(p).input_pins]
    sg=[p for p in N if 'GR_GaitSel' in ins(p) and 'execute' in ins(p)]; assert len(sg)==1,sg; sg=sg[0]
    ticks=[p for p in N if 'Tick' in tp(p) and any('Delta' in str(x.name) for x in info(p).output_pins) and 'then' in [str(x.name) for x in info(p).output_pins]]
    P('TICKS',[tp(p)[-40:] for p in ticks]); assert len(ticks)>=1,ticks; tick=ticks[0]; dtp=[str(x.name) for x in info(tick).output_pins if 'Delta' in str(x.name)][0]
    outs=[(q,str(ip.name)) for q in N for ip in info(q).input_pins if (sg,'then') in src((q,str(ip.name)))]; assert outs
    vel=(g.fn('/Script/Engine.Actor:GetVelocity'),'ReturnValue'); spd=(g.fn(M+'VSize',A=vel),'ReturnValue')
    tgt=(g.fn('/Script/Engine.MovementComponent:GetMaxSpeed',self=(g.fn('/Script/Engine.Pawn:GetMovementComponent'),'ReturnValue')),'ReturnValue')
    diff=(g.fn(M+'Abs',A=(g.fn(M+'Subtract_DoubleDouble',A=spd,B=tgt),'ReturnValue')),'ReturnValue')
    near=(g.fn(M+'Less_DoubleDouble',A=diff,B=(g.fn(M+'Multiply_DoubleDouble',A=tgt,B=0.15),'ReturnValue')),'ReturnValue')
    fwd=(g.fn('/Script/Engine.Actor:GetActorForwardVector'),'ReturnValue'); vn=(g.fn(M+'Normal',A=vel),'ReturnValue')
    aligned=(g.fn(M+'Greater_DoubleDouble',A=(g.fn(M+'Dot_VectorVector',A=fwd,B=vn),'ReturnValue'),B=0.978),'ReturnValue')
    moving=(g.fn(M+'Greater_DoubleDouble',A=spd,B=60.0),'ReturnValue')
    cond=(g.fn(M+'BooleanAND',A=(g.fn(M+'BooleanAND',A=near,B=aligned),'ReturnValue'),B=moving),'ReturnValue')
    newT=(g.fn(M+'SelectFloat',A=(g.fn(M+'Add_DoubleDouble',A=g.get('GR_SteadyT'),B=(tick,dtp)),'ReturnValue'),B=0.0,bPickA=cond),'ReturnValue')
    for d_ in outs: disconnect(d_)
    t=g.set('GR_SteadyT',newT,(sg,'then')); t=g.set('GR_Steady',(g.fn(M+'Greater_DoubleDouble',A=newT,B=0.35),'ReturnValue'),t)
    for d_ in outs: connect(t,d_)
    P('PAWN wired',len(outs))
run(PP,build_pawn); P('STEP pawn saved')
# ---- driver: Steady + loop databases
d=u.load_asset('/Game/Sphirus/Player/Anim/ABP_Sph_Driver')
if 'Steady' not in [str(x) for x in B.list_variables(d)]: B.add_variable(d,'Steady','bool')
L.compile_blueprint(d)
def build_drv(d):
    g=Gr(d); N=[pn(x) for x in B.find_nodes(g.g)]; tp=lambda p:str(info(p).type_id); ins=lambda p:[str(x.name) for x in info(p).input_pins]
    cast=[p for p in N if 'CastToBP_HybridA_Player' in tp(p)]; assert len(cast)==1,cast; cast=cast[0]; aso=[str(x.name) for x in info(cast).output_pins if str(x.name).startswith('As')][0]
    sg=[p for p in N if 'GaitSel' in ins(p) and 'execute' in ins(p) and 'LocoDB' not in ins(p)]; assert len(sg)==1,sg; sg=sg[0]
    outs=[(q,str(ip.name)) for q in N for ip in info(q).input_pins if (sg,'then') in src((q,str(ip.name)))]; assert outs
    gs=pn(g.e.add_get_member_variable_node('GR_Steady',PAWNC)); connect((cast,aso),(gs,'self'))
    for d_ in outs: disconnect(d_)
    t=g.set('Steady',(gs,'GR_Steady'),(sg,'then'))
    for d_ in outs: connect(t,d_)
    P('DRV steady wired',len(outs)); n_=0
    for p in N:
        v=pv(p,'LocoDB') if ('LocoDB' in ins(p) and 'execute' in ins(p)) else None
        if not v: continue
        gait=[k for k in ('Run','Jog','Walk') if '/PSD_Sph_%s.'%k in v]
        if not gait: continue
        gait=gait[0]; pre=src((p,'execute')); assert len(pre)==1,(gait,pre); pouts=[(q,str(ip.name)) for q in N for ip in info(q).input_pins if (p,'then') in src((q,str(ip.name)))]; assert pouts
        disconnect((p,'execute')); th,el=g.br(g.get('Steady'),pre[0]); connect(el,(p,'execute'))
        t2=g.set('LocoDB',D+'/PSD_Sph_%sLoop.PSD_Sph_%sLoop'%(gait,gait),th)
        for d_ in pouts: connect(t2,d_)
        n_+=1; P('DRV loop branch',gait,len(pouts))
    assert n_==3,n_
run('/Game/Sphirus/Player/Anim/ABP_Sph_Driver',build_drv); P('DONE')
