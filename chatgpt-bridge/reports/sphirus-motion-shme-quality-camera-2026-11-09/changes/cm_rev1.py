# cm_rev1.py (write): reversal database set (state-driven choice, like the steady loop sets). True-clip telemetry of the
# 180-degree keyboard reversal (P_phys_g/i/j seg 4): 0.5-0.7 s of blend soup with one-frame picks flipping between the
# 45/90/135/180 start-turn clips of both sides while the capsule turns. The turn family is only consistent for the 180
# case, so while the pawn is reversing the driver searches a small set: the gait's Start_Turn{L,R}180 clips (trimmed
# ranges) + the gait's Fwd_Stop (brake phase). Pawn: GR_Reverse = heading error > 100 deg, held until < 30 deg
# (hysteresis); driver: Reverse copied from the pawn, checked before the Steady branch of each gait.
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
import json
AT=u.AssetToolsHelpers.get_asset_tools(); AL=u.AnimationLibrary; D='/Game/Sphirus/Player/MM'; C='/Game/Sphirus/Player/Anim/Core/'
PP='/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; PAWNC=PP+'.BP_HybridA_Player_C'
plan=json.load(open(u.Paths.project_dir()+'Saved/Codex/Day_20261107/trim_plan.json'))
SETS={'PSD_Sph_WalkRev':['af_Loco_Walk_Start_TurnL180_Lfoot','af_Loco_Walk_Start_TurnR180_Rfoot','af_Loco_Walk_Fwd_Stop'],
      'PSD_Sph_JogRev':['af_Loco_Jog_Start_TurnL180_Lfoot','af_Loco_Jog_Start_TurnR180_Rfoot','af_Loco_Jog_Fwd_Stop'],
      'PSD_Sph_RunRev':['af_Loco_Run_Start_TurnL180_Lfoot','af_Loco_Run_Start_TurnR180_Rfoot','af_Loco_Run_Fwd_Stop']}
f=u.DataAssetFactory(); f.set_editor_property('data_asset_class',u.PoseSearchDatabase)
for name,clips in SETS.items():
    db=u.load_asset(D+'/'+name) if EA.does_asset_exist(D+'/'+name) else AT.create_asset(name,D,u.PoseSearchDatabase,f)
    db.set_editor_property('schema',u.load_asset(D+'/PSS_Sph_Loco')); assert EA.save_loaded_asset(db,False)
    for n in clips:
        a=u.load_asset(C+n); assert a,n; tr='SphDB_'+name.split('_')[-1]; L_=float(a.get_play_length()); rng=plan.get(n,{}).get('range') or [0.0,L_]
        if tr in [str(t) for t in AL.get_animation_notify_track_names(a)]: AL.remove_animation_notify_track(a,tr)
        AL.add_animation_notify_track(a,tr); st=AL.add_animation_notify_state_event(a,tr,float(rng[0]),float(rng[1]-rng[0]),u.AnimNotifyState_PoseSearchBranchIn); st.set_editor_property('database',db); assert EA.save_loaded_asset(a,False)
    assert EA.save_loaded_asset(db,False); print('DB',name,db.get_num_animation_assets())
