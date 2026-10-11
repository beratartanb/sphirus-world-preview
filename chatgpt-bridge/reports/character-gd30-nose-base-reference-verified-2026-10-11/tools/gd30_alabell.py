"""GD30 ala bottom-shell field with BELL weights: moves the bottom shell of the nose base (lobule bottom, alar rim, optionally the nostril sill)
along DIR by A(y) mm, A = monotone cubic through control points [y, mm]; lateral weight is a Gaussian bell exp(-0.5((|x-MX|-MU)/SG)^2) (one
smooth U across the lobule instead of a plateau that ends in a corner), times ss((|x|-XC0)/(XC1-XC0)) to keep the columella still, times the
shell weight ss((z_u+SH-z)/SH) (z_u = lowest down-facing skin z in the 0.1 cm (x, y) neighbourhood: the lower part of the lobule moves, its top
stays, so the lobule stretches = grows), times a soft lip floor ss((z-ZMIN)/ZF). Displacement smoothed by K graph-Laplacian passes.
usage: -- <in.npy> <topo.npz> <out.npy> <ctrl [[y,mm],..]> <dir [0,dy,dz]> <MU> <SG> <XC0> <XC1> <SH> <ZMIN> <ZF> [ZMAX=159.6] [K=3]"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD13_Identity_20261009/tools')); from gd13_common import NS, MX, skin_normals
a = sys.argv[sys.argv.index('--')+1:]; X = np.load(a[0]).astype(float); TP = np.load(a[1]); OUT = a[2]; CP = np.array(json.loads(a[3]), float); DIR = np.array(json.loads(a[4]), float); DIR /= np.linalg.norm(DIR)
MU, SG, XC0, XC1, SH, ZMIN, ZF = [float(v) for v in a[5:12]]; ZMAX = float(a[12]) if len(a) > 12 else 159.6; K = int(a[13]) if len(a) > 13 else 3
def ss(t): t = np.clip(t, 0, 1); return t*t*(3-2*t)
CP = CP[np.argsort(CP[:, 0])]; yc, fc = CP[:, 0], CP[:, 1]/10.0
def pchip(y):
    h = np.diff(yc); m = np.diff(fc)/h; d = np.zeros_like(fc)
    for i in range(1, len(fc)-1):
        if m[i-1]*m[i] > 0: w1, w2 = 2*h[i]+h[i-1], h[i]+2*h[i-1]; d[i] = (w1+w2)/(w1/m[i-1]+w2/m[i])
    d[0] = m[0]; d[-1] = m[-1]; out = np.zeros_like(y); k = np.clip(np.searchsorted(yc, y)-1, 0, len(yc)-2); t = (y-yc[k])/h[k]; inside = (y >= yc[0]) & (y <= yc[-1])
    out[inside] = ((2*t**3-3*t**2+1)*fc[k]+(t**3-2*t**2+t)*h[k]*d[k]+(-2*t**3+3*t**2)*fc[k+1]+(t**3-t**2)*h[k]*d[k+1])[inside]; return out
T = TP['loops'].reshape(-1, 3); T = T[(T < NS).all(1)]; E = np.unique(np.sort(np.r_[T[:, [0, 1]], T[:, [1, 2]], T[:, [2, 0]]], 1), axis=0)
I0 = np.r_[E[:, 0], E[:, 1]]; I1 = np.r_[E[:, 1], E[:, 0]]; DEG = np.bincount(I0, minlength=NS).astype(float)
def lap(F): acc = np.zeros_like(F); np.add.at(acc, I0, F[I1]); return acc/np.maximum(DEG, 1)[:, None]
S = X[:NS]; NN = skin_normals(X); x = np.abs(S[:, 0]-MX); y, z = S[:, 1], S[:, 2]
reg = (y > yc[0]-0.05) & (y < yc[-1]+0.05) & (z > ZMIN-0.2) & (z < ZMAX) & (x < MU+3.5*SG)
bx = np.round((S[:, 0]-MX)/0.1).astype(int); by = np.round(y/0.1).astype(int); zu = {}
for i in np.nonzero(reg & (NN[:, 2] < -0.2))[0]:
    k = (bx[i], by[i]); zu[k] = min(zu.get(k, 1e9), z[i])
w = np.zeros(NS)
for i in np.nonzero(reg)[0]:
    cand = [zu[(bx[i]+dx, by[i]+dy)] for dx in (-1, 0, 1) for dy in (-1, 0, 1) if (bx[i]+dx, by[i]+dy) in zu]
    if not cand: continue
    w[i] = ss((min(cand)+SH-z[i])/SH)*np.exp(-0.5*((x[i]-MU)/SG)**2)*ss((x[i]-XC0)/max(XC1-XC0, 1e-6))*ss((z[i]-ZMIN)/ZF)
D = (pchip(y)*w)[:, None]*DIR[None, :]
for _ in range(K): D = 0.5*D+0.5*lap(D)
D *= ss((z-(ZMIN-0.5*ZF))/(0.5*ZF))[:, None]
Y = X.copy(); Y[:NS] = S+D; np.save(OUT, Y); d = np.linalg.norm(D, axis=1)*10
print('ALABELL verts moved >0.05mm: %d, max %.2f mm' % ((d > 0.05).sum(), d.max()))
