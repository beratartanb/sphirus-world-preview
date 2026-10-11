"""GD31 nostril aperture projected size (geometry only, independent of lighting / texture): the aperture loop (cavity vertices touching outer
skin, data/cavity_idx.npy) of each side is projected with a solved camera; the visible loop area = convex-hull area of the projected loop
points (panel px^2), plus the aperture plane tilt: angle between the loop's best-fit plane normal and the camera view direction (0 = the
nostril faces the camera, 90 = seen edge-on) and the 3D tilt of the aperture long axis from horizontal (+ = front end higher).
usage: -- <cams.json> <topo.npz> <cavity idx.npy> label=head.npy [...]"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD13_Identity_20261009/tools')); from gd13_common import NS, MX, project, view_dir
a = sys.argv[sys.argv.index('--')+1:]; C = json.load(open(a[0])); TP = np.load(a[1]); CAV = np.load(a[2]); HEADS = a[3:]
T = TP['loops'].reshape(-1, 3); T = T[(T < NS).all(1)]; E = np.unique(np.sort(np.r_[T[:, [0, 1]], T[:, [1, 2]], T[:, [2, 0]]], 1), axis=0)
cav = np.zeros(NS, bool); cav[CAV] = True
LOOP = np.unique(np.r_[E[cav[E[:, 0]] & ~cav[E[:, 1]], 0], E[cav[E[:, 1]] & ~cav[E[:, 0]], 1]])
def hull_area(P):
    P = P[np.lexsort((P[:, 1], P[:, 0]))]
    def cross(o, a_, b): return (a_[0]-o[0])*(b[1]-o[1])-(a_[1]-o[1])*(b[0]-o[0])
    lo, up = [], []
    for p in P:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    for p in P[::-1]:
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0: up.pop()
        up.append(p)
    H = np.array(lo[:-1]+up[:-1]); x, y = H[:, 0], H[:, 1]; return 0.5*abs(np.dot(x, np.roll(y, 1))-np.dot(y, np.roll(x, 1)))
print('%-7s %-5s %s' % ('head', 'side', '  '.join('%-24s' % v for v in ('front', 'q3_faceR', 'q3_faceL', 'prof_faceL'))+'  axis tilt deg'))
for h in HEADS:
    lb, p = h.split('=', 1); X = np.load(p)[:NS]
    for sg, nm in ((1, '+x'), (-1, '-x')):
        L = LOOP[(X[LOOP, 0]-MX)*sg > 0]; Q = X[L]; c = Q.mean(0); U, s, Vt = np.linalg.svd(Q-c); nrm = Vt[2]; ax = Vt[0]
        if ax[1] < 0: ax = -ax
        tilt = np.degrees(np.arctan2(ax[2], np.hypot(ax[0], ax[1])))
        row = []
        for v in ('front', 'q3_faceR', 'q3_faceL', 'prof_faceL'):
            P2 = project(C[v], Q); ang = np.degrees(np.arccos(min(1.0, abs(float(nrm@view_dir(C[v]))))))
            row.append('%5.1f px2 @%4.0f deg' % (hull_area(P2), ang))
        print('%-7s %-5s %s  %+5.1f' % (lb, nm, '  '.join('%-24s' % r for r in row), tilt))
