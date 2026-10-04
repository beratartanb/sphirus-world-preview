"""GD11 refinement G: tagged strand LAYER renders (diagnostic, strand geometry - not UE). Orthographic, depth-buffered point splatting of
densified strand polylines + the build head (grey), shaded by depth. Views: back (camera behind, looking forward), rear3qR / rear3qL (45 deg).
Layers (per view, one panel each):
  A full hair | B full minus free nape locks (loose nape_free* / behind_ear / side_long) | C full minus main nape_to_bun strands |
  D ONLY main nape_to_bun strands (+ their roots as dots) | E ONLY free nape / behind-ear / long side locks | F ONLY bun-region points (bun sphere)
colours: main = warm brown, nape_to_bun = orange, free nape group = cyan, bun-region = yellow.
usage: blender -b --factory-startup --python blender_g11rg_layers.py -- <out.png> <hair_dir with strands.npz + strand_tags.json> <head.npy> [views=back,rear3qR,rear3qL]"""
import bpy, sys, os, json, math, numpy as np
a = sys.argv[sys.argv.index('--')+1:]; OUT, HD, HEAD = a[0], a[1], a[2]; VIEWS = (a[3] if len(a) > 3 else 'back,rear3qR,rear3qL').split(',')
d = np.load(os.path.join(HD, 'strands.npz')); M, L = d['main'], d['loose']; tg = json.load(open(os.path.join(HD, 'strand_tags.json')))
tm = np.array([t.split(':')[0] for t in tg['main']]); tl = np.array([t.split(':')[0] for t in tg['loose']])
hd = np.load(HEAD)[:24049]; BC = np.array([float(v) for v in os.environ.get('BUN_C', '1.2,-8.6,161.6').split(',')]); BR = float(os.environ.get('BUN_R', '3.2'))
FREE = np.isin(tl, ['nape_free', 'nape_free_g', 'behind_ear', 'side_long'])
NAPE = tm == 'nape_to_bun'
S = 26; W = H = 760; CZ = 158.0
def dense(P, n=3):
    t = np.linspace(0, 1, n, endpoint=False)[None, None, :, None]; A = P[:, :-1, None, :]; B_ = P[:, 1:, None, :]; return (A+(B_-A)*t).reshape(-1, 3)
def basis(view):
    yaw = {'back': 90.0, 'rear3qR': 45.0, 'rear3qL': 135.0}[view]      # camera forward direction (UE yaw) - looks at the head from behind
    f = np.array([math.cos(math.radians(yaw)), math.sin(math.radians(yaw)), 0.0]); r = np.array([-f[1], f[0], 0.0]); return f, r
def render(view, layers):
    f, r = basis(view); img = np.full((H, W, 3), 0.20, np.float32); zb = np.full((H, W), -1e9, np.float32)
    def splat(P, col, rad=1):
        if len(P) == 0: return
        u = P@r; v = P[:, 2]; dep = -(P@f)                                   # larger dep = closer to the camera (camera behind, looking along f)
        px = (W/2+u*S).astype(int); py = (H/2-(v-CZ)*S).astype(int); ok = (px >= rad) & (px < W-rad) & (py >= rad) & (py < H-rad)
        px, py, dep = px[ok], py[ok], dep[ok]; o = np.argsort(dep); px, py, dep = px[o], py[o], dep[o]
        dn = (dep-dep.min())/max(1e-6, dep.max()-dep.min()); shade = (0.55+0.45*dn)[:, None]*np.asarray(col, np.float32)[None]
        for dx in range(-rad+1, rad):
            for dy in range(-rad+1, rad):
                m = dep > zb[py+dy, px+dx]; zb[py[m]+dy, px[m]+dx] = dep[m]; img[py[m]+dy, px[m]+dx] = shade[m]
    splat(hd, (0.62, 0.60, 0.58), 2)
    for P, col in layers: splat(P, col, 1)
    return img
mainP = lambda sel: dense(M[sel]); looseP = lambda sel: dense(L[sel])
inb = np.linalg.norm(M-BC, axis=2) < BR
rows = []
for view in VIEWS:
    panels = [render(view, [(mainP(~NAPE), (0.55, 0.32, 0.16)), (mainP(NAPE), (0.95, 0.55, 0.2)), (looseP(~FREE), (0.7, 0.5, 0.3)), (looseP(FREE), (0.3, 0.9, 1.0))]),
              render(view, [(mainP(~NAPE), (0.55, 0.32, 0.16)), (mainP(NAPE), (0.95, 0.55, 0.2)), (looseP(~FREE), (0.7, 0.5, 0.3))]),
              render(view, [(mainP(~NAPE), (0.55, 0.32, 0.16)), (looseP(~FREE), (0.7, 0.5, 0.3)), (looseP(FREE), (0.3, 0.9, 1.0))]),
              render(view, [(mainP(NAPE), (0.95, 0.55, 0.2)), (M[NAPE][:, 0], (1, 1, 1))]),
              render(view, [(looseP(FREE), (0.3, 0.9, 1.0))]),
              render(view, [(M[inb], (1.0, 0.9, 0.25))])]
    rows.append(np.concatenate([np.pad(p, ((0, 4), (0, 4), (0, 0))) for p in panels], 1))
G = np.concatenate(rows, 0); o = bpy.data.images.new('o', G.shape[1], G.shape[0]); rgba = np.ones((G.shape[0], G.shape[1], 4), np.float32); rgba[..., :3] = G
o.pixels.foreach_set(np.ascontiguousarray(rgba[::-1]).ravel()); o.filepath_raw = os.path.abspath(OUT); o.file_format = 'PNG'; o.save()
print('LAYERS_OK', json.dumps({'main_nape_to_bun': int(NAPE.sum()), 'loose_free_nape_group': int(FREE.sum()), 'tags_main': {k: int((tm == k).sum()) for k in np.unique(tm)}, 'tags_loose': {k: int((tl == k).sum()) for k in np.unique(tl)}}))
