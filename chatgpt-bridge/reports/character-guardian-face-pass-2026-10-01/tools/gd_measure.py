"""GUARDIAN face pass: IPD-normalised feature metrics from MetaHuman tracker curves (reference vs candidates, same view).
usage: python gd_measure.py <view front|close> <ref.json> <cand.json> [<cand2.json> ...]"""
import json, sys, math
V = sys.argv[1]; F = sys.argv[2:]
def m(path):
    d = json.load(open(path)); P = lambda k: d[k]
    def cen(pts): return (sum(p[0] for p in pts)/len(pts), sum(p[1] for p in pts)/len(pts))
    out = {}
    for s in 'lr':
        up, lo = P(f'crv_eyelid_upper_{s}'), P(f'crv_eyelid_lower_{s}'); c = cen(up+lo)
        out[f'eye_c_{s}'] = c; out[f'eye_w_{s}'] = math.dist(up[0], up[-1])
        # aperture: max vertical gap between upper and lower lid at matched fractions
        n = min(len(up), len(lo)); out[f'eye_h_{s}'] = max(abs(up[i][1]-lo[n-1-i if abs(up[0][0]-lo[0][0]) > abs(up[0][0]-lo[-1][0]) else i][1]) for i in range(n))
    ipd = math.dist(out['eye_c_l'], out['eye_c_r']); eyey = (out['eye_c_l'][1]+out['eye_c_r'][1])/2; eyex = (out['eye_c_l'][0]+out['eye_c_r'][0])/2
    uo = P('crv_lip_upper_outer_l')+P('crv_lip_upper_outer_r'); lo_ = P('crv_lip_lower_outer_l')+P('crv_lip_lower_outer_r'); ui = P('crv_lip_upper_inner_l')+P('crv_lip_upper_inner_r'); li = P('crv_lip_lower_inner_l')+P('crv_lip_lower_inner_r')
    xs = [p[0] for p in uo+lo_]; mw = max(xs)-min(xs); mcx = (max(xs)+min(xs))/2
    def ycen(pts, x0, half=0.06*mw): q = [p[1] for p in pts if abs(p[0]-x0) < half]; return sum(q)/len(q) if q else float('nan')
    r = {'ipd_px': ipd}
    r['eye_width'] = (out['eye_w_l']+out['eye_w_r'])/2/ipd; r['eye_aperture'] = (out['eye_h_l']+out['eye_h_r'])/2/ipd; r['eye_ap_ratio'] = r['eye_aperture']/r['eye_width']
    r['mouth_width'] = mw/ipd; r['mouth_w/eye_w'] = mw/((out['eye_w_l']+out['eye_w_r'])/2)
    r['upper_lip_thick'] = (ycen(ui, mcx)-ycen(uo, mcx))/ipd; r['lower_lip_thick'] = (ycen(lo_, mcx)-ycen(li, mcx))/ipd
    r['eye_to_stomion'] = ((ycen(ui, mcx)+ycen(li, mcx))/2-eyey)/ipd; r['eye_to_upperlip'] = (ycen(uo, mcx)-eyey)/ipd
    ph = P('crv_lip_philtrum_l')+P('crv_lip_philtrum_r'); r['philtrum_top_to_lip'] = (ycen(uo, mcx)-min(p[1] for p in ph))/ipd
    nl, nr = P('crv_nasolabial_l'), P('crv_nasolabial_r'); top = lambda c: min(c, key=lambda p: p[1]); bot = lambda c: max(c, key=lambda p: p[1])
    r['nasolab_top_sep'] = abs(top(nl)[0]-top(nr)[0])/ipd; r['nasolab_bot_sep'] = abs(bot(nl)[0]-bot(nr)[0])/ipd; r['nasolab_top_y'] = (min(top(nl)[1], top(nr)[1])-eyey)/ipd
    r['mouth_center_dx'] = (mcx-eyex)/ipd
    # mouth corner height relative to centre (smile/frown)
    cl = min(uo+lo_, key=lambda p: p[0]); cr = max(uo+lo_, key=lambda p: p[0]); r['corner_drop'] = ((cl[1]+cr[1])/2-(ycen(ui, mcx)+ycen(li, mcx))/2)/ipd
    return r
R = [m(f) for f in F]; keys = list(R[0])
print('%-20s' % V + ''.join('%14s' % __import__('os').path.basename(f).replace('.json', '') for f in F) + '   cand/ref')
for k in keys: print('%-20s' % k + ''.join('%14.3f' % r[k] for r in R) + '   ' + ' '.join('%6.2f' % (r[k]/R[0][k] if R[0][k] else float('nan')) for r in R[1:]))
