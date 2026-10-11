"""GD39 body tone pass (user, 2026-10-12): body after the EVE base-mesh sheet, but staying faithful to the SPHIRUS / Guardian character
(grounded, lean, natural; user choices: reference SHAPE with SOFT definition, skeleton / proportions unchanged, clothes later).
One always-on morph GD39_Body on top of the current neutral (accepted_b2 + BR_Neutral v6 + LK_Neutral), bind space UE cm (x = subject's
left, y = front, z = up, midline x = -0.23). PROCEDURAL pass (no manual brush control): broad, low-amplitude, maskable fields only.
Measured vs the reference (shape ratios per height): waist 14 % wider / 9 % shallower (no taper), knee 17 % wider, ankle 13 % wider, thigh
16 % shallower, calf back 8 % flatter; flat featureless back, low flat glute, soft lower belly, no deltoid cap. Bust / proportions kept.
Fields (amplitudes x K, cm along the outward normal unless noted):
 torso  waist taper (flanks in), lower-abdomen flatten, soft linea alba + iliac (inguinal) line, lats under the axilla (V taper)
 back   spinal groove, erector masses, scapular (infraspinatus) fullness, lumbar dimples
 glute  upper / mid glute fullness (lift), lower glute less droop, glute medius roundness; gluteal cleft untouched
 legs   quadriceps front + vastus lateralis sweep, hamstrings, knee sides narrower, gastrocnemius heads, lower calf / Achilles slimmer
 arms   deltoid cap, triceps
Guard (as LK): no change at the neck seam (z > 138.5 fades over 2 cm), hands, feet (z < 12); 3 Laplacian passes on the delta.
Writes morph_gd39_body_lod{0..3}.json ({'Body': {'GD39_Body': {idx: [dx,dy,dz]}}}) + gd39_body_report.json.
usage: blender -b --factory-startup --python gd39_body_art.py -- <sculpt_package_v6.json.gz> <lk_lod0.json> <lod_dir> <out_dir> [K=1.0]"""
import sys, json, gzip, math, os
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
a = sys.argv[sys.argv.index('--')+1:]; PKG, LKJ, LODD, OUT = a[:4]; K = float(a[4]) if len(a) > 4 else 1.0
os.makedirs(OUT, exist_ok=True); E = lambda k, d: float(os.environ.get(k, d))
P = json.loads(gzip.open(PKG, 'rb').read()); NB = P['NB']; X = np.asarray(P['br_neutral'], np.float64)[:NB].copy(); T = np.asarray(P['body']['triangles'], np.int64)
for k_, v in json.load(open(LKJ))['Body']['LK_Neutral'].items(): X[int(k_)] += v      # current neutral = b2 + v6 + LK
MX = -0.23; x = X[:, 0]-MX; y, z = X[:, 1], X[:, 2]; ax = np.abs(x); sx = np.sign(x)+(x == 0)
W8 = P['weights']
def chain(pre): return np.asarray([sum(w for b, w in W8[v].items() if b.startswith(pre)) for v in range(NB)])
arm = chain(('upperarm', 'lowerarm', 'hand', 'clavicle')); leg = chain(('thigh', 'calf', 'foot')); hand = chain(('hand',)); uarm = chain(('upperarm',))
fnm = -np.cross(X[T[:, 1]]-X[T[:, 0]], X[T[:, 2]]-X[T[:, 0]]); N = np.zeros_like(X)
for k in range(3): np.add.at(N, T[:, k], fnm)
N /= np.maximum(np.linalg.norm(N, axis=1), 1e-9)[:, None]; Nx, Ny, Nz = N[:, 0], N[:, 1], N[:, 2]
def ss(v): v = np.clip(v, 0, 1); return v*v*(3-2*v)
def g(v, s): return np.exp(-(v/s)**2)
B = P['skeleton']['Body']['bind']; bt = lambda b: np.asarray(B[b]['translation'], float)
torso = (arm < 0.3)*(leg < 0.5)*(z < 138.0); back = ss((-Ny-0.35)/0.4); front = ss((Ny-0.35)/0.4); lateral = ss((np.abs(Nx)-0.35)/0.4)
D = np.zeros_like(X); rep = {}; parts = {}
def add(name, w, amp, vec=None):
    w = np.clip(w, 0, None); d = (amp*K)*w[:, None]*(N if vec is None else vec); D[:] += d; parts[name] = float(np.abs(amp*K)*w.max()*10)
