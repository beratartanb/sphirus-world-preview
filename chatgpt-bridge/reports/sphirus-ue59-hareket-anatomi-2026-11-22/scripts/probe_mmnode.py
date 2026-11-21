# probe_mmnode.py (read-only): Motion Matching node settings of ABP_Sph_GASP + the function graphs that call the MM library.
import unreal as u
T=u.BlueprintToolset; a=u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_GASP'); o=[]
for g in T.list_graphs(a):
    for n in T.find_nodes(g):
        cn=n.get_class().get_name()
        if cn=='AnimGraphNode_MotionMatching':
            nd=n.get_editor_property('node'); o.append('MM node in '+g.get_name()); o.append(nd.export_text()[:6000])
        elif cn=='AnimGraphNode_FootPlacement':
            nd=n.get_editor_property('node'); o.append('FP node'); o.append(nd.export_text()[:5000])
    if 'MotionMatching' in g.get_name() or 'PostSelection' in g.get_name():
        o.append('== graph '+g.get_name()+': '+', '.join(sorted(set(n.get_class().get_name() for n in T.find_nodes(g))))[:1500])
open(u.Paths.project_dir()+'Saved/UE59Work/r5/mmnode.txt','w',encoding='utf8').write('\n'.join(o)); print('MMNODE',len(o))
