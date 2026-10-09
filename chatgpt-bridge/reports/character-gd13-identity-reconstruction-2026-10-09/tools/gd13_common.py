"""GD13 Identity Master shared helpers (numpy, Blender python). Project frame = UE cm, DNA vertex order (33845 head verts), face toward +y,
up +z, image-right of a frontal camera = +x, facial midline x = MX.
Reference views = the user's 2026-10-09 6-view sheet panels (panel-original pixels, 483 x 541):
  front, q3_faceR (sees the subject's RIGHT side = -x), q3_faceL (sees LEFT = +x), prof_faceL (left profile, +x side).
Camera = perspective pinhole looking at the head (head pose per panel; the subject turns her head, the body does not count):
  Xc = R (X - CH), u = f Xc_x / (D + Xc_z) + cx, v = f Xc_y / (D + Xc_z) + cy, R = rot(rvec) @ R_FRONT, D fixed (cm)."""
import os, sys, json, math, gzip, numpy as np
ROOT = os.getcwd(); GD = os.path.join(ROOT, 'Saved/Codex/GD13_Identity_20261009')
sys.path.insert(0, os.path.join(ROOT, 'Tools/CharacterLookdev_20260930'))
from id_common import pkg, SEG
NH = 33845; NS = 24049; MX = -0.23; CH = np.array([MX, 5.0, 160.0])
R_FRONT = np.array([[1.0, 0, 0], [0, 0, -1.0], [0, -1.0, 0]])
VIEWS = ['front', 'q3_faceR', 'q3_faceL', 'prof_faceL']
def rodrigues(r):
    th = np.linalg.norm(r)
    if th < 1e-12: return np.eye(3)
    k = r/th; K = np.array([[0, -k[2], k[1]], [k[2], 0, -k[0]], [-k[1], k[0], 0]]); return np.eye(3)+math.sin(th)*K+(1-math.cos(th))*K@K
def cam_R(c): return rodrigues(np.asarray(c['rvec'], float))@R_FRONT
def project(c, X):
    Xc = (np.asarray(X, float)-CH)@cam_R(c).T; d = c['D']+Xc[..., 2]
    return np.stack([c['f']*Xc[..., 0]/d+c['cx'], c['f']*Xc[..., 1]/d+c['cy']], -1)
def proj_jac(c, X):
    """d(u,v)/dX per point: (N, 2, 3)"""
    R = cam_R(c); Xc = (np.asarray(X, float)-CH)@R.T; d = c['D']+Xc[:, 2]; f = c['f']
    Ju = np.zeros((len(Xc), 2, 3)); Ju[:, 0, 0] = f/d; Ju[:, 0, 2] = -f*Xc[:, 0]/d**2; Ju[:, 1, 1] = f/d; Ju[:, 1, 2] = -f*Xc[:, 1]/d**2
    return Ju@R
def depth(c, X): return ((np.asarray(X, float)-CH)@cam_R(c).T)[..., 2]
def view_dir(c):
    """world direction from the head toward the camera"""
    return -cam_R(c)[2]
# ---------- mirror map (DNA topology is symmetric about x = MX): nearest vertex to the mirrored position, per segment pair
def mirror_map(X=None, cache=os.path.join(GD, 'data/mirror_map.npy')):
    if os.path.exists(cache): return np.load(cache)
    X = np.asarray(X, float); M = np.arange(NH)
    pairs = [('skin', 'skin'), ('teeth', 'teeth'), ('saliva', 'saliva'), ('eyeL', 'eyeR'), ('eyeR', 'eyeL'), ('eyeshell', 'eyeshell'), ('lashes', 'lashes'), ('eyeEdge', 'eyeEdge'), ('cartilage', 'cartilage')]
    for a, b in pairs:
        ia = np.arange(*SEG[a]); ib = np.arange(*SEG[b]); Pa = X[ia].copy(); Pa[:, 0] = 2*MX-Pa[:, 0]; Pb = X[ib]
        for s in range(0, len(ia), 400):
            d = ((Pa[s:s+400, None, :]-Pb[None])**2).sum(-1); M[ia[s:s+400]] = ib[np.argmin(d, 1)]
    np.save(cache, M); return M
