"""GUARDIAN-13 face measurements on a DNA-order head npy (cm). usage: blender -b -P gd13_measure.py -- <a.npy> [<b.npy> ...]"""
import sys, json, numpy as np
MX = -0.25
SEM = json.load(open('Saved/Codex/CharacterGuardian_20261001/semantic_j.json'))['front']
def crv(X, k): return np.array([(X[np.array(t)]*np.array(w)[:, None]).sum(0) for t, w in SEM[k]])
def M(path):
    X = np.load(path); H = X[:24049]; ax = np.abs(H[:, 0]-MX)
    eA, eB = X[28955:29725].mean(0), X[29725:30495].mean(0); ipd = float(np.linalg.norm(eA-eB))
    def hw(z, ymin, dz=0.2, axmax=9.0):
        s = H[(np.abs(H[:, 2]-z) < dz) & (H[:, 1] > ymin) & (ax < axmax)]; return float(np.abs(s[:, 0]-MX).max())
    biz = 2*max(hw(z, 5.5, 0.25, 7.6) for z in (160.5, 161.0, 161.5))     # frontal zygomatic contour in front of the ear root
    midw = 2*hw(159.0, 6.0)                                             # upper-midface (cheek front) width
    malar = max(((hw(z, 9.5)), z) for z in np.arange(159.0, 162.0, 0.25))   # lateral extent of the cheek front (y > 9.5)
    chin = H[(ax < 0.6) & (H[:, 1] > 9.5) & (H[:, 2] > 145)][:, 2].min(); brow = 164.2; fh = float(brow-chin)
    def nose_w(z, depth):
        s = H[(np.abs(H[:, 2]-z) < 0.1) & (ax < 3)]; yf = s[s[:, 1] > 11][:, 1].max(); t = s[s[:, 1] > yf-depth]; return float(2*np.abs(t[:, 0]-MX).max())
    radix = nose_w(163.25, 0.4); bridge = nose_w(161.5, 0.4)
    alar = float(abs(crv(X, 'crv_nasolabial_l')[0, 0]-crv(X, 'crv_nasolabial_r')[0, 0]))
    L = np.vstack([crv(X, k) for k in SEM if k.startswith('crv_lip')]); mouth = float(L[:, 0].max()-L[:, 0].min())
    jaw = [round(2*hw(z, 2.0, 0.15), 3) for z in (150.5, 152.0, 153.5)]
    return dict(ipd=round(ipd, 3), bizygomatic=round(biz, 3), midface_w=round(midw, 3), face_h_brow_chin=round(fh, 3), w_h=round(biz/fh, 3), radix_w=round(radix, 3), bridge_w=round(bridge, 3),
                alar_w=round(alar, 3), mouth_w=round(mouth, 3), mouth_ipd=round(mouth/ipd, 3), mouth_alar=round(mouth/alar, 3), malar_lateral_x=round(malar[0], 3), malar_z=round(float(malar[1]), 2), jaw_w=jaw)
for p in sys.argv[sys.argv.index('--')+1:]: print('MEAS', p.split('/')[-1], json.dumps(M(p)))
