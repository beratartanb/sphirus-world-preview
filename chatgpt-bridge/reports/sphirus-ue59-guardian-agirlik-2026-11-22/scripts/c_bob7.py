exec(open(__import__('unreal').Paths.project_dir()+'Tools/UE59_20261119/b59.py',encoding='utf8').read())
# c_bob7.py (control job, in-memory build; saved later by a gated write job) on ABP_Sph_GASP (DRIVER) - round 7.
# PELVIS BOB / SWAY DAMPING. Measured (an_bob7.py f8_L_60, probe_loops7.py): the walk loop M_Neutral_Walk_Loop_F itself moves the pelvis
# 10.7 cm up and down (in game 10.8 - FootPlacement adds nothing), the CM jog used for tempo 10.4 (in game 14.2), run 9.7 (12.1). The user
# rejected the calmer Core Motion clip set on 2026-11-11 (stiff, no counter-rotation), so the clips stay and only the excess vertical /
# lateral pelvis excursion is damped BEFORE FootPlacement: a ModifyBone(pelvis, translation ADDITIVE, component space) between
# LocalToComponentSpace_0 and FootPlacement_0, value = SphBob (written by BP_HybridA_Player.GR_Bob each tick). FootPlacement / LegIK then
# plant the feet from the damped pelvis, so the legs carry the change (more knee flexion at mid-stance) instead of the feet sinking.
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
from qa_graph import obj
import re as _re
P='/Game/Sphirus/Player/GASP/ABP_Sph_GASP'; a=u.load_asset(P); have=[str(v) for v in B.list_variables(a)]
assert 'SphBob' not in have,'already built'
B.add_variable(a,'SphBob','Vector'); L.compile_blueprint(a)
ag=B.get_graph(a,'AnimGraph'); AN=[pn(x) for x in B.find_nodes(ag)]
fp=[p for p in AN if type(obj(p)).__name__=='AnimGraphNode_FootPlacement']; assert len(fp)==1; fp=fp[0]
s0=src((fp,'ComponentPose')); assert len(s0)==1 and 'LocalToComponentSpace' in type(obj(s0[0][0])).__name__, s0; prev=s0[0]
TID='Animation|SkeletalControls|KemiğiDönüştürme(Değiştirme)'
disconnect((fp,'ComponentPose'))
n_=B.create_node(ag,TID,(900,600)); assert n_; tq=pn(n_); n=obj(tq); nd=n.get_editor_property('node'); tx=nd.export_text()
def rep(t,key,val):
    t2,c=_re.subn(key+r'=(\([^()]*(\([^()]*\)[^()]*)*\)|[^,()]*)',key+'='+val,t,count=1)
    if not c: t2=t[:-1]+','+key+'='+val+')'
    return t2
tx=rep(tx,'BoneToModify','(BoneName="pelvis")'); tx=rep(tx,'TranslationMode','BMM_Additive'); tx=rep(tx,'TranslationSpace','BCS_ComponentSpace')
tx=rep(tx,'RotationMode','BMM_Ignore'); tx=rep(tx,'ScaleMode','BMM_Ignore')
nd.import_text(tx); n.set_editor_property('node',nd); chk=n.get_editor_property('node').export_text()
assert 'BoneName="pelvis"' in chk and 'TranslationMode=BMM_Additive' in chk and 'TranslationSpace=BCS_ComponentSpace' in chk, chk[:500]
ii=[str(x.name) for x in info(tq).input_pins]; print('MB pins',ii)
connect(prev,(tq,[x for x in ii if 'Pose' in x][0]))
g1=pn(GE(ag).add_get_member_variable_node('SphBob','')); connect((g1,'SphBob'),(tq,'Translation'))
oo=[str(x.name) for x in info(tq).output_pins]; connect((tq,oo[0]),(fp,'ComponentPose'))
L.compile_blueprint(a); e=errs(a); print('ERR',e); assert not e
print('BOB built', [str(q[0])[-40:] for q in src((fp,'ComponentPose'))], 'status', a.get_editor_property('status'))
