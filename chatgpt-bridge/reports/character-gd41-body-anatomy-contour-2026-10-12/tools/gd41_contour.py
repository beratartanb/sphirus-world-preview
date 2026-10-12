"""GD41 contour analysis: the body reference's silhouette CURVES (front-view width, side-view depth and the front / back lines) against the
SPHIRUS body, aligned by anatomical landmarks (bust apex, navel, crotch, knee, calf, ankle) so that different vertical proportions (the reference
has longer legs; our skeleton is kept) do not bias the shape ratios. Scale-free (per body height), true planar sections on our mesh.
Reference (private sheet): silhouettes from gd39_refsil json (rows top->bottom, run containing / nearest the body axis).
  front view : W_ref(f) = run width / H ; below the crotch the A-stance legs stay merged for a few rows -> halved when the run still contains the axis
  side view  : front / back lines relative to the THIGH anchor (section centre at f = 0.62, below the hanging hand) -> front_exc, back_exc;
               the forearm / hand hangs in front of the lower abdomen and thigh (f 0.395..0.60): the front line is interpolated there; the back
               line is clean. The anchor removes the reference's forward lean (a skeletal posture we cannot and must not copy); the lumbar
               hollow, glute projection, belly line and chest line shapes remain.
Ours: the same per z (0.5 cm) from planar sections (arms excluded), anchor = the left-thigh section centre at the aligned height.
Output: data/shape_plan.json (our z grid: aligned reference fraction, width ratios torso / leg, depth ratios, our and target front / back
lines, clamps) and meas/contour_curves.png.
usage: blender -b --factory-startup --python gd41_contour.py -- <pkg.json.gz> <lk_lod0.json> <refsil.json> <out_plan.json> <out_plot.png>"""
import sys, json, os
import numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD13_Identity_20261009/tools')); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gd13_img as gi; from gd41_lib import Body, ss
a = sys.argv[sys.argv.index('--')+1:]; PKG, LKJ, REFJ, OUTJ, OUTP = a[:5]
B = Body(PKG, LKJ); XR = B.XR; x, y, z = XR[:, 0], XR[:, 1], XR[:, 2]; HO, ZTOP = B.H, B.ZTOP
noarm = B.arm < 0.3; zg = np.arange(2.0, 136.0, 0.5)
_zc = [zz for zz in np.arange(70.0, 95.0, 0.25) if len(B.section(zz, noarm & (np.abs(x) < 1.5))) >= 2]; z_crotch = 80.3   # visual crotch (legs separate in the front silhouette), the same definition as the reference landmark
torso = noarm; legL = noarm & (x > 0)
def smooth(v, s=4):
    v = np.asarray(v, float); out = v.copy(); ok = ~np.isnan(v); idx = np.arange(len(v))
    if ok.sum() > 2: out[~ok] = np.interp(idx[~ok], idx[ok], v[ok])
    k = np.exp(-0.5*(np.arange(-3*s, 3*s+1)/s)**2); k /= k.sum(); return np.convolve(np.pad(out, 3*s, mode='edge'), k, 'valid')
def medf(v, r=3):
    v = np.asarray(v, float); out = v.copy()
    for i in range(len(v)):
        w = v[max(0, i-r):i+r+1]; w = w[~np.isnan(w)]; out[i] = np.median(w) if len(w) else np.nan
    return out
