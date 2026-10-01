"""GUARDIAN-3 pass: identity reconstruction in MetaHuman FACE-MODEL space (not surface ops on an old head).
Linearised face model X(c) = B + J (c - c0) (Jacobian from ue_gd3_jacobian.py, all 33845 DNA-order head verts incl. eyeballs / teeth,
so eye placement / IPD is a free model parameter). Gauss-Newton over coefficient deltas against Tier A evidence:
  - MetaHuman tracker curves of the Tier A front photo and the Tier A 3/4 photo (re-solved ~33 deg camera), bound to the mesh
    by barycentric semantic bindings (semantic_j.json),
  - Tier A point picks (pronasale, subnasale, alae, sellion, dorsum, ear tragus / lobe) and silhouette contour picks
    (jaw, chin, menton, far cheek in 3/4; jaw / chin / menton in front - cheek picks in front are on hair: excluded),
  - per-view 2D similarity (absolute photo scale is unknown; it is solved, not imposed),
  - optional Tier B right-profile line (modelling aid, low weight; Tier A dominates),
  - constraints: collar / neck weld fixed (z < 148), eyeballs follow their lid apertures (3D offset eyeball - lid centroid kept),
  - prior: geometric-effect-scaled Tikhonov on coefficient deltas.
usage: blender -b --factory-startup --python gd3_fit.py -- <out prefix> [json overrides]   (writes <prefix>_coefs.json, <prefix>.npy, <prefix>_report.json)"""
import sys, os, json, math, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930'))
from gd_common import topix, VIEWS, ref_curves, basis, head_topology
from gd3_jac_lib import load, SEGS, coef_types
a = sys.argv[sys.argv.index('--')+1:]; OUT = a[0]; O = json.loads(a[1]) if len(a) > 1 else {}
CFG = dict(ridge_pca=0.05, clamp_pca=3.5, free=['pca', 'trans'], lam_g=0.4, ridge=1e-4, max_step_cm=0.6, lam=0.0, w_curve=1.0, w_pick=1.5, w_cont=1.0, w_prof=0.25, w_collar=50.0, w_eye=30.0, iters=6, damp=0.6, base=None, brows=None, w_brow=0.8)
CFG.update(O)
B0, c0, J = load(np.float32); K = J.shape[0]
from id_common import head_base, umeyama
_s, _R, _t = umeyama(B0[:24049].astype(float), head_base()[:24049])   # MHC model space -> project head frame (cameras live here)
B0 = (_s*(B0.astype(float)@_R.T)+_t); J = (_s*np.einsum('kvc,dc->kvd', J, _R.astype(np.float32))).astype(np.float32)
SIM_MODEL = {'s': float(_s), 'R': _R.tolist(), 't': _t.tolist()}
if CFG['base']:   # continue from a previous solution (relinearised Jacobian should be used when the delta gets large)
    cb = np.asarray(json.load(open(CFG['base']))['coefs']); dc_init = cb-c0
else: dc_init = np.zeros(K)
SEM = json.load(open('Saved/Codex/CharacterGuardian_20261001/semantic_j.json'))
PK = json.load(open('Saved/Codex/CharacterIdentity_20260930/ref_picks.json'))
skin = np.arange(*SEGS['skin']); eL = np.arange(*SEGS['eyeL']); eR = np.arange(*SEGS['eyeR'])
def X_of(dc): return B0+np.tensordot(dc, J, 1)
# ---------- fixed vertex definitions on the base head
S0 = B0[:24049]
mid = np.abs(S0[:, 0]+0.24) < 0.35
def argmax_where(m, f): idx = np.nonzero(m)[0]; return int(idx[np.argmax(f(S0[idx]))])
V = {}
V['pronasale'] = argmax_where(mid & (S0[:, 2] > 157) & (S0[:, 2] < 161), lambda P: P[:, 1])
def profile_pts(z0, z1):   # midline anterior profile vertices (max y per 1 mm z bin)
    out = []
    for zz in np.arange(z0, z1, 0.1):
        m = mid & (np.abs(S0[:, 2]-zz) < 0.06)
        if m.any(): i = np.nonzero(m)[0]; out.append(int(i[np.argmax(S0[i, 1])]))
    return out
