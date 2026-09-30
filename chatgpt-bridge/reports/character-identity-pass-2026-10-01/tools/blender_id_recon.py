"""IDENTITY pass: multi-view reference-driven face reconstruction (target shape for the MetaHuman state fit).
Unknowns: displacements of K control points on the head skin (Gaussian RBF field) + a weak-perspective camera per reference view
(rotation, scale, 2D translation). Constraints (reference pixels, normalised by the view's inter-pupil distance):
  - MetaHuman tracker curves (eyelids, lips, philtrum, nasolabial): candidate points = the same curves tracked on the candidate
    render (known perspective camera) ray-cast onto the current mesh; reference points = the curves tracked on the reference
  - hand-picked semantic points (brows: candidate pixel -> ray cast; nose / ear: geometric definitions on the mesh)
  - silhouette contours: outermost skin vertex along a 2D normal inside a band must reach the reference contour
Priors: ridge on the displacements, mirror symmetry (weak), eyes / teeth / saliva locked, cranium untouched (no controls there).
Alternates pose refinement and a linear shape solve. Writes <out>/target.json (fit input), recon.json (stats), overlays.
usage: blender -b -P blender_id_recon.py -- <out_dir> [iterations]   env: RC_LAMBDA, RC_SYM, RC_SIGMA, RC_K"""
import bpy, sys, os, json, math
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930')); from id_common import *
a = sys.argv[sys.argv.index('--')+1:]; OUT = a[0]; ITERS = int(a[1]) if len(a) > 1 else 6; os.makedirs(OUT, exist_ok=True)
E = lambda k, d: float(os.environ.get(k, d)); I_ = 'Saved/Codex/CharacterIdentity_20260930'; TD = I_+'/track'
P = pkg(); NB = P['NB']; T = np.asarray(P['head']['triangles']); MI = np.asarray(P['head']['material_ids'])
X0 = head_brn()+np.load('Saved/Codex/CharacterFaceMatch_20260930/face_c/face_delta_lod0.npy')        # current candidate neutral (face_c)
if os.environ.get('RC_START'): X0 = np.load(os.environ['RC_START'])
NS = 24049; SK = T[MI == 0]
vn = np.zeros_like(X0); fn = np.cross(X0[T[:, 1]]-X0[T[:, 0]], X0[T[:, 2]]-X0[T[:, 0]]); fn = -fn
for k in range(3): np.add.at(vn, T[:, k], fn)
vn /= np.maximum(np.linalg.norm(vn, axis=1), 1e-9)[:, None]
PK = json.load(open(I_+'/ref_picks.json')); TR = json.load(open(TD+'/tracks.json'))
# ---------------------------------------------------------------- candidate anchors
bvh_all = BVHTree.FromPolygons([Vector(p) for p in X0], [list(t) for t in T[np.isin(MI, [0, 3, 4])]]); tri_all = T[np.isin(MI, [0, 3, 4])]
bvh_skin = BVHTree.FromPolygons([Vector(p) for p in X0], [list(t) for t in SK])
skin_ids = np.arange(NS)
def cam_basis(cam):
    x, y, z, yaw, pit = cam; cy, sy, cp, sp = math.cos(math.radians(yaw)), math.sin(math.radians(yaw)), math.cos(math.radians(pit)), math.sin(math.radians(pit))
    return np.array([x, y, z], float), np.array([cy*cp, sy*cp, sp]), np.array([-sy, cy, 0.0]), np.array([-cy*sp, -sy*sp, cp])
def raycast(cam, fov, W, H, px, py):
    o, f, r, u = cam_basis(cam); t = math.tan(math.radians(fov)/2); nx = (px/W-0.5)*2*t; ny = -(py/H-0.5)*2*t*(H/W)
    d = f+r*nx+u*ny; d /= np.linalg.norm(d); loc, nrm, idx, dist = bvh_all.ray_cast(Vector(o), Vector(d))
    if loc is None: return None
    loc = np.asarray(loc); tri = tri_all[idx]
    if not (tri < NS).all():   # hit an eyeball: snap to the nearest skin vertex (lid margin)
        k = skin_ids[np.argmin(np.linalg.norm(X0[:NS]-loc, axis=1))]; return ('v', int(k))
    A, B, C = X0[tri]; v0, v1, v2 = B-A, C-A, loc-A; d00, d01, d11, d20, d21 = v0@v0, v0@v1, v1@v1, v2@v0, v2@v1; den = d00*d11-d01*d01
    bv = (d11*d20-d01*d21)/den; bw = (d00*d21-d01*d20)/den; return ('t', tri.tolist(), [1-bv-bw, bv, bw])
