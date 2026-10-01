"""GUARDIAN-3: brow groom positions measured on the P real render (Tier A front camera) are ray-cast onto the P head and stored as mesh
barycentric points (the library brow groom is bound to the mesh, so these mesh points carry the brows on any identity). Pairs them with
the Tier A brow picks for gd3_fit.py ('brows' input). usage: blender -b -P blender_gd3_brow_bind.py -- <out json>"""
import bpy, sys, os, json, numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930'))
from gd_common import ray, head_topology
OUT = sys.argv[sys.argv.index('--')+1:][0]
X = np.load('Saved/Codex/CharacterGuardian2_20261001/face/headP.npy'); T, MI = head_topology(); TS = T[(MI == 0) & (T.max(1) < 24049)]
bvh = BVHTree.FromPolygons([Vector(p) for p in X[:24049]], [list(t) for t in TS])
# brow centre-line on zgf_real_F.png (P + SlightArch brows), Tier A front frame pixels (read off a 2x zoom crop)
P2 = {'R_head': (375, 352), 'R_mid': (315, 346), 'R_tail': (245, 362), 'L_head': (452, 355), 'L_mid': (505, 346), 'L_tail': (570, 351)}
bind = {}
for nm, (px, py) in P2.items():
    o, d = ray('front', px, py); hit, nrm, fi, dist = bvh.ray_cast(Vector(o), Vector(d))
    tri = TS[fi]; A, B, C = X[tri]; q = np.asarray(hit); v0, v1, v2 = B-A, C-A, q-A
    d00, d01, d11, d20, d21 = v0@v0, v0@v1, v1@v1, v2@v0, v2@v1; den = d00*d11-d01*d01; bv = (d11*d20-d01*d21)/den; bw = (d00*d21-d01*d20)/den
    bind[nm] = {'idx': [int(t) for t in tri], 'w': [float(1-bv-bw), float(bv), float(bw)], 'p': [round(float(x), 3) for x in q]}
PK = json.load(open('Saved/Codex/CharacterIdentity_20260930/ref_picks.json')); out = []
M = {'front': {'brow_R_head': 'R_head', 'brow_R_mid': 'R_mid', 'brow_R_tail': 'R_tail', 'brow_L_head': 'L_head', 'brow_L_mid': 'L_mid', 'brow_L_tail': 'L_tail'},
     'close': {'brow_near_head': 'R_head', 'brow_near_peak': 'R_mid', 'brow_near_tail': 'R_tail', 'brow_far_head': 'L_head', 'brow_far_peak': 'L_mid'}}
for view, mp in M.items():
    for p in PK[view]['points']:
        if p['name'] in mp: b = bind[mp[p['name']]]; out.append({'view': view, 'name': p['name'], 'idx': b['idx'], 'w': b['w'], 'ref': p['ref'], 'p3': b['p']})
json.dump(out, open(OUT, 'w'), indent=1); print('BROWBIND', len(out), json.dumps({k: v['p'] for k, v in bind.items()}))
