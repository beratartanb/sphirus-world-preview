"""probe233_camfn.py (measure): node census of the component SHM_UpdateCameraV21 (orbit / recentre / latch / follow members)."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import pn, info
import json
comp = u.load_asset('/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent')
ns = [str(info(pn(n)).type_id) for n in B.find_nodes(graph(comp, 'SHM_UpdateCameraV21'))]
out = {'nodes': len(ns), 'CamOrbit': sum('CamOrbit' in t for t in ns), 'CamRec': sum('CamRec' in t for t in ns), 'MoveLatch': sum('MoveLatch' in t for t in ns),
       'CamFol': sum('CamFol' in t for t in ns), 'CamClose': sum('CamClose' in t for t in ns), 'LastHitBy': sum('LastHitBy' in t for t in ns)}
print('CAMFN233 ' + json.dumps(out))
