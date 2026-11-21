import unreal as u, re
T=u.BlueprintToolset; a=u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_GASP'); o=[]
for g in T.list_graphs(a):
    for n in T.find_nodes(g):
        if n.get_class().get_name() in ('AnimGraphNode_FootPlacement','AnimGraphNode_MotionMatching','AnimGraphNode_OffsetRootBone'):
            inf=T.get_node_infos([n])[0]
            for p in inf.get_editor_property('input_pins'):
                nm=str(p.get_editor_property('name')); t=p.export_text(); con=re.findall(r'ConnectedPins=\(\(Node="[^"]*\.([A-Za-z0-9_]+)\'"',t)
                o.append('%s.%s = %s %s'%(n.get_name()[14:],nm,str(p.get_editor_property('value'))[:110],('<- '+con[0]) if con else ''))
            # function call nodes in this graph: names
    if g.get_name()=='AnimGraph':
        for n in T.find_nodes(g):
            if n.get_class().get_name()=='K2Node_CallFunction':
                try: o.append('CALL %s -> %s'%(n.get_name(),n.get_editor_property('function_reference').get_editor_property('member_name')))
                except Exception as e: pass
open(u.Paths.project_dir()+'Saved/UE59Work/r5/fp.txt','w',encoding='utf8').write('\n'.join(o)); print('FP',len(o))
