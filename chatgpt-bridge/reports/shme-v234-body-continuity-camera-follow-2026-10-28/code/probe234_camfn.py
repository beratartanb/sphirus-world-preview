"""probe234_camfn.py (measure): node census of SHM_UpdateCameraV21 incl. the V2.34 locomotion frame members (a build that failed leaves
an empty or partial function - 0 errors would still pass a smoke run). Prints CAMFN234 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import pn, info
import json
comp = u.load_asset('/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent')
ns = [str(info(pn(n)).type_id) for n in B.find_nodes(graph(comp, 'SHM_UpdateCameraV21'))]
out = {'nodes': len(ns), 'CamOrbit': sum('CamOrbit' in t for t in ns), 'CamRec': sum('CamRec' in t for t in ns), 'MoveLatch': sum('MoveLatch' in t for t in ns),
       'Loco': sum('Loco' in t for t in ns), 'InFrameOff': sum('InFrameOff' in t for t in ns),
       'setters': {k: sum(t.endswith('|Set' + k) for t in ns) for k in ('LocoYaw', 'LocoIFY', 'InFrameOff', 'LocoState', 'LocoLookD', 'MoveLatchYaw', 'CamRecDelta', 'CamEnv', 'CamEnvT', 'CamRecTurnSign')},
       'LastHitBy': sum('LastHitBy' in t for t in ns)}
out['ok'] = out['nodes'] > 1000 and all(v == 1 for v in out['setters'].values()) and out['Loco'] >= 20
print('CAMFN234 ' + json.dumps(out))
