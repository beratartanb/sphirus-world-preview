import unreal as u, re
T=u.BlueprintToolset; a=u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_GASP'); o=[]
for g in T.list_graphs(a):
    for n in T.find_nodes(g):
        cn=n.get_class().get_name()
        if cn in ('AnimGraphNode_FootPlacement','AnimGraphNode_OffsetRootBone','AnimGraphNode_Steering'):
            inf=T.get_node_infos([n])[0]
            for p in inf.get_editor_property('input_pins'):
                o.append('%s | %s | %s | id=%s'%(n.get_name(),str(p.get_editor_property('name')),str(p.get_editor_property('value')),str(p.get_editor_property('id')) if hasattr(p,'id') else p.export_text()[:160]))
            try: o.append('NODE '+n.get_name()+' '+n.get_editor_property('node').export_text()[:2500])
            except Exception as e: o.append('nodeerr '+repr(e)[:100])
open(u.Paths.project_dir()+'Saved/UE59Work/r6/fp6.txt','w',encoding='utf8').write('\n'.join(o)); print('FP6',len(o))
