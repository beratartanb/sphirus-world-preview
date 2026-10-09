"""GD13 Identity Master: MULTI-VIEW ANATOMICAL FIT of a DNA-order head to the user's 2026-10-09 6-view reference sheet.
Shape space = the MetaHuman face model (22 blended regions: 1198 identity PCA modes + region translation / scale; Jacobian from
CharacterGuardian3 ue_gd3_jacobian, moved into the project frame) applied as a displacement on the start head:
    X(dc) = X0 + sum_k dc_k J_k        (whole-face coherent anatomical modes, not local brushes)
Evidence per reference panel (head camera per panel, re-solved between shape steps = bundle adjustment):
  - MetaHuman tracker curves (eyelids, lips, philtrum, nasolabial) on the panel vs the same curves bound to the mesh (semantic_j),
    point-to-curve (normal) residuals + canthus / mouth-corner point residuals
  - silhouettes: automatic skin-key contours (profile front edge + under-chin, far 3/4 cheek / chin contour, front cheek: one-sided),
    manual contours (jaw borders, alar edges, nose tip, ear anchors); the model contour = outermost projected vertex of a material region
  - brow centre lines (material brow points of the start head, same as the GD13 diagnostic brow band) point-to-curve
  - landmark points (subnasale)
Priors: ridge on the geometric size of every mode (cm), neck (z < 147) / cranium (hair-covered) / ears held, step trust region.
Post: eyeballs made rigid (mean translation), optional left/right symmetrisation of the displacement (mirror map).
usage: blender -b --factory-startup --python gd13_fit.py -- <start.npy> <cams.json> <out prefix> [json overrides]"""
import sys, os, json, math, glob, time, numpy as np
sys.path.insert(0, os.path.dirname(__file__)); from gd13_common import *
from id_common import head_base, umeyama
a = sys.argv[sys.argv.index('--')+1:]; X0 = np.load(a[0]).astype(float); CAMS = json.load(open(a[1])); OUTP = a[2]
CFG = dict(lam=0.15, mu=4.0, iters=8, cam_iters=1, max_step=0.45, sym=1.0, w_curve=1.0, w_cont=1.0, w_brow=1.0, w_pt=1.0, w_neck=8.0, w_cran=2.0, w_ear=1.0,
           band=2.0, types=['pca', 'trans', 'scale'], views=VIEWS, clamp_pca=3.5, auto=True, solve_cams=True, front_cheek_two=0.3, lip_w=1.0, eye_w=1.5, nl_w=0.25)
CFG.update(json.loads(a[3]) if len(a) > 3 else {})
sys.stdout.reconfigure(line_buffering=True)
T0 = time.time(); MM = mirror_map(X0); TR = ref_tracks(); PK = json.load(open(os.path.join(GD, 'data/picks_manual.json'))); AUTO = json.load(open(os.path.join(GD, 'data/contours_auto.json')))
# ---------------- face-model Jacobian -> project frame, selected coefficient types
JD = os.path.join(ROOT, 'Saved/Codex/CharacterGuardian3_20261001/jac')
B0 = np.fromfile(JD+'/base.f32', np.float32).reshape(-1, 3).astype(float); c0 = np.asarray(json.load(open(JD+'/coef.json')))
from gd3_jac_lib import coef_types
TYP, REG = coef_types(c0)
if CFG.get('lead'):   # leading (largest-variance) PCA modes per region + region translation / scale, excluded regions frozen
    keep = []
    for r, (i, m) in enumerate(REG):
        if r in CFG.get('freeze_regions', []): continue
        nl = CFG.get('lead_region', {}).get(str(r), CFG['lead']); keep += list(range(i+9, i+9+min(nl, m)))
        if r not in CFG.get('no_rigid', []): keep += ([i+4] if 'scale' in CFG['types'] else [])+(list(range(i+5, i+8)) if 'trans' in CFG['types'] else [])
    SEL = np.array(sorted(keep))
