"""GD13 identity metrics: the SAME 2D definitions on the reference panel (tracker curves + manual picks) and on the candidate (mesh-bound
tracker curves / material landmarks projected with the solved camera of that panel). Values in % of the inter-eye distance (IPD = distance of
the two eyelid-opening centroids in that view); mm column = delta * the candidate's 3D eye-centre distance (5.95 cm) -> approximate only.
usage: blender -b --factory-startup --python gd13_metrics.py -- <head.npy> <cams.json> <out.json> [label]"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(__file__)); from gd13_common import *
a = sys.argv[sys.argv.index('--')+1:]; X = np.load(a[0]); C = json.load(open(a[1])); OUT = a[2]; LAB = a[3] if len(a) > 3 else os.path.basename(a[0])
MM = mirror_map(X); TR = ref_tracks(); PK = json.load(open(os.path.join(GD, 'data/picks_manual.json')))
S0 = np.load(os.path.join(GD, 'data/head_F1H.npy'))[:NS]; AX = np.abs(S0[:, 0]-MX); mid = AX < 0.35
def amw(m, f): i = np.nonzero(m)[0]; return int(i[np.argmax(f(S0[i]))])
PRN = amw(mid & (S0[:, 2] > 157) & (S0[:, 2] < 161), lambda P: P[:, 1])
zp = S0[PRN, 2]; cand = []
for zz in np.arange(zp-2.2, zp-0.3, 0.1):
    m = mid & (np.abs(S0[:, 2]-zz) < 0.06)
    if m.any(): cand.append(amw(m, lambda P: P[:, 1]))
SBN = int(min(cand, key=lambda i: S0[i, 1])); JAW = jaw_line(np.load(os.path.join(GD, 'data/head_F1H.npy')))
NOSE = np.nonzero((AX < 2.4) & (S0[:, 1] > 12.9) & (S0[:, 2] > 157.0) & (S0[:, 2] < 163.5))[0]
def curves_model(v):
    B = bindings(v, MM); out = {}
    for ck in TR[v]:
        if ck in B:
            P = bind_pts(B[ck], X); ok = ~np.isnan(P[:, 0]); Q = np.full((len(P), 2), np.nan); Q[ok] = project(C[v], P[ok]); out[ck] = Q
    return out
def m_front(cv, sub, alar, menton):
    """cv: curves dict (front). returns metric dict in px"""
    r = {}
    def c(k): return np.asarray(cv['crv_'+k], float)
    eL = np.vstack([c('eyelid_upper_l'), c('eyelid_lower_l')]); eR = np.vstack([c('eyelid_upper_r'), c('eyelid_lower_r')])
    cl, cr = np.nanmean(eL, 0), np.nanmean(eR, 0); ipd = np.linalg.norm(cl-cr); r['ipd_px'] = ipd
    for s in 'lr':
        u, l = c('eyelid_upper_'+s), c('eyelid_lower_'+s); r['eye_width_'+s] = np.linalg.norm(u[0]-u[-1])
        xs = np.linspace(np.nanmin(u[:, 0])+0.25*(np.nanmax(u[:, 0])-np.nanmin(u[:, 0])), np.nanmax(u[:, 0])-0.25*(np.nanmax(u[:, 0])-np.nanmin(u[:, 0])), 9)
        def yat(P, x): o = np.argsort(P[:, 0]); return np.interp(x, P[o, 0], P[o, 1])
        r['eye_aperture_'+s] = float(np.max(yat(l, xs)-yat(u, xs)))
    r['intercanthal'] = abs(c('eyelid_upper_l')[np.argmin(np.abs(c('eyelid_upper_l')[:, 0]-(cl[0]+cr[0])/2)), 0]-c('eyelid_upper_r')[np.argmin(np.abs(c('eyelid_upper_r')[:, 0]-(cl[0]+cr[0])/2)), 0])
    ey = (cl[1]+cr[1])/2; mx_ = (cl[0]+cr[0])/2
    uo = np.vstack([c('lip_upper_outer_l'), c('lip_upper_outer_r')]); lo = np.vstack([c('lip_lower_outer_l'), c('lip_lower_outer_r')])
    ui = np.vstack([c('lip_upper_inner_l'), c('lip_upper_inner_r')]); li = np.vstack([c('lip_lower_inner_l'), c('lip_lower_inner_r')])
    allx = np.r_[uo[:, 0], lo[:, 0]]; r['mouth_width'] = np.nanmax(allx)-np.nanmin(allx)
    def yat_mid(P, top=True):
        d = np.abs(P[:, 0]-mx_); k = np.argsort(d)[:3]; return np.nanmean(P[k, 1])
    st = (yat_mid(ui)+yat_mid(li))/2
    r['upper_lip_h'] = st-yat_mid(uo); r['lower_lip_h'] = yat_mid(lo)-st
    r['eye_to_stomion'] = st-ey; r['eye_to_subnasale'] = sub[1]-ey; r['subnasale_to_stomion'] = st-sub[1]
    r['alar_width'] = alar[1]-alar[0]
    if menton is not None: r['eye_to_menton'] = menton-ey; r['stomion_to_menton'] = menton-st
    return {k: float(v) for k, v in r.items()}
res = {}
# ---------- FRONT
v = 'front'; c = C[v]; RC = TR[v]; MCv = curves_model(v)
pk = PK[v]; rsub = next(p['p'] for p in pk['points'] if p['name'] == 'subnasale')
ral = [next(np.mean(cc['pts'], 0)[0] for cc in pk['contours'] if cc['name'] == 'alar_imgL'), next(np.mean(cc['pts'], 0)[0] for cc in pk['contours'] if cc['name'] == 'alar_imgR')]
rjaw = np.asarray(next(cc['pts'] for cc in pk['curves'] if cc.get('jaw')), float); rmen = rjaw[:, 1].max()
R = m_front(RC, rsub, ral, rmen)
msub = project(c, X[SBN][None])[0]; QN = project(c, X[NOSE]); band = np.abs(QN[:, 1]-np.mean([p[1] for cc in pk['contours'] if cc['name'].startswith('alar') for p in cc['pts']])) < 2.5
mal = [QN[band, 0].min(), QN[band, 0].max()]; QJ = project(c, X[JAW]); mmen = QJ[:, 1].max()
M = m_front(MCv, msub, mal, mmen)
eD = float(np.linalg.norm(X[28955:29725].mean(0)-X[29725:30495].mean(0)))
rows = []
for k in R:
    if k == 'ipd_px': continue
    rv, mv = R[k]/R['ipd_px']*100, M[k]/M['ipd_px']*100; rows.append((k, rv, mv, (mv-rv)/100*eD*10))
res['front'] = rows
# ---------- PROFILE (depth relations along the image x axis, normalised by the eye->stomion height of that view)
v = 'prof_faceL'; c = C[v]; AU = json.load(open(os.path.join(GD, 'data/contours_auto.json')))[v]['prof_front']; P = np.asarray(AU, float)
def prof_stats(P, ey, st):
    """P: front-edge points (x, y) per row (face to image-left). nasion = max x between brow and eye rows, pronasale = min x in nose rows,
    subnasale = max x between pronasale and stomion, labrale sup / inf = min x around the lips, pogonion = min x below the lips"""
    h = st-ey; f = lambda y0, y1: P[(P[:, 1] >= y0) & (P[:, 1] <= y1)]
    nas = f(ey-0.45*h, ey+0.05*h); nas = nas[np.argmax(nas[:, 0])]
    nos = f(ey+0.2*h, ey+0.85*h); prn = nos[np.argmin(nos[:, 0])]
    sbz = f(prn[1], st-0.05*h); sbn = sbz[np.argmax(sbz[:, 0])]
    ls = f(sbn[1], st); ls = ls[np.argmin(ls[:, 0])]; li = f(st, st+0.45*h); li = li[np.argmin(li[:, 0])]
    ch = f(st+0.45*h, st+1.2*h); pg = ch[np.argmin(ch[:, 0])]
    return dict(nose_projection=(sbn[0]-prn[0])/h, nasion_depth=(nas[0]-prn[0])/h, nose_length=(prn[1]-nas[1])/h, upper_lip_proj=(sbn[0]-ls[0])/h,
                lower_lip_vs_upper=(ls[0]-li[0])/h, chin_vs_lower_lip=(li[0]-pg[0])/h, subnasale_height=(sbn[1]-ey)/h)
ce = lambda cv: np.nanmean(np.vstack([cv['crv_eyelid_upper_l'], cv['crv_eyelid_lower_l']]), 0)
cst = lambda cv: (np.nanmean(np.asarray(cv['crv_lip_upper_inner_l'])[:, 1])+np.nanmean(np.asarray(cv['crv_lip_lower_inner_l'])[:, 1]))/2
RCp = TR[v]; Rp = prof_stats(P, ce(RCp)[1], cst(RCp))
# candidate profile edge: leftmost projected skin vertex per row (face region), same rows
Fv = np.nonzero((AX > -1) & (S0[:, 1] > 5.0) & (S0[:, 2] > 150.0) & ~((AX > 6.2) & (S0[:, 1] < 4.6)))[0]; Q = project(c, X[Fv]); rowsP = []
for y in np.arange(P[:, 1].min(), P[:, 1].max(), 1.0):
    m = np.abs(Q[:, 1]-y) < 0.6
    if m.any(): rowsP.append([Q[m, 0].min(), y])
MCp = curves_model(v); Mp = prof_stats(np.asarray(rowsP), ce(MCp)[1], cst(MCp))
res['profile'] = [(k, Rp[k]*100, Mp[k]*100, (Mp[k]-Rp[k])) for k in Rp]
json.dump(res, open(OUT, 'w'), indent=1)
print('METRICS', LAB)
for k, rv, mv, dmm in res['front']: print('  F %-22s ref %6.1f  cand %6.1f  %%IPD   delta %+5.2f mm' % (k, rv, mv, dmm))
for k, rv, mv, d in res['profile']: print('  P %-22s ref %6.1f  cand %6.1f  %% eye-stomion height  delta %+5.1f' % (k, rv, mv, d*100))
