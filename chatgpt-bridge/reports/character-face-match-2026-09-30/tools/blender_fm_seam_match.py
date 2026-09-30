"""FACE-MATCH §6: head/body seam ALBEDO match (texture only, low frequency, detail preserved -- no painted band).
Materials already share master + post-bake parameters (MI_LK_Body_Baked_E); the remaining step at the collar seam is albedo.
  1. position maps of the head (skin material) and body UVs (bind pose, br_neutral)
  2. seam = the 92 head/body weld pairs; low-frequency mean linear colour of the head texels and of the VISIBLE body texels
     (not under the head collar) within SEAM_W cm of each seam point, smoothed along the seam
  3. head collar gain g = 1+(body/head-1)*falloff(distance to seam, 0..SEAM_FADE cm): the head converges to the body exactly at
     the seam and is untouched beyond SEAM_FADE cm (face unaffected); multiplicative -> pores / freckles / detail kept
usage: blender -b --factory-startup --python blender_fm_seam_match.py -- <pkg> <head BC png> <body BC png> <out png>"""
import bpy, sys, os, json, gzip
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
a = sys.argv[sys.argv.index('--')+1:]; PKG, HBC, BBC, OUT = a
E = lambda k, d: float(os.environ.get(k, d))
P = json.loads(gzip.open(PKG, 'rb').read()); NB = P['NB']; XA = np.asarray(P['br_neutral'], np.float32); XB, XH = XA[:NB], XA[NB:]
TB = np.asarray(P['body']['triangles']); TH = np.asarray(P['head']['triangles']); MIH = np.asarray(P['head']['material_ids'])
UVB = np.asarray(P['body']['uv'], np.float32); UVH = np.asarray(P['head']['uv'], np.float32)
W = np.asarray(P['weld_pairs']); SEAM = XH[W[:, 1]-NB]; print('seam pts', len(SEAM), 'z range', SEAM[:, 2].min(), SEAM[:, 2].max())
def posmap(X, T, UV, R, keep=None):
    PM = np.full((R, R, 3), np.nan, np.float32)
    for ti, t in enumerate(T):
        if keep is not None and not keep[ti]: continue
        px = np.stack([np.mod(UV[ti][:, 0], 1.0)*R, (1-np.mod(UV[ti][:, 1], 1.0))*R], 1); A, B, C = px
        x0, y0 = np.floor(px.min(0)).astype(int); x1, y1 = np.ceil(px.max(0)).astype(int); x0, y0 = max(x0, 0), max(y0, 0); x1, y1 = min(x1, R-1), min(y1, R-1)
        if x1 < x0 or y1 < y0: continue
        yy, xx = np.mgrid[y0:y1+1, x0:x1+1].astype(np.float32)+0.5; d = (B[1]-C[1])*(A[0]-C[0])+(C[0]-B[0])*(A[1]-C[1])
        if abs(d) < 1e-9: continue
        l1 = ((B[1]-C[1])*(xx-C[0])+(C[0]-B[0])*(yy-C[1]))/d; l2 = ((C[1]-A[1])*(xx-C[0])+(A[0]-C[0])*(yy-C[1]))/d; l3 = 1-l1-l2; m = (l1 >= -0.01) & (l2 >= -0.01) & (l3 >= -0.01)
        if m.any(): PM[y0:y1+1, x0:x1+1][m] = l1[m, None]*X[t[0]]+l2[m, None]*X[t[1]]+l3[m, None]*X[t[2]]
    return PM
def load(fn):
    im = bpy.data.images.load(fn); w, h = im.size; x = np.asarray(im.pixels[:], np.float32).reshape(h, w, im.channels)[..., :3].copy(); bpy.data.images.remove(im); return x   # bottom-up rows
def s2l(x): return np.where(x <= 0.04045, x/12.92, ((x+0.055)/1.055)**2.4)
def l2s(x): x = np.clip(x, 0, 1); return np.where(x <= 0.0031308, x*12.92, 1.055*x**(1/2.4)-0.055)
def sstep(x): x = np.clip(x, 0, 1); return x*x*(3-2*x)
R = 1024
PH = posmap(XH, TH, UVH, R, MIH == 0); PB = posmap(XB, TB, UVB, R)
Hc = load(HBC); Bc = load(BBC); fh = Hc.shape[0]//R; fb = Bc.shape[0]//R
Hs = s2l(Hc.reshape(R, fh, R, fh, 3).mean((1, 3))); Bs = s2l(Bc.reshape(R, fb, R, fb, 3).mean((1, 3)))            # low-frequency linear colour per posmap texel
def seam_dist(PM):
    ok = ~np.isnan(PM[..., 0]); p = PM[ok]; d = np.full(len(p), 1e9); idx = np.zeros(len(p), int)
    for i, s in enumerate(SEAM):
        di = np.linalg.norm(p-s, axis=1); m = di < d; d[m] = di[m]; idx[m] = i
    return ok, d, idx
