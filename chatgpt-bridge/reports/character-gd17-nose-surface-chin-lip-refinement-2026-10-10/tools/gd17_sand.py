"""GD17 'sanding' of sculpt-stroke unevenness WITHOUT shrinking the anatomical form: the high-frequency part of the surface relief
(relief = (vertex - one-ring mean) . normal; hf = relief - its 2-ring smoothed version) is removed along the normal, only inside soft zone
masks, never on protected natural creases (alar crease / nostril sill / columella base, given as exclusion spheres). Large and mid forms
(bridge line, lobule volume, alar narrowing) are kept because only the hf band is touched. Iterated a few times with a step factor.
usage: blender -b --python gd17_sand.py -- <in.npy> <topo.npz> <out.npy> <zones json [[x,y,z,rx,ry,rz], ...]> <exclude json [[x,y,z,r], ...]> [iters=3] [step=0.8]"""
import sys, json, numpy as np
a = sys.argv[sys.argv.index('--')+1:]; X = np.load(a[0]); TP = np.load(a[1]); OUT = a[2]; ZN = json.loads(a[3]); EX = json.loads(a[4])
IT = int(a[5]) if len(a) > 5 else 3; ST = float(a[6]) if len(a) > 6 else 0.8; NS = 24049
T = TP['loops'].reshape(-1, 3); T = T[(T < NS).all(1)]; E = np.unique(np.sort(np.r_[T[:, [0, 1]], T[:, [1, 2]], T[:, [2, 0]]], 1), axis=0)
I0 = np.r_[E[:, 0], E[:, 1]]; I1 = np.r_[E[:, 1], E[:, 0]]; DEG = np.bincount(I0, minlength=NS).astype(float)
def lap(F): acc = np.zeros_like(F); np.add.at(acc, I0, F[I1]); return acc/np.maximum(DEG, 1)[:, None]
def normals(S):
    fn = np.cross(S[T[:, 1]]-S[T[:, 0]], S[T[:, 2]]-S[T[:, 0]]); N = np.zeros((NS, 3))
    for k in range(3): np.add.at(N, T[:, k], fn)
    return N/np.maximum(np.linalg.norm(N, axis=1), 1e-12)[:, None]
def ss(t): t = np.clip(t, 0, 1); return t*t*(3-2*t)
S = X[:NS].copy(); w = np.zeros(NS)
for x, y, z, rx, ry, rz in ZN:
    q = np.sqrt((((S-np.array([x, y, z]))/np.array([rx, ry, rz]))**2).sum(1)); w = np.maximum(w, ss((1-q)/0.35))
for x, y, z, r in EX:
    d = np.linalg.norm(S-np.array([x, y, z]), axis=1); w *= ss((d-r)/(0.5*r))
for _ in range(IT):
    N = normals(S); r = ((S-lap(S))*N).sum(1); hf = r-lap(lap(r[:, None]))[:, 0]
    S = S-(ST*w*hf)[:, None]*N
Y = X.copy(); Y[:NS] = S; np.save(OUT, Y); d = np.linalg.norm(Y-X, axis=1)*10
print('SAND verts w>0.05: %d, max change %.3f mm, mean (w>0.05) %.4f mm' % ((w > 0.05).sum(), d.max(), d[:NS][w > 0.05].mean()))
