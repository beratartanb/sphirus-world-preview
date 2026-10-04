"""GD11 refinement E: hair FLOW diagnostics in one fixed orthographic side frame (y-z, character right side, face to the right).
 - guide strands: main strands whose root lies in a slab (|x - PART_X| < 1.0 = midline, or x ~ +-3.2 = part side bands), coloured by root
   position front->back (red = hairline ... blue = crown/back); drawn as thin polylines over the skull silhouette (grey)
 - envelope profile: in the slab |x| < 2, for each angle th around the head centre HC (0 = vertex, + front, - back) the outer hair radius minus
   the scalp radius = stand-off curve s(th); printed per 5 deg and drawn as a strip chart under the image (one colour per strands file)
usage: blender -b -P blender_g11re_flow.py -- <out.png> <head.npy> <label1>=<strands1.npz> [<label2>=<strands2.npz> ...]"""
import bpy, sys, os, json, math, numpy as np
a = sys.argv[sys.argv.index('--')+1:]; OUT, HEAD = a[0], a[1]; SETS = [x.split('=', 1) for x in a[2:]]
NH = 24049; HC = np.array([0.0, 2.5, 160.5]); PX = -0.25
Y0, Y1, Z0, Z1, S = -16.0, 18.0, 146.0, 180.0, 22
W, H = int((Y1-Y0)*S), int((Z1-Z0)*S); CH = 260
hd = np.load(HEAD)[:NH]
def pix(P): return ((P[..., 1]-Y0)*S), ((Z1-P[..., 2])*S)
def line(img, p, q, col):
    n = int(max(abs(q[0]-p[0]), abs(q[1]-p[1])))+1
    for t in np.linspace(0, 1, n):
        x, y = int(p[0]+(q[0]-p[0])*t), int(p[1]+(q[1]-p[1])*t)
        if 0 <= x < W and 0 <= y < H: img[y, x] = col
def theta(P): return np.degrees(np.arctan2(P[..., 1]-HC[1], P[..., 2]-HC[2]))
def radius(P): return np.linalg.norm((P-HC)[..., 1:], axis=-1)
TH = np.arange(-110, 86, 5.0)
SLX = [float(v) for v in os.environ.get('SLAB', '0,2.0').split(',')]; inslab = lambda X: np.abs(np.abs(X[..., 0]-PX)-SLX[0]) < SLX[1]
sl = inslab(hd); th_h = theta(hd[sl]); r_h = radius(hd[sl])
scalp = np.array([r_h[np.abs(th_h-t) < 2.5].max() if (np.abs(th_h-t) < 2.5).any() else np.nan for t in TH])
panels = []; table = {}; cols = [(1.0, 0.55, 0.2), (0.3, 0.85, 1.0), (0.6, 1.0, 0.4), (1.0, 0.4, 0.8)]
chart = np.full((CH, W*len(SETS) if False else W, 3), 0.12, np.float32)
for si, (lab, fn) in enumerate(SETS):
    M = np.load(fn)['main']; img = np.full((H, W, 3), 0.16, np.float32)
    hy, hz = pix(hd); ok = (hy >= 0) & (hy < W) & (hz >= 0) & (hz < H); img[hz[ok].astype(int), hy[ok].astype(int)] = (0.42, 0.42, 0.42)
    root = M[:, 0]; rng = np.random.default_rng(1)
    for band, xc, wd, nmax in (('mid', PX, 1.0, 260), ('partL', PX+3.2, 0.6, 120), ('partR', PX-3.2, 0.6, 120)):
        idx = np.nonzero(np.abs(root[:, 0]-xc) < wd)[0]
        if len(idx) > nmax: idx = rng.choice(idx, nmax, replace=False)
        for i in idx:
            f = float(np.clip((theta(root[i])+100)/180, 0, 1)); c = np.array([f, 0.25+0.35*(1-abs(f-0.5)*2), 1-f], np.float32)
            py, pz = pix(M[i])
            for k in range(len(py)-1): line(img, (py[k], pz[k]), (py[k+1], pz[k+1]), c)
    P = M[inslab(M)]; th_p = theta(P); r_p = radius(P)
    env = np.array([np.percentile(r_p[np.abs(th_p-t) < 2.5], 99.5) if (np.abs(th_p-t) < 2.5).sum() > 20 else np.nan for t in TH])
    so = env-scalp; table[lab] = {f'{t:+.0f}': (None if np.isnan(v) else round(float(v), 2)) for t, v in zip(TH, so)}
    # envelope line on the panel (white)
    pts = [(HC[1]+math.sin(math.radians(t))*e, HC[2]+math.cos(math.radians(t))*e) for t, e in zip(TH, env) if not np.isnan(e)]
    for (y1, z1), (y2, z2) in zip(pts[:-1], pts[1:]): line(img, ((y1-Y0)*S, (Z1-z1)*S), ((y2-Y0)*S, (Z1-z2)*S), (1, 1, 1))
    cv = so[~np.isnan(so)]; tv = TH[~np.isnan(so)]
    for k in range(len(tv)-1):
        x1 = (tv[k]+110)/195*W; x2 = (tv[k+1]+110)/195*W; y1 = CH-10-cv[k]/6.0*(CH-30); y2 = CH-10-cv[k+1]/6.0*(CH-30)
        for dy in (0, 1): line(chart, (x1, y1+dy), (x2, y2+dy), cols[si % 4])
    panels.append(img)
for t in range(-100, 86, 20):   # chart grid: angle ticks every 20 deg, stand-off lines every 1 cm
    x = int((t+110)/195*W); chart[:, min(x, W-1)] = (0.3, 0.3, 0.3)
for v in range(0, 7): y = int(CH-10-v/6.0*(CH-30)); chart[y, :] = (0.25, 0.25, 0.25)
G = np.concatenate([np.concatenate(panels, 1), np.concatenate([chart]+[np.full_like(chart, 0.12)]*(len(panels)-1), 1)], 0)
o = bpy.data.images.new('o', G.shape[1], G.shape[0]); rgba = np.ones((G.shape[0], G.shape[1], 4), np.float32); rgba[..., :3] = G
o.pixels.foreach_set(np.ascontiguousarray(rgba[::-1]).ravel()); o.filepath_raw = os.path.abspath(OUT); o.file_format = 'PNG'; o.save()
print('FLOW', json.dumps({'standoff_cm_by_angle': table, 'angle': '0 = vertex, + = front, - = back (HC = 0, 2.5, 160.5)'}))