# ---------------- ours: sections
ET = np.array([B.extents(zz, torso) if zz >= z_crotch-0.5 else (np.nan,)*4 for zz in zg]); EL = np.array([B.extents(zz, legL) if zz < z_crotch+0.5 else (np.nan,)*4 for zz in zg])
fr_o, bk_o, wt_o = smooth(ET[:, 0], 2), smooth(ET[:, 1], 2), smooth(ET[:, 2]-ET[:, 3], 2); frl_o, bkl_o, wl_o = smooth(EL[:, 0], 2), smooth(EL[:, 1], 2), smooth(EL[:, 2]-EL[:, 3], 2)
def fo(zz): return (ZTOP-zz)/HO
def zi(zz): return int(np.argmin(np.abs(zg-zz)))
def z_argmin(W, z0, z1): m = (zg >= z0) & (zg <= z1) & ~np.isnan(W); i = np.nonzero(m)[0]; return float(zg[i[np.argmin(W[i])]])
def z_argmax(W, z0, z1): m = (zg >= z0) & (zg <= z1) & ~np.isnan(W); i = np.nonzero(m)[0]; return float(zg[i[np.argmax(W[i])]])
z_bust = float(np.asarray(B.P['breast_apex']['l'])[2]); z_navel = 104.0
z_knee = z_argmin(wl_o, ZTOP-0.76*HO, ZTOP-0.66*HO); z_calf = z_argmax(wl_o, 28.0, z_knee-3.0); z_ankle = z_argmin(frl_o-bkl_o, 6.0, 16.0)
LM_OUR = {'top': 0.0, 'bust': fo(z_bust), 'navel': fo(z_navel), 'crotch': fo(z_crotch), 'knee': fo(z_knee), 'calf': fo(z_calf), 'ankle': fo(z_ankle), 'sole': 1.0}
# ---------------- reference rows
R = json.load(open(REFJ))
def ref_rows(view):
    v = R[view]; rows = v['rows']; n = len(rows); f = (np.arange(n)+0.5)/v['height_px']
    x0 = np.array([np.nan if r is None else r[0] for r in rows], float); x1 = np.array([np.nan if r is None else r[1] for r in rows], float); return f, x0, x1, v