else: SEL = np.nonzero(np.isin(TYP, CFG['types']))[0]
_s, _R, _t = umeyama(B0[:NS], head_base()[:NS])
Js = []; off = 0
for f in sorted(glob.glob(JD+'/J_*.f32')):
    Jc = np.fromfile(f, np.float32).reshape(-1, NH, 3); ks = np.arange(off, off+len(Jc)); m = np.isin(ks, SEL)
    if m.any(): Js.append((_s*np.einsum('kvc,dc->kvd', Jc[m], _R.astype(np.float32))).astype(np.float32))
    off += len(Jc); del Jc
J = np.concatenate(Js, 0); del Js; K = len(J)
_n = np.sqrt((J.astype(np.float64)**2).sum(-1)); SC = np.sqrt((_n[:, :NS]**2).mean(-1)+0.3*_n.max(1)**2); SC[SC < 1e-6] = 1e-6; del _n   # cm: skin RMS + peak (any part) displacement per unit coefficient
JF = J.reshape(K, -1).astype(np.float64)   # flat for fast dense products
print('JAC', J.shape, 'types', {t: int((TYP[SEL] == t).sum()) for t in set(TYP[SEL])}, 'load %.1fs' % (time.time()-T0))
# ---------------- material masks / landmarks on the start head
S0 = X0[:NS]; AX = np.abs(S0[:, 0]-MX)
def vnormals(X):
    TRI = np.asarray(pkg()['head']['triangles']); TRI = TRI[(TRI < NS).all(1)]; P = X[:NS]; n = np.cross(P[TRI[:, 1]]-P[TRI[:, 0]], P[TRI[:, 2]]-P[TRI[:, 0]])
    N = np.zeros((NS, 3)); [np.add.at(N, TRI[:, k], n) for k in range(3)]; return -N/np.maximum(np.linalg.norm(N, axis=1), 1e-12)[:, None]   # DNA winding is inward: flip to outward
N0 = vnormals(X0)
_T = np.asarray(pkg()['head']['triangles']); _T = _T[(_T < NS).all(1)]; EDG = np.unique(np.sort(np.r_[_T[:, [0, 1]], _T[:, [1, 2]], _T[:, [2, 0]]], 1), axis=0)
def silhouette(X, c):
    """contour-generator vertices of the skin for camera c: front-facing endpoints of edges whose endpoints face opposite ways"""
    N = vnormals(X); R = cam_R(c); cpos = CH-c['D']*R[2]; s = ((cpos-X[:NS])*N).sum(1); e = EDG[(s[EDG[:, 0]] > 0) != (s[EDG[:, 1]] > 0)]
    m = np.zeros(NS, bool); m[np.where(s[e[:, 0]] > 0, e[:, 0], e[:, 1])] = True; return m
EAR = (AX > 6.2) & (S0[:, 1] < 4.6) & (S0[:, 2] > 154) & (S0[:, 2] < 168)
EARP = EAR & (AX > 7.0) & (S0[:, 2] < 167.0)   # protruding ear (helix / lobe / concha rim), no scalp
REGION = {'ear_R': np.nonzero(EARP & (S0[:, 0] < MX))[0], 'ear_L': np.nonzero(EARP & (S0[:, 0] > MX))[0],
          'face_noear': np.nonzero(~EAR & (S0[:, 2] > 147.0) & (S0[:, 1] > -1.5))[0],
          'face_nodown': np.nonzero(~EAR & (N0[:, 2] > -0.5) & (S0[:, 2] > 151.0) & (S0[:, 1] > -1.5))[0],
          'face_neck': np.nonzero(~EAR & (S0[:, 2] > 146.0) & (S0[:, 1] > 3.0))[0],
          'face_front': np.nonzero(~EAR & (S0[:, 1] > 5.0) & (S0[:, 2] > 150.0))[0],
          'jaw_zone': np.nonzero(~EAR & (S0[:, 1] > -0.5) & (S0[:, 2] > 150.8) & (S0[:, 2] < 156.5))[0],
          'submental': np.nonzero(~EAR & (S0[:, 1] > 5.0) & (S0[:, 2] > 150.2) & (S0[:, 2] < 155.0))[0],
          'nose': np.nonzero((AX < 2.4) & (S0[:, 1] > 12.9) & (S0[:, 2] > 157.0) & (S0[:, 2] < 163.5))[0]}
