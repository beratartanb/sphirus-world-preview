import unreal as u
T=u.BlueprintToolset; a=u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_GASP'); o=[]
for g in T.list_graphs(a):
    for n in T.find_nodes(g):
        cn=n.get_class().get_name()
        if cn in ('AnimGraphNode_Steering','AnimGraphNode_OffsetRootBone'):
            try: o.append('%s %s INFO %s'%(g.get_name(),n.get_name(),str(T.get_node_infos([n]))[:2500]))
            except Exception as e: o.append('info err '+str(e)[:200])
            try:
                sg=T.get_connected_subgraph(n) if hasattr(T,'get_connected_subgraph') else None; o.append('  SUB '+str(sg)[:1500])
            except Exception as e: o.append('  sub err '+str(e)[:200])
            try:
                b=n.get_editor_property('binding'); 
                for pn in ('property_bindings','PropertyBindings'):
                    try: o.append('  BIND '+str(b.get_editor_property(pn))[:1500])
                    except Exception as e: o.append('  bind err '+str(e)[:120])
                o.append('  BDIR '+', '.join(x for x in dir(b) if not x.startswith('_'))[:800])
            except Exception as e: o.append('  b err '+str(e)[:200])
open(u.Paths.project_dir()+'Saved/UE59Work/r5/steer2.txt','w',encoding='utf8').write('\n'.join(o)); print('STEER2',len(o))