ff, fx0, fx1, fv = ref_rows('front'); Hf = fv['height_px']; axf = fv['axis_x']
sf, sx0, sx1, sv = ref_rows('side'); Hs = sv['height_px']; sw = (sx1-sx0)/Hs
def argmin_in(f, w, a_, b_): m = (f >= a_) & (f <= b_) & ~np.isnan(w); i = np.nonzero(m)[0]; return float(f[i[np.argmin(w[i])]])
LM_REF = {'top': 0.0, 'bust': 0.253, 'navel': 0.395, 'crotch': 0.491, 'knee': argmin_in(ff, (fx1-fx0)/Hf, 0.66, 0.76), 'calf': None, 'ankle': argmin_in(sf, sw, 0.84, 0.96), 'sole': 1.0}
fw = (fx1-fx0)/Hf; merged = (ff > LM_REF['crotch']) & (fx0 < axf) & (fx1 > axf); fw[merged] = np.nan   # A-stance legs still joined just below the crotch: no single-leg width there (our legs stand apart: a halved merged width would count the stance gap)
leg_valid_f = float(ff[(ff > LM_REF['crotch']) & ~merged].min())
m = (ff > LM_REF['knee']+0.02) & (ff < 0.87); i = np.nonzero(m)[0]; LM_REF['calf'] = float(ff[i[np.argmax(fw[i])]])
keys = ['top', 'bust', 'navel', 'crotch', 'knee', 'calf', 'ankle', 'sole']
def f_ref_of(f_our): return np.interp(f_our, [LM_OUR[k] for k in keys], [LM_REF[k] for k in keys])
W_ref_f = smooth(medf(fw))
# side lines relative to the thigh anchor (f 0.62 +- 0.01: below the hanging hand, above the knee)
F_ANC = 0.62; anc = (sf >= F_ANC-0.01) & (sf <= F_ANC+0.01); anchor_x = float(np.nanmean(0.5*(sx0[anc]+sx1[anc])))
front_exc = medf((anchor_x-sx0)/Hs); back_exc = medf((sx1-anchor_x)/Hs)        # the figure faces image-left: front = smaller x
front_exc[(sf > 0.395) & (sf < 0.60)] = np.nan; front_exc = smooth(front_exc); back_exc = smooth(back_exc)
# our anchor = left-thigh section centre at the height that maps to f_ref = 0.62
f_our_anc = float(np.interp(F_ANC, [LM_REF[k] for k in keys], [LM_OUR[k] for k in keys])); z_anc = ZTOP-f_our_anc*HO; ia = zi(z_anc); c_anc = 0.5*(frl_o[ia]+bkl_o[ia])
fz = fo(zg); frz = f_ref_of(fz)
Wr = np.interp(frz, ff, W_ref_f)*HO; FEr = np.interp(frz, sf, front_exc)*HO; BEr = np.interp(frz, sf, back_exc)*HO
Dr = FEr+BEr; fr_t = c_anc+FEr; bk_t = c_anc-BEr
above = zg >= z_crotch-0.5; below = zg < z_crotch+0.5
RW_t = np.where(above, Wr/np.maximum(wt_o, 1e-3), np.nan); RW_l = np.where(below, Wr/np.maximum(wl_o, 1e-3), np.nan)
RD_t = np.where(above, Dr/np.maximum(fr_o-bk_o, 1e-3), np.nan); RD_l = np.where(below, Dr/np.maximum(frl_o-bkl_o, 1e-3), np.nan)
# clamps / keeps: bust band keeps the breast (front line and width), seam / shoulders -> 1, feet -> 1, bony hip / ribcage widths not below 0.95
bust_keep = ss((zg-(z_bust-10.5))/4.0)*ss(((z_bust+5.0)-zg)/3.0); top_keep = ss((zg-128.0)/5.0); foot_keep = ss((11.0-zg)/4.0)   # breast + inframammary band kept (the IMF underside folds under a width change); top_keep = ss((zg-128.0)/5.0); foot_keep = ss((11.0-zg)/4.0)
keep = np.clip(bust_keep+top_keep+foot_keep, 0, 1)
bony = np.maximum(ss((zg-84.0)/4.0)*ss((99.0-zg)/4.0), ss((zg-116.0)/3.0)*ss((124.0-zg)/3.0))   # hip / iliac band and lower ribcage
RW_t = np.nan_to_num(RW_t, nan=1.0); RW_t = np.where(RW_t < 1, np.maximum(RW_t, 0.80+0.15*bony), np.minimum(RW_t, 1.20))
RW_l = np.clip(np.nan_to_num(RW_l, nan=1.0), 0.80, 1.20); RD_t = np.clip(np.nan_to_num(RD_t, nan=1.0), 0.85, 1.25); RD_l = np.clip(np.nan_to_num(RD_l, nan=1.0), 0.85, 1.25)
low = ss((86.0-zg)/6.0)   # below the hip the merged-legs section width / depth depends on the stance gap (pose), not shape: the per-leg map takes over
keep_t = np.clip(keep+low, 0, 1)
RW_t = 1+(RW_t-1)*(1-keep_t); RD_t = 1+(RD_t-1)*(1-keep_t); RW_l = 1+(RW_l-1)*(1-foot_keep); RD_l = 1+(RD_l-1)*(1-foot_keep)
# the per-leg ratios are measurable only below the crotch: hold the crotch value up the thigh and fade to 1 toward the hip (no step at the crotch)
# per-leg ratios are valid only where the reference legs are separated (f_ref >= leg_valid_f): hold that value up to our crotch and fade to 1 above
z_lv = float(np.interp(leg_valid_f, [LM_REF[k] for k in keys], [LM_OUR[k] for k in keys])); z_lv = ZTOP-z_lv*HO; il = zi(z_lv)
up = zg > z_lv; hold = ss((z_crotch+16.0-zg)/(z_crotch+16.0-z_lv+1e-6))   # long fade up to the hip joint: the thigh depth change must melt into the glute / groin, no shelf at the crotch
RW_l = np.where(up, 1+(RW_l[il]-1)*hold, RW_l); RD_l = np.where(up, 1+(RD_l[il]-1)*hold, RD_l); plan_lv = z_lv
RW_t, RD_t, RW_l, RD_l = smooth(RW_t, 3), smooth(RD_t, 3), smooth(RW_l, 3), smooth(RD_l, 3)   # 1.5 cm sigma: no steps along z
fr_t = np.nan_to_num(fr_o)+(np.nan_to_num(fr_t)-np.nan_to_num(fr_o))*(1-keep); bk_t = np.nan_to_num(bk_o)+(np.nan_to_num(bk_t)-np.nan_to_num(bk_o))*(1-keep)
plan = {'leg_valid_z': plan_lv, 'H_our': HO, 'ztop': ZTOP, 'anchor_y': float(c_anc), 'anchor_z': float(z_anc), 'landmarks_ref': LM_REF, 'landmarks_our_z': {'bust': z_bust, 'navel': z_navel, 'crotch': z_crotch, 'knee': z_knee, 'calf': z_calf, 'ankle': z_ankle}, 'landmarks_our_f': LM_OUR,
        'z': zg.tolist(), 'f_ref': frz.tolist(), 'W_ref_cm': Wr.tolist(), 'W_torso_our': np.nan_to_num(wt_o).tolist(), 'W_leg_our': np.nan_to_num(wl_o).tolist(), 'RW_torso': RW_t.tolist(), 'RW_leg': RW_l.tolist(),
        'D_ref_cm': Dr.tolist(), 'D_torso_our': np.nan_to_num(fr_o-bk_o).tolist(), 'D_leg_our': np.nan_to_num(frl_o-bkl_o).tolist(), 'RD_torso': RD_t.tolist(), 'RD_leg': RD_l.tolist(),
        'front_our': np.nan_to_num(fr_o).tolist(), 'back_our': np.nan_to_num(bk_o).tolist(), 'front_leg_our': np.nan_to_num(frl_o).tolist(), 'back_leg_our': np.nan_to_num(bkl_o).tolist(),
        'front_target': fr_t.tolist(), 'back_target': bk_t.tolist(), 'keep': keep.tolist()}