mid = AX < 0.35
def argmax_where(m, f): i = np.nonzero(m)[0]; return int(i[np.argmax(f(S0[i]))])
LM = {}; LM['pronasale'] = argmax_where(mid & (S0[:, 2] > 157) & (S0[:, 2] < 161), lambda P: P[:, 1])
zp = S0[LM['pronasale'], 2]; cand = [int(np.nonzero(mid & (np.abs(S0[:, 2]-zz) < 0.06))[0][np.argmax(S0[mid & (np.abs(S0[:, 2]-zz) < 0.06), 1])]) for zz in np.arange(zp-2.2, zp-0.3, 0.1) if (mid & (np.abs(S0[:, 2]-zz) < 0.06)).any()]
LM['subnasale'] = int(min(cand, key=lambda i: S0[i, 1]))
BROW = {}
for side, sg in (('R', -1), ('L', 1)):
    idx = []
    for ax in np.arange(1.4, 5.01, 0.2):
        zc = 164.05+0.35*np.exp(-((ax-3.3)/1.5)**2)-0.35*np.clip((ax-4.5)/1.0, 0, 1)**1.5
        m = (np.abs(S0[:, 0]-(MX+sg*ax)) < 0.18) & (np.abs(S0[:, 2]-zc) < 0.25) & (S0[:, 1] > 6.0)
        if m.any(): idx.append(argmax_where(m, lambda P: P[:, 1]))
    BROW[side] = np.array(idx)
JAWALL = jaw_line(X0, N0)
STAY = {'neck': np.nonzero(S0[:, 2] < 147.0)[0][::7], 'cran': np.nonzero(((S0[:, 2] > 167.5) & (S0[:, 1] < 8.5)) | ((S0[:, 1] < -1.5) & (S0[:, 2] > 150)))[0][::5],
        'ear': np.nonzero(EAR)[0][::6]}
print('REGIONS', {k: len(v) for k, v in REGION.items()}, 'JAW', len(JAWALL), 'LM', LM, 'BROW', {k: len(v) for k, v in BROW.items()}, 'STAY', {k: len(v) for k, v in STAY.items()})
# ---------------- reference constraint sets
def poly_normals(P, hint):
    P = np.asarray(P, float); n = len(P)
    if n == 1: N = np.array([hint], float)
    else:
        T = np.gradient(P, axis=0); T /= np.maximum(np.linalg.norm(T, axis=1), 1e-9)[:, None]; N = np.stack([T[:, 1], -T[:, 0]], -1)
        N *= np.sign((N@np.asarray(hint, float)))[:, None]+(N@np.asarray(hint, float) == 0)[:, None]
    return N/np.linalg.norm(N, axis=1)[:, None]