# ---------------- torso
add('waist_taper', g(z-E('G_WAIST_Z', '104.0'), 6.5)*lateral*torso*ss((ax-6.0)/3.0), -E('G_WAIST', '0.50'))
add('lower_abdomen', g(x, 7.0)*g(z-95.5, 4.5)*ss((Ny-0.4)/0.4)*torso, -E('G_ABD', '0.30'))
add('linea_alba', g(x, 0.7)*ss((z-102.0)/2.0)*ss((119.0-z)/2.0)*ss((Ny-0.5)/0.3)*torso, -E('G_LINEA', '0.08'))
# iliac / inguinal line: segment from the ASIS (|x| 11.5, z 95.5) to the pubic tubercle (|x| 3.0, z 85.5), front surface
p0 = np.array([11.5, 95.5]); p1 = np.array([3.0, 85.5]); q = np.c_[ax, z]; t = np.clip(((q-p0)@(p1-p0))/((p1-p0)@(p1-p0)), 0, 1); dseg = np.linalg.norm(q-(p0+t[:, None]*(p1-p0)), axis=1)
add('iliac_line', g(dseg, 0.9)*front*(leg < 0.7)*ss((t-0.05)/0.2)*ss((0.95-t)/0.2), -E('G_ILIAC', '0.10'))
add('lats', g(ax-12.3, 2.5)*g(z-118.0, 5.0)*lateral*torso, E('G_LATS', '0.12'))
# ---------------- back
add('spinal_groove', g(x, 1.1)*ss((z-97.0)/3.0)*ss((133.0-z)/4.0)*back*torso, -E('G_SPINE', '0.15'))
add('erectors', g(ax-3.6, 1.6)*g(z-106.0, 7.0)*back*torso, E('G_ERECT', '0.10'))
add('scapula', g(ax-9.5, 4.0)*g(z-126.0, 5.0)*back*(arm < 0.5)*(z < 136.0), E('G_SCAP', '0.12'))
add('lumbar_dimples', g(ax-3.6, 0.9)*g(z-98.5, 1.0)*back, -E('G_DIMPLE', '0.10'))
# ---------------- glute (apex / fold from the profile like LK)
sel = back*(z > 70)*(z < 95)*(ax > 3)*(ax < 12)*(arm < 0.1); zs = np.arange(70.0, 95.0, 0.5); prof = []
for zz in zs:
    mm = (sel > 0.5)*(np.abs(z-zz) < 0.4)*(np.abs(ax-7.5) < 2.0); prof.append(y[mm].min() if mm.any() else np.nan)
prof = np.asarray(prof); z_apex = float(zs[np.nanargmin(prof)]); rep['glute_apex_z'] = z_apex
dprof = np.gradient(prof, zs); cand = [zz for zz, gg in zip(zs[::-1], dprof[::-1]) if zz < z_apex-4.0 and gg < 0.45]; z_fold = cand[0] if cand else z_apex-10.0; rep['glute_fold_z'] = float(z_fold)
cleft = ss((ax-1.2)/1.5); gb = back*(arm < 0.1)*cleft
add('glute_upper', g(ax-7.0, 4.0)*g(z-(z_apex+3.0), 4.0)*gb, E('G_GLUTE_UP', '0.40'))
add('glute_lower', g(ax-8.5, 4.0)*g(z-(z_fold+2.5), 2.5)*gb, -E('G_GLUTE_LOW', '0.15'))
add('glute_medius', g(ax-13.5, 2.8)*g(z-95.0, 3.5)*ss((np.abs(Nx)-0.2)/0.4)*(leg < 0.6)*(arm < 0.1), E('G_GMED', '0.18'))
# ---------------- legs (per side, along the bind thigh / calf axes)
for s, sg in (('l', 1), ('r', -1)):
    th, kn, an = bt(f'thigh_{s}'), bt(f'calf_{s}'), bt(f'foot_{s}'); side = (sx == sg)*(leg > 0.5)
    tt = (th[2]-z)/(th[2]-kn[2]); thigh = side*(tt > 0)*(tt < 1.05)
    out_ = sg*Nx   # lateral-facing component on this leg
    add(f'quads_{s}', g(tt-0.45, 0.22)*ss((Ny-0.2)/0.5)*thigh, E('G_QUAD', '0.25'))
    add(f'vlat_{s}', g(tt-0.50, 0.25)*ss((out_-0.3)/0.4)*thigh, E('G_VLAT', '0.15'))
    add(f'hams_{s}', g(tt-0.47, 0.20)*ss((-Ny-0.2)/0.5)*thigh*ss((tt-0.15)/0.1), E('G_HAMS', '0.15'))
    add(f'knee_sides_{s}', g(z-(kn[2]+1.0), 2.8)*ss((np.abs(Nx)-0.4)/0.4)*side, -E('G_KNEE', '0.20'))
    cs = (kn[2]-z)/(kn[2]-an[2]); calf = side*(cs > 0)*(cs < 1)
    add(f'gastro_med_{s}', g(cs-0.27, 0.12)*ss((-Ny+0.1)/0.5)*ss((-out_+0.3)/0.6)*calf, E('G_GMEDH', '0.25'))
    add(f'gastro_lat_{s}', g(cs-0.25, 0.11)*ss((-Ny+0.1)/0.5)*ss((out_+0.3)/0.6)*calf, E('G_GLATH', '0.15'))
    add(f'lower_calf_{s}', g(cs-0.75, 0.12)*calf, -E('G_ACHIL', '0.12'))
    # ---------------- arms
    ua, la = bt(f'upperarm_{s}'), bt(f'lowerarm_{s}'); C = ua+np.array([sg*1.5, 0.0, -2.5]); dd = np.linalg.norm(X-C, axis=1)
    asd = (sx == sg)*(arm > 0.3)
    add(f'deltoid_{s}', g(dd, 5.5)*(sx == sg)*ss((uarm-0.25)/0.4)*ss((sg*Nx+0.2)/0.5), E('G_DELT', '0.22'))   # lateral / anterior / posterior cap, upper-arm skinned skin only
    r = ((X-ua)@(la-ua))/((la-ua)@(la-ua)); add(f'triceps_{s}', g(r-0.45, 0.2)*ss((-Ny-0.3)/0.4)*asd*(r > 0)*(r < 1), E('G_TRI', '0.10'))
