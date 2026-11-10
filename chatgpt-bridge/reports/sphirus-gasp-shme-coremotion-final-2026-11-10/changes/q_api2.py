import unreal as u
from editor_toolset.toolsets.blueprint import BlueprintTools as B
bp=u.load_asset('/Game/Sphirus/Player/GASP/BP_Sph_GASP_B'); g=B.get_graph(bp,'EventGraph'); e=u.BlueprintGraphEditor.get_graph_editor(g)
import inspect
for m in ('list_available_nodes','create_node_from_name','find_event_node'):
    try: print('DOC',m,getattr(e,m).__doc__[:600])
    except Exception as x: print('DOC',m,x)
try:
    r=e.list_available_nodes('Parent'); print('AVAIL Parent',[str(x) for x in r][:40])
except Exception as x: print('AVAIL ERR',str(x)[:300])
for q in ('Üst','BeginPlay','Call to Parent'):
    try: r=e.list_available_nodes(q); print('AVAIL',q,[str(x) for x in r][:30])
    except Exception as x: print('AVAIL ERR',q,str(x)[:200])
d=B.get_graph_dsl_docs(); print('DSLDOCS',len(d)); open(u.Paths.project_dir()+'Tools/GASP_20261109/graph_dsl_docs.txt','w',encoding='utf8').write(d)
