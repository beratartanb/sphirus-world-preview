"""GD40 anatomical body pass (user, 2026-10-12, after GD39 'stayed too close to the low-quality body'): body FORM, posture, muscles and tissue
after the athletic base-mesh reference; overall proportions / slimness / look after the Guardian concept. Skeleton, height and proportions
unchanged (morph only). PROCEDURAL muscle atlas (no manual brush control), one always-on morph GD40_Body on top of the current neutral
(accepted_b2 + BR_Neutral v6 + LK_Neutral). Bind space UE cm: x = subject's left, y = front, z = up, midline x = -0.23.
Each muscle / groove is a surface primitive: centre snapped to the body surface (extreme vertex along the facing direction near the guess),
local frame (facing n0, fibre u, across v), weight exp(-(r^p)) with r^2 = (d.u/a)^2 + (d.v/b)^2 (p = 3: flat-topped belly with a defined
edge; p = 2 for grooves / tissue), gated by the vertex normal facing n0, displacement h along the vertex normal. Left-side definitions are
mirrored. Regions: rectus abdominis columns + intersections + linea alba + semilunar lines, external obliques, inguinal line, serratus,
upper pectoral; erectors, spinal groove, lumbar arch, lats, scapula (infraspinatus, medial border), lower trapezius, sacral dimples; gluteus
maximus / medius, infragluteal fold, trochanteric hollow, TFL; rectus femoris, vastus lateralis / medialis, sartorius groove, adductors,
hamstrings + groove, IT-band groove; patella, peripatellar hollows, knee sides; gastrocnemius heads + groove, soleus, Achilles, tibialis
anterior; deltoid (lateral / anterior / posterior), biceps, triceps, forearm extensors; tissue: lower-belly flatten, waist sides; inframammary
shelf softened (breast size kept). Guard: neck seam band (z > 138.5 fades) + 1.5 cm around the 92 head/body weld pairs, hands, feet.
Writes morph_gd40_body_lod{0..3}.json ({'Body': {'GD40_Body': {idx: [dx,dy,dz]}}}), gd40_body_delta_lod0.npy, gd40_body_report.json.
usage: blender -b --factory-startup --python gd40_body_anatomy.py -- <sculpt_package_v6.json.gz> <lk_lod0.json> <lod_dir> <out_dir> [K=1.0]"""
import sys, json, gzip, math, os
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.kdtree import KDTree
a_ = sys.argv[sys.argv.index('--')+1:]; PKG, LKJ, LODD, OUT = a_[:4]; K = float(a_[4]) if len(a_) > 4 else 1.0
os.makedirs(OUT, exist_ok=True); E = lambda k, d: float(os.environ.get(k, d))
P = json.loads(gzip.open(PKG, 'rb').read()); NB = P['NB']; X = np.asarray(P['br_neutral'], np.float64)[:NB].copy(); T = np.asarray(P['body']['triangles'], np.int64)
for k_, v in json.load(open(LKJ))['Body']['LK_Neutral'].items(): X[int(k_)] += v
MX = -0.23; XR = X.copy(); XR[:, 0] -= MX; x, y, z = XR[:, 0], XR[:, 1], XR[:, 2]
W8 = P['weights']
def chain(pre): return np.asarray([sum(w for b, w in W8[v].items() if b.startswith(pre)) for v in range(NB)])
arm = chain(('upperarm', 'lowerarm', 'hand', 'clavicle')); leg = chain(('thigh', 'calf', 'foot')); hand = chain(('hand', 'index', 'middle', 'ring', 'pinky', 'thumb'))
fnm = -np.cross(X[T[:, 1]]-X[T[:, 0]], X[T[:, 2]]-X[T[:, 0]]); N = np.zeros_like(X)
for k in range(3): np.add.at(N, T[:, k], fnm)
N /= np.maximum(np.linalg.norm(N, axis=1), 1e-9)[:, None]
def ss(v): v = np.clip(v, 0, 1); return v*v*(3-2*v)
def nrm(v): v = np.asarray(v, float); return v/max(np.linalg.norm(v), 1e-9)
B = P['skeleton']['Body']['bind']; bt = lambda b: np.asarray(B[b]['translation'], float)-np.array([MX, 0, 0])
TORSO = (arm < 0.3)*(leg < 0.5); LEGM = (leg > 0.4)*(arm < 0.2); ARMM = (arm > 0.4)*(hand < 0.3)
D = np.zeros_like(X); rep = {}
def snap(c, face, mask, rs=2.0):
    """surface point: among masked vertices within rs (cm) of the line through c along face, the one furthest along face"""
    f = nrm(face); d = XR-c; perp = d-np.outer(d@f, f); cand = np.nonzero(mask & (np.linalg.norm(perp, axis=1) < rs))[0]
    if not len(cand): cand = np.nonzero(mask)[0][np.argsort(np.linalg.norm(XR[mask]-c, axis=1))[:1]]
    return XR[cand[np.argmax(XR[cand]@f)]]
