# q_aggraph.py (measure): wiring of ABP_Sph_Driver's AnimGraph - every node with its class and the source of each linked
# input pin, to see where the PoseHistory collector and the MotionMatching node sit in the pose chain.
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
d=u.load_asset('/Game/Sphirus/Player/Anim/ABP_Sph_Driver'); ag=[g for g in B.list_graphs(d) if g.get_name()=='AnimGraph'][0]
nodes=B.find_nodes(ag); names={}
for n in nodes: names[str(pn(n))]=n.get_class().get_name()
for n in nodes:
    p=pn(n); i=info(p); links=[]
    for ip in i.input_pins:
        try:
            s=src((p,str(ip.name)))
            if s: links.append((str(ip.name),[names.get(str(q[0]),str(q[0]))+'.'+str(q[1]) for q in s]))
        except Exception: pass
    print('NODE',n.get_class().get_name(),str(i.type_id)[-60:],'| in:',links)
print('Q_DONE')
