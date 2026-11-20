import unreal as u
T=u.BlueprintToolset; a=u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_GASP'); o=[]
for g in T.list_graphs(a):
    ns=[n for n in T.find_nodes(g) if n.get_class().get_name().startswith('AnimGraphNode_')]
    if not ns: continue
    o.append('== '+g.get_name())
    for n in ns:
        cn=n.get_class().get_name()[14:]; ex=''
        try:
            nd=n.get_editor_property('node')
            for p in ('slot_name','alpha','alpha_input_type','alpha_curve_name','bone_to_modify','translation_mode','rotation_mode','b_alpha_bool_enabled','layer','tag'):
                try:
                    v=nd.get_editor_property(p); s=str(v.bone_name) if hasattr(v,'bone_name') else str(v)
                    ex+=' %s=%s'%(p,s.split('.')[-1][:30])
                except Exception: pass
        except Exception: pass
        o.append('  %s (%s)%s'%(cn,n.get_name()[14:],ex))
open(u.Paths.project_dir()+'Saved/UE59Work/r4/gasp_graph.txt','w',encoding='utf8').write('\n'.join(o)); print('GG',len(o))
