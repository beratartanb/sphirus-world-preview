"""GUARDIAN-9: profile-relevant Tier A 3/4 fit (verified ~33 deg solved camera, Tier A close picks). For each candidate head (npy):
  silhouette picks (sellion, dorsum_mid, pronasale, chin_p1..p4): image-right-most projected vertex of the nose (or chin) region at the pick row
  -> dx = candidate - reference (px; + = candidate projects more toward the viewer's right = more anterior / outward in this view)
  point picks (subnasale, alar_near, menton_c, jawbot_1/2): projected landmark vertex -> (dx, dy) px
  lip curves: mean distance of the mesh-bound tracker lip curves to the reference curves (px), upper / lower separately
usage: blender -b -P blender_gd9_q3prof.py -- <head.npy> [...]"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930'))
from gd_common import topix
PK = json.load(open('Saved/Codex/CharacterIdentity_20260930/ref_picks.json'))['close']; P = {p['name']: np.asarray(p['ref'], float) for p in PK['points']+PK['contours']}
SEM = json.load(open('Saved/Codex/CharacterGuardian_20261001/semantic_j.json'))['close']; RC = json.load(open('Saved/Codex/CharacterGuardian_20261001/track/ref_close.json'))
for hp in sys.argv[sys.argv.index('--')+1:]:
    X = np.load(hp); S = X[:24049]; mx = (X[28955:29725, 0].mean()+X[29725:30495, 0].mean())/2; r = {}
    nose = S[(np.abs(S[:, 0]-mx) < 0.9) & (S[:, 1] > 10.5) & (S[:, 2] > 157.0) & (S[:, 2] < 164.5)]; Qn = topix('close', nose)
    chin = S[(np.abs(S[:, 0]-mx) < 3.5) & (S[:, 1] > 7.0) & (S[:, 2] < 155.0) & (S[:, 2] > 149.0)]; Qc = topix('close', chin)
    for k, Q in (('sellion', Qn), ('dorsum_mid', Qn), ('pronasale', Qn), ('chin_p1', Qc), ('chin_p2', Qc), ('chin_p3', Qc), ('chin_p4', Qc)):
        x, y = P[k]; b = np.abs(Q[:, 1]-y) < 2.5
        if b.sum(): r[k] = round(float(Q[b, 0].max()-x), 1)
    # anterior mid-sagittal profile (cm): forehead -> nasion -> tip -> subnasale -> lips -> labiomental -> pogonion -> menton
    mid = np.abs(S[:, 0]-mx) < 0.3; prof = {}
    for z in np.arange(148.0, 168.01, 0.25):
        m = mid & (np.abs(S[:, 2]-z) < 0.14)
        if m.sum(): prof[round(float(z), 2)] = float(S[m, 1].max())
    zs = np.array(sorted(prof)); ys = np.array([prof[z] for z in zs])
    def ext(z0, z1, f): m = (zs >= z0) & (zs <= z1); i = np.nonzero(m)[0][f(ys[m])]; return round(float(zs[i]), 2), round(float(ys[i]), 2)
    tip = ext(157.5, 161.0, np.argmax); nas = ext(161.0, 164.5, np.argmin); subn = ext(156.2, tip[0]-0.5, np.argmin); ul = ext(155.4, subn[0], np.argmax); ll = ext(153.9, 155.4, np.argmax)
    pog = ext(150.6, 153.6, np.argmax); lm = ext(pog[0]+0.25, ll[0]-0.25, np.argmin); gl = ext(163.0, 166.5, np.argmax)
    r['profile_cm'] = {'glabella': gl, 'nasion': nas, 'pronasale': tip, 'subnasale': subn, 'labrale_sup': ul, 'labrale_inf': ll, 'labiomental': lm, 'pogonion': pog,
        'tip_projection_from_subnasale': round(tip[1]-subn[1], 2), 'nasion_depth_from_glabella': round(gl[1]-nas[1], 2), 'upper_lip_ahead_of_lower': round(ul[1]-ll[1], 2),
        'lower_lip_ahead_of_pogonion': round(ll[1]-pog[1], 2), 'labiomental_depth': round(min(ll[1], pog[1])-lm[1], 2), 'nose_length_nasion_tip': round(float(np.hypot(nas[0]-tip[0], nas[1]-tip[1])), 2)}
    for grp, keys in (('upper_lip', ('crv_lip_upper_outer_l', 'crv_lip_upper_outer_r')), ('lower_lip', ('crv_lip_lower_outer_l', 'crv_lip_lower_outer_r'))):
        ds = []
        for k in keys:
            pts = np.array([np.asarray(w) @ X[np.asarray(i)] for i, w in SEM[k]]); q = topix('close', pts); ref = np.asarray(RC[k], float); n = min(len(q), len(ref))
            ds.append((q[:n]-ref[:n]).mean(0))
        r[grp+'_mean_dxdy'] = np.round(np.mean(ds, 0), 1).tolist()
    tipv = S[mid][np.argmax(S[mid][:, 1])]; q0 = topix('close', np.stack([tipv, tipv+np.array([0, 1.0, 0])])); pxcm = float(q0[1, 0]-q0[0, 0])
    r['px_per_cm_anterior_in_3q'] = round(pxcm, 1); r['anterior_mm_equiv'] = {k: round(r[k]/pxcm*10, 1) for k in ('sellion', 'dorsum_mid', 'pronasale', 'chin_p1', 'chin_p2', 'chin_p3', 'chin_p4') if k in r}
    print('Q3PROF', os.path.basename(hp), json.dumps(r))
