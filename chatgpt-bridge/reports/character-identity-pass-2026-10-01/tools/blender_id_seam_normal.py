"""IDENTITY pass §20: head/body seam SHADING fix in texture space. The grazing-light seam line is a normal-map feature (baked
collar-band edges / groove texels next to the head UV border and the body's neck border), not albedo and not vertex normals
(measured: vertex-normal override at the 92 weld vertices and matched roughness left the line unchanged). Both normal maps are
blended toward flat (0.5, 0.5, 1) with a smooth 3D distance-to-seam falloff (full at the seam, none beyond SEAM_N_FADE cm):
no band edge, detail preserved away from the seam. Also returns island padding (texels outside the UV islands get the nearest
island value) so bilinear / mip sampling at the border never reads background.
usage: blender -b -P blender_id_seam_normal.py -- <head N png> <body N png> <out head png> <out body png>"""
import bpy, sys, os
import numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930')); from id_common import *
a = sys.argv[sys.argv.index('--')+1:]; HN, BN, OH, OB = a; E = lambda k, d: float(os.environ.get(k, d))
P = pkg(); NB = P['NB']; XA = np.asarray(P['br_neutral'], np.float32); XB, XH = XA[:NB], XA[NB:]
TB = np.asarray(P['body']['triangles']); TH = np.asarray(P['head']['triangles']); MIH = np.asarray(P['head']['material_ids'])
UVB = np.asarray(P['body']['uv'], np.float32); UVH = np.asarray(P['head']['uv'], np.float32); W = np.asarray(P['weld_pairs']); SEAM = XH[W[:, 1]-NB]
def posmap(X, T, UV, R, keep=None):
    PM = np.full((R, R, 3), np.nan, np.float32)
    for ti, t in enumerate(T):
        if keep is not None and not keep[ti]: continue
        px = np.stack([np.mod(UV[ti][:, 0], 1.0)*R, (1-np.mod(UV[ti][:, 1], 1.0))*R], 1); A, B, C = px
        x0, y0 = np.floor(px.min(0)).astype(int); x1, y1 = np.ceil(px.max(0)).astype(int); x0, y0 = max(x0, 0), max(y0, 0); x1, y1 = min(x1, R-1), min(y1, R-1)
        if x1 < x0 or y1 < y0: continue
        yy, xx = np.mgrid[y0:y1+1, x0:x1+1].astype(np.float32)+0.5; d = (B[1]-C[1])*(A[0]-C[0])+(C[0]-B[0])*(A[1]-C[1])
        if abs(d) < 1e-9: continue
        l1 = ((B[1]-C[1])*(xx-C[0])+(C[0]-B[0])*(yy-C[1]))/d; l2 = ((C[1]-A[1])*(xx-C[0])+(A[0]-C[0])*(yy-C[1]))/d; l3 = 1-l1-l2; m = (l1 >= -0.02) & (l2 >= -0.02) & (l3 >= -0.02)
        if m.any(): PM[y0:y1+1, x0:x1+1][m] = l1[m, None]*X[t[0]]+l2[m, None]*X[t[1]]+l3[m, None]*X[t[2]]
    return PM
def load(fn):
    im = bpy.data.images.load(fn); w, h = im.size; x = np.asarray(im.pixels[:], np.float32).reshape(h, w, im.channels)[..., :3].copy(); bpy.data.images.remove(im); return x   # bottom-up rows
def save(arr, fn):
    h, w = arr.shape[:2]; im = bpy.data.images.new('n', w, h, alpha=True); im.colorspace_settings.name = 'Non-Color'
    rgba = np.ones((h, w, 4), np.float32); rgba[..., :3] = np.clip(arr, 0, 1); im.pixels.foreach_set(rgba.ravel()); im.filepath_raw = fn; im.file_format = 'PNG'; im.save(); print('saved', fn)
def sstep(v): v = np.clip(v, 0, 1); return v*v*(3-2*v)
def pad(img, ok, it=24):
    o = img.copy(); m = ok.copy()
    for _ in range(it):
        acc = np.zeros_like(o); cnt = np.zeros(m.shape, np.float32)
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            mm = np.roll(m, (dy, dx), (0, 1)); acc += np.roll(o*m[..., None], (dy, dx), (0, 1)); cnt += mm
        new = (~m) & (cnt > 0); o[new] = acc[new]/cnt[new][:, None]; m = m | new
    return o
FADE = E('SEAM_N_FADE', '2.5'); R = 1024
for src, dst, X, T, UV, keep in ((HN, OH, XH, TH, UVH, MIH == 0), (BN, OB, XB, TB, UVB, None)):
    Nm = load(src); n = Nm.shape[0]; PM = posmap(X, T, UV, R, keep); ok = ~np.isnan(PM[..., 0])
    d = np.full((R, R), 99.0, np.float32); p = PM[ok]; dd = np.full(len(p), 99.0, np.float32)
    for s in SEAM: dd = np.minimum(dd, np.linalg.norm(p-s, axis=1))
    d[ok] = dd; w = 1-sstep(d/FADE)                                                                    # 1 at the seam -> 0 at FADE cm
    f = n//R; wu = np.repeat(np.repeat(w, f, 0), f, 1)[:n, :n]; oku = np.repeat(np.repeat(ok, f, 0), f, 1)[:n, :n]
    flat = np.array([0.5, 0.5, 1.0], np.float32); out = Nm*(1-wu[..., None])+flat*wu[..., None]
    out = pad(out, oku, 16 if n <= 1024 else 32)
    save(out, dst); print('SEAMN', os.path.basename(dst), 'texels blended', int((wu > 0.05).sum()), 'res', n)
print('SEAM_NORMAL_OK')