def prim(name, c, face, fiber, a, b, h, p=3.0, mask=None, gate=0.15, mirror=True, depth=5.0, vec=None):
    """add one surface primitive (and its mirror for left-side definitions); returns peak |displacement| mm"""
    mask = TORSO if mask is None else mask; peak = 0.0
    for sgn in ((1, -1) if mirror else (1,)):
        cc = np.array(c, float)*np.array([sgn, 1, 1]); fc = nrm(np.array(face, float)*np.array([sgn, 1, 1])); fb = np.array(fiber, float)*np.array([sgn, 1, 1])
        side = mask & ((x*sgn > -0.5) if mirror else np.ones(NB, bool))
        P0 = snap(cc, fc, side); u = nrm(fb-(fb@fc)*fc); v = np.cross(fc, u); d = XR-P0
        r2 = ((d@u)/a)**2+((d@v)/b)**2; w = np.exp(-(r2**(p/2)))*ss(((N@fc)-gate)/0.45)*(np.abs(d@fc) < depth)*side
        amp = (h/10.0)*K; D[:] += amp*w[:, None]*(N if vec is None else np.asarray(vec, float)[None, :]*np.array([sgn, 1, 1]))
        peak = max(peak, abs(amp)*w.max()*10)
    rep[name] = round(float(peak), 2); return peak
def chainprim(name, pts, faces, h, b, mask=None, p=2.0, mirror=True, gate=0.15):
    """polyline groove / band: union (max) of overlapping segment primitives"""
    mask = TORSO if mask is None else mask
    for sgn in ((1, -1) if mirror else (1,)):
        W = np.zeros(NB); side = mask & ((x*sgn > -0.5) if mirror else np.ones(NB, bool))
        for i in range(len(pts)-1):
            p0 = np.array(pts[i], float)*np.array([sgn, 1, 1]); p1 = np.array(pts[i+1], float)*np.array([sgn, 1, 1]); fc = nrm(np.array(faces[i], float)*np.array([sgn, 1, 1]))
            c = 0.5*(p0+p1); P0 = snap(c, fc, side); fb = p1-p0; L = max(np.linalg.norm(fb), 0.5); u = nrm(fb-(fb@fc)*fc); v = np.cross(fc, u); d = XR-P0
            r2 = ((d@u)/(0.62*L))**2+((d@v)/b)**2; W = np.maximum(W, np.exp(-(r2**(p/2)))*ss(((N@fc)-gate)/0.45)*(np.abs(d@fc) < 4.0)*side)
        D[:] += ((h/10.0)*K)*W[:, None]*N
    rep[name] = round(abs(h*K), 2)
G = lambda k, d: E('A_'+k, d)   # per-region amplitude multipliers (env A_<REGION>)
# ================= TORSO FRONT =================
fr = (0, 1, 0)
gA = G('ABS', '1.0')
for zc, f_ in ((118.6, 1.0), (113.0, 1.0), (107.6, 0.55)):   # rectus abdominis: 3 block pairs above the navel (z ~104); the lowest is softer
    prim(f'rectus_block_{zc:.0f}', (3.3, 14, zc), fr, (0, 0, 1), 2.4, 2.1, 1.6*gA*f_)
