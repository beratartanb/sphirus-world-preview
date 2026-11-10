# s2_bodylayer.py (write) on ABP_Sph_Body_GASP: SHME body layer after the breathing layer.
#   reads SphMotion SetX (brake settle deg), ChestLead (yaw deg), EffLean (deg); pitch = SetX + EffLean
#   spine_03: pitch*0.4 about PitchAxis + lead*0.5 about YawAxis ; spine_05: pitch*0.6 + lead*0.5   (additive, bone space)
#   axes are variables (PitchAxis default (0,0,-1), YawAxis (1,0,0)), calibrated in PIE afterwards.
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
from qa_graph import obj
P='/Game/Sphirus/Player/GASP/ABP_Sph_Body_GASP'; MC='/Game/Sphirus/Player/Motion/AC_Sph_Motion.AC_Sph_Motion_C'
a=u.load_asset(P); have=[str(v) for v in B.list_variables(a)]; assert 'SpineRot3' not in have
for n,t in (('SetX','float'),('ChestLead','float'),('EffLean','float'),('PitchAxis','Vector'),('YawAxis','Vector'),('SpineRot3','Rotator'),('SpineRot5','Rotator')): B.add_variable(a,n,t)
L.compile_blueprint(a)
def rot(g,pitch,yaw):
    pa=g.fn(M+'BreakVector',InVec=g.get('PitchAxis')); ya=g.fn(M+'BreakVector',InVec=g.get('YawAxis'))
    c=lambda ax:(g.fn(M+'Add_DoubleDouble',A=(g.fn(M+'Multiply_DoubleDouble',A=(pa,ax),B=pitch),'ReturnValue'),B=(g.fn(M+'Multiply_DoubleDouble',A=(ya,ax),B=yaw),'ReturnValue')),'ReturnValue')
    return (g.fn(M+'MakeRotator',Roll=c('X'),Pitch=c('Y'),Yaw=c('Z')),'ReturnValue')
def build(a):
    g=Gr(a); N=[pn(x) for x in B.find_nodes(g.g)]; ins=lambda p:[str(x.name) for x in info(p).input_pins]
    def consumers(ep): return [(q,str(ip.name)) for q in N for ip in info(q).input_pins if ep in src((q,str(ip.name)))]
    cr=[p for p in N if 'ClavRotR' in ins(p) and 'execute' in ins(p)]; assert len(cr)==1; cr=cr[0]
    T=consumers((cr,'then')); print('after ClavRotR',T)
    for x in T: disconnect(x)
    cst=[p for p in N if str(info(p).type_id).endswith('CastToAC_Sph_Motion')][0]; co=[str(x.name) for x in info(cst).output_pins]; asm=(cst,[x for x in co if x.startswith('As')][0])
    t=(cr,'then')
    for var in ('SetX','ChestLead','EffLean'):
        gv=g.pos(g.e.add_get_member_variable_node(var,MC)); connect(asm,(gv,'self')); t=g.set(var,(gv,var),t)
    pitch=(g.fn(M+'Add_DoubleDouble',A=g.get('SetX'),B=g.get('EffLean')),'ReturnValue')
    p3=(g.fn(M+'Multiply_DoubleDouble',A=pitch,B=0.4),'ReturnValue'); p5=(g.fn(M+'Multiply_DoubleDouble',A=pitch,B=0.6),'ReturnValue')
    y=(g.fn(M+'Multiply_DoubleDouble',A=g.get('ChestLead'),B=0.5),'ReturnValue')
    t=g.set('SpineRot3',rot(g,p3,y),t); t=g.set('SpineRot5',rot(g,p5,y),t)
    for x in T: connect(t,x)
    ag=B.get_graph(a,'AnimGraph'); AN=[pn(x) for x in B.find_nodes(ag)]
    root=[p for p in AN if type(obj(p)).__name__=='AnimGraphNode_Root'][0]; rin=[str(x.name) for x in info(root).input_pins]
    c2l=src((root,rin[0])); assert len(c2l)==1; c2l=c2l[0][0]; cin=[str(x.name) for x in info(c2l).input_pins][0]
    prev=src((c2l,cin)); assert len(prev)==1; prev=prev[0]; disconnect((c2l,cin))
    for bone,var in (('spine_03','SpineRot3'),('spine_05','SpineRot5')):
        n=B.create_node(ag,'Animation|SkeletalControls|KemiğiDönüştürme(Değiştirme)',(0,0)); tp=pn(n); nd=n.get_editor_property('node')
        br=nd.get_editor_property('bone_to_modify'); br.set_editor_property('bone_name',bone); nd.set_editor_property('bone_to_modify',br)
        nd.set_editor_property('rotation_mode',u.BoneModificationMode.BMM_ADDITIVE); nd.set_editor_property('rotation_space',u.BoneControlSpace.BCS_BONE_SPACE)
        nd.set_editor_property('translation_mode',u.BoneModificationMode.BMM_IGNORE); nd.set_editor_property('scale_mode',u.BoneModificationMode.BMM_IGNORE); n.set_editor_property('node',nd)
        ii=[str(x.name) for x in info(tp).input_pins]; connect(prev,(tp,[x for x in ii if 'Pose' in x][0]))
        gv=pn(GE(ag).add_get_member_variable_node(var,'')); connect((gv,var),(tp,'Rotation'))
        prev=(tp,[str(x.name) for x in info(tp).output_pins][0])
    connect(prev,(c2l,cin)); print('BODY layer wired')
run(P,build)
a=u.load_asset(P); cdo=u.get_default_object(a.generated_class())
cdo.set_editor_property('PitchAxis',u.Vector(0,0,-1)); cdo.set_editor_property('YawAxis',u.Vector(1,0,0))
for k in ('PitchAxis','YawAxis'): B.set_variable_instance_editable(a,k,True)
L.compile_blueprint(a); e=errs(a); print('ERR',e); assert not e; assert EA.save_loaded_asset(a,False); print('DONE')
