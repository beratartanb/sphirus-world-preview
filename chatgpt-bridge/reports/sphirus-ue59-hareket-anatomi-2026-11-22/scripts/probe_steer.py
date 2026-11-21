import unreal as u, re
T=u.BlueprintToolset; a=u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_GASP'); o=[]
for g in T.list_graphs(a):
    for n in T.find_nodes(g):
        cn=n.get_class().get_name()
        if cn in ('AnimGraphNode_Steering','AnimGraphNode_OrientationWarping'):
            t=n.get_editor_property('node').export_text()
            t=re.sub(r'(Source|ComponentPose|EvaluationData)=\([^)]*\),?','',t)
            o.append('%s / %s in %s: %s'%(cn[14:],n.get_name(),g.get_name(),t[:1500]))
            try:
                pins=[(p.get_name() if hasattr(p,'get_name') else str(p)) for p in T.get_node_pins(n)] if hasattr(T,'get_node_pins') else []
                o.append('  pins '+str(pins)[:600])
            except Exception as e: o.append('  pins err '+str(e)[:100])
o.append('TOOLSET '+', '.join(x for x in dir(T) if not x.startswith('_'))[:3000])
open(u.Paths.project_dir()+'Saved/UE59Work/r5/steer.txt','w',encoding='utf8').write('\n'.join(o)); print('STEER',len(o))
