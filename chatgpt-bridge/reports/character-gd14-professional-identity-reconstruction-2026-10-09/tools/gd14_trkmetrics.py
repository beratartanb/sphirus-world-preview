"""GD14: feature metrics from MetaHuman tracker curves (1x panel px; front ~15.3 px/cm): eye width / aperture / upper-lid peak position,
mouth width, vermilion heights, philtrum, lip-corner height relative to the stomion. usage: gd14_trkmetrics.py <ref tracks> <label tracks.json ...>"""
import json, sys, math
def lid(c, s):
    U, L = c[f'crv_eyelid_upper_{s}'], c[f'crv_eyelid_lower_{s}']
    xs = [p[0] for p in U]; w = math.dist(U[0], U[-1]); top = min(U, key=lambda p: p[1])
    def yat(C, x):
        best = min(C, key=lambda p: abs(p[0]-x)); return best[1]
    ap = max(yat(L, p[0])-p[1] for p in U[3:-3]); t = (top[0]-min(xs))/(max(xs)-min(xs))
    return w, ap, t
def mouth(c):
    pts = c['crv_lip_upper_outer_l']+c['crv_lip_upper_outer_r']; xl = min(pts, key=lambda p: p[0]); xr = max(pts, key=lambda p: p[0]); w = math.dist(xl, xr)
    cx = (xl[0]+xr[0])/2
    def yat(C, x): return min(C, key=lambda p: abs(p[0]-x))[1]
    uo = yat(c['crv_lip_upper_outer_l']+c['crv_lip_upper_outer_r'], cx); ui = yat(c['crv_lip_upper_inner_l']+c['crv_lip_upper_inner_r'], cx)
    li = yat(c['crv_lip_lower_inner_l']+c['crv_lip_lower_inner_r'], cx); lo = yat(c['crv_lip_lower_outer_l']+c['crv_lip_lower_outer_r'], cx)
    peak = min(c['crv_lip_upper_outer_l']+c['crv_lip_upper_outer_r'], key=lambda p: p[1])
    corner = (xl[1]+xr[1])/2; st = (ui+li)/2
    ph = c['crv_lip_philtrum_l']; phl = math.dist(ph[0], ph[-1])
    return w, ui-uo, lo-li, uo-peak[1], corner-st, phl
for f in sys.argv[1:]:
    d = json.load(open(f))
    for v in ('front', 'q3_faceR', 'q3_faceL'):
        if v not in d: continue
        c = d[v]['curves']
        try:
            el = lid(c, 'l'); er = lid(c, 'r'); m = mouth(c)
            print(f'{f.split("/")[-1].split(chr(92))[-1][:22]:22s} {v:9s} eyeL w{el[0]:5.1f} ap{el[1]:5.1f} pk{el[2]:.2f} | eyeR w{er[0]:5.1f} ap{er[1]:5.1f} pk{er[2]:.2f} | mouth w{m[0]:5.1f} upV{m[1]:4.1f} loV{m[2]:4.1f} bow{m[3]:4.1f} corner-st{m[4]:+5.1f} philtrum{m[5]:5.1f}')
        except Exception as e: print(f, v, 'ERR', e)
