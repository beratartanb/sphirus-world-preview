exec(open(__import__('unreal').Paths.project_dir()+'Tools/UE59_20261119/b59.py',encoding='utf8').read())
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
from qa_graph import obj
# probe_gait8.py (control, read-only): BP_Sph_GASPCharacter graphs - every node whose title / pins mention Fat, and the full node list of GetDesiredGait
a=u.load_asset('/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter'); o=[]
T=u.BlueprintToolset
for g in T.list_graphs(a):
    gn=str(g.get_name()) if hasattr(g,'get_name') else str(g)
    for n in T.find_nodes(g):
        try: inf=T.get_node_infos([n])[0]
        except Exception: continue
        title=str(n.get_name())+' '+str(n.get_class().get_name())
        try: title+=' '+str(inf.export_text())[:300]
        except Exception: pass
        pins=[]
        for pk in ('input_pins','output_pins'):
            for p in inf.get_editor_property(pk):
                pins.append('%s=%s'%(p.get_editor_property('name'),str(p.get_editor_property('value'))[:24]))
        line='%s | %s | %s'%(gn,title.replace(chr(10),' '),' ; '.join(pins)[:500])
        if 'Fat' in line or 'GetDesiredGait' in gn or 'Gait' in title: o.append(line)
open(u.Paths.project_dir()+'Saved/UE59Work/r8/gait8.txt','w',encoding='utf8').write('\n'.join(o)); print('GAIT8',len(o))
