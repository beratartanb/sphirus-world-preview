exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import src, pn, info, obj
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'
bp = u.load_asset(AP); sg = pn(graph(bp, 'SHM_Snapshot')); sn = [pn(n) for n in B.find_nodes(obj(sg))]
def tid(p):
    try: return str(info(p).type_id)
    except Exception as e: return 'ERR ' + str(e)[:60]
ws = [p for p in sn if tid(p).endswith('SetSHM238_WalkSkip')]
def walk(pin, d=0):
    for s in src(pin):
        n = s[0]; i = info(n); print('  ' * d, s[1], '<-', n.rsplit('.', 1)[-1], tid(n), [q.name for q in i.input_pins][:6])
        if d < 4:
            for q in i.input_pins:
                if q.name not in ('execute', 'self'): walk((n, q.name), d + 1)
for w in ws:
    print('SET', w.rsplit('.', 1)[-1], [q.name for q in info(w).input_pins]); walk((w, 'SHM238_WalkSkip'))