_zp = S0[argmax_where(mid & (S0[:, 2] > 157) & (S0[:, 2] < 161), lambda P: P[:, 1]), 2]
_pp = profile_pts(_zp-2.2, _zp-0.3); V['subnasale'] = int(min(_pp, key=lambda i: S0[i, 1]))
V['sellion'] = argmax_where(mid & (S0[:, 2] > 161.5) & (S0[:, 2] < 164) & (S0[:, 1] > 11), lambda P: -P[:, 1])
zp, zs = S0[V['pronasale'], 2], S0[V['sellion'], 2]
V['dorsum_mid'] = argmax_where(mid & (np.abs(S0[:, 2]-(zp+zs)/2) < 0.25), lambda P: P[:, 1])
for nm, sg in (('alar_R', -1), ('alar_L', 1), ('alar_near', -1)):
    # ala = lateral extreme of the nose wing: vertices in front of the local cheek surface (y above the cheek plane at that x) near the alar base
    m = (np.abs(S0[:, 2]-158.2) < 0.5) & (np.sign(S0[:, 0]+0.24) == sg) & (np.abs(S0[:, 0]+0.24) < 2.6) & (S0[:, 1] > float(CFG.get('alar_y', 12.7)))
    V[nm] = argmax_where(m, lambda P: np.abs(P[:, 0]+0.24))
for nm, p3 in (('ear_tragus', [-7.3, 3.4, 160.5]), ('ear_lobe', [-7.35, 2.65, 158.3])): V[nm] = int(np.argmin(np.linalg.norm(S0-np.asarray(p3), axis=1)))
# ---------- constraint assembly
def proj_jac(view, P, eps=1e-3):
    p0 = topix(view, P); Jp = np.zeros((len(P), 2, 3))
    for k in range(3):
        d = np.zeros(3); d[k] = eps; Jp[:, :, k] = (topix(view, P+d)-p0)/eps
    return p0, Jp
def bary_rows(bind):   # list of ([v0,v1,v2],[w0,w1,w2]) -> sparse weights
    idx = np.array([b[0] for b in bind]); w = np.array([b[1] for b in bind]); return idx, w
items = []   # (view, kind, idx[n,3], w[n,3], ref[n,2], weight[n], [axis weights])
AXW = {'alar_R': (1.0, 0.0), 'alar_L': (1.0, 0.0), 'alar_near': (1.0, 0.2), 'subnasale': (0.6, 0.25)}
for view in ('front', 'close'):
    R = ref_curves(view)
    for crv, bind in SEM[view].items():
        ref = np.asarray(R[crv], float)
        if len(ref) != len(bind): continue
        ok = [i for i, b in enumerate(bind) if b is not None]; idx, w = bary_rows([bind[i] for i in ok]); ref = ref[ok]
        far = view == 'close' and crv.endswith('_l')        # 3/4 view shows the character's right side; left (far) curves are partly occluded
        items.append((view, 'curve:'+crv, idx, w, ref, np.full(len(idx), CFG['w_curve']*(CFG.get('w_far', 0.25) if far else 1.0))))
    for p in PK[view]['points']:
        nm = p['name']
        if nm.startswith('brow'): continue
        vi = V.get(nm)
        if vi is None: continue
        items.append((view, 'pick:'+nm, np.array([[vi, vi, vi]]), np.array([[1.0, 0, 0]]), np.asarray([p['ref']], float), np.array([CFG['w_pick']*p.get('w', 1.0)]), AXW.get(nm, (1.0, 1.0))))
