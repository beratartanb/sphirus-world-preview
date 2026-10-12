"""GD44: silhouette LINE SHAPE analysis ("hatlar") — the shape of the body's outline between anatomical landmarks, ours vs the private
reference, scale-free and width-free: for each line segment between two landmarks the contour is compared as its SAG from the chord
(perpendicular offset, in our cm), so the anthropometrically verified widths (chord endpoints) stay ours while the curvature of the line
(where a muscle bulges, where a hollow sits) is compared with the reference. Residual = ref sag - our sag (+ = the reference bulges further out).
Front view (torso side line, outer / inner thigh, outer / inner calf) and side view (back line, front line; the reference front line is
contaminated by the hanging hand between navel and mid thigh and is skipped there). Landmark alignment as in gd4x_contour (bust, navel,
crotch, knee, calf, ankle). Writes <out.json> (per-segment residual profiles on our z) and <out.png> (overlay plots).
usage: blender -b --python gd44_sag.py -- <libdir> <pkg> <lk> <extra|-> <refsil.json> <shape_plan.json> <label> <out.json> <out.png>"""
import sys, os, json, numpy as np
sys.path.insert(0, sys.argv[sys.argv.index('--')+1]); from gd44_lib import Body, ss
sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD13_Identity_20261009/tools')); import gd13_img as gi
a = sys.argv[sys.argv.index('--')+2:]; PKG, LKJ, EXTRA, REFJ, PLAN, LAB, OUTJ, OUTP = a[:8]
B = Body(PKG, LKJ, extra=None if EXTRA == '-' else EXTRA); XR = B.XR; x, y, z = XR.T; HO, ZTOP = B.H, B.ZTOP
W8 = B.P['weights']; clav = np.asarray([sum(w for b_, w in W8[v].items() if b_.startswith('clavicle')) for v in range(B.NB)]); arm = B.arm-clav
pl = json.load(open(PLAN)); LMz = pl['landmarks_our_z']; LMf = pl['landmarks_ref']; z_crotch = LMz['crotch']
noarm = (arm < 0.3) & (B.hand < 0.1); torso = noarm; legL = noarm & (x > 0)
def smooth(v, s=3):
    v = np.asarray(v, float); out = v.copy(); ok = ~np.isnan(v); idx = np.arange(len(v))
    if ok.sum() > 2: out[~ok] = np.interp(idx[~ok], idx[ok], v[ok])
    k = np.exp(-0.5*(np.arange(-3*s, 3*s+1)/s)**2); k /= k.sum(); return np.convolve(np.pad(out, 3*s, mode='edge'), k, 'valid')
def medf(v, r=3):
    v = np.asarray(v, float); out = v.copy()
    for i in range(len(v)):
        w = v[max(0, i-r):i+r+1]; w = w[~np.isnan(w)]; out[i] = np.median(w) if len(w) else np.nan
    return out
zg = np.arange(6.0, 136.0, 0.5)
ET = np.array([B.extents(zz, torso) if zz >= z_crotch-0.5 else (np.nan,)*4 for zz in zg]); EL = np.array([B.extents(zz, legL) if zz < z_crotch+0.5 else (np.nan,)*4 for zz in zg])
our = {'half_w': smooth(0.5*(ET[:, 2]-ET[:, 3]), 2), 'leg_out': smooth(EL[:, 2], 2), 'leg_in': smooth(EL[:, 3], 2), 'front': smooth(np.where(np.isnan(ET[:, 0]), EL[:, 0], ET[:, 0]), 2), 'back': smooth(np.where(np.isnan(ET[:, 1]), EL[:, 1], ET[:, 1]), 2)}
# ---------------- reference rows -> our cm on our z (landmark-aligned)
R = json.load(open(REFJ)); keys = ['top', 'bust', 'navel', 'crotch', 'knee', 'calf', 'ankle', 'sole']
fo = lambda zz: (ZTOP-zz)/HO; LM_OUR = {'top': 0.0, 'sole': 1.0}; LM_OUR.update({k: fo(LMz[k]) for k in ('bust', 'navel', 'crotch', 'knee', 'calf', 'ankle')})
LM_REF = {'top': 0.0, 'sole': 1.0}; LM_REF.update({k: LMf[k] for k in ('bust', 'navel', 'crotch', 'knee', 'calf', 'ankle')})
f_ref_of = lambda f_our: np.interp(f_our, [LM_OUR[k] for k in keys], [LM_REF[k] for k in keys])
def ref_rows(view):
    v = R[view]; rows = v['rows']; n = len(rows); f = (np.arange(n)+0.5)/v['height_px']
    x0 = np.array([np.nan if r is None else r[0] for r in rows], float); x1 = np.array([np.nan if r is None else r[1] for r in rows], float); return f, x0, x1, v
