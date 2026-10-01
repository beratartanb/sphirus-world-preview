"""CORRECTIVE pass: head / body seam SHADING match (no colour paint). Measured 2026-10-01 at the 92 weld edges: body SRMF specular
0.68 vs head 0.54, body roughness 0.49 vs head 0.69, and the body normal map is flat (no detail) along the neck border while the head
collar carries pore detail -> a specular / roughness step reads as a thin line in grazing light (the line vanishes in clay).
Head collar only (body textures untouched): SRMF specular + roughness converge to the visible body values at the seam (low frequency,
multiplicative, faded over SEAM_FADE cm); head normal detail fades toward flat at the seam (N_MIN strength at the weld, full at N_FADE cm).
usage: blender -b --factory-startup --python blender_cr_seam_shading.py -- <pkg> <head SRMF png> <body SRMF png> <head N png> <out dir> <tag>"""
import bpy, sys, os, json, gzip
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
a = sys.argv[sys.argv.index('--')+1:]; PKG, HSR, BSR, HN, OUTD, TAG = a
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
Hc = load(HSR); Bc = load(BSR); fh = Hc.shape[0]//R; fb = Bc.shape[0]//R
Hs = Hc.reshape(R, fh, R, fh, 3).mean((1, 3)); Bs = Bc.reshape(R, fb, R, fb, 3).mean((1, 3))      # data maps: no sRGB decode
def seam_dist(PM):
    ok = ~np.isnan(PM[..., 0]); p = PM[ok]; d = np.full(len(p), 1e9); idx = np.zeros(len(p), int)
    for i, s in enumerate(SEAM):
        di = np.linalg.norm(p-s, axis=1); m = di < d; d[m] = di[m]; idx[m] = i
    return ok, d, idx
okH, dH, iH = seam_dist(PH); okB, dB, iB = seam_dist(PB)
bvh = BVHTree.FromPolygons([Vector(v) for v in XH], [list(t) for t in TH[MIH == 0]])
pb = PB[okB]; near = dB < E('SEAM_W', '1.5'); vis = np.ones(len(pb), bool)
for k in np.nonzero(near)[0]:
    loc, n_, fi, dd = bvh.find_nearest(Vector(pb[k].tolist()))
    if dd is not None and dd < 0.25: vis[k] = False
nS = len(SEAM); mh = np.zeros((nS, 3)); mb = np.zeros((nS, 3)); ch = np.zeros(nS); cb = np.zeros(nS)
sel = dH < E('SEAM_W', '1.5'); np.add.at(mh, iH[sel], Hs[okH][sel]); np.add.at(ch, iH[sel], 1)
sel = near & vis; np.add.at(mb, iB[sel], Bs[okB][sel]); np.add.at(cb, iB[sel], 1)
G = np.exp(-(np.linalg.norm(SEAM[:, None]-SEAM[None], axis=2)/E('SEAM_SIG', '2.5'))**2)
mh = (G@mh)/np.maximum(G@ch, 1e-6)[:, None]; mb = (G@mb)/np.maximum(G@cb, 1e-6)[:, None]
ratio = np.clip(mb/np.maximum(mh, 1e-4), 0.5, 1.6); ratio[:, 2] = 1.0                                  # channel 2 (mask) untouched
print('SRMF head mean', np.round(mh.mean(0), 3), 'body mean', np.round(mb.mean(0), 3), 'ratio mean', np.round(ratio.mean(0), 3))
def blur(m, r):
    k = r; c = np.cumsum(np.pad(m, ((k+1, k), (0, 0), (0, 0)), mode='edge'), 0); m = (c[2*k+1:]-c[:-2*k-1])/(2*k+1)
    c = np.cumsum(np.pad(m, ((0, 0), (k+1, k), (0, 0)), mode='edge'), 1); return (c[:, 2*k+1:]-c[:, :-2*k-1])/(2*k+1)
fall = 1-sstep(dH/E('SEAM_FADE', '3.0')); gain = np.ones((R, R, 3), np.float32); gain[okH] = 1+(ratio[iH]-1)*fall[:, None]; gain = blur(gain, 2)
def save(arr, fn, data):
    h, w = arr.shape[:2]; im = bpy.data.images.new('o', w, h, alpha=True); rgba = np.ones((h, w, 4), np.float32); rgba[..., :3] = np.clip(arr, 0, 1)
    if data: im.colorspace_settings.name = 'Non-Color'
    im.pixels.foreach_set(rgba.ravel()); im.filepath_raw = os.path.join(OUTD, fn); im.file_format = 'PNG'; im.save(); print('saved', fn, w, h)
gu = np.repeat(np.repeat(gain, fh, 0), fh, 1); save(Hc*gu, f'T_LK_Head_SRMF_{TAG}.png', True)
Nn = load(HN); fn_ = Nn.shape[0]//R if Nn.shape[0] >= R else 1
st = np.ones((R, R), np.float32); st[okH] = E('N_MIN', '0.3')+(1-E('N_MIN', '0.3'))*sstep(dH/E('N_FADE', '1.5')); st = blur(st[..., None].repeat(3, -1), 2)[..., 0]
if Nn.shape[0] < R: st = st.reshape(Nn.shape[0], R//Nn.shape[0], Nn.shape[0], R//Nn.shape[0]).mean((1, 3)); su = st
else: su = np.repeat(np.repeat(st, fn_, 0), fn_, 1)
v = Nn*2-1; flat = np.array([0, 0, 1.0], np.float32); v = flat+(v-flat)*su[..., None]; v /= np.maximum(np.linalg.norm(v, axis=-1, keepdims=True), 1e-6)
save(v*0.5+0.5, f'T_LK_Head_N_{TAG}.png', True)
json.dump({'srmf_head_mean': mh.mean(0).tolist(), 'srmf_body_mean': mb.mean(0).tolist(), 'ratio_mean': ratio.mean(0).tolist(), 'seam_fade_cm': E('SEAM_FADE', '3.0'), 'n_min': E('N_MIN', '0.3'), 'n_fade_cm': E('N_FADE', '1.5')}, open(os.path.join(OUTD, f'seam_shading_{TAG}.json'), 'w'), indent=1)
print('SEAM_SHADING_OK')
