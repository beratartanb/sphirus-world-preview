"""GUARDIAN-4: per-side face contour in the Tier A FRONT photo frame (IPD units from the eye midpoint, image right = character LEFT), candidate
vs the Tier A contour picks at the same proportional heights (eye line -> menton). Candidate silhouette = outermost projected skin vertex in
front of the neck (y > 3.0) per side within a 3 px band; picks: cheek_hi/mid/lo, jaw, chin. Also menton / pronasale offsets.
usage: blender -b -P blender_gd4_sidecontour.py -- <head.npy> [...]"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930'))
from gd_common import topix
R = json.load(open('Saved/Codex/CharacterGuardian_20261001/track/ref_front.json')); PK = json.load(open('Saved/Codex/CharacterIdentity_20260930/ref_picks.json'))['front']
c = lambda k: np.mean(np.asarray(R[k]), 0); eL = (c('crv_eyelid_upper_l')+c('crv_eyelid_lower_l'))/2; eR = (c('crv_eyelid_upper_r')+c('crv_eyelid_lower_r'))/2
ipd = np.linalg.norm(eL-eR); em = (eL+eR)/2; P = {p['name']: np.asarray(p['ref'], float) for p in PK['points']+PK['contours']}
men_r = (P['menton'][1]-em[1])/ipd
rows = {'cheek_hi': ('cheek_L_hi', 'cheek_R_hi'), 'cheek_mid': ('cheek_L_mid', 'cheek_R_mid'), 'cheek_lo': ('cheek_L_lo', 'cheek_R_lo'), 'jaw': ('jaw_L', 'jaw_R'), 'chin': ('chin_L', 'chin_R')}
ref = {k: {'h': round(float(((P[a][1]+P[b][1])/2-em[1])/ipd/men_r), 3), 'L': round(float((P[a][0]-em[0])/ipd), 3), 'R': round(float((em[0]-P[b][0])/ipd), 3)} for k, (a, b) in rows.items()}
out = {'ref': ref, 'ref_menton_off': round(float((P['menton'][0]-em[0])/ipd), 3)}
for hp in sys.argv[sys.argv.index('--')+1:]:
    X = np.load(hp); S = X[:24049]; pe = topix('front', np.stack([X[28955:29725].mean(0), X[29725:30495].mean(0)])); ip = np.linalg.norm(pe[0]-pe[1]); m = pe.mean(0)
    keep = S[:, 1] > float(os.environ.get('YMIN', '3.0')); Q = topix('front', S[keep]); Sk = S[keep]
    j = np.nonzero((Sk[:, 1] > 8) & (Sk[:, 2] > 148.5) & (Sk[:, 2] < 153.5))[0]; men = Q[j[np.argmax(Q[j, 1])]]; mh = (men[1]-m[1])/ip
    r = {'menton_off': round(float((men[0]-m[0])/ip), 3), 'menton_below_eyes_ipd': round(float(mh), 3)}
    for k, v in ref.items():
        y = m[1]+v['h']*mh*ip; band = np.abs(Q[:, 1]-y) < 3.0
        if band.sum() < 3: continue
        r[k] = {'L': round(float((Q[band, 0].max()-m[0])/ip), 3), 'R': round(float((m[0]-Q[band, 0].min())/ip), 3)}
        r[k]['dL'] = round(r[k]['L']-v['L'], 3); r[k]['dR'] = round(r[k]['R']-v['R'], 3)
    out[os.path.basename(hp)] = r
print('SIDECONTOUR', json.dumps(out))
