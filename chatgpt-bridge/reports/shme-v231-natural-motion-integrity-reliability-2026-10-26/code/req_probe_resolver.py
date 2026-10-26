exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import pn, info
bp = u.load_asset('/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent'); fg = graph(bp, 'SHM231_InspectResolve')
for n in B.find_nodes(fg):
    p = pn(n)
    try: t = str(info(p).type_id)
    except Exception as e: t = 'ERR ' + str(e)[:60]
    print('RN', p.rsplit('.', 1)[-1], n.get_class().get_name(), t[-60:], [q.name for q in info(p).input_pins][:5])
