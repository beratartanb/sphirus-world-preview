"""GD46: pose a build dir's Henley REST (outfit_geometry + weights) with a PIE pose dump by offline LBS and compare to that PIE run's Henley render readback.
usage: blender -b --python gd46_validate_rest.py -- <build_dir> <pie_pose.json> <pie_posed_meshes.json.gz> <sculpt_package.json.gz>"""
import sys, json, gzip, numpy as np
from mathutils import Vector, kdtree
BD, PJ, PM, PKG = sys.argv[sys.argv.index('--')+1:]
P = json.loads(gzip.open(PKG, 'rb').read()); BIND = P['skeleton']['Body']['bind']; BONES = list(BIND); BI = {b: i for i, b in enumerate(BONES)}; PT = json.load(open(PJ))['bones']
def qm(q):
    x, y, z, w = q; return np.array([[1-2*(y*y+z*z), 2*(x*y-z*w), 2*(x*z+y*w)], [2*(x*y+z*w), 1-2*(x*x+z*z), 2*(y*z-x*w)], [2*(x*z-y*w), 2*(y*z+x*w), 1-2*(x*x+y*y)]])
M = {}
for b in BONES:
    Rb = qm(BIND[b]['rotation']); tb = np.asarray(BIND[b]['translation']); v = PT.get(b, BIND[b]); Rp = qm(v['rotation']); tp = np.asarray(v['translation']); R = Rp@np.linalg.inv(Rb); M[b] = (R, tp-R@tb)
G = json.loads(gzip.open(BD+'/outfit_geometry.json.gz', 'rb').read())['henley']; W = json.loads(gzip.open(BD+'/outfit_weights.json.gz', 'rb').read())['henley']
X = np.asarray(G['positions']); Y = np.zeros_like(X)
for i, (x, ws) in enumerate(zip(X, W)):
    s = sum(w for b, w in ws.items() if b in M) or 1.0
    for b, w in ws.items():
        if b in M: R, t = M[b]; Y[i] += w/s*(R@x+t)
Q = np.asarray(json.loads(gzip.open(PM, 'rt').read())['Henley']['positions']); kd = kdtree.KDTree(len(Y))
for i, p in enumerate(Y): kd.insert(Vector(p), i)
kd.balance(); d = np.asarray([kd.find(Vector(q))[2] for q in Q]); print('VALREST p50 %.3f p95 %.3f max %.3f' % (np.percentile(d, 50), np.percentile(d, 95), d.max()))