def anchor_pos(an, X):
    if an[0] == 'v': return X[an[1]]
    return sum(w*X[i] for i, w in zip(an[1], an[2]))
def anchor_w(an): return ([an[1]], [1.0]) if an[0] == 'v' else (an[1], an[2])
# geometric definitions on the current mesh
S_ = X0[:NS]; mid = np.abs(S_[:, 0]) < 0.35
def prof_vertex(z0, z1, mode):
    m = mid & (S_[:, 2] > z0) & (S_[:, 2] < z1) & (S_[:, 1] > 8); ids = np.nonzero(m)[0]
    if mode == 'max': return int(ids[np.argmax(S_[ids, 1])])
    zb = np.round(S_[ids, 2]/0.15); best = {}
    for i, b in zip(ids, zb):
        if b not in best or S_[i, 1] > S_[best[b], 1]: best[b] = i
    prof = sorted(best.items()); k = min(prof, key=lambda kv: S_[kv[1], 1]); return int(k[1])
GEO = {}
GEO['pronasale'] = prof_vertex(157.8, 161.0, 'max'); zt = S_[GEO['pronasale'], 2]
GEO['subnasale'] = prof_vertex(156.6, zt-0.6, 'min'); GEO['sellion'] = prof_vertex(161.5, 164.6, 'min')
zm = 0.5*(S_[GEO['sellion'], 2]+zt); GEO['dorsum_mid'] = int(np.nonzero(mid & (np.abs(S_[:, 2]-zm) < 0.2) & (S_[:, 1] > 10))[0][np.argmax(S_[np.nonzero(mid & (np.abs(S_[:, 2]-zm) < 0.2) & (S_[:, 1] > 10))[0], 1])])
zs = S_[GEO['subnasale'], 2]; nose = (S_[:, 2] > zs-0.2) & (S_[:, 2] < zs+1.3) & (S_[:, 1] > 11) & (np.abs(S_[:, 0]) < 2.8); ids = np.nonzero(nose)[0]
GEO['alar_L'] = int(ids[np.argmax(S_[ids, 0])]); GEO['alar_R'] = int(ids[np.argmin(S_[ids, 0])])
ear = (S_[:, 0] < -6.3) & (S_[:, 1] > -3) & (S_[:, 1] < 3.5) & (S_[:, 2] > 150) & (S_[:, 2] < 165); ids = np.nonzero(ear)[0]
m2 = ids[(S_[ids, 2] > 155.5) & (S_[ids, 2] < 158.5) & (S_[ids, 0] < -6.8)]; GEO['tragus_R'] = int(m2[np.argmax(S_[m2, 1])]) if len(m2) else int(ids[0])
GEO['lobe_R'] = int(ids[np.argmin(S_[ids, 2])])
print('GEO', {k: np.round(S_[v], 2).tolist() for k, v in GEO.items()}, flush=True)
anchors = []   # (view, anchor, target2d, weight, kind, extra)
for vk, V in PK.items():
    if vk.startswith('_') or vk == 'tracker_weights': continue
    ci = TR[V['cand_image']]; ri = TR[V['image']]; W, H = ci['size']
    for cname, cpts in ci['curves'].items():
        rpts = ri['curves'].get(cname)
        if not rpts or len(rpts) != len(cpts): continue
        grp = next((g for g in PK['tracker_weights'] if g in cname), None); w = PK['tracker_weights'].get(grp, 0.5)/len(cpts)*8
        for cp, rp in zip(cpts, rpts):
            an = raycast(V['cam'], V['fov'], W, H, cp[0], cp[1])
            if an: anchors.append((vk, an, np.array(rp), w, 'pt', cname))
    for p in V['points']:
        an = ('v', GEO[p['geo']]) if 'geo' in p else raycast(V['cam'], V['fov'], W, H, *p['cand'])
        if an: anchors.append((vk, an, np.array(p['ref']), p['w'], 'pt', p['name']))
