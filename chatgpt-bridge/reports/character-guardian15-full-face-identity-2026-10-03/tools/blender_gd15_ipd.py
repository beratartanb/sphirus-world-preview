"""GUARDIAN-15 evidence-based IPD reduction variant: move each eye assembly (eyeball, eyeshell, lashes, eyeEdge) medially by D cm and carry the
orbit soft tissue with a smooth radial field around each eye centre (full weight within R0 of the centre in the x-z plane, fading to 0 at R1),
front-of-skull only (y > 5). The midline stays fixed (each side moves toward it), so the nasal bridge only compresses slightly.
usage: blender -b -P blender_gd15_ipd.py -- <in.npy> <out.npy> <D cm> [R0=1.7] [R1=3.4]"""
import sys, json, numpy as np
a = sys.argv[sys.argv.index('--')+1:]; X = np.load(a[0]).copy(); OUT = a[1]; D = float(a[2]); R0 = float(a[3]) if len(a) > 3 else 1.7; R1 = float(a[4]) if len(a) > 4 else 3.4
MX = -0.25; NH = 24049
def sstep(t): t = np.clip(t, 0, 1); return t*t*(3-2*t)
segs = {'A': (28955, 29725), 'B': (29725, 30495)}; cA = X[28955:29725].mean(0); cB = X[29725:30495].mean(0)
X0 = X.copy(); out = {}
for c in (cA, cB):
    sg = -np.sign(c[0]-MX)   # toward the midline
    # skin + other face verts on this side
    S = X0[:NH]; side = np.sign(S[:, 0]-MX) == np.sign(c[0]-MX)
    r = np.hypot(S[:, 0]-c[0], S[:, 2]-c[2]); w = (1-sstep((r-R0)/(R1-R0)))*sstep((S[:, 1]-5.0)/1.5)*side
    # do not cross the midline: scale by distance to midline
    w = w*sstep(np.abs(S[:, 0]-MX)/0.9)
    X[:NH, 0] += sg*D*w
    # eye assembly verts (eyeball, shell, lashes, edge) belonging to this eye: nearest eye centre
    E = np.arange(28955, 33459); P = X0[E]; mine = np.linalg.norm(P-c, axis=1) < np.linalg.norm(P-(cB if c is cA else cA), axis=1)
    X[E[mine], 0] += sg*D
out['ipd_before'] = round(float(np.linalg.norm(cA-cB)), 3); out['ipd_after'] = round(float(np.linalg.norm(X[28955:29725].mean(0)-X[29725:30495].mean(0))), 3)
np.save(OUT, X); print('IPD_OK', json.dumps(out))
