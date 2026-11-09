# cm_mmprobe.py: diagnostic probe in ABP_Sph_Driver. The pose history collector gets the tag 'PoseHistory'; each update
# PoseSearchLibrary.MotionMatch runs the same query the node runs and stores the selected asset name, time and wanted
# play rate in MM_Asset / MM_Time / MM_Rate (read by vid.py per frame). Gated by MM_Probe (default true for the audit).
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
_LF=open(u.Paths.project_dir()+'Saved/Codex/Day_20261107/mmprobe_progress.txt','w')
def P(*a):
    print(*a); print(*a,file=_LF); _LF.flush()
d=u.load_asset('/Game/Sphirus/Player/Anim/ABP_Sph_Driver')
have=[str(x) for x in B.list_variables(d)]
for n,t in (('MM_Asset','string'),('MM_Time','float'),('MM_Rate','float'),('MM_Probe','bool')):
    if n not in have: B.add_variable(d,n,t)
L.compile_blueprint(d)
ag=[g for g in B.list_graphs(d) if g.get_name()=='AnimGraph'][0]
ph=[n for n in B.find_nodes(ag) if 'HistoryCollector' in n.get_class().get_name()][0]; ph.set_editor_property('tag','PoseHistory'); P('TAG',ph.get_editor_property('tag'))
P('STEP tag'); eg=B.get_graph(d,'EventGraph'); ge=GE(eg); N=[pn(n) for n in B.find_nodes(eg)]; tp=lambda p:str(info(p).type_id)
ins=lambda p:[str(x.name) for x in info(p).input_pins]
sb=[p for p in N if 'BreathA' in ins(p) and 'execute' in ins(p)]; assert len(sb)==1; sb=sb[0]
outs=[(q,str(ip.name)) for q in N for ip in info(q).input_pins if (sb,'then') in src((q,str(ip.name)))]
f=lambda path:pn(ge.add_call_function_node(path))
br=pn(ge.add_branch_node()) if hasattr(ge,'add_branch_node') else pn(B.create_node(eg,'İşlevsellikler|AkışKontrolü|Dal',u.IntPoint(0,2400)))
gp=pn(ge.add_get_member_variable_node('MM_Probe','')); connect((gp,'MM_Probe'),(br,'Condition'))
P('STEP branch'); mm=f('/Script/PoseSearch.PoseSearchLibrary:MotionMatch'); P('MMPINS',ins(mm),[str(x.name) for x in info(mm).output_pins])
owner=f('/Script/Engine.AnimInstance:GetOwningComponent'); ai=f('/Script/Engine.SkeletalMeshComponent:GetAnimInstance'); connect((owner,'ReturnValue'),(ai,'self'))
connect((ai,'ReturnValue'),(mm,'AnimInstance'))
ARRT=[x for x in B.find_node_types(eg,'DiziOluştur')]; arr=pn(B.create_node(eg,ARRT[0],u.IntPoint(0,2600))) if ARRT else None
P('ARR',arr is not None,[x for x in B.find_node_types(eg,'MakeArray')][:3])
gdb=pn(ge.add_get_member_variable_node('LocoDB',''))
if arr:
    ap=[str(x.name) for x in info(arr).input_pins]; P('ARRPINS',ap); connect((gdb,'LocoDB'),(arr,ap[0])); connect((arr,'Array'),(mm,'AssetsToSearch'))
P('STEP arr'); value((mm,'PoseHistoryName'),'PoseHistory')
bk=[x for x in B.find_node_types(eg,'BreakPoseSearchBlueprintResult')]; P('BK',bk[:2]); bkn=pn(B.create_node(eg,bk[0],u.IntPoint(300,2600))); P('BKPINS',[str(x.name) for x in info(bkn).output_pins])
connect((mm,'Result'),(bkn,[str(x.name) for x in info(bkn).input_pins if str(x.name) not in ('execute',)][0]))
P('STEP break'); nm=f('/Script/Engine.KismetSystemLibrary:GetDisplayName'); connect((bkn,'SelectedAnim'),(nm,'Object'))
s1=pn(ge.add_set_member_variable_node('MM_Asset','')); connect((nm,'ReturnValue'),(s1,'MM_Asset'))
s2=pn(ge.add_set_member_variable_node('MM_Time','')); connect((bkn,'SelectedTime'),(s2,'MM_Time'))
s3=pn(ge.add_set_member_variable_node('MM_Rate','')); connect((bkn,'WantedPlayRate'),(s3,'MM_Rate'))
P('STEP sets'); [disconnect(d_) for d_ in outs]
connect((sb,'then'),(br,'execute')); connect((br,'then'),(s1,'execute')); connect((s1,'then'),(s2,'execute')); connect((s2,'then'),(s3,'execute'))
for d_ in outs: connect((s3,'then'),d_); connect((br,'else'),d_)
L.compile_blueprint(d); P('ERR_D',errs(d)); assert not errs(d)
cdo=u.get_default_object(d.generated_class()); cdo.set_editor_property('MM_Probe',True)
L.compile_blueprint(d); assert EA.save_loaded_asset(d,False); P('DONE')
