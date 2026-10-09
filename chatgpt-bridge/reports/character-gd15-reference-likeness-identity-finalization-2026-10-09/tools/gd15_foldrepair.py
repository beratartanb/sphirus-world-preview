"""GD14 fold repair (technical, not an artistic shape op): blend the displacement of a candidate back toward a base head inside small spheres
around folded lid-margin spots (smoothstep falloff, w=1 inside r0, 0 at r1), so the lid margin returns to the base's clean geometry.
usage: -- <cand.npy> <base.npy> <out.npy> <spots json [[x,y,z,r0,r1], ...] (project cm)>"""
import sys, json, numpy as np
a = sys.argv[sys.argv.index('--')+1:]; X = np.load(a[0]); B = np.load(a[1]); OUT = a[2]; SP = json.loads(a[3]); NS = 24049
w = np.zeros(NS)
for x, y, z, r0, r1 in SP:
    d = np.linalg.norm(X[:NS]-np.array([x, y, z]), axis=1); t = np.clip((r1-d)/(r1-r0), 0, 1); w = np.maximum(w, t*t*(3-2*t))
Y = X.copy(); Y[:NS] = X[:NS]-w[:, None]*(X[:NS]-B[:NS]); np.save(OUT, Y)
print('REPAIR verts w>0: %d, max change %.3f mm' % ((w > 0).sum(), 10*np.linalg.norm(Y-X, axis=1).max()))
