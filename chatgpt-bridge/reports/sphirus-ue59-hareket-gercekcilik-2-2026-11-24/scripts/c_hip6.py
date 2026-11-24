exec(open(__import__('unreal').Paths.project_dir()+'Tools/UE59_20261119/b59.py',encoding='utf8').read())
# c_hip6.py (control job, in-memory build; saved later by a gated write job) on ABP_Sph_GASP (DRIVER) - movement realism pass 2.
# HEAD LATERAL regression of pass 1 (run: visible head lateral 5.0-5.5 -> 5.9-6.9 cm): the shoulder correction turns the trunk about the
# vertical axis through spine_01, and the head sits 15-20 cm in front of that axis in the run lean, so it is swung sideways.
# The spine_01 ModifyBone gets an additive component-space translation SphSpineTr (written by GR_Bob, m_hip6_mcp.py) that moves the
# rotation axis onto the head: x = HD_T x sin(SH_Yaw) x (head forward offset from spine_01).
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
from qa_graph import obj
import re as _re
P='/Game/Sphirus/Player/GASP/ABP_Sph_GASP'; a=u.load_asset(P); have=[str(v) for v in B.list_variables(a)]
def rep(t,key,val):
    t2,c=_re.subn(key+r'=(\([^()]*(\([^()]*\)[^()]*)*\)|[^,()]*)',key+'='+val,t,count=1)
    if not c: t2=t[:-1]+','+key+'='+val+')'
    return t2
if 'SphSpineTr' in have: print('HIP6 already')
else:
    B.add_variable(a,'SphSpineTr','Vector'); L.compile_blueprint(a)
    ag=B.get_graph(a,'AnimGraph'); AN=[pn(x) for x in B.find_nodes(ag)]
    sp=[p for p in AN if type(obj(p)).__name__=='AnimGraphNode_ModifyBone' and 'BoneName="spine_01"' in obj(p).get_editor_property('node').export_text()]; assert len(sp)==1; sp=sp[0]
    n=obj(sp); nd=n.get_editor_property('node'); t=nd.export_text(); t=rep(t,'TranslationMode','BMM_Additive'); t=rep(t,'TranslationSpace','BCS_ComponentSpace'); nd.import_text(t); n.set_editor_property('node',nd)
    c=n.get_editor_property('node').export_text(); assert 'TranslationMode=BMM_Additive' in c and 'TranslationSpace=BCS_ComponentSpace' in c and 'RotationMode=BMM_Additive' in c, c[:500]
    try: B.reconstruct_node(sp)
    except Exception as e: print('HIP6 reconstruct n/a',repr(e)[:80])
    print('HIP6 pins',[str(x.name) for x in info(sp).input_pins])
    g=pn(GE(ag).add_get_member_variable_node('SphSpineTr','')); connect((g,'SphSpineTr'),(sp,'Translation'))
    L.compile_blueprint(a); e=errs(a); print('ERR',e); assert not e
    print('HIP6 built', [str(q[0])[-30:] for q in src((sp,'Translation'))])
