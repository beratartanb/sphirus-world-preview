# c4_breath.py (write) on ABP_Sph_Body_GASP (visible MetaHuman body, after the UEFN->MH retarget):
# breathing layer driven by the owner's AC_Sph_Motion.EUse (Sphirus effort):
#   BreathAmt  -> FInterpTo(0.3 + 0.7 EUse, 1.5/s)        (calm base breath + effort)
#   BreathPhase-> (phase + dt * (0.22 + 0.5 EUse) * 360) % 360  (13 -> 43 breaths/min)
#   s = sin(phase) * BreathAmt ; chest (spine_05) and clavicles rotate additively in bone space by s * deg about a
#   tunable axis (ChestAxis/ClavAxisL/ClavAxisR, ChestDeg 2.0, ClavDeg 2.5) - axes calibrated in PIE afterwards.
# AnimGraph: Retarget -> LocalToComponent -> TMB spine_05 -> TMB clavicle_l -> TMB clavicle_r -> ComponentToLocal -> Output.
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
from qa_graph import obj
P='/Game/Sphirus/Player/GASP/ABP_Sph_Body_GASP'; MC='/Game/Sphirus/Player/Motion/AC_Sph_Motion.AC_Sph_Motion_C'
a=u.load_asset(P); have=[str(v) for v in B.list_variables(a)]
for n,t in [('EUse','float'),('BreathAmt','float'),('BreathPhase','float'),('ChestDeg','float'),('ClavDeg','float'),('ChestAxis','Vector'),('ClavAxisL','Vector'),('ClavAxisR','Vector'),('ChestRot','Rotator'),('ClavRotL','Rotator'),('ClavRotR','Rotator')]:
    if n not in have: B.add_variable(a,n,t)
L.compile_blueprint(a)
def rot_of(g,axis,deg,s):
    k=(g.fn(M+'Multiply_DoubleDouble',A=s,B=g.get(deg)),'ReturnValue')
    br=g.fn(M+'BreakVector',InVec=g.get(axis))
    return (g.fn(M+'MakeRotator',Roll=(g.fn(M+'Multiply_DoubleDouble',A=(br,'X'),B=k),'ReturnValue'),Pitch=(g.fn(M+'Multiply_DoubleDouble',A=(br,'Y'),B=k),'ReturnValue'),Yaw=(g.fn(M+'Multiply_DoubleDouble',A=(br,'Z'),B=k),'ReturnValue')),'ReturnValue')
