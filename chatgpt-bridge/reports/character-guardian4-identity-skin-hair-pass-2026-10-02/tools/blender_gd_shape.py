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
        if op['op'] not in ('xscale', 'vault', 'crown'):
            c = np.asarray(op['c'], float)*np.array([side, 1, 1]); r = np.asarray(op['r'], float); p = op.get('p', 1.0)
            q = np.linalg.norm((S-c)/r, axis=1); w = sstep(1-q)**p*sstep((S[:, 2]-146.5)/2.0)
        if op['op'] == 'xscale':   # smooth lateral widening: x' = mx + (x-mx)*(1+k*g(z)*front(y)*lat(|x-mx|)); g = gaussian band, front fades toward the back
            mx = op.get('mx', -0.24); g = np.exp(-((S[:, 2]-op['zc'])/op['zr'])**2); fr = sstep((S[:, 1]-op.get('y0', -1.0))/op.get('yw', 3.0))
            lat = sstep((np.abs(S[:, 0]-mx)-op.get('xmin', 0.0))/op.get('xw', 1.5)) if op.get('xmin') is not None else np.ones(len(S))
            w = g*fr*lat*sstep((S[:, 2]-146.5)/2.0)*((np.sign(S[:, 0]-mx) == op['side']) if op.get('side') else 1.0); disp = np.zeros_like(S); disp[:, 0] = w*op['k']*(S[:, 0]-mx)
            if op.get('ky'): disp[:, 1] = w*op['ky']
        elif op['op'] == 'move': d = np.asarray(op['d'], float)*np.array([side, 1, 1]); disp = w[:, None]*d
        elif op['op'] == 'scale':
            pv = np.asarray(op.get('pivot', op['c']), float)*np.array([side, 1, 1]); s = np.asarray(op['s'], float); disp = w[:, None]*((S-pv)*(s-1))
        elif op['op'] == 'normal':
            N = np.zeros_like(X); fn = -np.cross(X[T[:, 1]]-X[T[:, 0]], X[T[:, 2]]-X[T[:, 0]])
            for k in range(3): np.add.at(N, T[:, k], fn)
            N /= np.maximum(np.linalg.norm(N, axis=1), 1e-9)[:, None]; disp = w[:, None]*N[SOFT]*op['amt']
        elif op['op'] == 'vault':   # cranium large form: lower / round the vault, hold width higher, shorten the occiput (skin above z0 only, collar untouched)
            z0, zt, mx = op['z0'], op['ztop'], op.get('mx', -0.25); t = np.clip((S[:, 2]-z0)/(zt-z0), 0, 1); ts = t*t*(3-2*t)
            disp = np.zeros_like(S)
            disp[:, 2] = -op.get('drop', 0.0)*ts**1.6
            disp[:, 0] = (S[:, 0]-mx)*op.get('widen', 0.0)*np.sin(np.pi*np.clip(t*op.get('widen_peak', 1.2), 0, 1))
            yb = op.get('back_y', -4.0); wb = np.clip((yb-S[:, 1])/op.get('back_w', 4.0), 0, 1); wb = wb*wb*(3-2*wb)*np.clip((S[:, 2]-(z0-op.get('back_dz', 3.0)))/3.0, 0, 1)
            disp[:, 1] = op.get('shorten', 0.0)*wb
            w = (ts > 0) | (wb > 0)
        elif op['op'] == 'crown':   # coronal vault fullness: radial push in the x-z plane from (mx, zc), peaking at the upper-lateral vault (angle 'ang'
            # from vertical) -> broader, flatter-topped coronal section without a corner; 'top' lowers the vertex smoothly; fades below z0 and toward the face (y > yf)
            mx, zc = op.get('mx', -0.25), op['zc']; dx = S[:, 0]-mx; dz = S[:, 2]-zc; rr = np.hypot(dx, dz)+1e-6; th = np.arctan2(np.abs(dx), dz)
            prof = np.exp(-((th-op.get('ang', 0.75))/op.get('angw', 0.45))**2); zf = sstep((S[:, 2]-op['z0'])/op.get('zw', 3.0))
            yf = 1-sstep((S[:, 1]-op.get('yf', 6.0))/op.get('yfw', 3.0)); w = prof*zf*yf
            disp = np.zeros_like(S); amt = op.get('amt', 0.0)*w; disp[:, 0] = amt*dx/rr; disp[:, 2] = amt*dz/rr
            tw = np.exp(-(th/op.get('topw', 0.5))**2)*zf*yf; disp[:, 2] += -op.get('top', 0.0)*tw
            yb = op.get('back_y', -99); wb = sstep((yb-S[:, 1])/op.get('back_w', 4.0))*sstep((S[:, 2]-op.get('bz0', op['z0']))/op.get('bzw', op.get('zw', 3.0))); disp[:, 1] += op.get('shorten', 0.0)*wb; w = np.maximum(w, np.maximum(tw, wb))
        elif op['op'] == 'smooth':   # Taubin (volume-preserving) smoothing inside the weight: softens creases / ridges without shrinking the form
            E = np.r_[T[:, [0, 1]], T[:, [1, 2]], T[:, [2, 0]]]; E = np.r_[E, E[:, ::-1]]; deg = np.bincount(E[:, 0], minlength=len(X)).astype(float)
            Wfull = np.zeros(len(X)); Wfull[SOFT] = w; Y = X.copy()
            for it in range(op.get('iters', 10)):
                for lam in (op.get('lam', 0.5), -op.get('lam', 0.5)-0.03):
                    acc = np.zeros_like(Y); np.add.at(acc, E[:, 0], Y[E[:, 1]]); L = acc/np.maximum(deg, 1)[:, None]-Y; Y = Y+(lam*Wfull)[:, None]*L
            disp = (Y-X)[SOFT]
        X[SOFT] += disp
        for sg in op.get('rigid', []):
            lo, hi = SEG[sg]
            if op['op'] == 'move': X[lo:hi] += np.asarray(op['d'], float)*np.array([side, 1, 1])
        log.append((op.get('name', op['op']), side, round(float(np.linalg.norm(disp, axis=1).max()*10), 2), int((w > 0.01).sum())))
np.save(OUT, X); print('SHAPE_OK', OUT, json.dumps(log))