okH, dH, iH = seam_dist(PH); okB, dB, iB = seam_dist(PB)
bvh = BVHTree.FromPolygons([Vector(v) for v in XH], [list(t) for t in TH[MIH == 0]])   # body texels hidden under the head collar are excluded
pb = PB[okB]; near = dB < E('SEAM_W', '1.5')
vis = np.ones(len(pb), bool)
for k in np.nonzero(near)[0]:
    loc, n_, fi, dd = bvh.find_nearest(Vector(pb[k].tolist()))
    if dd is not None and dd < 0.25: vis[k] = False
hcol = Hs[okH]; bcol = Bs[okB]; nS = len(SEAM); mh = np.zeros((nS, 3)); mb = np.zeros((nS, 3)); ch = np.zeros(nS); cb = np.zeros(nS)
sel = dH < E('SEAM_W', '1.5'); np.add.at(mh, iH[sel], hcol[sel]); np.add.at(ch, iH[sel], 1)
sel = near & vis; np.add.at(mb, iB[sel], bcol[sel]); np.add.at(cb, iB[sel], 1)
G = np.exp(-(np.linalg.norm(SEAM[:, None]-SEAM[None], axis=2)/E('SEAM_SIG', '2.5'))**2)                      # smoothing along the seam
mh = (G@mh)/np.maximum(G@ch, 1e-6)[:, None]; mb = (G@mb)/np.maximum(G@cb, 1e-6)[:, None]
ratio = np.clip(mb/np.maximum(mh, 1e-5)*np.array([E('SEAM_KR', '1'), E('SEAM_KG', '1'), E('SEAM_KB', '1')]), E('SEAM_MIN', '0.7'), E('SEAM_MAX', '1.3'))   # K: render calibration (lighting / scatter map differences)
print('texels head-side', int((dH < E('SEAM_W', '1.5')).sum()), 'body-side visible', int((near & vis).sum()), 'hidden', int((near & ~vis).sum()))
print('ratio body/head (lin) mean', np.round(ratio.mean(0), 3), 'min', np.round(ratio.min(0), 3), 'max', np.round(ratio.max(0), 3))
print('head mean', np.round(mh.mean(0), 4), 'body mean', np.round(mb.mean(0), 4))
fall = 1-sstep(dH/E('SEAM_FADE', '5.0')); gain = np.ones((R, R, 3), np.float32); gain[okH] = 1+(ratio[iH]-1)*fall[:, None]
def blur(m, r):
    k = r; c = np.cumsum(np.pad(m, ((k+1, k), (0, 0), (0, 0)), mode='edge'), 0); m = (c[2*k+1:]-c[:-2*k-1])/(2*k+1)
    c = np.cumsum(np.pad(m, ((0, 0), (k+1, k), (0, 0)), mode='edge'), 1); return (c[:, 2*k+1:]-c[:, :-2*k-1])/(2*k+1)
gain = blur(gain, 2)                                                                                         # soften texel steps (low frequency only)
gu = np.repeat(np.repeat(gain, fh, 0), fh, 1)
Lh = s2l(Hc)*gu; out = l2s(Lh); h, w = out.shape[:2]
im = bpy.data.images.new('seam', w, h, alpha=True); rgba = np.ones((h, w, 4), np.float32); rgba[..., :3] = out
im.pixels.foreach_set(rgba.ravel()); im.filepath_raw = OUT; im.file_format = 'PNG'; im.save()
gp = np.clip((gain-0.8)/0.4, 0, 1); im2 = bpy.data.images.new('g', R, R); r2 = np.ones((R, R, 4), np.float32); r2[..., :3] = gp; im2.pixels.foreach_set(r2.ravel()); im2.filepath_raw = OUT.replace('.png', '_gain.png'); im2.file_format = 'PNG'; im2.save()
json.dump({'ratio_mean': ratio.mean(0).tolist(), 'ratio_min': ratio.min(0).tolist(), 'ratio_max': ratio.max(0).tolist(), 'head_mean': mh.mean(0).tolist(), 'body_mean': mb.mean(0).tolist(), 'fade_cm': E('SEAM_FADE', '5.0'), 'band_cm': E('SEAM_W', '1.5')}, open(OUT.replace('.png', '_stats.json'), 'w'), indent=1)
print('SEAM_OK', OUT)