print('anchors', len(anchors), flush=True)
# ---------------------------------------------------------------- RBF controls (head skin, face + front neck + ears; not cranium top/back)
rng = np.random.default_rng(1); reg = (S_[:, 1] > -4.0) & (S_[:, 2] > 146.0) & (S_[:, 2] < 169.5)
cand = np.nonzero(reg)[0]; K = int(E('RC_K', '220')); sel = [cand[rng.integers(len(cand))]]; dmin = np.linalg.norm(S_[cand]-S_[sel[0]], axis=1)
for _ in range(K-1): j = int(np.argmax(dmin)); sel.append(cand[j]); dmin = np.minimum(dmin, np.linalg.norm(S_[cand]-S_[cand[j]], axis=1))
CP = S_[sel]; SIG = E('RC_SIGMA', '1.5')
lockm = np.zeros(len(X0), bool); lockm[SEG['teeth'][0]:SEG['eyeR'][1]] = True                        # teeth, saliva, eyeballs
def Phi(Xs): return np.exp(-(np.linalg.norm(Xs[:, None, :]-CP[None], axis=2)/SIG)**2)
PhiAll = np.zeros((len(X0), K), np.float32)
for s0 in range(0, len(X0), 4000): PhiAll[s0:s0+4000] = Phi(X0[s0:s0+4000])
PhiAll[lockm] = 0.0; PhiAll[S_[:, 2].size:] *= 1.0
guard = sstep = lambda x: np.clip(x, 0, 1)**2*(3-2*np.clip(x, 0, 1))
g = guard((X0[:, 2]-146.5)/2.0); PhiAll *= g[:, None]                                                   # collar / seam region untouched
mir = np.array([np.argmin(np.linalg.norm(CP-(c*np.array([-1, 1, 1])), axis=1)) for c in CP])
def phi_of(an): ids, ws = anchor_w(an); return sum(w*PhiAll[i] for i, w in zip(ids, ws))
# ---------------------------------------------------------------- weak-perspective cameras
def rodrigues(w):
    th = np.linalg.norm(w)
    if th < 1e-12: return np.eye(3)
    k = w/th; Kx = np.array([[0, -k[2], k[1]], [k[2], 0, -k[0]], [-k[1], k[0], 0]]); return np.eye(3)+math.sin(th)*Kx+(1-math.cos(th))*Kx@Kx
def init_R(yaw):
    _, f, r, u = cam_basis([0, 0, 0, yaw, 0]); return np.stack([r, -u, f])        # rows: image right, image down, forward
views = {vk: V for vk, V in PK.items() if not vk.startswith('_') and vk != 'tracker_weights'}
eyeL = X0[SEG['eyeL'][0]:SEG['eyeL'][1]].mean(0); eyeR = X0[SEG['eyeR'][0]:SEG['eyeR'][1]].mean(0)
CAMS = {}
for vk, V in views.items():
    R = init_R(V['yaw_guess']); A = [(an, tg) for (v, an, tg, w, kd, nm) in anchors if v == vk]
    Xa = np.array([anchor_pos(an, X0) for an, _ in A]); Y = np.array([tg for _, tg in A]); pr = Xa@R[:2].T
    s = np.sqrt(((Y-Y.mean(0))**2).sum()/((pr-pr.mean(0))**2).sum()); t = Y.mean(0)-s*pr.mean(0); CAMS[vk] = [R, s, t]
