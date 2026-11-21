# c_steer5.py (control, in-memory): Steering nodes of ABP_Sph_GASP: set properties from builtins.STEER (dict name -> value text) + compile.
import unreal as u, builtins, re
T=u.BlueprintToolset; a=u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_GASP'); S=getattr(builtins,'STEER',None) or {}; done=0
for g in T.list_graphs(a):
    for n in T.find_nodes(g):
        if n.get_class().get_name()=='AnimGraphNode_Steering':
            nd=n.get_editor_property('node'); t=nd.export_text(); t0=t
            for k,v in S.items():
                m=re.search(r'\b%s=([-0-9.]+)'%k,t); assert m,k; t=t.replace(m.group(0),'%s=%s'%(k,v))
            if t!=t0: nd.import_text(t); n.modify(); n.set_editor_property('node',nd)
            done+=1; print('STEER5',n.get_name(),' '.join(re.search(r'\b%s=([-0-9.]+)'%k,n.get_editor_property('node').export_text()).group(0) for k in ('ProceduralTargetTime','AnimatedTargetTime','MinScaleRatio','MaxScaleRatio','DisableSteeringBelowSpeed')))
u.BlueprintEditorLibrary.compile_blueprint(a); print('STEER5 status',a.get_editor_property('status'),done)
