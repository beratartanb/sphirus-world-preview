"""GD12 surface-anchored sculpt brushes on a DNA-order head npy (UE cm; x lateral, y forward, z up; midline x = MX).
Brushes (applied in order, each mirrored when "sym"):
  anchor: [dx, z]          -> the front-most skin vertex at |x - MX| ~ dx (+x side; -x mirrored) and height z (y ignored: no off-surface centres)
          or [dx, z, "side"] -> the outer-most (max |x|) skin vertex at that height in front of the ear (for cheek / jaw sides)
  r: radius cm (or [r_xy, r_z] for an ellipsoid), falloff (1 - q^2)^2
  gate: min dot(vertex normal, anchor normal) (default 0.2) -> never reaches the inner lip / mouth bag / back of a lid
  mode: "inflate" amt cm along the vertex normal (negative deflates) | "move" d [dx, dy, dz] cm (dx mirrored) | "smooth" iters, k (Laplacian of the
        displacement-free surface toward neighbour mean, weighted) | "relax" iters (Taubin, shape-preserving)
  protect: vertices in the protected set (lid margins, eyes interior, mouth interior) never move (soft ramp ~0.4 cm)
usage: blender -b --python blender_gd12_sculpt.py -- <in.npy> <brushes.json> <out.npy>"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930')); from id_common import pkg, SEG
a = sys.argv[sys.argv.index('--')+1:]; X0 = np.load(a[0]); X = X0.copy(); J = json.load(open(a[1])); MX = J.get('mx', -0.23); NH = 24049
T = np.asarray(pkg()['head']['triangles']); T = T[(T < NH).all(1)]
E = np.r_[T[:, [0, 1]], T[:, [1, 2]], T[:, [2, 0]]]; E = np.r_[E, E[:, ::-1]]; DEG = np.bincount(E[:, 0], minlength=NH).astype(float)
def normals(H):
    N = np.zeros_like(H); fn = -np.cross(H[T[:, 1]]-H[T[:, 0]], H[T[:, 2]]-H[T[:, 0]])
    for k in range(3): np.add.at(N, T[:, k], fn)
    N /= np.maximum(np.linalg.norm(N, axis=1), 1e-9)[:, None]
    if (N[H[:, 1] > 12, 1]).mean() < 0: N = -N
    return N
def lap(F):
    acc = np.zeros_like(F); np.add.at(acc, E[:, 0], F[E[:, 1]]); return acc/np.maximum(DEG, 1)[:, None] if F.ndim == 2 else acc/np.maximum(DEG, 1)
def ss(t): t = np.clip(t, 0, 1); return t*t*(3-2*t)
H0 = X0[:NH]; ax0 = np.abs(H0[:, 0]-MX)
# protected: eyelid margins (thin band around each eye opening), mouth interior (behind the lip front), ear
prot = np.zeros(NH)
for sd in (1, -1):
    c = np.array([MX+sd*2.97, 10.5, 162.25]); d = np.sqrt((((H0-c)/np.array([1.75, 2.0, 0.95]))**2).sum(1)); prot = np.maximum(prot, 1-ss((d-0.92)/0.25))
cell = (np.round((H0[:, 0]-MX)/0.25)).astype(int)*100000+(np.round(H0[:, 2]/0.25)).astype(int); ymax = {}
for cc, yy in zip(cell, H0[:, 1]): ymax[cc] = max(ymax.get(cc, -1e9), yy)
depth = np.array([ymax[cc]-yy for cc, yy in zip(cell, H0[:, 1])])
mouth_in = (ax0 < 2.9) & (H0[:, 2] > 154.4) & (H0[:, 2] < 156.1) & (depth > 0.35)
prot = np.maximum(prot, mouth_in.astype(float)); prot = np.maximum(prot, ((ax0 > 6.3) & (H0[:, 1] < 4.2) & (H0[:, 2] > 154) & (H0[:, 2] < 168)).astype(float))
for _ in range(4): prot = np.maximum(prot, 0.6*lap(prot))
FREE = 1-np.clip(prot, 0, 1)
SKIN = np.zeros(NH, bool); SKIN[:SEG['skin'][1]] = True
def anchor(H, spec, sd):
    dx, z = spec[0], spec[1]; side = len(spec) > 2 and spec[2] == 'side'
    for tol in (1.0, 2.0, 4.0):
        cand = np.nonzero(SKIN & (np.abs(H[:, 2]-z) < 0.22*tol) & (np.abs(np.abs(H[:, 0]-MX)-dx) < 0.35*tol if not side else True) & ((H[:, 0]-MX)*sd >= -0.05))[0]
        if len(cand): break
    if side: cand = cand[H[cand, 1] > 1.0]; i = cand[np.argmax(np.abs(H[cand, 0]-MX))]
    else: i = cand[np.argmax(H[cand, 1])]
    return i
log = []
for b in J['brushes']:
    H = X[:NH].copy(); N = normals(H); moved = np.zeros(NH)
    sides = (1, -1) if b.get('sym', True) else (1,)
    for sd in sides:
        i = anchor(H, b['anchor'], sd); c = H[i]; n0 = N[i]
        r = b['r'] if isinstance(b['r'], list) else [b['r'], b['r']]
        q2 = ((H[:, 0]-c[0])**2+(H[:, 1]-c[1])**2)/r[0]**2+(H[:, 2]-c[2])**2/r[1]**2
        w = np.clip(1-q2, 0, 1)**2*(N@n0 > b.get('gate', 0.2))*FREE
        if sd == -1 and abs(c[0]-MX) < 0.3: continue   # midline brush: applied once
        m = b['mode']
        if m == 'inflate': X[:NH] += (b['amt']*w)[:, None]*N
        elif m == 'move':
            d = np.array(b['d'], float); d[0] *= sd; X[:NH] += w[:, None]*d
        moved = np.maximum(moved, w)
    if b['mode'] in ('smooth', 'relax'):
        w = np.zeros(NH)
        for sd in sides:
            i = anchor(H, b['anchor'], sd); c = H[i]; r = b['r'] if isinstance(b['r'], list) else [b['r'], b['r']]
            q2 = ((H[:, 0]-c[0])**2+(H[:, 1]-c[1])**2)/r[0]**2+(H[:, 2]-c[2])**2/r[1]**2; w = np.maximum(w, np.clip(1-q2, 0, 1)**2*FREE)
        Y = X[:NH].copy()
        for _ in range(b.get('iters', 4)):
            if b['mode'] == 'smooth': Y = Y+(b.get('k', 0.5)*w)[:, None]*(lap(Y)-Y)
            else:
                Y = Y+(0.5*w)[:, None]*(lap(Y)-Y); Y = Y+(-0.53*w)[:, None]*(lap(Y)-Y)
        X[:NH] = Y; moved = w
    dd = np.linalg.norm(X[:NH]-H, axis=1)*10; log.append((b['name'], round(float(dd.max()), 2), int((dd > 0.05).sum())))
    print('BRUSH %-22s max %.2f mm verts %d' % log[-1])
np.save(a[2], X); dd = np.linalg.norm(X[:NH]-X0[:NH], axis=1)*10; print('GD12_SCULPT_OK total max %.2f mm moved %d' % (dd.max(), (dd > 0.05).sum()))
