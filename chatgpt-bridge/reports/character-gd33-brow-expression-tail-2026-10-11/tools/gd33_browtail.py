"""GD33 brow-tail extension of the GD16 reference brow stations (brow3d json: per side medial -> lateral stations with skin points top / cen / bot).
User: the brow tail at the temple is short and does not continue in the reference's form. Measured in the solved cameras (GD33 r/tail_*.png):
the reference tail turns DOWN along the orbital rim and tapers (profile: ~2-2.5 mm lower at the end), the model tail stays level and ends
bluntly. Per side: the last two existing stations are lowered (DROPX x 0.5 / 1.0), then NEW stations are appended along the lateral tangent
with a growing downward component (EXT cm along the tangent, DROP cm down at the tip, s^1.5 profile) and a thickness taper to TAPER x the last
station's half-height. Every point is projected back to the head skin (nearest surface point). Medial / body stations are unchanged.
usage: blender -b --factory-startup --python gd33_browtail.py -- <head.npy> <brow3d in.json> <brow3d out.json> EXT DROP DROPX NEW TAPER"""
import sys, os, json, numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930')); from gd_common import head_topology
a = sys.argv[sys.argv.index('--')+1:]; HEAD, IN, OUT = a[:3]; EXT, DROP, DROPX = (float(v) for v in a[3:6]); NEW = int(a[6]); TAPER = float(a[7])
X = np.load(HEAD)[:24049]; T, MI = head_topology(); TT = T[(MI == 0) & (T.max(1) < 24049)]
bvh = BVHTree.FromPolygons([tuple(map(float, p)) for p in X], [tuple(int(i) for i in t) for t in TT])
def surf(p): loc, nrm, idx, d = bvh.find_nearest(Vector(tuple(float(v) for v in p))); return np.asarray(loc)
B = json.load(open(IN)); DOWN = np.array([0.0, 0.0, -1.0]); rep = {}
for side in ('imgL', 'imgR'):
    st = [dict(s) for s in B[side]]
    for j, w in ((-2, 0.5), (-1, 1.0)):   # lower the two lateral-most existing stations
        for k in ('top', 'cen', 'bot'): st[j][k] = surf(np.array(st[j][k])+DOWN*DROPX*w).round(4).tolist()
    C = [np.array(s['cen']) for s in st]; Hl = 0.5*(np.array(st[-1]['top'])-np.array(st[-1]['bot']))
    t = C[-1]-C[-2]; t[2] = 0.0; t /= np.linalg.norm(t)   # horizontal lateral tangent
    new = []
    for k in range(1, NEW+1):
        s = k/NEW; c = surf(C[-1]+t*EXT*s+DOWN*DROP*s**1.5); h = Hl*(1-(1-TAPER)*s)
        new.append({'col': None, 'top': surf(c+h).round(4).tolist(), 'cen': c.round(4).tolist(), 'bot': surf(c-h).round(4).tolist(), 'tail_ext': round(s, 3),
                    'thick_mm': round(float(np.linalg.norm(surf(c+h)-surf(c-h)))*10, 2)})
    B[side] = st+new
    rep[side] = {'old_tip_cen': [round(v, 3) for v in C[-1]], 'new_tip_cen': new[-1]['cen'], 'tip_move_mm': round(float(np.linalg.norm(np.array(new[-1]['cen'])-C[-1]))*10, 2),
                 'tip_drop_mm': round(float(C[-1][2]-new[-1]['cen'][2])*10, 2), 'end_thick_mm': new[-1]['thick_mm']}
B['tail_extension'] = {'EXT_cm': EXT, 'DROP_cm': DROP, 'DROPX_cm': DROPX, 'NEW': NEW, 'TAPER': TAPER, 'report': rep}
json.dump(B, open(OUT, 'w'), indent=1); print('BROWTAIL', json.dumps(rep))
