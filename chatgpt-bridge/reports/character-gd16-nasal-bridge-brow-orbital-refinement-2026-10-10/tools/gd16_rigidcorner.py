"""GD16 technical commissure repair: a preset mouth blend shears the tiny commissure triangles (area ratio 0.06). Inside small spheres around
each mouth corner the blend DISPLACEMENT (cand - pre-blend head) is replaced by its local weighted mean (w = 1 inside r0 -> 0 at r1,
smoothstep), so the corner translates rigidly with the lips and keeps the pre-blend (healthy) corner geometry. Not a shape op.
usage: -- <cand.npy> <preblend.npy> <out.npy> <spots json [[x,y,z,r0,r1], ...]>"""
import sys, json, numpy as np
a = sys.argv[sys.argv.index('--')+1:]; X = np.load(a[0]); B = np.load(a[1]); OUT = a[2]; SP = json.loads(a[3]); NS = 24049
D = X[:NS]-B[:NS]; Y = X.copy()
for x, y, z, r0, r1 in SP:
    d = np.linalg.norm(B[:NS]-np.array([x, y, z]), axis=1); t = np.clip((r1-d)/(r1-r0), 0, 1); w = t*t*(3-2*t)
    m = w > 0; mean = (D[m]*w[m, None]).sum(0)/w[m].sum(); D = D-w[:, None]*(D-mean)
Y[:NS] = B[:NS]+D; np.save(OUT, Y); print('RIGIDCORNER max change %.3f mm' % (10*np.linalg.norm(Y-X, axis=1).max()))
