"""GD11 refinement D: where does the long back-of-head profile come from? Orthographic side silhouettes (y-z plane, x ignored) of
  head (DNA-order npy, skin), main hair WITHOUT the bun region, bun region (points inside BUN_K * R_BUN of the bun centre), loose strands,
drawn as coloured layers in one fixed frame, plus a table of back extents (most negative y) per height band and the hair stand-off behind the
skull (hair back y - skull back y). Strand points are taken as built (builder head = SPH_HEAD_NPY), with the builder head drawn too.
usage: blender -b -P blender_g11rd_backsil.py -- <out.png> <strands.npz> <build_head.npy> <face_head.npy> <bun_cx,cy,cz> <bun_r> [<strands2.npz> ...]"""
import bpy, sys, os, json, numpy as np
a = sys.argv[sys.argv.index('--')+1:]; OUT, SN, BH, FH = a[0], a[1], a[2], a[3]; BC = np.array([float(v) for v in a[4].split(',')]); BR = float(a[5]); EXTRA = a[6:]
NH = 24049; K = float(os.environ.get('BUN_K', '1.45'))
Y0, Y1, Z0, Z1, S = -16.0, 18.0, 140.0, 178.0, 24   # cm frame, px per cm
W, H = int((Y1-Y0)*S), int((Z1-Z0)*S)
def raster(P, img, col, r=0):
    yy = ((P[:, 1]-Y0)*S).astype(int); zz = ((Z1-P[:, 2])*S).astype(int); ok = (yy >= 0) & (yy < W) & (zz >= 0) & (zz < H)
    m = np.zeros((H, W), bool); m[zz[ok], yy[ok]] = True
    for _ in range(r): m = m | np.roll(m, 1, 0) | np.roll(m, -1, 0) | np.roll(m, 1, 1) | np.roll(m, -1, 1)
    return m
def back(P, z0, z1):
    s = P[(P[:, 2] >= z0) & (P[:, 2] < z1)]; return float(s[:, 1].min()) if len(s) else None
def dense(Pl, n=3):   # densify strand polylines so silhouettes are solid
    t = np.linspace(0, 1, n, endpoint=False)[None, None, :, None]; A = Pl[:, :-1, None, :]; B_ = Pl[:, 1:, None, :]; return (A+(B_-A)*t).reshape(-1, 3)
d = np.load(SN); M = d['main']; L = d['loose']
dist = np.linalg.norm(M-BC, axis=2); inbun = dist < K*BR
Mp = M.reshape(-1, 3); bunP = M[inbun]; mainP = M[~inbun]
hb = np.load(BH)[:NH]; hf = np.load(FH)[:NH]
img = np.full((H, W, 3), 0.18, np.float32)
layers = [l for l in [('main', dense(np.where(inbun[..., None], np.nan, M)).astype(np.float32), (0.85, 0.45, 0.15)), ('bun', bunP, (0.95, 0.85, 0.2)), ('loose', dense(L), (0.6, 0.9, 1.0))] if not (os.environ.get('NOLOOSE') and l[0] == 'loose')]
for nm, P, col in layers:
    P = P[~np.isnan(P).any(1)]; m = raster(P, img, col, 1); img[m] = col
for nm, P, col in (('build head', hb, (0.55, 0.55, 0.55)), ('face head', hf, (0.85, 0.85, 0.85))):
    m = raster(P, img, col, 0); img[m] = col if nm == 'face head' else img[m]*0.5+np.array(col)*0.5
# grid lines every 2 cm in y (back) for reading
for yv in np.arange(-16, 0, 2.0): img[:, int((yv-Y0)*S)] = img[:, int((yv-Y0)*S)]*0.6+0.4*np.array([0.3, 0.3, 0.6])
tab = {}
for z0 in np.arange(150, 176, 2.0):
    z1 = z0+2; hs = back(hf, z0, z1); hm = back(mainP[~np.isnan(mainP).any(1)], z0, z1); bu = back(bunP, z0, z1); lo = back(L.reshape(-1, 3), z0, z1)
    tab[f'{z0:.0f}-{z1:.0f}'] = {'skull': None if hs is None else round(hs, 2), 'main': None if hm is None else round(hm, 2), 'bun': None if bu is None else round(bu, 2), 'loose': None if lo is None else round(lo, 2),
                                 'main_standoff': None if (hs is None or hm is None) else round(hs-hm, 2)}
res = {'bun_centre': BC.tolist(), 'bun_r': BR, 'bun_points_frac': round(float(inbun.mean()), 3), 'skull_back_min_y': round(float(hf[:, 1].min()), 2), 'build_head_back_min_y': round(float(hb[:, 1].min()), 2),
       'hair_back_min_y': round(float(np.nanmin(M[..., 1])), 2), 'bands': tab}
for ex in EXTRA:   # outline of another strands set in white for comparison
    M2 = np.load(ex)['main']; m = raster(dense(M2), img, (1, 1, 1), 1); e = m & ~(np.roll(m, 1, 0) & np.roll(m, -1, 0) & np.roll(m, 1, 1) & np.roll(m, -1, 1)); img[e] = (1, 1, 1)
    res['extra_'+os.path.basename(os.path.dirname(ex))+'_hair_back_min_y'] = round(float(M2[..., 1].min()), 2)
o = bpy.data.images.new('o', W, H); rgba = np.ones((H, W, 4), np.float32); rgba[..., :3] = img
o.pixels.foreach_set(np.ascontiguousarray(rgba[::-1]).ravel()); o.filepath_raw = os.path.abspath(OUT); o.file_format = 'PNG'; o.save(); print('BACKSIL', json.dumps(res))
