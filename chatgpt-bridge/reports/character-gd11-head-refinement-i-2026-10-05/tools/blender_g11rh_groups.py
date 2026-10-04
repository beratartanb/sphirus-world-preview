"""GD11 refinement H: GROUP-coloured strand layers (diagnostic, strand geometry) for the behind-ear -> nape 'L' read. Orthographic, depth-buffered.
Views (rows): rear3qR (camera behind character right, 45 deg), rear3qL. Panels (columns):
  A full, every group coloured | B only side_to_bun + back_to_bun (main) | C only nape_to_bun (main) | D only free nape / behind-ear / ear_lock / temple_veil (loose)
  E full with the bun region removed (points within BUN_R of the bun centre hidden) | F full, flat neutral colour (silhouette / edge read)
colours: front/top main grey-brown, side_to_bun green, back_to_bun gold, nape_to_bun orange, partcover/baby dark, behind_ear blue, ear_lock magenta, temple_veil violet,
         nape_free* cyan, side_long white, other loose light grey.
usage: blender -b --factory-startup --python blender_g11rh_groups.py -- <out.png> <hair_dir> <head.npy>   env BUN_C=x,y,z BUN_R=r"""
import bpy, sys, os, json, math, numpy as np
a = sys.argv[sys.argv.index('--')+1:]; OUT, HD, HEAD = a[0], a[1], a[2]
d = np.load(os.path.join(HD, 'strands.npz')); M, L = d['main'], d['loose']; tg = json.load(open(os.path.join(HD, 'strand_tags.json')))
tm = np.array([t.split(':')[0] for t in tg['main']]); tl = np.array([t.split(':')[0] for t in tg['loose']])
hd = np.load(HEAD)[:24049]; BC = np.array([float(v) for v in os.environ.get('BUN_C', '1.2,-8.4,162.0').split(',')]); BR = float(os.environ.get('BUN_R', '3.3'))
CM = {'front_to_bun': (0.45, 0.38, 0.32), 'top_to_bun': (0.5, 0.42, 0.34), 'side_to_bun': (0.25, 0.75, 0.3), 'back_to_bun': (0.9, 0.75, 0.25), 'nape_to_bun': (1.0, 0.5, 0.12), 'partcover_or_baby': (0.3, 0.25, 0.2), 'corner_to_bun': (1.0, 0.2, 0.2), 'nape_lock': (1.0, 0.35, 0.1), 'nape_fine': (1.0, 0.9, 0.6)}
CL = {'under_ear': (1.0, 1.0, 0.2), 'behind_ear': (0.3, 0.5, 1.0), 'ear_lock': (1.0, 0.3, 0.9), 'temple_veil': (0.7, 0.4, 1.0), 'nape_free': (0.2, 0.95, 1.0), 'nape_free_g': (0.2, 0.95, 1.0), 'side_long': (1, 1, 1)}
S = 30; W, H = 760, 820; CZ = 158.5
def dense(P, n=3):
    if len(P) == 0: return np.zeros((0, 3))
    t = np.linspace(0, 1, n, endpoint=False)[None, None, :, None]; A = P[:, :-1, None, :]; B_ = P[:, 1:, None, :]; return (A+(B_-A)*t).reshape(-1, 3)
def render(view, layers, cut_bun=False):
    yaw = {'rear3qR': 45.0, 'rear3qL': 135.0}[view]; f = np.array([math.cos(math.radians(yaw)), math.sin(math.radians(yaw)), 0.0]); r = np.array([-f[1], f[0], 0.0])
    img = np.full((H, W, 3), 0.2, np.float32); zb = np.full((H, W), -1e9, np.float32)
    def splat(P, col, rad=1):
        if len(P) == 0: return
        if cut_bun: P = P[np.linalg.norm(P-BC, axis=1) > BR]
        u = P@r; v = P[:, 2]; dep = -(P@f); px = (W/2+u*S).astype(int); py = (H/2-(v-CZ)*S).astype(int)
        ok = (px >= rad) & (px < W-rad) & (py >= rad) & (py < H-rad); px, py, dep = px[ok], py[ok], dep[ok]
        if len(dep) == 0: return
        dn = (dep-dep.min())/max(1e-6, np.ptp(dep)); shade = (0.55+0.45*dn)[:, None]*np.asarray(col, np.float32)[None]
        for dx in range(-rad+1, rad):
            for dy in range(-rad+1, rad):
                m = dep > zb[py+dy, px+dx]; zb[py[m]+dy, px[m]+dx] = dep[m]; img[py[m]+dy, px[m]+dx] = shade[m]
    splat(hd, (0.62, 0.6, 0.58), 2)
    for P, col in layers: splat(P, col)
    return img
def mainL(groups=None): return [(dense(M[tm == g]), c) for g, c in CM.items() if groups is None or g in groups]
def looseL(fams=None, default=(0.8, 0.8, 0.8)):
    out = []
    for fam in np.unique(tl):
        if fams is not None and fam not in fams: continue
        out.append((dense(L[tl == fam]), CL.get(fam, default)))
    return out
rows = []
for view in ('rear3qR', 'rear3qL'):
    full = mainL()+looseL()
    panels = [render(view, full), render(view, mainL({'side_to_bun', 'back_to_bun'})), render(view, mainL({'nape_to_bun', 'corner_to_bun', 'nape_lock', 'nape_fine'})),
              render(view, looseL({'behind_ear', 'ear_lock', 'temple_veil', 'nape_free', 'nape_free_g', 'side_long', 'under_ear'})), render(view, full, cut_bun=True),
              render(view, [(P, (0.55, 0.42, 0.3)) for P, _ in full])]
    rows.append(np.concatenate([np.pad(p, ((0, 4), (0, 4), (0, 0))) for p in panels], 1))
G = np.concatenate(rows, 0); o = bpy.data.images.new('o', G.shape[1], G.shape[0]); rgba = np.ones((G.shape[0], G.shape[1], 4), np.float32); rgba[..., :3] = G
o.pixels.foreach_set(np.ascontiguousarray(rgba[::-1]).ravel()); o.filepath_raw = os.path.abspath(OUT); o.file_format = 'PNG'; o.save()
print('GROUPS_OK', json.dumps({'main': {k: int((tm == k).sum()) for k in np.unique(tm)}, 'loose': {k: int((tl == k).sum()) for k in np.unique(tl)}}))
