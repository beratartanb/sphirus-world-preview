"""pass UU: residual between the intended head (target npy, DNA order) and the auto-rigged result (postrig npy), mapped onto the face SKM
dynamic-mesh vertex order (nearest postrig vertex; split seam duplicates share the value). Eyelid margins, eyeballs, mouth interior and lips are
excluded (the rig owns them). Writes [[index, dx, dy, dz], ...] (cm) for ue_g11uu_apply.py.
usage: blender -b --python blender_g11uu_residual.py -- <target.npy> <postrig.npy> <dm.json> <out.json>"""
import sys, os, json, numpy as np, mathutils
a = sys.argv[sys.argv.index('--')+1:]; T = np.load(a[0])[:24049]; P = np.load(a[1])[:24049]; D = np.array(json.load(open(a[2]))); MX = -0.23
def ss(t): t = np.clip(t, 0, 1); return t*t*(3-2*t)
H = T; ax = np.abs(H[:, 0]-MX); eye = np.zeros(len(H))
for sd in (1, -1):
    c = np.array([MX+sd*2.97, 10.5, 162.25]); d = np.sqrt((((H-c)/np.array([2.1, 2.4, 1.45]))**2).sum(1)); eye = np.maximum(eye, 1-ss((d-0.8)/0.35))
mouth = (1-ss((ax-2.6)/0.4))*ss((H[:, 2]-154.0)/0.3)*(1-ss((H[:, 2]-156.6)/0.3))*ss((H[:, 1]-11.0)/0.5)
W = np.ones(len(T)) if os.environ.get("RESID_NOMASK") else (1-eye)*(1-mouth); R = (T-P)*W[:, None]   # v2: RESID_NOMASK=1 -> no eye / mouth mask (the partial mask left a slope break along its boundary = dark lines)
# v3: LOW-PASS the residual over the head surface (graph diffusion) -> only broad shape differences are baked; the auto-rig's own smoothing of
# accumulated sub-mm op noise is kept (a raw residual bake re-introduced lumps = the 'muscular' look of uu31b)
NL = int(os.environ.get('RESID_LOWPASS', '0'))
if NL:
    sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930')); from id_common import pkg
    TRI = np.asarray(pkg()['head']['triangles']); T3 = TRI[(TRI < len(T)).all(1)]; E = np.r_[T3[:, [0, 1]], T3[:, [1, 2]], T3[:, [2, 0]]]; E = np.r_[E, E[:, ::-1]]
    DEG = np.bincount(E[:, 0], minlength=len(T)).astype(float)
    for _ in range(NL):
        acc = np.zeros_like(R); np.add.at(acc, E[:, 0], R[E[:, 1]]); R = R+0.5*(acc/np.maximum(DEG, 1)[:, None]-R)
kd = mathutils.kdtree.KDTree(len(P))
for i, p in enumerate(P): kd.insert(p, i)
kd.balance(); out = []; dmax = 0.0; far = 0
for j, q in enumerate(D):
    co, i, dist = kd.find(q)
    if dist > 0.02: far += 1; continue
    r = R[i]
    if np.linalg.norm(r) > 0.003: out.append([j, round(float(r[0]), 5), round(float(r[1]), 5), round(float(r[2]), 5)]); dmax = max(dmax, float(np.linalg.norm(r)))
json.dump(out, open(a[3], 'w')); print('RESID n_moved %d of %d (unmatched %d), max %.2f mm' % (len(out), len(D), far, dmax*10))