for zc, f_ in ((115.8, 1.0), (110.2, 0.8)):
    prim(f'rectus_intersect_{zc:.0f}', (3.3, 14, zc), fr, (1, 0, -0.08), 2.6, 0.55, -1.1*gA*f_, p=2)
prim('linea_alba', (0, 14, 114.5), fr, (0, 0, 1), 7.5, 0.6, -1.6*gA, p=2, mirror=False)
chainprim('semilunar', [(7.0, 14, 121.0), (6.8, 14, 113.0), (6.2, 14, 105.0), (5.3, 14, 98.0)], [fr, (0.25, 1, 0), (0.3, 1, 0)], -1.3*gA, 0.65)
prim('ext_oblique', (11.3, 10, 103.5), (0.65, 0.76, 0), (-0.4, 0, -1), 4.0, 2.4, 2.4*G('OBLM', '1.0'))
chainprim('inguinal_line', [(12.0, 13, 96.5), (9.0, 14, 92.5), (6.0, 14, 89.0), (3.5, 14, 86.5)], [(0.45, 1, 0), fr, fr], -2.0*G('OBL', '1.0'), 0.8, mask=TORSO*(leg < 0.7))
for i, zc in enumerate((121.5, 118.6, 115.8)):
    prim(f'serratus_{i}', (12.9, 5, zc), (0.8, 0.6, 0), (0.3, 0.75, -0.6), 1.5, 0.75, 1.4*G('SERR', '1.0'))
