"""GD13: solve the per-panel head camera (rvec, f, cx, cy; D fixed) from identity-neutral tracker anchors (eyelids x3, outer / inner lips),
mesh side = semantic_j bindings evaluated on <head.npy>. Grid over yaw / pitch / roll for the start, then damped Gauss-Newton (numeric).
usage: blender -b --factory-startup --python gd13_camsolve.py -- <head.npy> <out cams.json> [D=150] [extra picks json]"""
import sys, os, json, math, numpy as np
sys.path.insert(0, os.path.dirname(__file__)); from gd13_common import *
a = sys.argv[sys.argv.index('--')+1:]; X = np.load(a[0]); OUT = a[1]; D = float(a[2]) if len(a) > 2 else 150.0
MM = mirror_map(X); TR = ref_tracks()
USE = {'front': ['eyelid_upper_l', 'eyelid_lower_l', 'eyelid_upper_r', 'eyelid_lower_r', 'lip_upper_outer_l', 'lip_upper_outer_r', 'lip_lower_outer_l', 'lip_lower_outer_r', 'lip_upper_inner_l', 'lip_upper_inner_r'],
       'q3_faceR': ['eyelid_upper_r', 'eyelid_lower_r', 'eyelid_upper_l', 'eyelid_lower_l', 'lip_upper_outer_r', 'lip_lower_outer_r', 'lip_upper_outer_l', 'lip_lower_outer_l', 'lip_upper_inner_r'],
       'q3_faceL': ['eyelid_upper_l', 'eyelid_lower_l', 'eyelid_upper_r', 'eyelid_lower_r', 'lip_upper_outer_l', 'lip_lower_outer_l', 'lip_upper_outer_r', 'lip_lower_outer_r', 'lip_upper_inner_l'],
       'prof_faceL': ['eyelid_upper_l', 'eyelid_lower_l', 'lip_upper_outer_l', 'lip_lower_outer_l']}
def wt(k): return 3.0 if 'eyelid' in k else (0.5 if 'inner' in k else 1.0)
out = {}
for v in VIEWS:
    B = bindings(v, MM); P3, P2, W = [], [], []
    for k in USE[v]:
        ck = "crv_"+k; p3 = bind_pts(B[ck], X); p2 = TR[v][ck]; n = min(len(p3), len(p2)); ok = ~np.isnan(p3[:n, 0]); P3.append(p3[:n][ok]); P2.append(p2[:n][ok]); W.append(np.full(ok.sum(), wt(k)))
    P3 = np.vstack(P3); P2 = np.vstack(P2); W = np.concatenate(W)
    def sim_fit(c):   # best f, cx, cy for a rotation (linear in f, cx, cy)
        Xc = (P3-CH)@cam_R(c).T; d = c['D']+Xc[:, 2]; q = Xc[:, :2]/d[:, None]
        A = np.zeros((2*len(q), 3)); A[0::2, 0] = q[:, 0]; A[1::2, 0] = q[:, 1]; A[0::2, 1] = 1; A[1::2, 2] = 1; b = P2.ravel(); ww = np.repeat(np.sqrt(W), 2)
        s = np.linalg.lstsq(A*ww[:, None], b*ww, rcond=None)[0]; c['f'], c['cx'], c['cy'] = float(s[0]), float(s[1]), float(s[2]); return c
    def res(c): return ((project(c, P3)-P2)*np.sqrt(W)[:, None]).ravel()
    best = None
    for yaw in np.arange(-95, 96, 5.0):
        for pit in (-20, -10, 0, 10, 20):
            for rol in (-10, 0, 10):
                Rh = rodrigues(np.radians([0, 0, 1.0])*0)  # placeholder
                # head rotation in camera space: yaw about camera y (down axis), pitch about camera x, roll about camera z
                Ry = rodrigues(np.array([0, math.radians(yaw), 0])); Rx = rodrigues(np.array([math.radians(pit), 0, 0])); Rz = rodrigues(np.array([0, 0, math.radians(rol)]))
                Rm = Rz@Rx@Ry; ang = math.acos(max(-1, min(1, (np.trace(Rm)-1)/2)))
                if ang < 1e-9: rv = np.zeros(3)
                else: rv = ang/(2*math.sin(ang))*np.array([Rm[2, 1]-Rm[1, 2], Rm[0, 2]-Rm[2, 0], Rm[1, 0]-Rm[0, 1]])
                c = sim_fit({'rvec': rv, 'D': D, 'f': 1.0, 'cx': 0.0, 'cy': 0.0})
                if c['f'] <= 0: continue
                e = float((res(c)**2).sum())
                if best is None or e < best[0]: best = (e, dict(c), (yaw, pit, rol))
    c = best[1]; pv = lambda c: np.r_[c['rvec'], c['f'], c['cx'], c['cy']]
    def unp(p): return {'rvec': p[:3], 'D': D, 'f': p[3], 'cx': p[4], 'cy': p[5]}
    p = pv(c); lam = 1e-3
    for it in range(60):
        r0 = res(unp(p)); Jm = np.zeros((len(r0), 6))
        for j in range(6):
            dp = np.zeros(6); h = 1e-5 if j < 3 else max(abs(p[j])*1e-6, 1e-4); dp[j] = h; Jm[:, j] = (res(unp(p+dp))-r0)/h
        H = Jm.T@Jm; g = Jm.T@r0; step = -np.linalg.solve(H+lam*np.diag(np.diag(H)), g); pn = p+step
        if (res(unp(pn))**2).sum() < (r0**2).sum(): p = pn; lam *= 0.5
        else: lam *= 4
    c = unp(p); r = (project(c, P3)-P2); rms = float(np.sqrt((np.linalg.norm(r, axis=1)**2).mean()))
    eL, eR = X[28955:29725].mean(0), X[29725:30495].mean(0); ipd_px = float(np.linalg.norm(project(c, eL[None])-project(c, eR[None])))
    R = cam_R(c); fw = -R[2]; yaw = math.degrees(math.atan2(fw[0], fw[1])); pit = math.degrees(math.asin(np.clip(fw[2], -1, 1)))
    out[v] = {'rvec': c['rvec'].tolist(), 'D': D, 'f': float(c['f']), 'cx': float(c['cx']), 'cy': float(c['cy']), 'rms_px': rms, 'n': int(len(P3)), 'grid_start': best[2],
              'cam_dir_yaw_deg': yaw, 'cam_dir_pitch_deg': pit, 'px_per_cm_at_head': float(c['f']/D), 'eye_centre_dist_px': ipd_px}
    print('CAM', v, json.dumps({k: (round(x, 3) if isinstance(x, float) else x) for k, x in out[v].items() if k != 'rvec'}))
json.dump(out, open(OUT, 'w'), indent=1); print('CAMSOLVE_OK', OUT)
