"""GUARDIAN-15 face measurements (cm) on DNA-order head npys. usage: blender -b -P gd15_measure.py -- <a.npy> [...]"""
import sys, json, numpy as np
MX = -0.25; SEM = json.load(open('Saved/Codex/CharacterGuardian_20261001/semantic_j.json'))['front']
def crv(X, k): return np.array([(X[np.array(t)]*np.array(w)[:, None]).sum(0) for t, w in SEM[k]])
def M(p):
    X = np.load(p); H = X[:24049]; ax = np.abs(H[:, 0]-MX)
    eA, eB = X[28955:29725].mean(0), X[29725:30495].mean(0); ipd = float(np.linalg.norm(eA-eB)); ez = (eA[2]+eB[2])/2
    def hw(z, ymin, dz=0.2, axmax=7.6):
        s = H[(np.abs(H[:, 2]-z) < dz) & (H[:, 1] > ymin) & (ax < axmax)]; return float(np.abs(s[:, 0]-MX).max())
    chin = H[(ax < 0.6) & (H[:, 1] > 9.5) & (H[:, 2] > 145)]; cz = float(chin[:, 2].min())
    L = np.vstack([crv(X, k) for k in SEM if k.startswith('crv_lip')]); mouth = float(L[:, 0].max()-L[:, 0].min()); mz = float(L[:, 2].mean())
    alar = float(abs(crv(X, 'crv_nasolabial_l')[0, 0]-crv(X, 'crv_nasolabial_r')[0, 0]))
    up = crv(X, 'crv_eyelid_upper_l'); lo = crv(X, 'crv_eyelid_lower_l'); eo = float((up[:, 2].max()-lo[:, 2].min())/(up[:, 0].max()-up[:, 0].min()))
    # brow: highest-forward ridge point above the eye at |x| 1.5..5 -> brow z at the brow-hair band (skin z max y within z 164..167)
    bz = []
    for xx in (1.8, 3.0, 4.2, 5.2):
        s = H[(np.abs(ax-xx) < 0.15) & (H[:, 2] > 163.5) & (H[:, 2] < 167.5) & (H[:, 1] > 8)]; bz.append(round(float(s[np.argmax(s[:, 1]), 2]), 2))
    # malar apex: most anterior-lateral point (y + 0.5*|x|) in the cheek region
    c = H[(ax > 2.5) & (ax < 6.5) & (H[:, 2] > 157.5) & (H[:, 2] < 161.5) & (H[:, 1] > 6)]; k = np.argmax(c[:, 1]+0.5*np.abs(c[:, 0]-MX))
    out = dict(ipd=round(ipd, 3), face_h_eye_chin=round(ez-cz, 3), bizygomatic=round(2*max(hw(z, 5.5, 0.25) for z in (160.5, 161, 161.5)), 3),
               lower_cheek_w_z156=round(2*hw(156.0, 6.0), 3), mouth_level_w=round(2*hw(mz, 5.0), 3), mouth_w=round(mouth, 3), mouth_ipd=round(mouth/ipd, 3),
               mouth_alar=round(mouth/alar, 3), mouth_biz=round(mouth/(2*max(hw(z, 5.5, 0.25) for z in (160.5, 161, 161.5))), 3), mouth_chin=round(mz-cz, 3),
               chin_pad_w=round(2*hw(cz+1.2, 9.0, 0.2, 4), 3), malar_apex=[round(float(c[k, 0]-MX), 2), round(float(c[k, 1]), 2), round(float(c[k, 2]), 2)],
               eye_open=round(eo, 3), brow_z_by_x=bz, brow_eye_dz=round(float(np.mean(bz[:3])-ez), 3))
    out['w_h'] = round(out['bizygomatic']/out['face_h_eye_chin'], 3); return out
for p in sys.argv[sys.argv.index('--')+1:]: print('M15', p.split('/')[-1], json.dumps(M(p)))
