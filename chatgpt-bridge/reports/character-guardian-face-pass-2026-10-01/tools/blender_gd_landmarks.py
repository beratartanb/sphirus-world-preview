"""GUARDIAN face pass: geometric landmarks of a head npy (eye centres, canthi from the bound lid curves, pronasale, subnasale, alar
lateral points, stomion, menton, chin width) projected into the reference frames and compared with the reference picks / tracker curves,
in units of the projected inter-pupil distance (front) . Prints 3D landmark positions too (for placing shape handles).
usage: blender -b --factory-startup --python blender_gd_landmarks.py -- <semantic.json> <head.npy> [...]"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930'))
from gd_common import *
a = sys.argv[sys.argv.index('--')+1:]; SEM = json.load(open(a[0])); PK = json.load(open(I+'/ref_picks.json'))
def lm(X):
    S = X[:24049]; x, y, z = S[:, 0], S[:, 1], S[:, 2]; mid = np.abs(x) < 0.3; L = {}
    L['eyeL'] = X[28955:29725].mean(0); L['eyeR'] = X[29725:30495].mean(0)
    for s in 'lr':
        up = SEM['front'][f'crv_eyelid_upper_{s}']; L[f'canth_a_{s}'] = np.asarray(up[0][1])@X[up[0][0]]; L[f'canth_b_{s}'] = np.asarray(up[-1][1])@X[up[-1][0]]
    m = mid & (z > 157.0) & (z < 161.5); L['pronasale'] = S[np.nonzero(m)[0][np.argmax(y[m])]]
    # subnasale: deepest point of the OUTER midline profile (per-z max y) between the tip and the upper-lip vermilion
    m = mid & (z < L['pronasale'][2]-0.5) & (z > L['pronasale'][2]-3.5); ids = np.nonzero(m)[0]; bins = {}
    for i in ids:
        b = int(round(z[i]/0.15))
        if b not in bins or y[i] > y[bins[b]]: bins[b] = i
    env = sorted(bins.items()); env_y = np.array([y[i] for _, i in env]); k = int(np.argmin(env_y[:max(3, len(env_y)*2//3)])); L['subnasale'] = S[env[k][1]]
    # alar: widest nose-wing points (forward of the cheek / lip junction) just above the subnasale
    m = (np.abs(z-(L['subnasale'][2]+0.45)) < 0.4) & (y > L['subnasale'][1]-1.6) & (np.abs(x-L['pronasale'][0]) < 2.6)
    ids = np.nonzero(m)[0]; L['alar_l'] = S[ids[np.argmax(x[ids])]]; L['alar_r'] = S[ids[np.argmin(x[ids])]]
    m = mid & (z > 149) & (z < L['subnasale'][2]-2) & (y > 8); ids = np.nonzero(m)[0]; zs = np.sort(z[ids])
    chin_ids = ids[np.argsort(z[ids])]; L['menton'] = None
    for i in chin_ids:   # lowest midline point that is still on the chin front (y within 3 cm of the chin max)
        if y[i] > y[ids].max()-2.6: L['menton'] = S[i]; break
    return L
for hp in a[1:]:
    X = np.load(hp); L = lm(X); tag = os.path.basename(hp).replace('.npy', '')
    print('LM3D', tag, {k: np.round(v, 2).tolist() for k, v in L.items() if v is not None})
    for view in ('front', 'close'):
        P2 = {k: topix(view, [v])[0] for k, v in L.items() if v is not None}; ipd = np.linalg.norm(P2['eyeL']-P2['eyeR']); ey = (P2['eyeL'][1]+P2['eyeR'][1])/2
        rc = ref_curves(view); el = np.mean(rc['crv_eyelid_upper_l']+rc['crv_eyelid_lower_l'], 0); er = np.mean(rc['crv_eyelid_upper_r']+rc['crv_eyelid_lower_r'], 0); ripd = np.linalg.norm(el-er); rey = (el[1]+er[1])/2
        pk = {p['name']: p['ref'] for p in PK[view]['points']+PK[view]['contours']}
        out = {}
        if view == 'front':
            out['eye->subnasale'] = ((P2['subnasale'][1]-ey)/ipd, (pk['subnasale'][1]-rey)/ripd)
            out['alar width'] = (abs(P2['alar_l'][0]-P2['alar_r'][0])/ipd, abs(pk['alar_L'][0]-pk['alar_R'][0])/ripd)
            out['eye->pronasale'] = ((P2['pronasale'][1]-ey)/ipd, (pk['pronasale'][1]-rey)/ripd)
            if L['menton'] is not None: out['eye->menton'] = ((P2['menton'][1]-ey)/ipd, (pk['menton'][1]-rey)/ripd)
            out['intercanthal(l_a..r_a)'] = (abs(P2['canth_a_l'][0]-P2['canth_a_r'][0])/ipd, abs(rc['crv_eyelid_upper_l'][0][0]-rc['crv_eyelid_upper_r'][0][0])/ripd)
            out['outer canthi'] = (abs(P2['canth_b_l'][0]-P2['canth_b_r'][0])/ipd, abs(rc['crv_eyelid_upper_l'][-1][0]-rc['crv_eyelid_upper_r'][-1][0])/ripd)
        else:
            out['eye->subnasale'] = ((P2['subnasale'][1]-ey)/ipd, (pk['subnasale'][1]-rey)/ripd)
            out['eye->pronasale'] = ((P2['pronasale'][1]-ey)/ipd, (pk['pronasale'][1]-rey)/ripd)
            out['pronasale dx from eye mid'] = ((P2['pronasale'][0]-(P2['eyeL'][0]+P2['eyeR'][0])/2)/ipd, (pk['pronasale'][0]-(el[0]+er[0])/2)/ripd)
        print('LM2D', tag, view, {k: (round(c, 3), round(r, 3), round(c/r if r else 0, 2)) for k, (c, r) in out.items()})
