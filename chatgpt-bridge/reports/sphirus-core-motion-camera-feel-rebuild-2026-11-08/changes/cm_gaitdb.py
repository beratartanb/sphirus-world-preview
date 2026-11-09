# cm_gaitdb.py: gait-split Motion Matching databases. One 44-clip database let the search mix walk starts into jogging and
# running (audit: walk start clip dominant at 330-480 cm/s). Three databases on the same schema:
#   PSD_Sph_Walk: idle + idle turns + all walk clips (23)
#   PSD_Sph_Jog:  idle + all jog clips (16)
#   PSD_Sph_Run:  idle + all run clips (8)
# Clips get a second BranchIn notify track (SphDB2) pointing at their gait database; PSD_Sph_Loco2 stays untouched.
# The driver picks the database from the pawn's GR_GaitSel (0 walk, 1 jog, 2 run) unless crouched.
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
AT=u.AssetToolsHelpers.get_asset_tools(); AL=u.AnimationLibrary; D='/Game/Sphirus/Player/MM'; C='/Game/Sphirus/Player/Anim/Core/'
PAWNC='/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player.BP_HybridA_Player_C'
IDLE=['af_Stand_Idle_02_WeightShift']
TURNS=['af_Stand_Idle_Turn%s%03d'%(s,a) for s in 'LR' for a in (45,90,135,180)]
WALK=['af_Loco_Walk_Fwd','af_Loco_Walk_Fwd_Start','af_Loco_Walk_Fwd_Stop','af_Loco_Walk_Fwd_Pivot','af_Loco_Walk_FwdLeft','af_Loco_Walk_FwdRight']+['af_Loco_Walk_Start_Turn%s%03d_%sfoot'%(s,a,s) for s in 'LR' for a in (45,90,135,180)]
JOG=[x.replace('Walk','Jog') for x in WALK]
RUN=['af_Loco_Run_Fwd','af_Loco_Run_Fwd_Start','af_Loco_Run_Fwd_Stop']+['af_Loco_Run_Start_Turn%s%03d_%sfoot'%(s,a,s) for s in 'LR' for a in (90,180)]
SETS={'PSD_Sph_Walk':IDLE+TURNS+WALK,'PSD_Sph_Jog':IDLE+JOG,'PSD_Sph_Run':IDLE+RUN}
f=u.DataAssetFactory(); f.set_editor_property('data_asset_class',u.PoseSearchDatabase)
dbs={}
done=all(EA.does_asset_exist(D+'/'+n) and u.load_asset(D+'/'+n).get_num_animation_assets()==len(c) for n,c in SETS.items())
print('DBS_DONE',done)
for name,clips in ([] if done else SETS.items()):
    db=u.load_asset(D+'/'+name) if EA.does_asset_exist(D+'/'+name) else AT.create_asset(name,D,u.PoseSearchDatabase,f)
    db.set_editor_property('schema',u.load_asset(D+'/PSS_Sph_Loco')); db.set_editor_property('continuing_pose_cost_bias',-0.04); assert EA.save_loaded_asset(db,False); dbs[name]=db
for name,clips in ([] if done else SETS.items()):
    db=dbs[name]
    for n in clips:
        a=u.load_asset(C+n); assert a,n
        tr='SphDB_'+name.split('_')[-1]
        if tr in [str(t) for t in AL.get_animation_notify_track_names(a)]: AL.remove_animation_notify_track(a,tr)
        AL.add_animation_notify_track(a,tr); st=AL.add_animation_notify_state_event(a,tr,0.0,float(a.get_play_length()),u.AnimNotifyState_PoseSearchBranchIn); st.set_editor_property('database',db)
        assert EA.save_loaded_asset(a,False)
    assert EA.save_loaded_asset(db,False); print('DB',name,db.get_num_animation_assets())
# driver: database from the pawn's gait
d=u.load_asset('/Game/Sphirus/Player/Anim/ABP_Sph_Driver')
if 'GaitSel' not in [str(x) for x in B.list_variables(d)]: B.add_variable(d,'GaitSel','int')
L.compile_blueprint(d)
eg=B.get_graph(d,'EventGraph'); ge=GE(eg); N=[pn(n) for n in B.find_nodes(eg)]; tp=lambda p:str(info(p).type_id); ins=lambda p:[str(x.name) for x in info(p).input_pins]
def pv(p,k):
    try: return str(B.get_pin_value([x for x in info(p).input_pins if str(x.name)==k][0].pin_id))
    except Exception: return None
# the crouch branch's else-setter writes PSD_Sph_Loco2; replace that setter with the gait selection
loco=[p for p in N if 'LocoDB' in ins(p) and 'execute' in ins(p) and 'PSD_Sph_Loco2' in (pv(p,'LocoDB') or '')]; assert len(loco)==1,loco; loco=loco[0]
pre=src((loco,'execute')); outs=[(q,str(ip.name)) for q in N for ip in info(q).input_pins if (loco,'then') in src((q,str(ip.name)))]
pawn=pn(ge.add_call_function_node('/Script/Engine.AnimInstance:TryGetPawnOwner'))
cast=pn(B.create_node(eg,'İşlevsellikler|Casting|CastToBP_HybridA_Player',u.IntPoint(0,3000))); co=[str(x.name) for x in info(cast).output_pins]; connect((pawn,'ReturnValue'),(cast,'Object'))
gs=pn(ge.add_get_member_variable_node('GR_GaitSel',PAWNC)); connect((cast,[x for x in co if x.startswith('As')][0]),(gs,'self'))
sg=pn(ge.add_set_member_variable_node('GaitSel','')); connect((gs,'GR_GaitSel'),(sg,'GaitSel'))
disconnect((loco,'execute'))
for s_ in pre: connect(s_,(cast,'execute'))
connect((cast,'then'),(sg,'execute')); connect((cast,'CastFailed'),(loco,'execute'))
b2=pn(ge.add_branch_node()); eq2=pn(ge.add_call_function_node(M+'EqualEqual_IntInt')); g2=pn(ge.add_get_member_variable_node('GaitSel','')); connect((g2,'GaitSel'),(eq2,'A')); value((eq2,'B'),2); connect((eq2,'ReturnValue'),(b2,'Condition')); connect((sg,'then'),(b2,'execute'))
sr=pn(ge.add_set_member_variable_node('LocoDB','')); value((sr,'LocoDB'),D+'/PSD_Sph_Run.PSD_Sph_Run'); connect((b2,'then'),(sr,'execute'))
b1=pn(ge.add_branch_node()); eq1=pn(ge.add_call_function_node(M+'EqualEqual_IntInt')); g1=pn(ge.add_get_member_variable_node('GaitSel','')); connect((g1,'GaitSel'),(eq1,'A')); value((eq1,'B'),1); connect((eq1,'ReturnValue'),(b1,'Condition')); connect((b2,'else'),(b1,'execute'))
sj=pn(ge.add_set_member_variable_node('LocoDB','')); value((sj,'LocoDB'),D+'/PSD_Sph_Jog.PSD_Sph_Jog'); connect((b1,'then'),(sj,'execute'))
sw=pn(ge.add_set_member_variable_node('LocoDB','')); value((sw,'LocoDB'),D+'/PSD_Sph_Walk.PSD_Sph_Walk'); connect((b1,'else'),(sw,'execute'))
for d_ in outs: disconnect(d_)
for d_ in outs:
    for s_ in (sr,sj,sw,loco): connect((s_,'then'),d_)
L.compile_blueprint(d); print('ERR_D',errs(d)); assert not errs(d); assert EA.save_loaded_asset(d,False); print('DONE')
