"""pass BB2: brow centreline / thickness / extent per column for OURS (exact strand mask: no-brow minus brow capture) and the REFERENCE
(darkness-weighted centroid inside a fixed window above each eye), in the solved front reference frame; converts to model |x| / z (cm)
with the reference-camera projection and writes a mapping table + a gridded debug crop with both centrelines and +-1 sigma edges.
usage: blender -b --python blender_g11bb_browfit.py -- <ours_brow.png> <ours_nobrow.png> <ref.png> <face npy> <out.json> <debug prefix>"""
import bpy, sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930')); from gd_common import topix
a = sys.argv[sys.argv.index('--')+1:]
def load(p):
    im = bpy.data.images.load(os.path.abspath(p)); w, h = im.size; return np.nan_to_num(np.array(im.pixels[:], np.float32).reshape(h, w, 4)[::-1][..., :3])
def blur(Z, s):
    r = int(3*s)+1; k = np.exp(-0.5*(np.arange(-r, r+1)/s)**2); k /= k.sum()
    Z = np.apply_along_axis(lambda v: np.convolve(v, k, 'same'), 1, Z); return np.apply_along_axis(lambda v: np.convolve(v, k, 'same'), 0, Z)
lum = lambda A: A @ np.array([0.3, 0.59, 0.11])
OW, ON, RF = load(a[0]), load(a[1]), load(a[2]); X = np.load(a[3])[:24049]; MX = -0.23
Dm = np.clip(blur(lum(ON)-lum(OW), 1.5), 0, None); Lr = blur(lum(RF), 1.5)
Y0, Y1 = 340, 388
def stats(wcol):
    s = wcol.sum()
    if s <= 1e-6: return None
    yy = np.arange(Y0, Y1); c = (yy*wcol).sum()/s; sd = np.sqrt(((yy-c)**2*wcol).sum()/s); return c, sd, s
ours, ref = {}, {}
for x in range(240, 590):
    st = stats(np.where(Dm[Y0:Y1, x] > 0.02, Dm[Y0:Y1, x], 0)); 
    if st: ours[x] = st
    col = Lr[Y0:Y1, x]; hi = np.percentile(Lr[Y0-22:Y0+4, x], 60); dk = np.clip(hi-col-0.02, 0, None)
    st = stats(dk)
    if st: ref[x] = st
# coverage-based extents (strength >= 25% of the brow's median strength), per side
cx = 413.0; out = {'sides': {}}
# px -> model: fit |x| (cm) and z (cm) as linear functions of px from face vertices in the brow area
B = X[(np.abs(X[:, 0]-MX) < 6.5) & (X[:, 2] > 162.8) & (X[:, 2] < 166.5) & (X[:, 1] > 9.0)]; Q = topix('front', B)
Ax = np.c_[Q[:, 0], np.ones(len(Q))]; kx = np.linalg.lstsq(Ax, B[:, 0], rcond=None)[0]; Az = np.c_[Q[:, 1], np.ones(len(Q))]; kz = np.linalg.lstsq(Az, B[:, 2], rcond=None)[0]
out['px_to_x'] = kx.tolist(); out['px_to_z'] = kz.tolist()
for side, sel in (('imgL', lambda x: x < cx), ('imgR', lambda x: x >= cx)):
    so = {x: v for x, v in ours.items() if sel(x)}; sr = {x: v for x, v in ref.items() if sel(x)}
    def ext(d):
        m = np.median([v[2] for v in d.values()]); xs = sorted(x for x, v in d.items() if v[2] >= 0.25*m); return xs[0], xs[-1]
    eo, er = ext(so), ext(sr)
    rows = []
    for x in range(min(eo[0], er[0]), max(eo[1], er[1])+1):
        rows.append([x, *(so[x][:2] if x in so else (None, None)), *(sr[x][:2] if x in sr else (None, None))])
    out['sides'][side] = {'ours_extent_px': eo, 'ref_extent_px': er, 'rows': rows}
json.dump(out, open(a[4], 'w'))
for side, d in out['sides'].items():
    print('FIT', side, 'ours x %d..%d ref x %d..%d' % (*d['ours_extent_px'], *d['ref_extent_px']))
    for r in d['rows'][::8]:
        f = lambda v: '%6.1f' % v if v is not None else '   -  '
        print('FITROW x%d ours c%s sd%s | ref c%s sd%s' % (r[0], f(r[1]), f(r[2]), f(r[3]), f(r[4])))
for nm, IMG in (('ours', OW), ('ref', RF)):
    O = IMG.copy()
    for d, col in ((ours, (0.1, 0.9, 1.0)), (ref, (1, 0, 1))):
        for x, (c, sd, s) in d.items():
            for yv in (c, c-sd, c+sd):
                yi = int(round(yv))
                if 0 <= yi < O.shape[0]: O[yi, x] = col
    S = O[330:400, 240:590]; S = np.repeat(np.repeat(S, 4, 0), 4, 1); S4 = np.concatenate([S, np.ones(S.shape[:2]+(1,), np.float32)], -1)[::-1]
    o = bpy.data.images.new('d', S4.shape[1], S4.shape[0]); o.pixels.foreach_set(np.ascontiguousarray(S4).ravel()); o.filepath_raw = os.path.abspath(a[5]+'_'+nm+'.png'); o.file_format = 'PNG'; o.save()
print('FIT px_to_x', np.round(kx, 4).tolist(), 'px_to_z', np.round(kz, 4).tolist())