def project(vk, Xs): R, s, t = CAMS[vk]; return s*(Xs@R[:2].T)+t
def ipd(vk): R, s, t = CAMS[vk]; return s*np.linalg.norm((eyeL-eyeR)@R[:2].T)
def refine_pose(X, vk, n=15):
    R, s, t = CAMS[vk]; A = [(an, tg, w) for (v, an, tg, w, kd, nm) in anchors if v == vk]; Xa = np.array([anchor_pos(an, X) for an, _, _ in A]); Y = np.array([tg for _, tg, _ in A]); Wt = np.array([w for _, _, w in A])
    for _ in range(n):
        pr = s*(Xa@R[:2].T)+t; r = (pr-Y).ravel(); J = []
        for k in range(3):
            dw = np.zeros(3); dw[k] = 1e-4; R2 = R@rodrigues(dw) if False else rodrigues(dw)@R; J.append(((s*(Xa@R2[:2].T)+t)-pr).ravel()/1e-4)
        J.append((Xa@R[:2].T).ravel()); J.append(np.tile([1.0, 0.0], len(Xa))); J.append(np.tile([0.0, 1.0], len(Xa)))
        J = np.stack(J, 1); ww = np.repeat(Wt, 2); dx = np.linalg.lstsq(J*ww[:, None], -r*ww, rcond=None)[0]
        R = rodrigues(dx[:3])@R; s += dx[3]; t = t+dx[4:6]
    CAMS[vk] = [R, s, t]
def contour_rows(X, vk, V):
    rows = []; R, s, t = CAMS[vk]; pr = project(vk, X[:NS])
    face = (X[:NS, 1] > 2.5) & (X[:NS, 2] > 147.5) & (X[:NS, 2] < 168)
    Nn = np.zeros_like(X[:NS]); fn_ = -np.cross(X[SK[:, 1]]-X[SK[:, 0]], X[SK[:, 2]]-X[SK[:, 0]])
    for kk in range(3): np.add.at(Nn, SK[:, kk], fn_)
    Nn /= np.maximum(np.linalg.norm(Nn, axis=1), 1e-9)[:, None]; occl = np.abs(Nn@R[2]) < E('RC_SIL', '0.22')   # occluding-contour vertices only
    for c in V['contours']:
        n = np.array(c['n'], float); n /= np.linalg.norm(n); tt = np.array([-n[1], n[0]]); p = np.array(c['ref'])
        m = face & occl
        if c['region'] == 'jaw': m &= (X[:NS, 2] < 156.0) & (X[:NS, 2] > 148.5) & (X[:NS, 1] > 4.0)
        if c['region'] == 'far': m &= (X[:NS, 0] > 0.5) & (X[:NS, 2] > 150.0)
        n3 = n[0]*R[0]+n[1]*R[1]; m &= (Nn@n3) > 0.3                                                        # silhouette facing outward along n
        band = np.abs((pr-p)@tt) < c['band']; ids = np.nonzero(m & band)[0]
        if not len(ids): continue
        k = ids[np.argmax(pr[ids]@n)]; rows.append((k, n, p, c['w'], c['name']))
    return rows
# ---------------------------------------------------------------- alternate pose / shape
d = np.zeros((K, 3)); LAM = E('RC_LAMBDA', '0.02'); SYM = E('RC_SYM', '0.3'); hist = []
def cur(): return X0+(PhiAll@d).astype(np.float64)
for it in range(ITERS):
    X = cur()
    if it < int(E('RC_POSE_IT', '2')):
        for vk in views: refine_pose(X, vk)
    rows = []; rhs = []; wts = []
    for vk, V in views.items():
        R, s, t = CAMS[vk]; nrm = 1.0/ipd(vk)
        for (v, an, tg, w, kd, nm) in anchors:
            if v != vk: continue
            ph = phi_of(an); base = s*(anchor_pos(an, X0)@R[:2].T)+t          # linear in d: proj(x0 + ph d)
            for ax in range(2):
                rows.append(np.kron(ph, s*R[ax])*nrm); rhs.append((tg[ax]-base[ax])*nrm); wts.append(w)
        for (k, n, p, w, nm) in contour_rows(X, vk, V):
            ph = PhiAll[k]; base = s*(X0[k]@R[:2].T)+t; Rn = s*(n[0]*R[0]+n[1]*R[1])
            rows.append(np.kron(ph, Rn)*nrm); rhs.append(float(n@(p-base))*nrm); wts.append(w*1.5)
    A = np.array(rows); b = np.array(rhs); Wt = np.sqrt(np.array(wts))
    M = (A*Wt[:, None]).T@(A*Wt[:, None]); v = (A*Wt[:, None]).T@(b*Wt)
    Ireg = LAM*np.diag(np.tile([1.0, E('RC_DY', '1.0'), 1.0], K)); Msym = np.zeros((3*K, 3*K)); F = np.diag([-1.0, 1, 1])
    for i, j in enumerate(mir):                                                    # || d_i - F d_j ||^2
        Si = np.zeros((3, 3*K)); Si[:, 3*i:3*i+3] = np.eye(3); Si[:, 3*j:3*j+3] -= F; Msym += Si.T@Si
    sol = np.linalg.solve(M+Ireg+SYM*Msym, v); d = sol.reshape(K, 3)
    X = cur(); res = {}
    for vk in views:
        e = [np.linalg.norm(project(vk, anchor_pos(an, X)[None])[0]-tg)/ipd(vk) for (v, an, tg, w, kd, nm) in anchors if v == vk]; res[vk] = round(float(np.mean(e)), 4)
    dm = np.linalg.norm(X-X0, axis=1); hist.append({'it': it, 'mean_err_ipd': res, 'disp_max_mm': round(float(dm.max()*10), 2), 'disp_p95_mm': round(float(np.percentile(dm[:NS][dm[:NS] > 0.01], 95)*10), 2) if (dm[:NS] > 0.01).any() else 0})
    print('IT', hist[-1], flush=True)