prim('upper_pectoral', (6.5, 12, 133.2), fr, (1, 0, -0.15), 4.0, 1.9, 1.6*G('PEC', '1.0'))
# tissue: flatter lower belly, narrower waist
prim('lower_belly_flatten', (0, 15, 101.5), fr, (0, 0, 1), 5.0, 8.5, -7.0*G('BELLY', '1.0'), p=2, mirror=False)
prim('waist_sides', (13.0, 3, float(E('A_WAIST_Z', '109.5'))), (1, 0, 0), (0, 0, 1), 5.8, 4.5, -6.5*G('WAIST', '1.0'), p=2)
# ================= TORSO BACK =================
bk = (0, -1, 0)
prim('erector', (3.6, -5, 106.0), bk, (0, 0, 1), 11.0, 1.7, 2.8*G('BACK', '1.0'))
prim('spinal_groove', (0, -5, 112.0), bk, (0, 0, 1), 15.0, 0.8, -2.6*G('BACK', '1.0'), p=2, mirror=False)
prim('lumbar_arch', (0, -4, 105.0), bk, (0, 0, 1), 6.0, 9.0, -4.5*G('POSTURE', '1.0'), p=2, mirror=False)
prim('lats', (12.8, -3, 116.5), (0.6, -0.8, 0), (0.35, 0, 1), 7.5, 3.0, 2.8*G('BACK', '1.0'))
prim('infraspinatus', (9.5, -6, 126.0), bk, (0.3, 0, 1), 3.6, 3.4, 2.8*G('BACK', '1.0'))
prim('scapula_medial_border', (5.8, -7, 126.0), bk, (0, 0, 1), 5.0, 0.8, -1.4*G('BACK', '1.0'), p=2)
prim('lower_trapezius', (3.6, -7, 123.5), bk, (0.45, 0, 1), 6.0, 2.0, 1.2*G('BACK', '1.0'))
prim('sacral_dimples', (3.6, -6, 98.5), bk, (0, 0, 1), 0.9, 0.9, -1.5*G('BACK', '1.0'), p=2)
# ================= GLUTES / HIP =================
GM = TORSO+LEGM > 0
prim('glute_max', (7.4, -8, 88.5), bk, (0, 0, 1), 6.2, float(E('A_GLUTE_B', '6.6')), 7.5*G('GLUTE', '1.0'), mask=GM, p=3)
chainprim('infragluteal_fold', [(3.0, -6, 83.2), (6.0, -7, 83.6), (9.0, -7, 84.0), (11.5, -6, 84.8)], [(0, -0.85, -0.5)]*3, -2.6*G('GLUTE', '1.0'), 0.8, mask=GM)
prim('glute_medius', (12.8, -4, 95.0), (0.75, -0.66, 0), (0, 0, 1), 3.6, 3.0, 2.8*G('GLUTE', '1.0'), mask=GM)
prim('trochanteric_hollow', (15.2, 1, 85.0), (1, 0, 0), (0, 0, 1), 3.0, 2.5, -1.8*G('HOLLOW', '1.0'), mask=GM, p=2)
prim('tfl', (12.5, 6, 89.0), (0.7, 0.7, 0), (0.15, -0.2, -1), 3.6, 1.8, 2.0*G('HIP', '1.0'), mask=GM)
# ================= LEGS =================
H_, K_, A_ = bt('thigh_l'), bt('calf_l'), bt('foot_l'); ax_t = K_-H_; Lt = np.linalg.norm(ax_t); ax_c = A_-K_; Lc = np.linalg.norm(ax_c)
at = lambda t: H_+t*ax_t; ac = lambda s: K_+s*ax_c
gL = G('THIGH', '1.0'); gC = G('CALF', '1.0'); gK = G('KNEE', '1.0')
prim('rectus_femoris', at(0.45)+[0, 6, 0], fr, ax_t, 0.30*Lt, 2.7, 3.8*gL, mask=LEGM)
prim('vastus_lateralis', at(0.56)+[4, 4, 0], (0.72, 0.69, 0), ax_t, 0.30*Lt, 3.1, 4.2*gL, mask=LEGM)
prim('vastus_medialis', at(0.86)+[-3, 4, 0], (-0.62, 0.78, 0), ax_t, 0.11*Lt, 2.9, 4.2*gL, mask=LEGM)
chainprim('sartorius_groove', [at(0.10)+[3.5, 5, 0], at(0.35)+[1.5, 6, 0], at(0.60)+[-1.5, 5, 0], at(0.85)+[-4.0, 2, 0]], [(0.4, 1, 0), (0, 1, 0), (-0.5, 0.85, 0)], -1.6*gL, 0.8, mask=LEGM)
prim('adductors', at(0.25)+[-4, 0, 0], (-1, 0.25, 0), ax_t, 0.18*Lt, 3.4, 2.2*gL, mask=LEGM)
prim('biceps_femoris', at(0.55)+[2.5, -5, 0], (0.5, -0.86, 0), ax_t, 0.28*Lt, 2.7, 3.3*gL, mask=LEGM)
prim('semitendinosus', at(0.55)+[-2.5, -5, 0], (-0.5, -0.86, 0), ax_t, 0.28*Lt, 2.7, 3.3*gL, mask=LEGM)
prim('hamstring_groove', at(0.62)+[0, -6, 0], bk, ax_t, 0.22*Lt, 0.7, -1.2*gL, mask=LEGM, p=2)
prim('it_band_groove', at(0.62)+[6, -1, 0], (1, -0.15, 0), ax_t, 0.22*Lt, 0.8, -1.4*gL, mask=LEGM, p=2)
prim('patella', K_+[0, 5, 3.0], fr, (0, 0, 1), 2.2, 2.0, 2.4*gK, mask=LEGM, p=4)
prim('peripatellar_hollow_lat', K_+[2.6, 4, 2.0], (0.6, 0.8, 0), (0, 0, 1), 2.4, 1.0, -2.2*gK, mask=LEGM, p=2)
prim('peripatellar_hollow_med', K_+[-2.6, 4, 2.0], (-0.6, 0.8, 0), (0, 0, 1), 2.4, 1.0, -2.2*gK, mask=LEGM, p=2)
prim('knee_side_lat', K_+[5, 0, 1.0], (1, 0, 0), (0, 0, 1), 3.0, 3.0, -2.6*gK, mask=LEGM, p=2)
prim('knee_side_med', K_+[-5, 0, 1.0], (-1, 0, 0), (0, 0, 1), 3.0, 3.0, -2.6*gK, mask=LEGM, p=2)
prim('gastroc_medial', ac(0.27)+[-2.5, -4, 0], (-0.55, -0.83, 0), ax_c, 6.5, 3.1, 5.5*gC, mask=LEGM)
prim('gastroc_lateral', ac(0.24)+[2.5, -4, 0], (0.55, -0.83, 0), ax_c, 5.5, 2.7, 3.8*gC, mask=LEGM)
prim('gastroc_groove', ac(0.30)+[0, -5, 0], bk, ax_c, 5.0, 0.7, -1.4*gC, mask=LEGM, p=2)
prim('soleus_lat', ac(0.50)+[3.5, -1, 0], (0.95, -0.3, 0), ax_c, 5.0, 2.1, 1.7*gC, mask=LEGM)
prim('soleus_med', ac(0.50)+[-3.5, -1, 0], (-0.95, -0.3, 0), ax_c, 5.0, 2.1, 1.7*gC, mask=LEGM)
prim('achilles_slim_lat', ac(0.78)+[2.5, -1, 0], (1, -0.2, 0), ax_c, 4.0, 2.6, -2.2*gC, mask=LEGM, p=2)
prim('achilles_slim_med', ac(0.78)+[-2.5, -1, 0], (-1, -0.2, 0), ax_c, 4.0, 2.6, -2.2*gC, mask=LEGM, p=2)
prim('tibialis_anterior', ac(0.30)+[2.5, 4, 0], (0.55, 0.83, 0), ax_c, 7.0, 1.8, 2.4*gC, mask=LEGM)
# ================= ARMS =================
U_, E_, Hd_ = bt('upperarm_l'), bt('lowerarm_l'), bt('hand_l'); ua = E_-U_; la = Hd_-E_; lat = nrm(np.array([0.8, 0, 0.6])-(np.array([0.8, 0, 0.6])@nrm(ua))*nrm(ua))
gA_ = G('ARM', '1.0')
prim('deltoid_lateral', U_+0.16*ua+1.2*lat, lat, ua, 5.0, 4.2, 4.0*gA_, mask=ARMM)
prim('deltoid_anterior', U_+0.12*ua+[0, 3, 0], fr, ua, 4.0, 2.2, 2.0*gA_, mask=ARMM)
prim('deltoid_posterior', U_+0.12*ua+[0, -3, 0], bk, ua, 4.0, 2.2, 2.0*gA_, mask=ARMM)
prim('deltoid_insertion_groove', U_+0.42*ua+1.0*lat, lat, ua, 2.0, 1.8, -1.0*gA_, mask=ARMM, p=2)
prim('biceps', U_+0.58*ua+[0, 2.5, 0], fr, ua, 7.0, 2.2, 2.4*gA_, mask=ARMM)
prim('triceps', U_+0.45*ua+[0, -2.5, 0], bk, ua, 8.0, 2.7, 2.8*gA_, mask=ARMM)
flat = nrm(np.array([0.8, 0, 0.6])-(np.array([0.8, 0, 0.6])@nrm(la))*nrm(la))
prim('forearm_extensors', E_+0.22*la+1.0*flat, flat, la, 5.0, 2.2, 1.8*gA_, mask=ARMM)
# ================= BREAST: inframammary shelf softened (size kept) =================
AP = P['breast_apex']; nbr = [set() for _ in range(NB)]
for tri in T:
    for i in range(3): nbr[tri[i]].update((tri[(i+1) % 3], tri[(i+2) % 3]))
