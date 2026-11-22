exec(open(__import__('unreal').Paths.project_dir()+'Tools/UE59_20261119/b59.py',encoding='utf8').read())
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
from qa_graph import obj
a=u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_GASP'); o=['GRAPHS '+' '.join(str(g).split(':')[-1].split("'")[0] for g in B.list_graphs(a))]
for gn in ('IsStarting','IsPivoting','Get_PoseSearchDatabases','Update_MotionMatching'):
    gs=[g for g in B.list_graphs(a) if str(g).split(':')[-1].split("'")[0]==gn]
    if not gs: o.append('NOGRAPH '+gn); continue
    for p in [pn(x) for x in B.find_nodes(gs[0])]:
        i=info(p); t=str(i.type_id)[:70]; ins=[]
        for x in i.input_pins:
            s=src((p,str(x.name))); dv=''
            try: dv=str(x.get_editor_property('value'))[:20]
            except Exception: pass
            ins.append('%s=%s%s'%(str(x.name),dv,('<-'+str(s[0][0]).split('.')[-1][-18:]+'.'+s[0][1]) if s else ''))
        o.append('%s | %s | %s | %s'%(gn,str(p).split('.')[-1][-26:],t,' ; '.join(ins)[:400]))
open(u.Paths.project_dir()+'Saved/UE59Work/r7/starting7.txt','w',encoding='utf8').write('\n'.join(o)); print('ST7',len(o))
