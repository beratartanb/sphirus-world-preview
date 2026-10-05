"""GD11 refinement O: strand-geometry renders of SELECTED tag groups only (diagnosis A-F): depth-buffered line raster of the main + loose strands
whose strand_tags match any of the given prefixes, over the build head (grey dots). Views: q3R, profR, rear3qR, back, front.
usage: blender -b --factory-startup --python blender_g11ro_tagview.py -- <out.png> <hair_dir> <head.npy> "<tag prefixes comma-separated>" [views comma-separated]
e.g. tags "nape_field:join" | "nape_field:free,nape_field:wisp" | "ear_frame" | "front_to_bun,side_to_bun" | "" (= everything)"""
import bpy, sys, os, json, math, numpy as np
a = sys.argv[sys.argv.index('--')+1:]; OUT, HD, HEAD, TAGS = a[0], a[1], a[2], [t for t in a[3].split(',') if t]; VIEWS = (a[4] if len(a) > 4 else 'q3R,profR,rear3qR,back').split(',')
d = np.load(os.path.join(HD, 'strands.npz')); M, L = d['main'], d['loose']; tg = json.load(open(os.path.join(HD, 'strand_tags.json'))); tm = np.array(tg['main']); tl = np.array(tg['loose']); hd = np.load(HEAD)[:24049]
def sel(tags, T): return np.ones(len(T), bool) if not TAGS else np.array([any(t.startswith(p) for p in TAGS) for t in T])
sm, sl = sel(TAGS, tm), sel(TAGS, tl); S = 30; W, H = 764, 824; CZ = 160.0
COL = {'nape_field:join': (1.0, 0.5, 0.1), 'nape_field:free': (0.2, 0.9, 1.0), 'nape_field:wisp': (1.0, 0.9, 0.2), 'ear_frame': (1.0, 0.3, 0.9), 'front_to_bun': (0.3, 0.9, 0.3), 'side_to_bun': (0.9, 0.8, 0.3), 'top_to_bun': (0.5, 0.7, 1.0), 'back_to_bun': (0.8, 0.6, 0.9), 'temple_veil': (0.7, 0.4, 1.0), 'front_side_frame': (1.0, 0.4, 0.6)}
def col(t):
    for k, c in COL.items():
        if t.startswith(k): return c
    return (0.75, 0.75, 0.75)
def basis(v):
    yaw = {'rear3qR': 45.0, 'rear3qL': 135.0, 'profR': 0.0, 'profL': 180.0, 'back': 90.0, 'front': -90.0, 'q3R': -45.0, 'q3L': -135.0}[v]; f = np.array([math.cos(math.radians(yaw)), math.sin(math.radians(yaw)), 0.0]); r = np.array([-f[1], f[0], 0.0]); return f, r
def render(v):
    f, r = basis(v); img = np.full((H, W, 3), 0.2, np.float32); zb = np.full((H, W), -1e9, np.float32)
    def pix(P): return (W/2+(P@r)*S).astype(int), (H/2-(P[:, 2]-CZ)*S).astype(int), -(P@f)
    px, py, dp = pix(hd); ok = (px >= 1) & (px < W-1) & (py >= 1) & (py < H-1); px, py, dp = px[ok], py[ok], dp[ok]
    for i in np.argsort(dp):
        zb[py[i], px[i]] = dp[i]; img[py[i], px[i]] = 0.45
    for S_, T_, ms in ((M, tm, sm), (L, tl, sl)):
        idx = np.flatnonzero(ms)
        for i in idx[::max(1, len(idx)//9000)]:
            st = S_[i]; x, y, dep = pix(st); c = col(T_[i])
            for k in range(len(x)-1):
                n = int(max(abs(x[k+1]-x[k]), abs(y[k+1]-y[k])))+1
                for t in np.linspace(0, 1, n):
                    xi, yi = int(x[k]+(x[k+1]-x[k])*t), int(y[k]+(y[k+1]-y[k])*t); de = dep[k]+(dep[k+1]-dep[k])*t
                    if 0 <= xi < W and 0 <= yi < H and de > zb[yi, xi]-0.8: img[yi, xi] = c; zb[yi, xi] = max(zb[yi, xi], de)
    return img
G = np.concatenate([np.pad(render(v), ((0, 4), (0, 4), (0, 0))) for v in VIEWS], 1)
o = bpy.data.images.new('o', G.shape[1], G.shape[0]); rgba = np.ones((G.shape[0], G.shape[1], 4), np.float32); rgba[..., :3] = G
o.pixels.foreach_set(np.ascontiguousarray(rgba[::-1]).ravel()); o.filepath_raw = os.path.abspath(OUT); o.file_format = 'PNG'; o.save(); print('TAGVIEW_OK', OUT, 'main', int(sm.sum()), 'loose', int(sl.sum()))
