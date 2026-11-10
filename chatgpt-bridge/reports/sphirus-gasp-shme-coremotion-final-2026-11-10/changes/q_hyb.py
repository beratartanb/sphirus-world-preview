# q_hyb.py (read-only): BP_HybridA_Player graphs, node-type histogram per graph, leader-pose / input / CMC writers.
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
import collections
bp=u.load_asset('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player')
for g in B.list_graphs(bp):
    ns=B.find_nodes(g); c=collections.Counter()
    for n in ns:
        t=str(info(pn(n)).type_id)
        if any(k in t for k in ('LeaderPose','SetMaster','Input','Mapping','MovementInput','MaxWalkSpeed','MaxAcceleration','Braking','RotationRate','OrientRotation','UseControllerDesired','SetActorRotation','Possess','Olay','Event','Timeline','SetAnimInstanceClass','Cast')): c[t]+=1
    print('GRAPH',g.get_name(),len(ns),dict(c.most_common(25)))
print('VARS',[str(v) for v in B.list_variables(bp)])