X = cur()
# per-anchor report + overlays on the reference images
rep = {}
for vk, V in views.items():
    e0 = {}; e1 = {}
    for (v, an, tg, w, kd, nm) in anchors:
        if v != vk: continue
        CAMS_bk = CAMS[vk]; e1.setdefault(nm, []).append(float(np.linalg.norm(project(vk, anchor_pos(an, X)[None])[0]-tg)/ipd(vk)))
        e0.setdefault(nm, []).append(float(np.linalg.norm(project(vk, anchor_pos(an, X0)[None])[0]-tg)/ipd(vk)))
    rep[vk] = {k: [round(np.mean(e0[k]), 3), round(np.mean(e1[k]), 3)] for k in e1}
    im = bpy.data.images.load(os.path.abspath(f"{TD}/{V['image']}.png")); w_, h_ = im.size; Aimg = np.asarray(im.pixels[:], np.float32).reshape(h_, w_, im.channels)[::-1, :, :3].copy()
    def dot(p, c, r=2):
        x, y = int(p[0]), int(p[1]); Aimg[max(y-r, 0):y+r+1, max(x-r, 0):x+r+1] = c
    sil0 = project(vk, X0[:NS]); sil1 = project(vk, X[:NS])
    for (v, an, tg, w, kd, nm) in anchors:
        if v != vk: continue
        dot(tg, (1, 0.1, 0.1)); dot(project(vk, anchor_pos(an, X0)[None])[0], (0.2, 0.4, 1), 1); dot(project(vk, anchor_pos(an, X)[None])[0], (0.1, 1, 0.2), 1)
    for (k, n, p, w, nm) in contour_rows(X, vk, V): dot(p, (1, 0.1, 0.1), 3); dot(sil1[k], (0.1, 1, 0.2), 2)
    o = bpy.data.images.new('o', w_, h_); rgba = np.ones((h_, w_, 4), np.float32); rgba[..., :3] = Aimg[::-1]; o.pixels.foreach_set(rgba.ravel()); o.filepath_raw = os.path.abspath(f'{OUT}/_fit_{vk}.png'); o.file_format = 'PNG'; o.save()
np.save(f'{OUT}/recon_head.npy', X)
t = {'head': X[:NS].round(5).tolist(), 'teeth': X0[24049:28295].round(5).tolist(), 'eyeL': X0[28955:29725].round(5).tolist(), 'eyeR': X0[29725:30495].round(5).tolist()}
json.dump(t, open(f'{OUT}/target.json', 'w'))
json.dump({'hist': hist, 'per_anchor_err_ipd_before_after': rep, 'cams': {k: {'R': v[0].tolist(), 's': v[1], 't': v[2].tolist()} for k, v in CAMS.items()}, 'geo': {k: int(v) for k, v in GEO.items()},
           'params': {'K': K, 'sigma': SIG, 'lambda': LAM, 'sym': SYM}}, open(f'{OUT}/recon.json', 'w'), indent=1)
print('RECON_OK', OUT)