NBR = [np.fromiter(q, np.int64) for q in nbr]
wimf = np.zeros(NB)
for sk_, Ap in AP.items():
    Ap = np.asarray(Ap)-np.array([MX, 0, 0]); dx = x-Ap[0]; dz = z-Ap[2]
    band = np.exp(-((np.sqrt((dx/6.0)**2+((dz+5.5)/2.2)**2)-1.0)/0.45)**2)*ss((Ap[2]-1.0-z)/2.0)*ss((y-(Ap[1]-8.0))/3.0)*TORSO
    wimf = np.maximum(wimf, band)
Y = XR+D
for _ in range(int(10*E('A_IMF', '0.6'))):
    M = np.asarray([Y[n].mean(0) if len(n) else Y[i] for i, n in enumerate(NBR)]); Y += (0.5*wimf)[:, None]*(M-Y)
D = Y-XR
# ================= guards + smoothing =================
wp = np.asarray(P['weld_pairs'])[:, 0]; kd = KDTree(len(wp))
for j, i in enumerate(wp): kd.insert(tuple(XR[i]), j)
kd.balance(); dseam = np.array([kd.find(tuple(p))[2] for p in XR])
guard = ss((138.5-z)/2.0)*ss((dseam-1.5)/1.5)*(1-ss((hand-0.2)/0.3))*ss((z-12.0)/4.0)
D *= guard[:, None]
for _ in range(int(E('A_SMOOTH', '2'))):
    M = np.asarray([D[n].mean(0) if len(n) else D[i] for i, n in enumerate(NBR)]); D = 0.5*D+0.5*M; D *= guard[:, None]
