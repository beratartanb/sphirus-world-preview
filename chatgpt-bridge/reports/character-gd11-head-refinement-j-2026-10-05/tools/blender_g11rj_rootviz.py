"""GD11 refinement J: ROOT / FLOW / EDGE diagnostic on the hairless build head (strand geometry).
Panels (views back, rear3qR, profR, profL): head grey (depth shaded); the soft nape / behind-ear hairline curve (green) and the ear outline
(white); ROOTS of the nape field as dots: join (orange) / free (cyan) / wisp (yellow); the MAIN FLOW drawn as thin lines for a subsample of join
strands (orange) and free strands (cyan); edge wisps (yellow); ear-frame roots (magenta dots) and their hanging paths (magenta, thin).
usage: blender -b --factory-startup --python blender_g11rj_rootviz.py -- <out.png> <hair_dir> <head.npy>"""
import bpy, sys, os, json, math, numpy as np
a = sys.argv[sys.argv.index('--')+1:]; OUT, HD, HEAD = a[0], a[1], a[2]
d = np.load(os.path.join(HD, 'strands.npz')); M, L = d['main'], d['loose']; tg = json.load(open(os.path.join(HD, 'strand_tags.json')))
tm = np.array(tg['main']); tl = np.array(tg['loose']); hd = np.load(HEAD)[:24049]
def sstep(t): t = np.clip(t, 0, 1); return t*t*(3-2*t)
def zh_back(x, y):
    th = abs(math.degrees(math.atan2(x, y-2.5))); zc = 151.2+2.2*(abs(x)/6.0)**2+0.35*math.sin(x*2.3+0.7); zs = float(np.interp(th, [112, 122, 132, 142, 152], [161.0, 159.2, 157.4, 155.6, 153.4]))
    w = sstep((abs(x)-3.4)/1.6); return (1-w)*zc+w*zs
S = 30; W, H = 760, 820; CZ = 157.5
def basis(v):
    yaw = {'back': 90.0, 'rear3qR': 45.0, 'profR': 0.0, 'profL': 180.0}[v]; f = np.array([math.cos(math.radians(yaw)), math.sin(math.radians(yaw)), 0.0]); r = np.array([-f[1], f[0], 0.0]); return f, r
def render(v):
    f, r = basis(v); img = np.full((H, W, 3), 0.2, np.float32); zb = np.full((H, W), -1e9, np.float32)
    def pix(P): return (W/2+(P@r)*S).astype(int), (H/2-(P[:, 2]-CZ)*S).astype(int), -(P@f)
    px, py, dp = pix(hd); ok = (px >= 1) & (px < W-1) & (py >= 1) & (py < H-1); px, py, dp = px[ok], py[ok], dp[ok]; o = np.argsort(dp)
    dn = (dp-dp.min())/np.ptp(dp)
    for i in o:
        for dx in (0, 1):
            for dy in (0, 1): zb[py[i]+dy, px[i]+dx] = dp[i]; img[py[i]+dy, px[i]+dx] = 0.38+0.3*dn[i]
    def dots(P, col, rad=2):
        if len(P) == 0: return
        x, y, dep = pix(P)
        for xi, yi, de in zip(x, y, dep):
            if rad <= xi < W-rad and rad <= yi < H-rad and de > zb[yi, xi]-0.6: img[yi-rad+1:yi+rad, xi-rad+1:xi+rad] = col
    def lines(Pl, col):
        for st in Pl:
            x, y, dep = pix(st)
            for k in range(len(x)-1):
                n = int(max(abs(x[k+1]-x[k]), abs(y[k+1]-y[k])))+1
                for t in np.linspace(0, 1, n):
                    xi, yi = int(x[k]+(x[k+1]-x[k])*t), int(y[k]+(y[k+1]-y[k])*t); de = dep[k]+(dep[k+1]-dep[k])*t
                    if 0 <= xi < W and 0 <= yi < H and de > zb[yi, xi]-0.8: img[yi, xi] = col
    # hairline curve and ear outline
    hl = []
    for th in np.linspace(96, 180, 60):
        for sg in (1, -1):
            x_ = sg*7.0*math.sin(math.radians(th)); y_ = 2.5+7.0*math.cos(math.radians(th)); hl.append([x_, y_, zh_back(x_, y_)])
    hl = np.asarray(hl); hl = hl[np.argsort(np.arctan2(hl[:, 0], -hl[:, 1]))]; dots(hl, (0.2, 1.0, 0.3), 2)
    for sg in (1, -1):
        e = hd[(sg*hd[:, 0] > 7.6) & (hd[:, 1] > -0.5) & (hd[:, 1] < 4.2) & (hd[:, 2] > 156.5) & (hd[:, 2] < 166.5)]; dots(e, (0.95, 0.95, 0.95), 1)
    kinds = {'nape_field:join': (1.0, 0.5, 0.1), 'nape_field:free': (0.2, 0.9, 1.0), 'nape_field:wisp': (1.0, 0.9, 0.2), 'nape_lock': (1.0, 0.4, 0.1)}
    for k, col in kinds.items():
        sel = np.array([t.startswith(k) for t in tm]); P = M[sel]
        if len(P) == 0: continue
        dots(P[:, 0], col, 2); lines(P[::max(1, len(P)//140)], col)
    sel = np.array([t.startswith('ear_frame') or t.startswith('under_ear') for t in tl]); P = L[sel]
    if len(P): dots(P[:, 0], (1.0, 0.3, 0.9), 2); lines(P[::max(1, len(P)//60)], (1.0, 0.3, 0.9))
    return img
G = np.concatenate([np.pad(render(v), ((0, 4), (0, 4), (0, 0))) for v in ('back', 'rear3qR', 'profR', 'profL')], 1)
o = bpy.data.images.new('o', G.shape[1], G.shape[0]); rgba = np.ones((G.shape[0], G.shape[1], 4), np.float32); rgba[..., :3] = G
o.pixels.foreach_set(np.ascontiguousarray(rgba[::-1]).ravel()); o.filepath_raw = os.path.abspath(OUT); o.file_format = 'PNG'; o.save(); print('ROOTVIZ_OK')
