"""GUARDIAN-4: robust per-side jaw lower-border comparison (project frame, cm; L = +x). Facial midline = mean x of pronasale/subnasale ridge.
For depth slices y (posterior ramus -> chin) finds per side the jaw border point (outer-lower corner of the slice section) and reports
L-R differences of border height (z) and half-width; plus the 3D path length menton -> border point at y=1.5 per side (mandibular body proxy).
usage: blender -b -P blender_gd4_jawborder.py -- <head.npy> [...]"""
import sys, os, json, numpy as np
for hp in sys.argv[sys.argv.index('--')+1:]:
    X = np.load(hp); S = X[:24049]; eL = X[28955:29725].mean(0); eR = X[29725:30495].mean(0); ez = (eL[2]+eR[2])/2; mx0 = (eL[0]+eR[0])/2
    fr = (S[:, 1] > 6) & (np.abs(S[:, 0]-mx0) < 1.5)
    def ridge(z0, z1): i = np.nonzero(fr & (S[:, 2] > z0) & (S[:, 2] < z1))[0]; return S[i[np.argmax(S[i, 1])]]
    mid = float(np.mean([ridge(ez-4.5, ez-1.5)[0], ridge(ez-6.8, ez-5.2)[0]])); chin = ridge(ez-12.5, ez-9.5)
    m = (S[:, 1] > chin[1]-3.5) & (np.abs(S[:, 0]-chin[0]) < 1.6) & (S[:, 2] > 146.5) & (S[:, 2] < chin[2]); i = np.nonzero(m)[0]; men = S[i[np.argmin(S[i, 2])]]
    rows = {}; pts = {'L': [], 'R': []}
    for y in (1.5, 3.0, 4.5, 6.0, 7.5, 9.0):
        r = {}
        for side, sg in (('L', 1), ('R', -1)):
            mm = (np.abs(S[:, 1]-y) < 0.15) & (sg*(S[:, 0]-mid) > 1.0) & (S[:, 2] > 147.5) & (S[:, 2] < ez-6)
            P = S[mm]; k = np.argmax(sg*(P[:, 0]-mid)*0.7-(P[:, 2]-148)); p = P[k]; pts[side].append(p); r[side] = (round(float(sg*(p[0]-mid)), 2), round(float(p[2]), 2))
        rows[f'y{y}'] = {'hw_L': r['L'][0], 'hw_R': r['R'][0], 'z_L': r['L'][1], 'z_R': r['R'][1], 'dhw': round(r['L'][0]-r['R'][0], 2), 'dz': round(r['L'][1]-r['R'][1], 2)}
    body = {s: round(float(np.linalg.norm(np.diff(np.r_[[men], np.asarray(pts[s])[::-1]], axis=0), axis=1).sum()), 2) for s in pts}
    print('JAWB', os.path.basename(hp), json.dumps({'menton_off_nose_mid': round(float(men[0]-mid), 3), 'menton_off_eye_mid': round(float(men[0]-mx0), 3), 'body_path_L_R': body, 'slices': rows}))
