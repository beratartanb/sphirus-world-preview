"""GUARDIAN-2: per-side asymmetry from tracker curves (reference tracker json vs candidate curves json in the same frame), IPD units.
Image left = character right (_r curves). usage: python gd2_asym.py <ref.json> <cand curves.json> [...]"""
import json, sys, math
def m(p):
    d = json.load(open(p)); c = lambda k: d[k]
    cen = lambda P: (sum(x for x, y in P)/len(P), sum(y for x, y in P)/len(P))
    eu = {s: c('crv_eyelid_upper_'+s) for s in 'lr'}; el = {s: c('crv_eyelid_lower_'+s) for s in 'lr'}
    E = {s: cen(eu[s]+el[s]) for s in 'lr'}; ipd = math.dist(E['l'], E['r'])
    o = {}
    for s in 'lr':
        up = min(y for x, y in eu[s]); lo = max(y for x, y in el[s]); w = max(x for x, y in eu[s]+el[s])-min(x for x, y in eu[s]+el[s])
        o['aperture_'+s] = (lo-up)/ipd; o['eyewidth_'+s] = w/ipd
    o['eye_height_r_minus_l'] = (E['l'][1]-E['r'][1])/ipd          # + = character right eye higher (smaller y)
    lu = c('crv_lip_upper_outer_l')+c('crv_lip_upper_outer_r'); xs = [p[0] for p in lu]
    cl = max(lu, key=lambda p: p[0]); cr = min(lu, key=lambda p: p[0]); mid = (cl[0]+cr[0])/2
    st = [p for p in c('crv_lip_upper_inner_l')+c('crv_lip_upper_inner_r')]; cy = min(st, key=lambda p: abs(p[0]-mid))[1]
    o['corner_drop_l'] = (cl[1]-cy)/ipd; o['corner_drop_r'] = (cr[1]-cy)/ipd       # + = corner below centre stomion
    o['mouth_shift'] = (mid-(E['l'][0]+E['r'][0])/2)/ipd
    return o
R = m(sys.argv[1]); print('%-22s %8s' % ('metric', 'ref')+''.join('%10s' % p.split('/')[-1][:9] for p in sys.argv[2:]))
C = [m(p) for p in sys.argv[2:]]
for k in R: print('%-22s %8.3f' % (k, R[k])+''.join('%10.3f' % c[k] for c in C))