# breast: soften the inframammary 'shelf' (masked relaxation of the IMF band, size unchanged), as in LK but on the lower perimeter only
AP = P['breast_apex']
nbr0 = [set() for _ in range(NB)]
for tri in T:
    for i in range(3): nbr0[tri[i]].update((tri[(i+1) % 3], tri[(i+2) % 3]))
NB0 = [np.fromiter(q_, np.int64) for q_ in nbr0]
wimf = np.zeros(NB)
for sk_, A in AP.items():
    A = np.asarray(A); dx = X[:, 0]-A[0]; dz = X[:, 2]-A[2]
    band = g(np.sqrt((dx/6.0)**2+((dz+5.5)/2.2)**2)-1.0, 0.45)*ss((A[2]-1.0-X[:, 2])/2.0)*ss((X[:, 1]-(A[1]-8.0))/3.0)*torso
    wimf = np.maximum(wimf, band)
IMF = E('G_IMF', '0.6'); Y = X+D
for _ in range(int(10*IMF)):
    M = np.asarray([Y[n].mean(0) if len(n) else Y[i] for i, n in enumerate(NB0)]); Y += (0.5*wimf)[:, None]*(M-Y)
D = Y-X; parts['imf_soften'] = float(np.linalg.norm((Y-X)*wimf[:, None], axis=1).max()*10)
guard = ss((138.5-z)/2.0)*(1-ss((hand-0.2)/0.3))*ss((z-12.0)/4.0)
D *= guard[:, None]
nbr = [set() for _ in range(NB)]
for tri in T:
    for i in range(3): nbr[tri[i]].update((tri[(i+1) % 3], tri[(i+2) % 3]))
NBR = [np.fromiter(sx_, np.int64) for sx_ in nbr]
for _ in range(int(E('G_SMOOTH', '3'))):
    M = np.asarray([D[n].mean(0) if len(n) else D[i] for i, n in enumerate(NBR)]); D = 0.5*D+0.5*M; D *= guard[:, None]
mag = np.linalg.norm(D, axis=1); ids = np.nonzero(mag > 0.002)[0]
rep.update({'verts': int(len(ids)), 'max_mm': float(mag.max()*10), 'p99_mm': float(np.percentile(mag[ids], 99)*10), 'K': K, 'parts_peak_mm': parts,
            'env': {k: v for k, v in os.environ.items() if k.startswith('G_')}})
json.dump({'Body': {'GD39_Body': {str(int(i)): [round(float(v), 5) for v in D[i]] for i in ids}}, 'Head': {}}, open(os.path.join(OUT, 'morph_gd39_body_lod0.json'), 'w'))
np.save(os.path.join(OUT, 'gd39_body_delta_lod0.npy'), D)
bvh = BVHTree.FromPolygons([Vector(p) for p in X], [list(t_) for t_ in T])
for lod in (1, 2, 3):
    gl = json.load(gzip.open(os.path.join(LODD, f'lod_Body_{lod}.json.gz'), 'rt')); PL = np.asarray(gl['positions']); res = {}; far = 0
    for vi, p in enumerate(PL):
        loc, nrm, fi, dist = bvh.find_nearest(Vector(p))
        if fi is None or dist > 1.0: far += 1; continue
        tri = T[fi]; A_, B_, C_ = X[tri[0]], X[tri[1]], X[tri[2]]; qq = np.asarray(loc)
        v0, v1, v2 = B_-A_, C_-A_, qq-A_; d00, d01, d11, d20, d21 = v0@v0, v0@v1, v1@v1, v2@v0, v2@v1; den = d00*d11-d01*d01 or 1e-12
        bv = (d11*d20-d01*d21)/den; bw = (d00*d21-d01*d20)/den; bu = 1-bv-bw; dd_ = bu*D[tri[0]]+bv*D[tri[1]]+bw*D[tri[2]]
        if np.linalg.norm(dd_) > 0.002: res[str(vi)] = [round(float(v), 5) for v in dd_]
    json.dump({'Body': {'GD39_Body': res}, 'Head': {}}, open(os.path.join(OUT, f'morph_gd39_body_lod{lod}.json'), 'w')); rep[f'lod{lod}'] = {'verts': len(res), 'far': far}
json.dump(rep, open(os.path.join(OUT, 'gd39_body_report.json'), 'w'), indent=1)
print('GD39BODY', json.dumps({k: v for k, v in rep.items() if k != 'env'}))