# ---------- tracker curves bound to the mesh (semantic_j: barycentric bindings in DNA order, 'front' and 'close' (= subject's right 3/4))
SEMJ = os.path.join(ROOT, 'Saved/Codex/CharacterGuardian_20261001/semantic_j.json')
def swap_lr(k): return k[:-2]+('_r' if k.endswith('_l') else '_l') if k[-2:] in ('_l', '_r') else k
def bindings(view, MM=None):
    S = json.load(open(SEMJ))
    def cv(v): return [None if (e is None or e[0] is None) else (np.asarray(e[0]), np.asarray(e[1])) for e in v]
    if view == 'front': return {k: cv(v) for k, v in S['front'].items()}
    B = {k: cv(v) for k, v in S['close'].items()}
    if view == 'q3_faceR': return B
    MM = mirror_map() if MM is None else MM   # left-side views: mirror the right 3/4 bindings and swap the curve sides
    return {swap_lr(k): [None if e is None else (MM[e[0]], e[1]) for e in v] for k, v in B.items()}
def bind_pts(B, X): return np.array([np.full(3, np.nan) if e is None else e[1]@X[e[0]] for e in B])
def ref_tracks(path=os.path.join(GD, 'trk/tracks_ref.json')): return {k: {c: np.asarray(p, float) for c, p in v['curves'].items()} for k, v in json.load(open(path)).items()}
def save_cams(C, path): json.dump({k: {kk: (np.asarray(vv).tolist() if isinstance(vv, np.ndarray) else vv) for kk, vv in v.items()} for k, v in C.items()}, open(path, 'w'), indent=1)
def load_cams(path): return json.load(open(path))
# ---------- skin normals (DNA winding is inward -> flipped) and the mandibular border material line
_TRI = None
def skin_normals(X):
    global _TRI
    if _TRI is None: T = np.asarray(pkg()['head']['triangles']); _TRI = T[(T < NS).all(1)]
    P = np.asarray(X, float)[:NS]; n = np.cross(P[_TRI[:, 1]]-P[_TRI[:, 0]], P[_TRI[:, 2]]-P[_TRI[:, 0]])
    N = np.zeros((NS, 3)); [np.add.at(N, _TRI[:, k], n) for k in range(3)]; return -N/np.maximum(np.linalg.norm(N, axis=1), 1e-12)[:, None]
def jaw_line(X, N=None):
    """per sagittal slice (|x - MX| = 0 .. 5.75 cm, both sides) walk the front-most skin vertex per 1 mm height bin downward from below the
    mouth and return the first one whose normal already faces down (n_z < -0.5) = the lower border of the chin / mandible (material vertex ids)"""
    S = np.asarray(X, float)[:NS]; N = skin_normals(X) if N is None else N; ax = np.abs(S[:, 0]-MX); out = {}
    ear = (ax > 6.2) & (S[:, 1] < 4.6) & (S[:, 2] > 154) & (S[:, 2] < 168)
    for side, sg in (('R', -1), ('L', 1)):
        ids = []
        for a in np.arange(0.0, 5.76, 0.25):
            z0 = 154.0 if a < 2.2 else (154.6 if a < 3.5 else 157.0)
            m = (np.abs(S[:, 0]-(MX+sg*a)) < 0.15) & (S[:, 2] > 149.8) & (S[:, 2] < z0) & ~ear & (S[:, 1] > -1.0)
            idx = np.nonzero(m)[0]
            if not len(idx): continue
            zb = np.floor(S[idx, 2]/0.1).astype(int); hit = None
            for b in sorted(set(zb), reverse=True):
                k = idx[zb == b]; v = int(k[np.argmax(S[k, 1])])
                if N[v, 2] < -0.5: hit = v; break
            if hit is not None: ids.append(hit)
        out[side] = ids
    return np.array(out['R'][::-1]+out['L'][1:], int)
