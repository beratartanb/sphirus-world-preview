# probe_mb.py (read-only): ModifyBone nodes of ABP_Sph_Body_GASP: bone, space, source variable of the Rotation pin
import unreal as u
T=u.BlueprintToolset; a=u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_Body_GASP'); o=[]
g=[x for x in T.list_graphs(a) if x.get_name()=='AnimGraph'][0]
for n in T.find_nodes(g):
    cn=n.get_class().get_name()
    if cn not in ('AnimGraphNode_ModifyBone','AnimGraphNode_LookAt','AnimGraphNode_TwoBoneIK'): continue
    nd=n.get_editor_property('node'); inf=T.get_node_infos([n])[0]; srcs=[]
    for p in inf.input_pins:
        try:
            lk=[str(x) for x in p.linked_to] if hasattr(p,'linked_to') else []
        except Exception as e: lk=[str(e)[:30]]
        if lk or str(p.name) in ('Rotation','Alpha'): srcs.append('%s<-%s'%(p.name,lk))
    try: bn=str(nd.get_editor_property('bone_to_modify').get_editor_property('bone_name'))
    except Exception as e: bn='?'
    try: sp=str(nd.get_editor_property('rotation_space')).split('.')[-1].split(':')[0]
    except Exception: sp=''
    o.append('%s | %s | %s | %s | %s'%(n.get_name(),cn[14:],bn,sp,' ; '.join(srcs)[:300]))
if not o: o=['none']
try: o.append('PINFIELDS '+str([x for x in dir(inf.input_pins[0]) if not x.startswith('_')]))
except Exception as e: o.append('E '+str(e))
open(u.Paths.project_dir()+'Saved/UE59Work/r4/mb_nodes.txt','w',encoding='utf8').write('\n'.join(o)); print('MB',len(o))
