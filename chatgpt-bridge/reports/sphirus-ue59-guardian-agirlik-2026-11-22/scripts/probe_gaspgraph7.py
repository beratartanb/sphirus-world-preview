exec(open(__import__('unreal').Paths.project_dir()+'Tools/UE59_20261119/b59.py',encoding='utf8').read())
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
from qa_graph import obj
a=u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_GASP'); ag=B.get_graph(a,'AnimGraph'); AN=[pn(x) for x in B.find_nodes(ag)]; o=[]
for p in AN:
    t=type(obj(p)).__name__
    if not t.startswith('AnimGraphNode'): continue
    ins=[]
    for x in info(p).input_pins:
        s=src((p,str(x.name)))
        if s: ins.append('%s<-%s'%(str(x.name),','.join(type(obj(q[0])).__name__.replace('AnimGraphNode_','')+'.'+str(q[0]).split('.')[-1][-12:] for q in s)))
    o.append('%s %s | %s'%(t.replace('AnimGraphNode_',''),str(p).split('.')[-1],' ; '.join(ins)))
open(u.Paths.project_dir()+'Saved/UE59Work/r7/gaspgraph7.txt','w',encoding='utf8').write('\n'.join(o)); print('GG7',len(o))
