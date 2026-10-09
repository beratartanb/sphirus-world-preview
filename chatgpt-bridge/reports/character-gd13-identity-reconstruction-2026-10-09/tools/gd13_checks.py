"""GD13 technical geometry checks of a DNA-order head vs references: finite / count, folded edges (dihedral > 120 deg, fold-scan method),
eyelid-eyeball penetration (lid skin inside the eyeball sphere in front of the eye), degenerate / inverted triangles vs the start head,
left/right symmetry of the displacement, per-region displacement (signed normal + mean 3-axis vector) vs one or more base heads.
usage: -- <head.npy> <out.json> base1.npy [base2.npy ...]"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(__file__)); from gd13_common import *
a = sys.argv[sys.argv.index('--')+1:]; X = np.load(a[0]); OUT = a[1]; BASES = a[2:]
T = np.asarray(pkg()['head']['triangles']); TS = T[(T < NS).all(1)]; MM = mirror_map()
def fold(Y):
    E = np.r_[TS[:, [0, 1]], TS[:, [1, 2]], TS[:, [2, 0]]]; F = np.r_[np.arange(len(TS))]*1; F = np.r_[np.arange(len(TS)), np.arange(len(TS)), np.arange(len(TS))]
    key = np.sort(E, 1); o = np.lexsort((key[:, 1], key[:, 0])); ks = key[o]; fs = F[o]; same = (ks[1:] == ks[:-1]).all(1); pr = np.c_[fs[:-1][same], fs[1:][same]]
    n = np.cross(Y[TS[:, 1]]-Y[TS[:, 0]], Y[TS[:, 2]]-Y[TS[:, 0]]); n /= np.maximum(np.linalg.norm(n, axis=1), 1e-12)[:, None]
    return int(((n[pr[:, 0]]*n[pr[:, 1]]).sum(1) < -0.5).sum())
def lid_pen(Y):
    out = {}
    for k in ('eyeL', 'eyeR'):
        E = Y[SEG[k][0]:SEG[k][1]]; c = E.mean(0); r = np.linalg.norm(E-c, axis=1); rs = np.percentile(r, 50)
        S = Y[:NS]; d = np.linalg.norm(S-c, axis=1); m = (d < 2.0) & (S[:, 1] > c[1]+0.3)
        out[k] = dict(min_clear_mm=round(float((d[m]-rs).min()*10), 2), n_inside_0p3mm=int(((d[m]-rs) < -0.03).sum()))
    return out
def tri_area(Y): return 0.5*np.linalg.norm(np.cross(Y[TS[:, 1]]-Y[TS[:, 0]], Y[TS[:, 2]]-Y[TS[:, 0]]), axis=1)
res = dict(head=os.path.basename(a[0]), n=int(len(X)), finite=bool(np.isfinite(X).all()), folds=fold(X[:NS]), lids=lid_pen(X))
S0 = np.load(BASES[0])[:NS] if BASES else None
if S0 is not None:
    A0, A1 = tri_area(S0), tri_area(X[:NS]); res['area_ratio_min'] = round(float((A1/np.maximum(A0, 1e-12)).min()), 3); res['area_ratio_max'] = round(float((A1/np.maximum(A0, 1e-12)).max()), 3)
    n0 = np.cross(S0[TS[:, 1]]-S0[TS[:, 0]], S0[TS[:, 2]]-S0[TS[:, 0]]); n1 = np.cross(X[TS[:, 1]]-X[TS[:, 0]], X[TS[:, 2]]-X[TS[:, 0]])
    res['flipped_tris_vs_base'] = int((((n0*n1).sum(1)) < 0).sum())
REGIONS = {}
def regions(S):
    ax = np.abs(S[:, 0]-MX); y, z = S[:, 1], S[:, 2]; ear = (ax > 6.2) & (y < 4.6) & (z > 154) & (z < 168); f = ~ear & (y > 3)
    return {'forehead': f & (z > 165.0), 'temple': ~ear & (ax > 4.8) & (z > 162) & (z < 167) & (y > 0) & (y < 9),
            'brow_supraorbital': f & (z > 163.3) & (z <= 165.0) & (ax > 0.9) & (ax < 5.2), 'glabella_radix': f & (z > 161.5) & (z <= 165.0) & (ax <= 0.9),
            'upper_lid': f & (z > 162.2) & (z <= 163.6) & (ax > 1.0) & (ax < 4.6) & (y > 9.5), 'lower_lid_infraorbital': f & (z > 160.6) & (z <= 162.2) & (ax > 1.2) & (ax < 4.8),
            'malar_zygoma': f & (z > 159.0) & (z <= 161.2) & (ax > 3.4) & (ax < 6.4), 'mid_cheek': f & (z > 156.5) & (z <= 159.0) & (ax > 2.6) & (ax < 6.2),
            'lower_cheek_jowl': f & (z > 152.5) & (z <= 156.5) & (ax > 3.4) & (ax < 6.4), 'nose_dorsum': f & (z > 159.6) & (z <= 162.2) & (ax < 1.2) & (y > 11),
            'nose_tip_alae': f & (z > 157.3) & (z <= 159.6) & (ax < 2.4) & (y > 12.3), 'upper_lip': f & (z > 155.9) & (z <= 157.3) & (ax < 2.8) & (y > 11),
            'lower_lip': f & (z > 154.6) & (z <= 155.9) & (ax < 2.8) & (y > 11), 'chin': f & (z > 151.3) & (z <= 154.6) & (ax < 2.6) & (y > 9),
            'jaw_body_angle': ~ear & (z > 150.5) & (z <= 156.5) & (ax >= 2.6) & (ax < 6.4) & (y > -1) & (y < 9), 'submental': ~ear & (z > 148.5) & (z <= 151.6) & (ax < 3.5) & (y > 4) & (y < 12),
            'cranium': (z > 168) | ((y < -1.5) & (z > 150)), 'neck': z < 148.5, 'ears': ear}
for b in BASES:
    B = np.load(b); D = X[:NS]-B[:NS]; N = skin_normals(B); dn = (D*N).sum(1); R = regions(B[:NS]); rows = {}
    for k, m in R.items():
        if not m.any(): continue
        rows[k] = dict(n=int(m.sum()), normal_mean_mm=round(float(dn[m].mean()*10), 2), abs_max_mm=round(float(np.linalg.norm(D[m], axis=1).max()*10), 2),
                       vec_mean_mm=[round(float(v*10), 2) for v in D[m].mean(0)], moved_gt_0p5mm=int((np.linalg.norm(D[m], axis=1) > 0.05).sum()))
    Dm = D[MM[:NS]].copy(); Dm[:, 0] *= -1; asym = np.linalg.norm(D-Dm, axis=1)
    dd = np.linalg.norm(D, axis=1)
    res['vs_'+os.path.basename(b)] = dict(max_mm=round(float(dd.max()*10), 2), mean_moved_mm=round(float(dd[dd > 0.01].mean()*10), 2), n_moved_0p1mm=int((dd > 0.01).sum()), n_moved_1mm=int((dd > 0.1).sum()),
                                          disp_asym_p99_mm=round(float(np.percentile(asym, 99)*10), 2), regions=rows)
json.dump(res, open(OUT, 'w'), indent=1); print('CHECKS', json.dumps({k: v for k, v in res.items() if not k.startswith('vs_')}))
for k, v in res.items():
    if k.startswith('vs_'): print('DISP', k, v['max_mm'], v['mean_moved_mm'], v['n_moved_1mm'], 'asym99', v['disp_asym_p99_mm'])
