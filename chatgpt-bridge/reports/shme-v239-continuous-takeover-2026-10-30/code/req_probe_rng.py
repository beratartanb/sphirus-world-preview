exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import src, pn, info, obj
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'
bp = u.load_asset(AP); gp = pn(graph(bp, 'Update_MotionMatching')); nodes = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(gp))}
p = nodes['K2Node_CallFunction_336']; i = info(p)
print([a for a in dir(i) if not a.startswith('_')][:40])
for q in i.input_pins: print(q.name, repr(q.value))
q2 = [pn(n) for n in B.find_nodes(obj(pn(graph(bp, 'SHM_Snapshot'))))]
for x in q2:
    try:
        if 'InRange' in str(info(x).type_id): print('SNAP', x.rsplit('.',1)[-1], [(q.name, repr(q.value)) for q in info(x).input_pins][:3])
    except Exception: pass
