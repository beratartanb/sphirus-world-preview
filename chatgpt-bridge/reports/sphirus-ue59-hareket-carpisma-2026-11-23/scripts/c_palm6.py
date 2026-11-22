exec(open(__import__('unreal').Paths.project_dir()+'Tools/UE59_20261119/b59.py',encoding='utf8').read())
# c_palm6.py (control job, in-memory build; saved later by a gated write job) on ABP_Sph_Body_GASP - round 6b.
# PALM ALIGNMENT for the contact hand support. The reach IK (two TwoBoneIK nodes, p6_reach.py) only placed the wrist; the hand kept the
# rotation of the running / standing arm, so the palm did not face the surface (user review). Two ModifyBone nodes (hand_r, hand_l) are
# inserted after the IK nodes: rotation REPLACE in WORLD space, value = PalmR / PalmL (written by the player each tick from the surface
# normal), alpha = PalmAR / PalmAL (contact reach envelope of that hand; the door-handle reach leaves them at 0).
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
from qa_graph import obj
import re as _re
P='/Game/Sphirus/Player/GASP/ABP_Sph_Body_GASP'; a=u.load_asset(P); have=[str(v) for v in B.list_variables(a)]
assert 'PalmAR' not in have,'already built'
for n,t in (('PalmR','Rotator'),('PalmL','Rotator'),('PalmAR','float'),('PalmAL','float')): B.add_variable(a,n,t)
L.compile_blueprint(a)
ag=B.get_graph(a,'AnimGraph'); AN=[pn(x) for x in B.find_nodes(ag)]
c2l=[p for p in AN if 'ComponentToLocal' in type(obj(p)).__name__]; assert len(c2l)==1; c2l=c2l[0]
cin=[str(x.name) for x in info(c2l).input_pins][0]; s0=src((c2l,cin)); assert len(s0)==1,s0; prev=s0[0]; print('PREV',str(prev[0])[-40:],prev[1])
mb=[p for p in AN if type(obj(p)).__name__=='AnimGraphNode_ModifyBone']; tid=info(mb[0]).type_id; print('TID',str(tid)[:160])
disconnect((c2l,cin))
def rep(t,key,val):
    t2,c=_re.subn(key+r'=(\([^()]*(\([^()]*\)[^()]*)*\)|[^,()]*)',key+'='+val,t,count=1)
    if not c: t2=t[:-1]+','+key+'='+val+')'
    return t2
k=0
for hand,rv,av in (('hand_r','PalmR','PalmAR'),('hand_l','PalmL','PalmAL')):
    n_=B.create_node(ag,tid,(2600+k*360,900)); assert n_; tq=pn(n_); n=obj(tq); nd=n.get_editor_property('node'); tx=nd.export_text()
    if k==0: print('MB default',tx[:700])
    tx=rep(tx,'BoneToModify','(BoneName="%s")'%hand); tx=rep(tx,'RotationMode','BMM_Replace'); tx=rep(tx,'RotationSpace','BCS_WorldSpace')
    tx=rep(tx,'TranslationMode','BMM_Ignore'); tx=rep(tx,'ScaleMode','BMM_Ignore')
    nd.import_text(tx); n.set_editor_property('node',nd); chk=n.get_editor_property('node').export_text()
    assert ('BoneName="%s"'%hand) in chk and 'RotationMode=BMM_Replace' in chk and 'RotationSpace=BCS_WorldSpace' in chk, chk[:500]
    ii=[str(x.name) for x in info(tq).input_pins]; print('MB pins',ii)
    connect(prev,(tq,[x for x in ii if 'Pose' in x][0]))
    assert 'Rotation' in ii and 'Alpha' in ii, ii
    g1=pn(GE(ag).add_get_member_variable_node(rv,'')); connect((g1,rv),(tq,'Rotation'))
    g2=pn(GE(ag).add_get_member_variable_node(av,'')); connect((g2,av),(tq,'Alpha'))
    oo=[str(x.name) for x in info(tq).output_pins]; prev=(tq,oo[0]); k+=1
connect(prev,(c2l,cin))
L.compile_blueprint(a); e=errs(a); print('ERR',e); assert not e
print('PALM built', [str(q[0])[-36:] for q in src((c2l,cin))], 'status', a.get_editor_property('status'))