# ---- pawn
bp0=u.load_asset(PP)
if 'GR_Reverse' not in [str(x) for x in B.list_variables(bp0)]: B.add_variable(bp0,'GR_Reverse','bool')
L.compile_blueprint(bp0); del bp0; gc.collect(); print('STEP pawn var')
def build_pawn(bp):
    g=Gr(bp); N=[pn(x) for x in B.find_nodes(g.g)]; ins=lambda p:[str(x.name) for x in info(p).input_pins]
    she=[p for p in N if 'GR_HeadErr' in ins(p) and 'execute' in ins(p)]; assert len(she)==1; she=she[0]
    outs=[(q,str(ip.name)) for q in N for ip in info(q).input_pins if (she,'then') in src((q,str(ip.name)))]; assert outs
    hi=(g.fn(M+'Greater_DoubleDouble',A=g.get('GR_HeadErr'),B=100.0),'ReturnValue'); keep=(g.fn(M+'Greater_DoubleDouble',A=g.get('GR_HeadErr'),B=30.0),'ReturnValue')
    # no SelectBool in KismetMathLibrary: rev = (Reverse AND keep) OR (NOT Reverse AND hi)
    a1=(g.fn(M+'BooleanAND',A=g.get('GR_Reverse'),B=keep),'ReturnValue')
    a2=(g.fn(M+'BooleanAND',A=(g.fn(M+'Not_PreBool',A=g.get('GR_Reverse')),'ReturnValue'),B=hi),'ReturnValue')
    rev=(g.fn(M+'BooleanOR',A=a1,B=a2),'ReturnValue')
    for d_ in outs: disconnect(d_)
    t=g.set('GR_Reverse',rev,(she,'then'))
    for d_ in outs: connect(t,d_)
    print('PAWN reverse wired',len(outs))
run(PP,build_pawn); print('STEP pawn saved')
# ---- driver
d=u.load_asset('/Game/Sphirus/Player/Anim/ABP_Sph_Driver')
if 'Reverse' not in [str(x) for x in B.list_variables(d)]: B.add_variable(d,'Reverse','bool')
L.compile_blueprint(d)
def pv(p,k):
    try: return str(B.get_pin_value([x for x in info(p).input_pins if str(x.name)==k][0].pin_id))
    except Exception: return None
def build_drv(d):
    g=Gr(d); N=[pn(x) for x in B.find_nodes(g.g)]; tp=lambda p:str(info(p).type_id); ins=lambda p:[str(x.name) for x in info(p).input_pins]
    cast=[p for p in N if 'CastToBP_HybridA_Player' in tp(p)]; assert len(cast)==1; cast=cast[0]; aso=[str(x.name) for x in info(cast).output_pins if str(x.name).startswith('As')][0]
    ss=[p for p in N if 'Steady' in ins(p) and 'execute' in ins(p) and 'LocoDB' not in ins(p)]; assert len(ss)==1,ss; ss=ss[0]
    outs=[(q,str(ip.name)) for q in N for ip in info(q).input_pins if (ss,'then') in src((q,str(ip.name)))]; assert outs
    gr=pn(g.e.add_get_member_variable_node('GR_Reverse',PAWNC)); connect((cast,aso),(gr,'self'))
    for d_ in outs: disconnect(d_)
    t=g.set('Reverse',(gr,'GR_Reverse'),(ss,'then'))
    for d_ in outs: connect(t,d_)
    print('DRV reverse wired',len(outs)); n_=0
    # the loop setters (LocoDB = *Loop) hang off Branch(Steady).then; that Branch is the insertion point
    for p in N:
        v=pv(p,'LocoDB') if ('LocoDB' in ins(p) and 'execute' in ins(p)) else None
        if not v or 'Loop.' not in v: continue
        gait=[k for k in ('Run','Jog','Walk') if '/PSD_Sph_%sLoop.'%k in v][0]
        br_=src((p,'execute')); assert len(br_)==1 and str(br_[0][1])=='then',br_; br_=br_[0][0]
        pre=src((br_,'execute')); assert len(pre)==1
        pouts=[(q,str(ip.name)) for q in N for ip in info(q).input_pins if (p,'then') in src((q,str(ip.name)))]; assert pouts
        disconnect((br_,'execute')); th,el=g.br(g.get('Reverse'),pre[0]); connect(el,(br_,'execute'))
        t2=g.set('LocoDB',D+'/PSD_Sph_%sRev.PSD_Sph_%sRev'%(gait,gait),th)
        for d_ in pouts: connect(t2,d_)
        n_+=1; print('DRV rev branch',gait,len(pouts))
    assert n_==3,n_
run('/Game/Sphirus/Player/Anim/ABP_Sph_Driver',build_drv); print('DONE')
