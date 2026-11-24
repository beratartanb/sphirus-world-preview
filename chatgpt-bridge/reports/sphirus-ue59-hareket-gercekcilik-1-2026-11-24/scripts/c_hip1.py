exec(open(__import__('unreal').Paths.project_dir()+'Tools/UE59_20261119/b59.py',encoding='utf8').read())
# c_hip1.py (control job, in-memory build; saved later by a gated write job) on ABP_Sph_GASP (DRIVER) - movement realism pass 1.
# HIP SWAY. Measured (an_hip.py f9_L): the walk loop M_Neutral_Walk_Loop_F turns the hip line 16.6 deg and tilts it 13.0 deg per cycle
# (sprint 24.9 / 14.9), identical on the driver and on the visible body = the clip, not a procedural layer. Pelvis translation is in a
# normal range (4.4 cm lateral, 4.6 cm vertical). The existing pelvis ModifyBone (SphBob, before FootPlacement) gets an ADDITIVE
# component-space rotation SphHipRot that removes part of the cyclic hip-line yaw / tilt; a new ModifyBone on spine_01 (SphSpineRot)
# gives the trunk the opposite rotation so shoulders / head keep their own motion. FootPlacement then plants the feet from the
# corrected pelvis. Values are written each tick by BP_HybridA_Player.GR_Bob (m_hip1_mcp.py).
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
from qa_graph import obj
import re as _re
P='/Game/Sphirus/Player/GASP/ABP_Sph_GASP'; a=u.load_asset(P); have=[str(v) for v in B.list_variables(a)]
def rep(t,key,val):
    t2,c=_re.subn(key+r'=(\([^()]*(\([^()]*\)[^()]*)*\)|[^,()]*)',key+'='+val,t,count=1)
    if not c: t2=t[:-1]+','+key+'='+val+')'
    return t2
if 'SphHipRot' in have: print('HIP1 already')
else:
    for v_ in ('SphHipRot','SphSpineRot'): B.add_variable(a,v_,'Rotator')
    L.compile_blueprint(a); assert 'SphHipRot' in [str(v) for v in B.list_variables(a)]
    ag=B.get_graph(a,'AnimGraph'); AN=[pn(x) for x in B.find_nodes(ag)]
    fp=[p for p in AN if type(obj(p)).__name__=='AnimGraphNode_FootPlacement']; assert len(fp)==1; fp=fp[0]
    s0=src((fp,'ComponentPose')); mb=s0[0][0]; n=obj(mb); assert type(n).__name__=='AnimGraphNode_ModifyBone', type(n).__name__
    nd=n.get_editor_property('node'); tx=nd.export_text(); assert 'BoneName="pelvis"' in tx, tx[:300]
    tx=rep(tx,'RotationMode','BMM_Additive'); tx=rep(tx,'RotationSpace','BCS_ComponentSpace'); nd.import_text(tx); n.set_editor_property('node',nd)
    chk=n.get_editor_property('node').export_text(); assert 'RotationMode=BMM_Additive' in chk and 'RotationSpace=BCS_ComponentSpace' in chk and 'TranslationMode=BMM_Additive' in chk, chk[:600]
    g1=pn(GE(ag).add_get_member_variable_node('SphHipRot','')); connect((g1,'SphHipRot'),(mb,'Rotation'))
    TID=str(info(mb).type_id); disconnect((fp,'ComponentPose'))
    n_=B.create_node(ag,TID,(1150,760)); assert n_; tq=pn(n_); n2=obj(tq); nd2=n2.get_editor_property('node'); t2=nd2.export_text()
    t2=rep(t2,'BoneToModify','(BoneName="spine_01")'); t2=rep(t2,'TranslationMode','BMM_Ignore'); t2=rep(t2,'RotationMode','BMM_Additive'); t2=rep(t2,'RotationSpace','BCS_ComponentSpace'); t2=rep(t2,'ScaleMode','BMM_Ignore')
    nd2.import_text(t2); n2.set_editor_property('node',nd2); c2=n2.get_editor_property('node').export_text(); assert 'BoneName="spine_01"' in c2 and 'RotationMode=BMM_Additive' in c2, c2[:500]
    ii=[str(x.name) for x in info(tq).input_pins]; oo=[str(x.name) for x in info(tq).output_pins]; mo=[str(x.name) for x in info(mb).output_pins]
    connect((mb,mo[0]),(tq,[x for x in ii if 'Pose' in x][0]))
    g2=pn(GE(ag).add_get_member_variable_node('SphSpineRot','')); connect((g2,'SphSpineRot'),(tq,'Rotation')); connect((tq,oo[0]),(fp,'ComponentPose'))
    L.compile_blueprint(a); e=errs(a); print('ERR',e); assert not e
    print('HIP1 built', [str(q[0])[-40:] for q in src((fp,'ComponentPose'))], [str(q[0])[-40:] for q in src((tq,[x for x in ii if 'Pose' in x][0]))])
