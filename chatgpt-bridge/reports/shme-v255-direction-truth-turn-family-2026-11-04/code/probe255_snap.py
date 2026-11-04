"""probe255_snap.py (measure): exec order of the V2.38 / V2.54 contract setters in SHM_Snapshot and the GR velocity write, node census. Read only."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, src, pn, info, obj
import json
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'
bp = u.load_asset(AP); sg = pn(graph(bp, 'SHM_Snapshot')); sn = [pn(n) for n in B.find_nodes(obj(sg))]
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
T = {p: tid(p) for p in sn}
def short(p): return p.rsplit('.', 1)[-1] + ':' + T.get(p, '').rsplit('|', 1)[-1]
keys = ('SHM238', 'SHM254', 'SHM228', 'ClipYaw', 'ClipSpeed', 'GR241', 'LocoExplore', 'LocoState', 'LocoOn', 'LocoYaw')
rows = []
for p in sn:
    if any(k in T[p] for k in keys) and '|Set' in T[p]:
        pre = [short(s_[0]) + '.' + str(s_[1]) for s_ in src((p, 'execute'))]
        rows.append((short(p), pre))
print('SNAP255 n=%d' % len(sn))
for r in rows: print('SN', r[0], '<-', r[1])
g2 = '/Game/GraceRanger/BP_GR_Player'; bp2 = u.load_asset(g2); gg = None
for g in B.list_graphs(bp2):
    if pn(g).endswith('GR_Impl_CP_PhysicalRedirect'): gg = pn(g)
sn2 = [pn(n) for n in B.find_nodes(obj(gg))]; T.update({p: tid(p) for p in sn2})
print('GR nodes', len(sn2))
for p in sn2:
    t = T[p]
    if any(k in t for k in ('Velocity', 'ClipYaw', 'ClipSpeed', 'GetActorForwardVector', 'SetActorRotation', 'GetMaxAcceleration', 'DesiredDir', 'GroundFriction')):
        ins = []
        for q in info(p).input_pins:
            if q.connected_pins: ins.append(str(q.name) + '<-' + ','.join(pn(c.node).rsplit('.', 1)[-1] + ':' + tid(pn(c.node)).rsplit('|', 1)[-1] for c in q.connected_pins))
        print('GR', short(p), ins[:6])
