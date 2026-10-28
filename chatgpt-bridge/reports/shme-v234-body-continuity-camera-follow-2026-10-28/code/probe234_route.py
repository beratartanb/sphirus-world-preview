"""probe234_route.py (measure): census of SHM_UpdateCameraV21 + SHM_UpdateRouting after a V2.34 build (setters of the new state must exist,
node counts must not collapse). Prints ROUTE234 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import pn, info
import json
comp = u.load_asset('/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent')
out = {}
for gname, need in (('SHM_UpdateCameraV21', ('LocoYaw', 'CamEnv', 'CamRecTurnSign')), ('SHM_UpdateRouting', ('SHM234_RevAgo', 'SHM234_RevDir', 'Family', 'FamilyTime'))):
    ns = [str(info(pn(n)).type_id) for n in B.find_nodes(graph(comp, gname))]
    out[gname] = {'nodes': len(ns), 'setters': {k: sum(t.endswith('|Set' + k) for t in ns) for k in need}}
out['ok'] = out['SHM_UpdateCameraV21']['nodes'] > 1500 and out['SHM_UpdateRouting']['nodes'] > 150 and all(v >= 1 for g in ('SHM_UpdateCameraV21', 'SHM_UpdateRouting') for v in out[g]['setters'].values())
print('ROUTE234 ' + json.dumps(out))