if CFG['brows']:
    for b in json.load(open(CFG['brows'])):
        items.append((b['view'], 'brow:'+b['name'], np.array([b['idx']]), np.array([b['w']]), np.asarray([b['ref']], float), np.array([CFG['w_brow']])))
CONT = [(view, c) for view in ('front', 'close') for c in PK[view]['contours'] if not (view == 'front' and c['name'].startswith('cheek') and not CFG.get('front_cheeks'))]
def similarity(P, Q, w):   # weighted 2D similarity P->Q: q = s R p + t
    w = w/w.sum(); mp, mq = (w[:, None]*P).sum(0), (w[:, None]*Q).sum(0); A, Bq = P-mp, Q-mq
    C = (w[:, None, None]*(Bq[:, :, None]*A[:, None, :])).sum(0); U, Sg, Vt = np.linalg.svd(C); D = np.eye(2); D[1, 1] = np.sign(np.linalg.det(U@Vt))
    Rm = U@D@Vt; s = (Sg*np.diag(D)).sum()/(w*(A**2).sum(1)).sum(); return s, Rm, mq-s*Rm@mp
CREP = {}
_T, _MI = head_topology(); TS = _T[(_MI == 0) & (_T.max(1) < 24049)]
def vnormals(XS):
    fn = np.cross(XS[TS[:, 1]]-XS[TS[:, 0]], XS[TS[:, 2]]-XS[TS[:, 0]]); N = np.zeros_like(XS)
    for k in range(3): np.add.at(N, TS[:, k], fn)
    N /= np.maximum(np.linalg.norm(N, axis=1), 1e-9)[:, None]
    if np.mean(N[:, 1][XS[:, 1] > 10]) < 0: N = -N        # outward
    return N