def clean_rows(P, win=21, tol=2.5, drop=()):
    P = np.asarray(P, float); keep = np.ones(len(P), bool)
    for lo, hi in drop: keep &= ~((P[:, 1] >= lo) & (P[:, 1] <= hi))
    P = P[keep]; med = np.array([np.median(P[max(0, i-win//2):i+win//2+1, 0]) for i in range(len(P))]); return P[np.abs(P[:, 0]-med) < tol]
CONT = {v: [] for v in VIEWS}
def add_cont(v, name, region, P, hint, mode, w, sub=1, axis=False):
    """axis=True: contour extracted per image row / column -> the model point is selected along the fixed axis 'hint' (outermost in that row),
    the residual is the axis distance times |cos| of the local contour normal (= point-to-line distance, stable in concave regions)"""
    P = np.asarray(P, float)
    if len(P) == 0: return
    N = poly_normals(P, hint)
    if axis: h = np.asarray(hint, float)/np.linalg.norm(hint); cs = np.clip(np.abs(N@h), 0.2, 1.0); P, cs = P[::sub], cs[::sub]; N = np.tile(h, (len(P), 1))
    else: P, N, cs = P[::sub], N[::sub], np.ones(len(P[::sub]))
    CONT[v].append(dict(name=name, region=region, P=P, N=N, CS=cs, mode=mode, w=w))
for v in VIEWS:
    for c in PK.get(v, {}).get('contours', []): add_cont(v, c['name'], c['region'], c['pts'], c['nrm'], c['mode'], c['w'])
if CFG['auto']:
    A = AUTO
    add_cont('prof_faceL', 'prof_front', 'face_front', clean_rows(A['prof_faceL']['prof_front'], 9, 3.0, [(171, 183)]), [-1, 0], 'two', 1.0, 2, True)
    pu = np.asarray(A['prof_faceL']['prof_under'], float); pu = pu[pu[:, 0] <= CFG.get('under_xmax', 130)]; add_cont('prof_faceL', 'prof_under', 'submental', pu, [0, 1], 'two', 0.4, 2, True)
    add_cont('q3_faceR', 'far_R', 'face_noear', clean_rows(A['q3_faceR']['far_R'], 21, 2.5, [(0, 240), (304, 323)]), [1, 0], 'two', 0.8, 2, True)
    add_cont('q3_faceL', 'far_L', 'face_noear', clean_rows(A['q3_faceL']['far_L'], 21, 2.5, [(0, 240), (316, 349)]), [-1, 0], 'two', 0.8, 2, True)
    for nm, hint in (('cheek_imgL', [-1, 0]), ('cheek_imgR', [1, 0])):
        P = clean_rows(A['front'][nm], 15, 3.0); add_cont('front', nm+'_one', 'face_noear', P[P[:, 1] < 295], hint, 'one', 0.5, 2, True)
        add_cont('front', nm+'_two', 'face_noear', P[P[:, 1] >= 295], hint, 'two', CFG['front_cheek_two'], 2, True)
CURVES = {'front': {'eyelid': CFG['eye_w'], 'lip_upper_outer': CFG['lip_w'], 'lip_lower_outer': CFG['lip_w'], 'lip_upper_inner': 0.6*CFG['lip_w'], 'lip_lower_inner': 0.6*CFG['lip_w'], 'philtrum': 0.3, 'nasolabial': CFG['nl_w']}}
def curve_w(v, k):
    side = k[-1]; near = {'q3_faceR': 'r', 'q3_faceL': 'l', 'prof_faceL': 'l'}.get(v)
    base = next((w for t, w in CURVES['front'].items() if t in k), 0.0)
    if v == 'front': return base
    if v == 'prof_faceL':
        if side != near: return 0.0
        return base if 'eyelid' in k else (0.5*base if 'outer' in k else (0.3*base if 'nasolabial' in k else 0.0))
    if side != near: return 0.35*base if ('eyelid' in k or 'outer' in k) else 0.0
    return base
BIND = {v: bindings(v, MM) for v in VIEWS}
# ---------------- residual assembly (linearised at X): rows = (vertex ids, vertex weights, 2D direction in px -> scalar, target), weight
DUMP = None
def build(X, cams, need_rows=True):
    rows = []; stats = {}
    for v in CFG['views']:
        c = cams[v]; ppc = c['f']/c['D']; st = stats.setdefault(v, {})
        def add(ids, ws, d2, r, w, grp, pref=None):   # r = current signed residual in px along d2 (unit), w weight, pref = reference image point
            ids = np.asarray(ids); ws = np.asarray(ws, float); d2 = np.asarray(d2, float)
            if pref is None: pref = project(c, (ws@X[ids])[None])[0]-r*d2
            rows.append((ids, ws, d2, float(r)/ppc, float(w), v, np.asarray(pref, float))); st.setdefault(grp, []).append(float(r)/ppc*10)
        # tracker curves
        for ck, rp in TR[v].items():
            k = ck[4:]; w = curve_w(v, k)*CFG['w_curve']
            if w <= 0 or ck not in BIND[v]: continue
            B = BIND[v][ck]; ok = [i for i, e in enumerate(B) if e is not None]
            if not ok: continue
            P3 = np.array([B[i][1]@X[B[i][0]] for i in ok]); q = project(c, P3)
            seg_a, seg_b = rp[:-1], rp[1:]
            for j, i in enumerate(ok):
                d = seg_b-seg_a; L2 = (d**2).sum(1)+1e-9; t = np.clip(((q[j]-seg_a)*d).sum(1)/L2, 0, 1); F = seg_a+t[:, None]*d; s = np.argmin(((F-q[j])**2).sum(1))
                n = np.array([-d[s, 1], d[s, 0]]); n /= np.linalg.norm(n)+1e-12; add(B[i][0], B[i][1], n, n@(q[j]-F[s]), w, 'curve_'+k.rsplit('_', 1)[0])
            if ('eyelid_upper' in k or 'lip_upper_outer' in k) and v == 'front':
                for i, ri in ((ok[0], 0), (ok[-1], -1)):
                    if i in (0, len(B)-1):
                        qq = project(c, (B[i][1]@X[B[i][0]])[None])[0]
                        for d2 in ((1, 0), (0, 1)): add(B[i][0], B[i][1], d2, np.dot(d2, qq-rp[ri]), w, 'corner', rp[ri])
        # contours (silhouette = outermost vertex of the material region inside a tangent band)
        SIL = None
        for C in CONT[v]:
            ids = REGION[C['region']]
            if C['mode'] == 'sil':
                if SIL is None: SIL = silhouette(X, c)
                ids = ids[SIL[ids]]
            Q = project(c, X[ids])
            for p, n, cs in zip(C['P'], C['N'], C['CS']):
                t = np.array([n[1], -n[0]]); m = np.abs((Q-p)@t) < CFG['band']*(1.5 if C['mode'] == 'sil' else 1)
                if not m.any(): continue
                dd = (Q[m]-p)@n; j = np.nonzero(m)[0][np.argmin(np.abs(dd)) if C['mode'] == 'sil' else np.argmax(dd)]; r = (Q[j]-p)@n*cs; n = n*cs
                if DUMP is not None: DUMP.setdefault(v, []).append([C['name'], p.tolist(), Q[j].tolist(), float(r), int(ids[j]), X[ids[j]].round(2).tolist()])
                if C['mode'] == 'one' and r > 0: st.setdefault('cont_'+C['name'], []).append(0.0); continue
                add([ids[j]], [1.0], n, r, C['w']*CFG['w_cont'], 'cont_'+C['name'], p)
        # brow centre lines
        for cv in PK.get(v, {}).get('curves', []):
            MV = JAWALL if cv.get('jaw') else BROW[cv['brow']]; tag = 'jaw' if cv.get('jaw') else 'brow_'+cv['brow']
            rp = np.asarray(cv['pts'], float); q = project(c, X[MV]); seg_a, seg_b = rp[:-1], rp[1:]; d = seg_b-seg_a; L2 = (d**2).sum(1)
            for j, vid in enumerate(MV):
                t = ((q[j]-seg_a)*d).sum(1)/L2; s = np.argmin(np.where((t >= 0) & (t <= 1), ((seg_a+np.clip(t, 0, 1)[:, None]*d-q[j])**2).sum(1), 1e9))
                if not (0 <= t[s] <= 1): continue
                F = seg_a[s]+t[s]*d[s]; n = np.array([-d[s, 1], d[s, 0]]); n /= np.linalg.norm(n); add([vid], [1.0], n, n@(q[j]-F), cv['w']*CFG['w_brow'], tag, F)
        for pt in PK.get(v, {}).get('points', []):
            vid = LM[pt['lm']]; qq = project(c, X[vid][None])[0]
            for d2 in ((1, 0), (0, 1)): add([vid], [1.0], d2, np.dot(d2, qq-np.asarray(pt['p'])), pt['w']*CFG['w_pt'], 'pt_'+pt['name'], pt['p'])
    return rows, {v: {g: (len(x), float(np.sqrt(np.mean(np.square(x))))) for g, x in s.items()} for v, s in stats.items()}
def summarize(stats):
    out = {}
    for v, s in stats.items():
        allr = [r for g, (n, r) in s.items()]; out[v] = {g: '%d:%.2fmm' % (n, r) for g, (n, r) in sorted(s.items())}
    return out
def total_err(X, cams):
    rows, _ = build(X, cams); return sum(w*r*r for _, _, _, r, w, _, _ in rows)
# ---------------- camera refinement (6 params per view, numeric GN on the same residuals, shape fixed)
def refine_cam(X, cams, v):
    c = dict(cams[v]); keep = CFG['views']; CFG['views'] = [v]
    def rv(p): cc = dict(c); cc['rvec'] = list(p[:3]); cc['f'], cc['cx'], cc['cy'] = p[3], p[4], p[5]; return cc
    rows0, _ = build(X, {v: c}); P3 = np.array([ws@X[ids] for ids, ws, _, _, _, _, _ in rows0]); D2 = np.array([r[2] for r in rows0]); PR = np.array([r[6] for r in rows0]); WW = np.sqrt([r[4] for r in rows0])
    def res(p):   # fixed correspondences (ICP step), px
        cc = rv(p); return WW*((project(cc, P3)-PR)*D2).sum(1)
    p = np.r_[c['rvec'], c['f'], c['cx'], c['cy']]; lam = 1e-2
    for it in range(6):
        r0 = res(p); Jm = np.stack([(res(p+dp)-r0)/dp[j] for j, dp in enumerate(np.diag([2e-4, 2e-4, 2e-4, 2.0, 0.2, 0.2]))], 1)
        H = Jm.T@Jm; step = -np.linalg.solve(H+lam*np.diag(np.diag(H))+1e-9*np.eye(6), Jm.T@r0); pn = p+step
        if (res(pn)**2).sum() < (res(p)**2).sum(): p = pn; lam *= 0.5
        else: lam *= 5
    CFG['views'] = keep; return rv(p)
def cg_solve(A, W, b, D, dc, iters=600, tol=1e-7):
    """minimise sum W (A x - b)^2 + sum D (dc + x)^2 by Jacobi-preconditioned CG with mat-vec products only (Blender numpy has no fast BLAS)"""
    At = np.ascontiguousarray(A.T); g = At@(W*b)-D*dc; M = (At**2)@W+D
    def Hv(v): return At@(W*(A@v))+D*v
    x = np.zeros_like(g); r = g.copy(); z = r/M; p = z.copy(); rz = r@z; n0 = np.sqrt(g@g)+1e-30
    for k in range(iters):
        Hp = Hv(p); al = rz/(p@Hp); x += al*p; r -= al*Hp
        if np.sqrt(r@r) < tol*n0: break
        z = r/M; rzn = r@z; p = z+(rzn/rz)*p; rz = rzn
    print('  CG', k, 'rel %.2e' % (np.sqrt(r@r)/n0)); return x
def nearest_skin(X, cache=os.path.join(GD, 'data/nearest_skin.npy')):
    if os.path.exists(cache): return np.load(cache)
    NN = np.zeros(NH, int); NN[:NS] = np.arange(NS); P = X[:NS]
    for s0 in range(NS, NH, 300):
        Q = X[s0:s0+300]; NN[s0:s0+300] = np.argmin(((Q[:, None, :]-P[None])**2).sum(-1), 1)
    np.save(cache, NN); return NN
# ---------------- shape iterations
dc = np.zeros(K); X = X0.copy(); cams = {v: dict(CAMS[v]) for v in VIEWS}
for v in cams: cams[v]['rvec'] = list(cams[v]['rvec'])
DUMP = {} if CFG.get('dump') else None
print('BUILD0', '%.0fs' % (time.time()-T0)); _, st0 = build(X, cams); print('START', json.dumps(summarize(st0))); hist = []
if DUMP is not None: json.dump(DUMP, open(OUTP+'_dump.json', 'w')); DUMP = None
if CFG.get('dump_only'): sys.exit(0)
for it in range(CFG['iters']):
    if CFG['solve_cams'] and it > 0:
        for v in CFG['views']: cams[v] = refine_cam(X, cams, v)
    t0 = time.time(); rows, st = build(X, cams); tb = time.time()
    vids = np.unique(np.concatenate([r[0] for r in rows]+[STAY['neck'], STAY['cran'], STAY['ear']])); pos = {int(x): i for i, x in enumerate(vids)}; JV = J[:, vids, :].astype(np.float64)   # K x V x 3
    R_ = len(rows); PID = np.zeros((R_, 3), int); WS = np.zeros((R_, 3)); G = np.zeros((R_, 3)); b = np.zeros(R_); W = np.zeros(R_)
    for i, (ids, ws, d2, r, w, v, _) in enumerate(rows):
        c = cams[v]; ppc = c['f']/c['D']; P = (ws@X[ids])[None]; Jp = proj_jac(c, P)[0]/ppc; G[i] = Jp.T@d2   # cm image shift per cm 3D
        PID[i, :len(ids)] = [pos[int(x)] for x in ids]; WS[i, :len(ids)] = ws; b[i] = -r; W[i] = w
    A = sum(np.einsum('krd,rd->rk', JV[:, PID[:, j], :], G*WS[:, j:j+1]) for j in range(3))
    # stay rows (3D displacement from X0 -> 0)
    SA, Sb, SW = [], [], []
    for nm, wv in (('neck', CFG['w_neck']), ('cran', CFG['w_cran']), ('ear', CFG['w_ear'])):
        pp = np.array([pos[int(x)] for x in STAY[nm]]); SA.append(JV[:, pp, :].transpose(1, 2, 0).reshape(-1, K)); Sb.append(-(X[STAY[nm]]-X0[STAY[nm]]).ravel()); SW.append(np.full(3*len(pp), wv/len(pp)*60))
    A = np.vstack([A]+SA); b = np.r_[b, np.concatenate(Sb)]; W = np.r_[W, np.concatenate(SW)]
    t1 = time.time(); ddc = cg_solve(A, W, b, CFG['lam']*SC**2+CFG['mu']*(TYP[SEL] == 'pca'), dc)
    dX = (ddc@JF).reshape(NH, 3); mx = np.abs(np.linalg.norm(dX[:NS], axis=1)).max(); sc = min(1.0, CFG['max_step']/max(mx, 1e-9))
    if CFG.get('debug'):
        nn = np.linalg.norm(dX[:NS], axis=1); iv = int(np.argmax(nn)); print('  DBG maxvert', iv, X[iv].round(2), dX[iv].round(2), 'p99 %.2f p90 %.2f' % (np.percentile(nn, 99), np.percentile(nn, 90)))
        o = np.argsort(-SC*np.abs(ddc))[:8]; print('  DBG modes', [(int(SEL[i]), str(TYP[SEL][i]), round(float(ddc[i]), 2), round(float(SC[i]), 3)) for i in o])
        lin = A@ddc; print('  DBG data pred: |b| %.3f |b-A x| %.3f ; reg %.3f' % (np.sqrt((W*b*b).sum()), np.sqrt((W*(b-lin)**2).sum()), np.sqrt((CFG['lam']*SC**2*(dc+ddc)**2).sum())))
        nr = len(rows); print('  DBG rows', nr, 'stay', len(b)-nr, 'data part |b-Ax| %.3f' % np.sqrt((W[:nr]*(b[:nr]-lin[:nr])**2).sum()), 'stay part %.3f' % np.sqrt((W[nr:]*(b[nr:]-lin[nr:])**2).sum()))
    dc += sc*ddc; pc = TYP[SEL] == 'pca'; dc[pc] = np.clip(c0[SEL][pc]+dc[pc], -CFG['clamp_pca'], CFG['clamp_pca'])-c0[SEL][pc]
    X = X0+(dc@JF).reshape(NH, 3); t2 = time.time()
    _, st1 = build(X, cams); E = sum(n*r*r for s in st1.values() for (n, r) in s.values())
    hist.append(dict(it=it, step_scale=sc, max_step_cm=float(mx*sc), E=E)); print('IT', it, 'scale %.2f maxstep %.2fcm E %.1f' % (sc, mx*sc, E), 'build %.0fs asm %.0fs solve %.0fs post %.0fs total %.0fs' % (tb-t0, t1-tb, t2-t1, time.time()-t2, time.time()-T0))
# ---------------- post: optional low-pass of the skin displacement (broad forms only), rigid eyeballs, symmetrise
D = X-X0
if CFG.get('lowpass', 0) > 0:
    nb = [[] for _ in range(NS)]
    for i0, i1 in EDG: nb[i0].append(i1); nb[i1].append(i0)
    deg = np.array([len(x) for x in nb], float); I0 = np.repeat(np.arange(NS), [len(x) for x in nb]); I1 = np.concatenate([np.array(x, int) for x in nb])
    Ds = D[:NS].copy(); fix = np.zeros(NS, bool); fix[STAY['neck']] = True
    for _ in range(int(CFG['lowpass'])):
        avg = np.zeros((NS, 3)); np.add.at(avg, I0, Ds[I1]); avg /= np.maximum(deg, 1)[:, None]; Ds = Ds+0.5*(avg-Ds)
    hf = D[:NS]-Ds; print('LOWPASS', CFG['lowpass'], 'removed detail rms %.2f mm max %.2f mm' % (10*np.sqrt((hf**2).sum(1).mean()), 10*np.linalg.norm(hf, axis=1).max()))
    # non-skin parts (teeth, saliva, eyeballs, eye shell, lashes, eye edge, cartilage) follow their nearest skin vertex (start head);
    # eyeballs move rigidly with the mean of their nearest lid / canthus skin vertices
    D[:NS] = Ds; NN = nearest_skin(X0)
    for k in ('teeth', 'saliva', 'eyeshell', 'lashes', 'eyeEdge', 'cartilage'): i0, i1 = SEG[k]; D[i0:i1] = Ds[NN[i0:i1]]
    for k in ('eyeL', 'eyeR'): i0, i1 = SEG[k]; D[i0:i1] = Ds[np.unique(NN[i0:i1])].mean(0)
X = X0+D
D = X-X0
for k in ('eyeL', 'eyeR'): i0, i1 = SEG[k]; D[i0:i1] = D[i0:i1].mean(0)
if CFG['sym'] > 0:
    Dm = D[MM].copy(); Dm[:, 0] *= -1; D = (1-0.5*CFG['sym'])*D+0.5*CFG['sym']*Dm
    for k in ('eyeL', 'eyeR'): i0, i1 = SEG[k]; D[i0:i1] = D[i0:i1].mean(0)
X = X0+D
for v in CFG['views']: cams[v] = refine_cam(X, cams, v)
_, stF = build(X, cams); print('FINAL', json.dumps(summarize(stF)))
if CFG.get('dump'): DUMP = {}; build(X, cams); json.dump(DUMP, open(OUTP+'_dumpF.json', 'w')); DUMP = None
np.save(OUTP+'.npy', X); save_cams(cams, OUTP+'_cams.json')
dn = np.linalg.norm(D[:NS], axis=1)
rep = dict(cfg=CFG, start=summarize(st0), final=summarize(stF), hist=hist, disp_cm=dict(max=float(dn.max()), mean_moved=float(dn[dn > 0.01].mean()), n_moved_1mm=int((dn > 0.1).sum())),
           dc_rms=float(np.sqrt(np.mean(dc**2))), top_modes=[(int(SEL[i]), str(TYP[SEL][i]), float(dc[i]), float(SC[i]*abs(dc[i]))) for i in np.argsort(-SC*np.abs(dc))[:25]])
json.dump(rep, open(OUTP+'_report.json', 'w'), indent=1); np.save(OUTP+'_dc.npy', dc); print('FIT_OK', OUTP, json.dumps(rep['disp_cm']), '%.0fs' % (time.time()-T0))