mag = np.linalg.norm(D, axis=1); ids = np.nonzero(mag > 0.002)[0]
rep_all = {'K': K, 'verts': int(len(ids)), 'max_mm': float(mag.max()*10), 'p99_mm': float(np.percentile(mag[ids], 99)*10), 'seam_pairs_max_mm': float(mag[wp].max()*10), 'primitives_peak_mm': rep,
           'env': {k: v for k, v in os.environ.items() if k.startswith('A_')}}
json.dump({'Body': {'GD40_Body': {str(int(i)): [round(float(v), 5) for v in D[i]] for i in ids}}, 'Head': {}}, open(os.path.join(OUT, 'morph_gd40_body_lod0.json'), 'w'))
np.save(os.path.join(OUT, 'gd40_body_delta_lod0.npy'), D)
Xa = X.copy(); bvh = BVHTree.FromPolygons([Vector(p) for p in Xa], [list(t_) for t_ in T])
for lod in (1, 2, 3):
    gl = json.load(gzip.open(os.path.join(LODD, f'lod_Body_{lod}.json.gz'), 'rt')); PL = np.asarray(gl['positions']); res = {}; far = 0
    for vi, p in enumerate(PL):
        loc, nr_, fi, dist = bvh.find_nearest(Vector(p))
        if fi is None or dist > 1.0: far += 1; continue
        tri = T[fi]; A0, B0, C0 = Xa[tri[0]], Xa[tri[1]], Xa[tri[2]]; qq = np.asarray(loc)
        v0, v1, v2 = B0-A0, C0-A0, qq-A0; d00, d01, d11, d20, d21 = v0@v0, v0@v1, v1@v1, v2@v0, v2@v1; den = d00*d11-d01*d01 or 1e-12
        bv = (d11*d20-d01*d21)/den; bw = (d00*d21-d01*d20)/den; bu = 1-bv-bw; dd_ = bu*D[tri[0]]+bv*D[tri[1]]+bw*D[tri[2]]
        if np.linalg.norm(dd_) > 0.002: res[str(vi)] = [round(float(v), 5) for v in dd_]
    json.dump({'Body': {'GD40_Body': res}, 'Head': {}}, open(os.path.join(OUT, f'morph_gd40_body_lod{lod}.json'), 'w')); rep_all[f'lod{lod}'] = {'verts': len(res), 'far': far}
json.dump(rep_all, open(os.path.join(OUT, 'gd40_body_report.json'), 'w'), indent=1)
print('GD40BODY', json.dumps({k: v for k, v in rep_all.items() if k not in ('env', 'primitives_peak_mm')}))
print('GD40PRIMS', json.dumps(rep))
