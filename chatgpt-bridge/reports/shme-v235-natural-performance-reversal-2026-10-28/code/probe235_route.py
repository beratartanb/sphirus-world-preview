"""probe235_route.py (measure): census of SHM_UpdateRouting after the V2.35 routing build (V2.34 setters present, node count not
collapsed, the V2.35 RevOverHard read present) + SHM_UpdateCameraV21 untouched (> 1500 nodes). Prints ROUTE235 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import pn, info
import json
comp = u.load_asset('/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent')
out = {}
for gname, need in (('SHM_UpdateCameraV21', ('LocoYaw', 'CamEnv', 'CamRecTurnSign')), ('SHM_UpdateRouting', ('SHM234_RevAgo', 'SHM234_RevDir', 'SHM234_GapT', 'Family', 'FamilyTime'))):
    ns = [str(info(pn(n)).type_id) for n in B.find_nodes(graph(comp, gname))]
    out[gname] = {'nodes': len(ns), 'setters': {k: sum(t.endswith('|Set' + k) for t in ns) for k in need}, 'revover': sum('RevOverHard' in t for t in ns), 'gapkeep': sum('RevGapKeep' in t for t in ns)}
out['ok'] = (out['SHM_UpdateCameraV21']['nodes'] > 1500 and out['SHM_UpdateRouting']['nodes'] > 150 and out['SHM_UpdateRouting']['revover'] >= 1 and out['SHM_UpdateRouting']['gapkeep'] >= 1
             and all(v >= 1 for g in ('SHM_UpdateCameraV21', 'SHM_UpdateRouting') for v in out[g]['setters'].values()))
print('ROUTE235 ' + json.dumps(out))