def build(a):
    g=Gr(a); N=[pn(x) for x in B.find_nodes(g.g)]
    ev=[p for p in N if str(info(p).type_id).endswith('OlayBlueprintUpdateAnimation')]; assert len(ev)==1; ev=ev[0]
    outs=[str(x.name) for x in info(ev).output_pins]; print('EV outs',outs); dtp=(ev,[x for x in outs if 'Delta' in x][0])
    old=[(q,str(ip.name)) for q in N for ip in info(q).input_pins if (ev,'then') in src((q,str(ip.name)))]
    for d_ in old: disconnect(d_)
    pawn=(g.fn('/Script/Engine.AnimInstance:TryGetPawnOwner'),'ReturnValue')
    comp=(g.fn('/Script/Engine.Actor:GetComponentByClass',self=pawn,ComponentClass=MC),'ReturnValue')
    cst=g.pos(B.create_node(g.g,'İşlevsellikler|Casting|CastToAC_Sph_Motion',(0,0))); co=[str(x.name) for x in info(cst).output_pins]; print('CAST',co)
    connect(comp,(cst,'Object')); connect((ev,'then'),(cst,'execute'))
    asm=(cst,[x for x in co if x.startswith('As')][0])
    eg=g.pos(g.e.add_get_member_variable_node('EUse',MC)); connect(asm,(eg,'self'))
    t=g.set('EUse',(eg,'EUse'),(cst,'then'))
    sa=g.pos(g.e.add_set_member_variable_node('BreathAmt','')); connect(t,(sa,'execute')); connect((cst,'CastFailed'),(sa,'execute'))
    tgt=(g.fn(M+'Add_DoubleDouble',A=(g.fn(M+'Multiply_DoubleDouble',A=g.get('EUse'),B=0.7),'ReturnValue'),B=0.3),'ReturnValue')
    connect((g.fn(M+'FInterpTo',Current=g.get('BreathAmt'),Target=tgt,DeltaTime=dtp,InterpSpeed=1.5),'ReturnValue'),(sa,'BreathAmt'))
    t=(sa,'then')
    rate=(g.fn(M+'Add_DoubleDouble',A=(g.fn(M+'Multiply_DoubleDouble',A=g.get('EUse'),B=0.5),'ReturnValue'),B=0.22),'ReturnValue')
    ph=(g.fn(M+'Add_DoubleDouble',A=g.get('BreathPhase'),B=(g.fn(M+'Multiply_DoubleDouble',A=(g.fn(M+'Multiply_DoubleDouble',A=dtp,B=rate),'ReturnValue'),B=360.0),'ReturnValue')),'ReturnValue')
    t=g.set('BreathPhase',(g.fn(M+'Percent_FloatFloat',A=ph,B=360.0),'ReturnValue'),t)
    s=(g.fn(M+'Multiply_DoubleDouble',A=(g.fn(M+'DegSin',A=g.get('BreathPhase')),'ReturnValue'),B=g.get('BreathAmt')),'ReturnValue')
    t=g.set('ChestRot',rot_of(g,'ChestAxis','ChestDeg',s),t)
    t=g.set('ClavRotL',rot_of(g,'ClavAxisL','ClavDeg',s),t)
    t=g.set('ClavRotR',rot_of(g,'ClavAxisR','ClavDeg',s),t)
    for d_ in old: connect(t,d_)
    print('EVENT chain built; old targets',len(old))
    # ---- anim graph
    ag=B.get_graph(a,'AnimGraph'); AN=[pn(x) for x in B.find_nodes(ag)]
    root=[p for p in AN if type(obj(p)).__name__=='AnimGraphNode_Root'][0]; rt=[p for p in AN if 'RetargetPoseFromMesh' in type(obj(p)).__name__][0]
    rin=[str(x.name) for x in info(root).input_pins]; print('ROOT in',rin); s0=src((root,rin[0])); print('ROOT src',s0); disconnect((root,rin[0]))
    def mk(tid):
        n=B.create_node(ag,tid,(0,0)); assert n,tid; p=pn(n); print('NODE',tid,'in',[str(x.name) for x in info(p).input_pins],'out',[str(x.name) for x in info(p).output_pins]); return p
    l2c=mk('Animasyon|AlanlarıDönüştür|YereldenBileşene'); connect(s0[0],(l2c,[str(x.name) for x in info(l2c).input_pins][0]))
    prev=(l2c,[str(x.name) for x in info(l2c).output_pins][0])
    for bone,var in (('spine_05','ChestRot'),('clavicle_l','ClavRotL'),('clavicle_r','ClavRotR')):
        tp=mk('Animation|SkeletalControls|KemiğiDönüştürme(Değiştirme)'); n=obj(tp); nd=n.get_editor_property('node')
        br=nd.get_editor_property('bone_to_modify'); br.set_editor_property('bone_name',bone); nd.set_editor_property('bone_to_modify',br)
        nd.set_editor_property('rotation_mode',u.BoneModificationMode.BMM_ADDITIVE); nd.set_editor_property('rotation_space',u.BoneControlSpace.BCS_BONE_SPACE)
        nd.set_editor_property('translation_mode',u.BoneModificationMode.BMM_IGNORE); nd.set_editor_property('scale_mode',u.BoneModificationMode.BMM_IGNORE)
        n.set_editor_property('node',nd)
        ins=[str(x.name) for x in info(tp).input_pins]; print('TMB',bone,'pins',ins)
        connect(prev,(tp,[x for x in ins if 'Pose' in x][0]))
        gv=pn(GE(ag).add_get_member_variable_node(var,'')); rp=[x for x in ins if x=='Rotation']
        assert rp,('no Rotation pin',ins); connect((gv,var),(tp,'Rotation'))
        prev=(tp,[str(x.name) for x in info(tp).output_pins][0])
    c2l=mk('Animasyon|AlanlarıDönüştür|YereliçinBileşen'); connect(prev,(c2l,[str(x.name) for x in info(c2l).input_pins][0]))
    connect((c2l,[str(x.name) for x in info(c2l).output_pins][0]),(root,rin[0])); print('ANIMGRAPH wired')
run(P,build)
a=u.load_asset(P); cdo=u.get_default_object(a.generated_class())
for k,v in (('ChestDeg',2.0),('ClavDeg',2.5),('ChestAxis',u.Vector(0,0,1)),('ClavAxisL',u.Vector(0,0,1)),('ClavAxisR',u.Vector(0,0,1)),('BreathAmt',0.3)): cdo.set_editor_property(k,v)
L.compile_blueprint(a); e=errs(a); print('ERR',e); assert not e; assert EA.save_loaded_asset(a,False); print('DONE')
