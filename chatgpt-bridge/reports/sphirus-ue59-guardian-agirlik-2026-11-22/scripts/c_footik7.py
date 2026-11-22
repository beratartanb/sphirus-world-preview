exec(open(__import__('unreal').Paths.project_dir()+'Tools/UE59_20261119/b59.py',encoding='utf8').read())
# c_footik7.py (control job, in-memory build; saved later by a gated write job) on ABP_Sph_Body_GASP (VISIBLE body) - round 7.
# FOOT CLEARANCE. The visible feet passed through low obstacles while walking / stumbling over them (toe 10-13 cm into a 25 cm log; the
# trailing foot of a stumble 10.7 cm). Two TwoBoneIK nodes (foot_r, foot_l) are inserted after the palm nodes, before ComponentToLocal:
# effector = FootTR / FootTL (world space, written by BP_HybridA_Player.GR_Foot: the foot raised above the surface under it), joint target
# = the calf in its own bone space (the knee keeps its bend direction), alpha = FootAR / FootAL (0 unless a lift is needed). No stretching.
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
from qa_graph import obj
import re as _re
P='/Game/Sphirus/Player/GASP/ABP_Sph_Body_GASP'; a=u.load_asset(P); have=[str(v) for v in B.list_variables(a)]
assert 'FootAR' not in have,'already built'
for n,t in (('FootTR','Vector'),('FootTL','Vector'),('FootAR','float'),('FootAL','float')): B.add_variable(a,n,t)
L.compile_blueprint(a)
ag=B.get_graph(a,'AnimGraph'); AN=[pn(x) for x in B.find_nodes(ag)]
c2l=[p for p in AN if 'ComponentToLocal' in type(obj(p)).__name__]; assert len(c2l)==1; c2l=c2l[0]
cin=[str(x.name) for x in info(c2l).input_pins][0]; s0=src((c2l,cin)); assert len(s0)==1,s0; prev=s0[0]; print('PREV',str(prev[0])[-40:])
disconnect((c2l,cin))
def rep(t,key,val):
    t2,c=_re.subn(key+r'=(\([^()]*(\([^()]*\)[^()]*)*\)|[^,()]*)',key+'='+val,t,count=1)
    if not c: t2=t[:-1]+','+key+'='+val+')'
    return t2
k=0
for foot,calf,tv,av in (('foot_r','calf_r','FootTR','FootAR'),('foot_l','calf_l','FootTL','FootAL')):
    n_=B.create_node(ag,'Animation|SkeletalControls|İkiKemikIK',(3400+k*360,900)); assert n_; tq=pn(n_); n=obj(tq); nd=n.get_editor_property('node'); tx=nd.export_text()
    tx=rep(tx,'IKBone','(BoneName="%s")'%foot); tx=rep(tx,'EffectorLocationSpace','BCS_WorldSpace'); tx=rep(tx,'JointTargetLocationSpace','BCS_BoneSpace')
    tx=rep(tx,'JointTarget','(bUseSocket=False,BoneReference=(BoneName="%s"),SocketReference=(SocketName="None"))'%calf); tx=rep(tx,'bAllowStretching','False')
    nd.import_text(tx); n.set_editor_property('node',nd); chk=n.get_editor_property('node').export_text()
    assert ('BoneName="%s"'%foot) in chk and 'EffectorLocationSpace=BCS_WorldSpace' in chk, chk[:500]
    ii=[str(x.name) for x in info(tq).input_pins]; print('IK pins',ii)
    connect(prev,(tq,[x for x in ii if 'Pose' in x][0]))
    g1=pn(GE(ag).add_get_member_variable_node(tv,'')); connect((g1,tv),(tq,'EffectorLocation'))
    g2=pn(GE(ag).add_get_member_variable_node(av,'')); connect((g2,av),(tq,'Alpha'))
    oo=[str(x.name) for x in info(tq).output_pins]; prev=(tq,oo[0]); k+=1
connect(prev,(c2l,cin))
L.compile_blueprint(a); e=errs(a); print('ERR',e); assert not e
print('FOOTIK built', [str(q[0])[-36:] for q in src((c2l,cin))], 'status', a.get_editor_property('status'))