def build(dc):
    X = X_of(dc); rows_A = []; rows_r = []; rows_w = []; rep = {}
    # per view: projections of all item points, similarity on curves + picks
    sims = {}
    for view in ('front', 'close'):
        its = [it for it in items if it[0] == view]
        P = np.concatenate([(X[it[2]]*it[3][:, :, None]).sum(1) for it in its]); p0, _ = proj_jac(view, P)
        ref = np.concatenate([it[4] for it in its]); ww = np.concatenate([it[5] for it in its]); sims[view] = similarity(p0, ref, ww)
    for it in items:
        view, kind, idx, w, ref, wt = it[:6]; ax = np.asarray(it[6] if len(it) > 6 else (1.0, 1.0)); s, Rm, t = sims[view]
        P = (X[idx]*w[:, :, None]).sum(1); p0, Jp = proj_jac(view, P); q = (s*(Rm@p0.T)).T+t
        # d point / d c : sum_j w_nj J[:, idx_nj, :]  -> [n, K, 3]
        dP = np.einsum('nj,knjc->nkc', w, J[:, idx, :])
        A = s*np.einsum('ab,nbc,nkc->nak', Rm, Jp, dP)          # [n, 2, K]
        r = ref-q
        rows_A.append(A.reshape(-1, K)); rows_r.append(r.reshape(-1)); rows_w.append((wt[:, None]*ax[None, :]).reshape(-1))
        rep.setdefault(kind.split(':')[0]+'_'+view, []).append(float(np.sqrt((r**2).sum(1).mean())))
        if not kind.startswith('curve'): CREP[view+':'+kind] = [round(float(x), 1) for x in r[0]]
        else: CREP[view+':'+kind] = round(float(np.sqrt((r**2).sum(1).mean())), 1)
    # silhouette contours: outermost skin vertex along n within the band (front-facing region), residual along n
    NS = vnormals(X[:24049])
    for view, c in CONT:
        s, Rm, t = sims[view]; P = X[skin]; p0 = topix(view, P); cam_o = basis(VIEWS[view]['cam'])[0]; vd = P-cam_o; vd /= np.linalg.norm(vd, axis=1)[:, None]; vis = np.abs((NS*vd).sum(1)) < 0.3; q = (s*(Rm@p0.T)).T+t; n = np.asarray(c['n'], float); n /= np.linalg.norm(n); tv = np.array([-n[1], n[0]])
        ref = np.asarray(c['ref'], float); band = (np.abs((q-ref)@tv) < c.get('band', 6)*1.5) & vis
        if c.get('region') == 'far': band &= P[:, 1] > 2.0
        if c.get('region') == 'face': band &= (P[:, 1] > 0.0) & (P[:, 2] > 151.0) & (P[:, 2] < 163.0) & ~((np.abs(P[:, 0]) > 6.4) & (P[:, 1] < 4.5))   # exclude ears
        if c.get('region') == 'jaw': band &= (P[:, 2] > (148.4 if view == "front" else 149.8)) & (P[:, 2] < 156) & (P[:, 1] > (0.5 if view == "front" else 3.0))
        if not band.any(): continue
        bi = np.nonzero(band)[0]; vi = skin[bi[np.argmax(q[bi]@n)]]
        pp, Jp = proj_jac(view, X[[vi]]); qq = s*(Rm@pp[0])+t; res = float((ref-qq)@n)
        A = s*np.einsum('a,ab,bc,kc->k', n, Rm, Jp[0], J[:, vi, :])
        rows_A.append(A[None]); rows_r.append(np.array([res])); rows_w.append(np.array([CFG['w_cont']*c.get('w', 1.0)*(CFG.get('w_cheek', 0.5) if c.get('region') == 'face' else 1.0)]))
        rep.setdefault('contour_'+view, []).append(abs(res)); CREP[view+':'+c['name']] = round(res, 1)
    # Tier B right profile (aid): anterior silhouette max y per z, fitted ortho similarity brow->menton (from blender_gd_profile.py logic)
    if CFG['w_prof'] > 0 and os.path.exists('Saved/Codex/CharacterGuardian3_20261001/refB_profile_p5.json'):
        PR = json.load(open('Saved/Codex/CharacterGuardian3_20261001/refB_profile_p5.json'))   # {'z_cm': [...], 'y_cm': [...]} ref profile already mapped to head cm (brow/menton anchored)
        Sk = X[:24049]
        for zz, yy in zip(PR['z'], PR['y']):
            m = (np.abs(Sk[:, 2]-zz) < 0.12) & (np.abs(Sk[:, 0]+0.24) < 1.5)
            if not m.any(): continue
            bi = np.nonzero(m)[0]; vi = bi[np.argmax(Sk[bi, 1])]; res = (yy-Sk[vi, 1])*28.0
            rows_A.append((J[:, vi, 1]*28.0)[None]); rows_r.append(np.array([res])); rows_w.append(np.array([CFG['w_prof']]))
            rep.setdefault('profile_B', []).append(abs(res)/28.0)
    # collar fixed
    col = np.nonzero(X[:24049, 2] < 148.0)[0][::7]
    for k in range(3): rows_A.append(J[:, col, k].T*28.0); rows_r.append(-(X[col, k]-B0[col, k])*28.0); rows_w.append(np.full(len(col), CFG['w_collar']))
    # eyeballs follow lid apertures: (eyeball centroid - lid curve centroid) kept as in base (3D)
    for e, (crvs, idx) in {'L': (('crv_eyelid_upper_l', 'crv_eyelid_lower_l'), eL), 'R': (('crv_eyelid_upper_r', 'crv_eyelid_lower_r'), eR)}.items():
        bi = np.concatenate([np.asarray([b[0] for b in SEM['front'][c] if b is not None]) for c in crvs]); bw = np.concatenate([np.asarray([b[1] for b in SEM['front'][c] if b is not None]) for c in crvs])
        lidc = lambda XX: ((XX[bi]*bw[:, :, None]).sum(1)).mean(0)
        off0 = B0[idx].mean(0)-lidc(B0); off = X[idx].mean(0)-lidc(X)
        dlid = np.einsum('nj,knjc->kc', bw, J[:, bi, :])/len(bi); deye = J[:, idx, :].mean(1)
        for k in range(3): rows_A.append(((deye-dlid)[:, k]*28.0)[None]); rows_r.append(np.array([(off0-off)[k]*28.0])); rows_w.append(np.array([CFG['w_eye']]))
    A = np.concatenate(rows_A, 0); r = np.concatenate(rows_r); w = np.concatenate(rows_w)
    return A, r, w, {k: round(float(np.mean(v)), 3) for k, v in rep.items()}, sims
