"""GUARDIAN face pass: art-directed structural shape ops on a DNA-order head (npy, UE cm), applied sequentially on top of the sculpt layer.
ops json: list of {"name", "op": "move"|"scale"|"normal", "c": [x,y,z], "r": [rx,ry,rz] (ellipsoid radii, cm), "d": [dx,dy,dz] (move, cm),
  "s": [sx,sy,sz] + "pivot" (scale), "amt" (normal, cm), "mirror": bool (also at x -> -x with dx -> -dx), "p": falloff power (default 1),
  "rigid": [segments moved rigidly with the weight at the op centre, e.g. "teeth", "saliva"]}
Weight = smoothstep(1 - |(X-c)/r|)**p on skin + cartilage (lid-attached meshes follow skin via the MetaHuman fit). Collar guard: no change
below z 146.5 (smooth to z 148.5) so the head / body weld stays exact. Eyeballs move only when listed in "rigid".
usage: blender -b --factory-startup --python blender_gd_shape.py -- <in.npy> <ops.json> <out.npy>"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930'))
from id_common import pkg, SEG
a = sys.argv[sys.argv.index('--')+1:]; X = np.load(a[0]).copy(); OPS = json.load(open(a[1])); OUT = a[2]
P = pkg(); T = np.asarray(P['head']['triangles'])
def sstep(x): x = np.clip(x, 0, 1); return x*x*(3-2*x)
SOFT = np.r_[np.arange(*SEG['skin']), np.arange(*SEG['cartilage'])]
log = []
for op in OPS:
    for side in ([1, -1] if op.get('mirror') else [1]):
        S = X[SOFT]
        if op['op'] != 'xscale':
            c = np.asarray(op['c'], float)*np.array([side, 1, 1]); r = np.asarray(op['r'], float); p = op.get('p', 1.0)
            q = np.linalg.norm((S-c)/r, axis=1); w = sstep(1-q)**p*sstep((S[:, 2]-146.5)/2.0)
        if op['op'] == 'xscale':   # smooth lateral widening: x' = mx + (x-mx)*(1+k*g(z)*front(y)*lat(|x-mx|)); g = gaussian band, front fades toward the back
            mx = op.get('mx', -0.24); g = np.exp(-((S[:, 2]-op['zc'])/op['zr'])**2); fr = sstep((S[:, 1]-op.get('y0', -1.0))/op.get('yw', 3.0))
            lat = sstep((np.abs(S[:, 0]-mx)-op.get('xmin', 0.0))/op.get('xw', 1.5)) if op.get('xmin') is not None else np.ones(len(S))
            w = g*fr*lat*sstep((S[:, 2]-146.5)/2.0); disp = np.zeros_like(S); disp[:, 0] = w*op['k']*(S[:, 0]-mx)
            if op.get('ky'): disp[:, 1] = w*op['ky']
        elif op['op'] == 'move': d = np.asarray(op['d'], float)*np.array([side, 1, 1]); disp = w[:, None]*d
        elif op['op'] == 'scale':
            pv = np.asarray(op.get('pivot', op['c']), float)*np.array([side, 1, 1]); s = np.asarray(op['s'], float); disp = w[:, None]*((S-pv)*(s-1))
        elif op['op'] == 'normal':
            N = np.zeros_like(X); fn = -np.cross(X[T[:, 1]]-X[T[:, 0]], X[T[:, 2]]-X[T[:, 0]])
            for k in range(3): np.add.at(N, T[:, k], fn)
            N /= np.maximum(np.linalg.norm(N, axis=1), 1e-9)[:, None]; disp = w[:, None]*N[SOFT]*op['amt']
        X[SOFT] += disp
        for sg in op.get('rigid', []):
            lo, hi = SEG[sg]
            if op['op'] == 'move': X[lo:hi] += np.asarray(op['d'], float)*np.array([side, 1, 1])
        log.append((op.get('name', op['op']), side, round(float(np.linalg.norm(disp, axis=1).max()*10), 2), int((w > 0.01).sum())))
np.save(OUT, X); print('SHAPE_OK', OUT, json.dumps(log))