json.dump(plan, open(OUTJ, 'w'))
print('CONTOUR landmarks ref f:', {k: round(float(v), 3) for k, v in LM_REF.items()}, '| ours f:', {k: round(float(v), 3) for k, v in LM_OUR.items()}, '| ours z:', {k: round(v, 1) for k, v in plan['landmarks_our_z'].items()}, '| anchor y %.2f at z %.1f' % (c_anc, z_anc))
for nm, zz in (('ribcage', 120), ('waist', 112), ('navel', 104), ('pelvis', 96), ('hip', 90), ('crotch', 82)):
    i = zi(zz); print('CONTOUR torso %-8s z %3d | width our %.1f ref %.1f ratio %.3f | depth our %.1f ref %.1f ratio %.3f | front %.1f -> %.1f  back %.1f -> %.1f' % (nm, zz, wt_o[i], Wr[i], RW_t[i], fr_o[i]-bk_o[i], Dr[i], RD_t[i], fr_o[i], fr_t[i], bk_o[i], bk_t[i]))
for nm, zz in (('upper thigh', 74), ('mid thigh', 64), ('low thigh', 56), ('knee', z_knee), ('calf', z_calf), ('low calf', 24), ('ankle', z_ankle)):
    i = zi(zz); print('CONTOUR leg   %-11s z %5.1f | width our %.1f ref %.1f ratio %.3f | depth our %.1f ref %.1f ratio %.3f' % (nm, zz, wl_o[i], Wr[i], RW_l[i], frl_o[i]-bkl_o[i], Dr[i], RD_l[i]))
# ---------------- plot (3 panels): width, depth, side lines
Wp, Hp = 1500, 560; IMG = np.full((Hp, Wp, 3), 0.12); COL = {'ref': (1.0, 0.75, 0.2), 'our': (0.4, 0.8, 1.0), 'tgt': (0.5, 1.0, 0.5)}
def panel(ix, series, ylim):
    px0 = ix*500+40; px1 = ix*500+480; py0, py1 = 40, 520
    for yy in np.linspace(ylim[0], ylim[1], 6):
        r = int(py1-(yy-ylim[0])/(ylim[1]-ylim[0])*(py1-py0)); IMG[r, px0:px1] = 0.25
    for zz in (z_ankle, z_calf, z_knee, z_crotch, z_navel, z_bust):
        cc = int(px0+(zz/140.0)*(px1-px0)); IMG[py0:py1, cc] = 0.35
    for lab, (vz, vv) in series.items():
        c = np.array(COL[lab.split(':')[0]])
        for zz, val in zip(vz, vv):
            if np.isnan(val): continue
            r = int(py1-(val-ylim[0])/(ylim[1]-ylim[0])*(py1-py0)); cc = int(px0+(zz/140.0)*(px1-px0))
            if py0 <= r < py1 and px0 <= cc < px1: IMG[r-1:r+1, cc-1:cc+1] = c
panel(0, {'our:t': (zg, np.where(above, wt_o, np.nan)), 'our:l': (zg, np.where(below, wl_o, np.nan)), 'ref': (zg, Wr)}, (0, 40))
panel(1, {'our:t': (zg, np.where(above, fr_o-bk_o, np.nan)), 'our:l': (zg, np.where(below, frl_o-bkl_o, np.nan)), 'ref': (zg, Dr)}, (0, 30))
panel(2, {'our:f': (zg, np.where(above, fr_o, frl_o)), 'our:b': (zg, np.where(above, bk_o, bkl_o)), 'ref:f': (zg, c_anc+FEr), 'ref:b': (zg, c_anc-BEr), 'tgt:f': (zg, np.where(above, fr_t, np.nan)), 'tgt:b': (zg, np.where(above, bk_t, np.nan))}, (-16, 20))
gi.save(OUTP, IMG[::-1].copy()); print('CONTOUR_OK')
