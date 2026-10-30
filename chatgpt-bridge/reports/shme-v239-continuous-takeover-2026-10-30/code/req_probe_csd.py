exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import src, pn, info, obj
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'
bp = u.load_asset(AP)
gs_ = list(B.list_graphs(bp))
names = [g.get_name() for g in gs_] if gs_ else []
print('GRAPHS', len(names), names[:60])
for gn in names:
    try: gp = pn(graph(bp, gn))
    except Exception as e: continue
    for n in B.find_nodes(obj(gp)):
        p = pn(n)
        try: t = str(info(p).type_id)
        except Exception: continue
        if t.endswith('SetCurrentSelectedDatabase') or t.endswith('SetSHM_HoldDB'): print('W', gn, p.rsplit('.', 1)[-1], t[-30:])
