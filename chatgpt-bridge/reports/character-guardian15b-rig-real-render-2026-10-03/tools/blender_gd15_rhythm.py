"""GUARDIAN-15 lower-face vertical rhythm: distributed downward z displacement dz(z) (piecewise-linear knots, smoothed) over the perioral /
chin front, so the mouth moves down without dragging the chin: subnasale fixed (K5 nose untouched) -> philtrum lengthens -> stomion / lower
lip / labiomental move most -> chin pad less -> menton almost fixed -> jaw border fixed. Lateral fade keeps cheek width; front-only (y fade).
usage: blender -b -P blender_gd15_rhythm.py -- <in.npy> <out.npy> <scale=1.0>   (knots in mm at scale 1: stomion -1.5)"""
import sys, json, numpy as np
a = sys.argv[sys.argv.index('--')+1:]; X0 = np.load(a[0]); X = X0.copy(); OUT = a[1]; SC = float(a[2]) if len(a) > 2 else 1.0
MX = -0.25; NH = 24049
def sstep(t): t = np.clip(t, 0, 1); return t*t*(3-2*t)
ZK = np.array([149.2, 150.2, 151.4, 152.6, 153.8, 154.6, 155.65, 156.4, 157.0, 157.55]); DK = -0.1*SC*np.array([0.0, 0.15, 0.45, 0.75, 1.25, 1.45, 1.5, 1.0, 0.45, 0.0])
S = X0[:NH]; ax = np.abs(S[:, 0]-MX)
dz = np.interp(S[:, 2], ZK, DK, left=0.0, right=0.0)
w = (1-sstep((ax-3.0)/1.8))*sstep((S[:, 1]-8.5)/1.5)
X[:NH, 2] += dz*w
d = np.abs(X[:, 2]-X0[:, 2])
print('RHYTHM_OK', json.dumps({'scale': SC, 'max_mm': round(10*float(d.max()), 2)}))
np.save(OUT, X)