ff, fx0, fx1, fv = ref_rows('front'); Hf = fv['height_px']; axf = fv['axis_x']; cmf = HO/Hf
sf, sx0, sx1, sv = ref_rows('side'); Hs = sv['height_px']; cms = HO/Hs
fw = 0.5*(fx1-fx0)*cmf; merged = (ff > LM_REF['crotch']) & (fx0 < axf) & (fx1 > axf); fw[merged] = np.nan
leg_valid_f = float(ff[(ff > LM_REF['crotch']) & ~merged & ~np.isnan(fx0)].min())
# reference leg lines (A-stance, legs separated below leg_valid_f): outer = run edge away from the axis; the run stored is the one containing / nearest the axis -> for the
# left leg (image right of the axis) inner = x0, outer = x1 when x0 > axf; when the run is the right leg (x1 < axf) mirror it
leg_out = np.full(len(ff), np.nan); leg_in = np.full(len(ff), np.nan)
for i in range(len(ff)):
    if ff[i] <= leg_valid_f or np.isnan(fx0[i]): continue
    if fx0[i] >= axf: leg_in[i] = (fx0[i]-axf)*cmf; leg_out[i] = (fx1[i]-axf)*cmf
    elif fx1[i] <= axf: leg_in[i] = (axf-fx1[i])*cmf; leg_out[i] = (axf-fx0[i])*cmf
F_ANC = 0.62; anc = (sf >= F_ANC-0.01) & (sf <= F_ANC+0.01); anchor_x = float(np.nanmean(0.5*(sx0[anc]+sx1[anc])))
front_r = (anchor_x-sx0)*cms; back_r = (sx1-anchor_x)*cms; front_r[(sf > 0.395) & (sf < 0.60)] = np.nan
def ref_on_z(fr, vals):
    vals = medf(vals); out = np.full(len(zg), np.nan)
    for i, zz in enumerate(zg):
        fq = f_ref_of(fo(zz)); k = np.argmin(np.abs(fr-fq))
        if abs(fr[k]-fq) < 0.004 and not np.isnan(vals[k]): out[i] = vals[k]
    return smooth(out, 2) if (~np.isnan(out)).sum() > 3 else out
ref = {'half_w': ref_on_z(ff, fw), 'leg_out': ref_on_z(ff, leg_out), 'leg_in': ref_on_z(ff, leg_in), 'front': ref_on_z(sf, front_r), 'back': ref_on_z(sf, back_r)}
# our side lines relative to OUR thigh anchor (section centre at the aligned height) so that the forward lean of the reference does not enter
z_anc = float(ZTOP-HO*np.interp(F_ANC, [LM_REF[k] for k in keys], [LM_OUR[k] for k in keys])); i_anc = int(np.argmin(np.abs(zg-z_anc)))
our_anchor = 0.5*(our['front'][i_anc]+our['back'][i_anc]); our['front_rel'] = our['front']-our_anchor; our['back_rel'] = our_anchor-our['back']
# ---------------- segments: (line key ours, line key ref, z_top, z_bottom, name, sign: +1 = outward is +value)
zk, zc_, zcalf, zank = LMz['knee'], z_crotch, LMz['calf'], LMz['ankle']
SEG = [('half_w', 'half_w', 132.0, 110.0, 'torso_armpit_waist'), ('half_w', 'half_w', 110.0, 90.0, 'torso_waist_hip'), ('leg_out', 'leg_out', 88.0, zk, 'thigh_outer'), ('leg_in', 'leg_in', zc_-2.0, zk, 'thigh_inner'),
       ('leg_out', 'leg_out', zk, zank, 'calf_outer'), ('leg_in', 'leg_in', zk, zank, 'calf_inner'), ('back_rel', 'back', 132.0, 108.0, 'back_upper_lumbar'), ('back_rel', 'back', 108.0, 86.0, 'back_lumbar_glute'),
       ('back_rel', 'back', 86.0, zk, 'back_glute_knee'), ('back_rel', 'back', zk, zank, 'back_calf'), ('front_rel', 'front', 132.0, 112.0, 'front_chest_waist'), ('front_rel', 'front', 78.0, zk, 'front_thigh'), ('front_rel', 'front', zk, zank, 'front_shin')]
