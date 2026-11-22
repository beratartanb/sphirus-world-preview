import unreal as u
T=u.BlueprintToolset; o=[x for x in dir(T) if not x.startswith('_')]
print('BPT6',o)
a=u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_GASP')
for g in T.list_graphs(a):
    for n in T.find_nodes(g):
        if n.get_class().get_name()=='AnimGraphNode_MotionMatching':
            for p in T.get_node_infos([n])[0].get_editor_property('input_pins'):
                nm=str(p.get_editor_property('name'))
                if nm in ('BlendTime','MaxActiveBlends','BlendOption','Database'): print('MM',nm,p.get_editor_property('value'),'|',p.export_text()[:260])
