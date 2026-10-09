"""GD13: identity metrics from MetaHuman tracker curves ONLY, identical method on the reference panel and on candidate skin renders made with
the solved camera of that panel (render px / 2 = panel px). Values in % of the eye-centroid distance of that image.
usage: -- <ref tracks.json> <render tracks.json> <out.json> cand_prefix1 [cand_prefix2 ...]   (views: front, q3_faceR, q3_faceL)"""
import sys, os, json, numpy as np
a = sys.argv[sys.argv.index('--')+1:]; RT = json.load(open(a[0])); CT = json.load(open(a[1])); OUT = a[2]; PRE = a[3:]
def met(cv, s=1.0):
    c = {k: np.asarray(v, float)*s for k, v in cv.items()}
    if not c: return None
    eL = np.vstack([c['crv_eyelid_upper_l'], c['crv_eyelid_lower_l']]).mean(0); eR = np.vstack([c['crv_eyelid_upper_r'], c['crv_eyelid_lower_r']]).mean(0)
    ipd = np.linalg.norm(eL-eR); ey = (eL[1]+eR[1])/2; mx = (eL[0]+eR[0])/2; r = {}
    def yat(P, x): o = np.argsort(P[:, 0]); return np.interp(x, P[o, 0], P[o, 1])
    for s_ in 'lr':
        u, l = c['crv_eyelid_upper_'+s_], c['crv_eyelid_lower_'+s_]; r['eye_width_'+s_] = np.linalg.norm(u[0]-u[-1])
        xs = np.linspace(u[:, 0].min(), u[:, 0].max(), 13)[3:-3]; r['eye_aperture_'+s_] = np.max(yat(l, xs)-yat(u, xs))
    uo = np.vstack([c['crv_lip_upper_outer_l'], c['crv_lip_upper_outer_r']]); lo = np.vstack([c['crv_lip_lower_outer_l'], c['crv_lip_lower_outer_r']])
    ui = np.vstack([c['crv_lip_upper_inner_l'], c['crv_lip_upper_inner_r']]); li = np.vstack([c['crv_lip_lower_inner_l'], c['crv_lip_lower_inner_r']])
    allx = np.r_[uo[:, 0], lo[:, 0]]; r['mouth_width'] = allx.max()-allx.min(); mmx = (allx.max()+allx.min())/2
    def ymid(P): k = np.argsort(np.abs(P[:, 0]-mmx))[:3]; return P[k, 1].mean()
    st = (ymid(ui)+ymid(li))/2; r['upper_lip_h'] = st-ymid(uo); r['lower_lip_h'] = ymid(lo)-st; r['eye_to_stomion'] = st-ey
    ph = [c['crv_lip_philtrum_l'], c['crv_lip_philtrum_r']]; top = np.array([P[np.argmin(P[:, 1])] for P in ph]); bot = np.array([P[np.argmax(P[:, 1])] for P in ph])
    r['eye_to_nosebase'] = top[:, 1].mean()-ey; r['philtrum_len'] = (bot[:, 1]-top[:, 1]).mean(); r['nosebase_to_stomion'] = st-top[:, 1].mean()
    nl = [c['crv_nasolabial_l'], c['crv_nasolabial_r']]; nt = np.array([P[np.argmin(P[:, 1])] for P in nl]); nb = np.array([P[np.argmax(P[:, 1])] for P in nl])
    r['alar_crease_width'] = abs(nt[0, 0]-nt[1, 0]); r['nasolabial_bottom_width'] = abs(nb[0, 0]-nb[1, 0]); r['eye_to_alar_crease'] = nt[:, 1].mean()-ey
    return {k: float(v/ipd*100) for k, v in r.items()}
res = {}
for v in ('front', 'q3_faceR', 'q3_faceL'):
    R = met(RT[v]['curves']); res[v] = {'ref': R}
    for p in PRE:
        k = f'{p}_{v}'
        if k in CT and CT[k]['curves']: res[v][p] = met(CT[k]['curves'], 0.5)
json.dump(res, open(OUT, 'w'), indent=1)
for v, d in res.items():
    print('VIEW', v, ' '.join(['ref']+[p for p in PRE if p in d]))
    for k in d['ref']:
        print('  %-24s' % k, '%6.1f' % d['ref'][k], ' '.join('%6.1f (%+5.1f)' % (d[p][k], d[p][k]-d['ref'][k]) for p in PRE if p in d))