def sag(line, z0, z1, n=25):
    zs = np.linspace(z0, z1, n); v = np.interp(zs, zg, line); ok = ~np.isnan(v)
    if ok.sum() < n*0.6: return zs, np.full(n, np.nan)
    v = np.where(ok, v, np.interp(zs, zs[ok], v[ok])); chord = v[0]+(v[-1]-v[0])*(zs-z0)/(z1-z0); return zs, v-chord
res = {'label': LAB, 'segments': {}}; lines_txt = []
for ko, kr, z0, z1, nm in SEG:
    zs, so = sag(our[ko], z0, z1); _, sr = sag(ref[kr], z0, z1); d = sr-so
    if np.isnan(d).all(): res['segments'][nm] = None; lines_txt.append('SAG %-20s n/a (reference line missing here)' % nm); continue
    res['segments'][nm] = {'z': [round(float(v), 2) for v in zs], 'sag_our': [round(float(v), 2) for v in so], 'sag_ref': [round(float(v), 2) for v in sr], 'residual': [round(float(v), 2) for v in d]}
    k = int(np.nanargmax(np.abs(d))); lines_txt.append('SAG %-20s max|res| %5.2f cm at z %5.1f (ref %+5.2f / our %+5.2f)  mean|res| %4.2f' % (nm, abs(d[k]), zs[k], sr[k], so[k], np.nanmean(np.abs(d))))
json.dump(res, open(OUTJ, 'w'), indent=1); print('\n'.join(lines_txt))
# ---------------- overlay plot: half-width (front), leg outer / inner, side front / back: ours (white) vs reference (orange), z vertical
Wp, Hp = 1500, 1300; img = np.zeros((Hp, Wp, 3)); img[:] = 0.08
def plot(col0, col1, zz, vals, color, xscale=14.0, xoff=0.0):
    for i in range(len(zz)-1):
        if np.isnan(vals[i]) or np.isnan(vals[i+1]): continue
        p0 = (int(col0+(vals[i]+xoff)*xscale), int(Hp-20-(zz[i]-4)*9.5)); p1 = (int(col0+(vals[i+1]+xoff)*xscale), int(Hp-20-(zz[i+1]-4)*9.5))
        n = max(abs(p1[0]-p0[0]), abs(p1[1]-p0[1]), 1)
        for t in np.linspace(0, 1, n+1):
            px, py = int(p0[0]+(p1[0]-p0[0])*t), int(p0[1]+(p1[1]-p0[1])*t)
            if 0 <= px < Wp and 0 <= py < Hp: img[py, px] = color; img[py, min(px+1, Wp-1)] = color
WH, OR = (0.95, 0.95, 0.95), (1.0, 0.6, 0.15)
plot(60, 0, zg, our['half_w'], WH); plot(60, 0, zg, ref['half_w'], OR)                 # torso half width
plot(60, 0, zg, our['leg_out'], WH); plot(60, 0, zg, ref['leg_out'], OR); plot(60, 0, zg, our['leg_in'], WH); plot(60, 0, zg, ref['leg_in'], OR)
plot(800, 0, zg, our['front_rel'], WH, xoff=20); plot(800, 0, zg, ref['front'], OR, xoff=20); plot(800, 0, zg, -our['back_rel'], WH, xoff=20); plot(800, 0, zg, -ref['back'], OR, xoff=20)
gi.save(OUTP, img); print('SAG_PLOT', OUTP)