GV = np.r_[np.arange(0, 24049, 5), np.arange(*SEGS['eyeL'], 7), np.arange(*SEGS['eyeR'], 7), np.arange(*SEGS['teeth'], 11)]
JG = J[:, GV, :].reshape(K, -1).T.astype(np.float64)            # geometric prior rows (cm)
PG = JG.T@JG/len(GV)*(28.0**2)                                   # mean squared displacement, px^2 units
TY, REG = coef_types(c0); FREE = np.isin(TY, CFG['free']); FI = np.nonzero(FREE)[0]
RID = np.where(TY == 'pca', CFG['ridge_pca'], CFG['ridge'])[FI]
dc = dc_init.copy(); hist = []
for it in range(CFG['iters']):
    A, r, w, rep, sims = build(dc); hist.append(rep); A = A[:, FI]; PGf = PG[np.ix_(FI, FI)]
    W = w[:, None]*A; H = A.T@W+CFG['lam_g']*len(r)*PGf+len(r)*np.diag(RID); g = A.T@(w*r)-CFG['lam_g']*len(r)*(PGf@dc[FI])-len(r)*RID*dc[FI]
    st = np.linalg.solve(H, g); step = np.zeros(K); step[FI] = st; mx = float(np.linalg.norm(np.tensordot(step, J[:, :24049], 1), axis=1).max())
    if mx > CFG['max_step_cm']: step *= CFG['max_step_cm']/mx
    dc = dc+CFG['damp']*step
    pm = TY == 'pca'; lim = np.maximum(CFG['clamp_pca'], np.abs(c0[pm])); c_new = np.clip(c0[pm]+dc[pm], -lim, lim); dc[pm] = c_new-c0[pm]
    print('IT', it, json.dumps(rep), 'step_cm', round(min(mx, CFG['max_step_cm']), 3), 'max|pca|', round(float(np.abs(c0[pm]+dc[pm]).max()), 2))
A, r, w, rep, sims = build(dc); hist.append(rep)
X = X_of(dc); np.save(OUT+'.npy', X.astype(np.float64))
eye = lambda XX: (XX[eL].mean(0), XX[eR].mean(0))
(e0L, e0R), (e1L, e1R) = eye(B0), eye(X)
report = {'cfg': CFG, 'hist': hist, 'ipd_cm': [float(np.linalg.norm(e0L-e0R)), float(np.linalg.norm(e1L-e1R))], 'eye_z': [float((e0L[2]+e0R[2])/2), float((e1L[2]+e1R[2])/2)],
          'max_disp_cm': float(np.linalg.norm(X[:24049]-B0[:24049], axis=1).max()), 'sims': {v: [float(s[0])] for v, s in sims.items()}, 'sims_full': {v: [float(s[0]), np.asarray(s[1]).tolist(), np.asarray(s[2]).tolist()] for v, s in sims.items()}, 'vertices': V, 'model_to_world': SIM_MODEL}
json.dump({'coefs': (c0+dc).tolist()}, open(OUT+'_coefs.json', 'w')); json.dump(report, open(OUT+'_report.json', 'w'), indent=1)
print('CONTOURS', json.dumps(CREP)); print('FIT_DONE', json.dumps({k: report[k] for k in ('ipd_cm', 'eye_z', 'max_disp_cm', 'sims')}), json.dumps(hist[-1]))
