exec(open(__import__('unreal').Paths.project_dir()+'Tools/UE59_20261119/b59.py',encoding='utf8').read())
# c_hip3.py (control job, in-memory build; saved later by a gated write job) on ABP_Sph_GASP (DRIVER) - movement realism pass 2.
# HEAD STABILITY regression of pass 1: the shoulder-line correction (SH_Yaw, on spine_01) also turned the head, whose neck in the clip
# counter-rotates the FULL shoulder swing: head yaw per cycle went 2.4 -> 9.6 deg in run and 3.7 -> 8.1 in sprint (an_head2.py).
# New ModifyBone on neck_01 (additive, component space, rotation SphNeckRot) right after the spine_01 node gives the head the opposite
# of the shoulder correction, so the head keeps the clip's own (stable) orientation. Written each tick by GR_Bob (m_hip3_mcp.py).
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
from qa_graph import obj
import re as _re
P='/Game/Sphirus/Player/GASP/ABP_Sph_GASP'; a=u.load_asset(P); have=[str(v) for v in B.list_variables(a)]
def rep(t,key,val):
    t2,c=_re.subn(key+r'=(\([^()]*(\([^()]*\)[^()]*)*\)|[^,()]*)',key+'='+val,t,count=1)
    if not c: t2=t[:-1]+','+key+'='+val+')'
    return t2
if 'SphNeckRot' in have: print('HIP3 already')
else:
    B.add_variable(a,'SphNeckRot','Rotator'); L.compile_blueprint(a); assert 'SphNeckRot' in [str(v) for v in B.list_variables(a)]
    ag=B.get_graph(a,'AnimGraph'); AN=[pn(x) for x in B.find_nodes(ag)]
    fp=[p for p in AN if type(obj(p)).__name__=='AnimGraphNode_FootPlacement']; assert len(fp)==1; fp=fp[0]
    s0=src((fp,'ComponentPose')); sp=s0[0][0]; n=obj(sp); assert type(n).__name__=='AnimGraphNode_ModifyBone'; assert 'BoneName="spine_01"' in n.get_editor_property('node').export_text()
    TID=str(info(sp).type_id); disconnect((fp,'ComponentPose'))
    n_=B.create_node(ag,TID,(1450,760)); assert n_; tq=pn(n_); n2=obj(tq); nd2=n2.get_editor_property('node'); t2=nd2.export_text()
    t2=rep(t2,'BoneToModify','(BoneName="neck_01")'); t2=rep(t2,'TranslationMode','BMM_Ignore'); t2=rep(t2,'RotationMode','BMM_Additive'); t2=rep(t2,'RotationSpace','BCS_ComponentSpace'); t2=rep(t2,'ScaleMode','BMM_Ignore')
    nd2.import_text(t2); n2.set_editor_property('node',nd2); c2=n2.get_editor_property('node').export_text(); assert 'BoneName="neck_01"' in c2 and 'RotationMode=BMM_Additive' in c2, c2[:500]
    ii=[str(x.name) for x in info(tq).input_pins]; oo=[str(x.name) for x in info(tq).output_pins]; mo=[str(x.name) for x in info(sp).output_pins]
    connect((sp,mo[0]),(tq,[x for x in ii if 'Pose' in x][0]))
    g2=pn(GE(ag).add_get_member_variable_node('SphNeckRot','')); connect((g2,'SphNeckRot'),(tq,'Rotation')); connect((tq,oo[0]),(fp,'ComponentPose'))
    L.compile_blueprint(a); e=errs(a); print('ERR',e); assert not e
    print('HIP3 built', [str(q[0])[-40:] for q in src((fp,'ComponentPose'))])
