# probe_floor.py (read-only): what is under the bedroom standing spot and on top of the bed (multi line traces, editor world)
import unreal as u
w=u.UnrealEditorSubsystem().get_editor_world(); o=[]
for nm,(x,y) in (('stand',(1300,770)),('bedmid',(1215,770)),('bedfeet',(1215,700)),('bedhead',(1215,840)),('room',(1340,800))):
    for cx,tq in (('complex',True),('simple',False)):
        hs=u.SystemLibrary.line_trace_multi(w,u.Vector(x,y,700),u.Vector(x,y,440),u.TraceTypeQuery.TRACE_TYPE_QUERY1,tq,[],u.DrawDebugTrace.NONE,True) or []
        o.append('%s %s: %s'%(nm,cx,' | '.join('%.1f %s'%(h.to_tuple()[4].z,(h.to_tuple()[9].get_actor_label() if h.to_tuple()[9] else '?')[:28]) for h in hs)[:300]))
        h=u.SystemLibrary.line_trace_single(w,u.Vector(x,y,700),u.Vector(x,y,440),u.TraceTypeQuery.TRACE_TYPE_QUERY1,tq,[],u.DrawDebugTrace.NONE,True)
        if h: t=h.to_tuple(); o.append('   first %.1f %s'%(t[4].z,t[9].get_actor_label() if t[9] else '?'))
n=u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_GASP'); T=u.BlueprintToolset
g=[x for x in T.list_graphs(n) if x.get_name()=='AnimGraph'][0]
for nd in T.find_nodes(g):
    if nd.get_class().get_name()=='AnimGraphNode_FootPlacement':
        s=nd.get_editor_property('node'); o.append('FP props: '+' '.join(x for x in dir(s) if not x.startswith('_'))[:900])
        for k in ('leg_definitions','LegDefinitions'):
            try: o.append('legs: '+str(s.get_editor_property(k))[:900])
            except Exception as e: o.append('legs? '+str(e)[:80])
open(u.Paths.project_dir()+'Saved/UE59Work/r4/floor_probe.txt','w',encoding='utf8').write('\n'.join(o)); print('FLOOR',len(o))
