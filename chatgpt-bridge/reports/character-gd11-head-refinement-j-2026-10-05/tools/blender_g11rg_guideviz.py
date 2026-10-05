"""GD11 refinement G: draw the editable guides (guides.json) of chosen groups over the build head, coloured per group, for the report.
Views: back, rear3qR, front3qR, sideR. Each guide is drawn as a thick polyline with a dot at its first control point (root).
usage: blender -b --factory-startup --python blender_g11rg_guideviz.py -- <out.png> <guides.json> <head.npy> [<guides2.json> drawn as grey ghost]"""
import bpy, sys, os, json, math, numpy as np
a = sys.argv[sys.argv.index('--')+1:]; OUT, GJ, HEAD = a[0], a[1], a[2]; GHOST = a[3] if len(a) > 3 else None
G = json.load(open(GJ)); hd = np.load(HEAD)[:24049]
COL = {'nape_to_bun': (1.0, 0.55, 0.15), 'back_to_bun': (0.85, 0.75, 0.3), 'bun_loops': (1.0, 0.95, 0.2), 'nape_free_g': (0.3, 0.95, 1.0), 'behind_ear': (0.4, 0.6, 1.0),
       'front_side_frame': (1.0, 0.35, 0.6), 'temple_veil': (0.75, 0.45, 1.0), 'ff_wave': (0.9, 0.9, 0.9), 'face_frame': (0.7, 0.7, 0.7), 'corner_to_bun': (1.0, 0.15, 0.15), 'nape_lock': (1.0, 0.3, 0.05), 'nape_spine': (1.0, 0.45, 0.1)}
S = 24; W = H = 720; CZ = 159.0
def view_basis(v):
    yaw = {'back': 90.0, 'rear3qR': 45.0, 'front3qR': -55.0, 'sideR': 0.0}[v]; f = np.array([math.cos(math.radians(yaw)), math.sin(math.radians(yaw)), 0.0]); r = np.array([-f[1], f[0], 0.0]); return f, r
def pix(P, f, r): return W/2+(P@r)*S, H/2-(P[:, 2]-CZ)*S, -(P@f)
def render(v):
    f, r = view_basis(v); img = np.full((H, W, 3), 0.18, np.float32); zb = np.full((H, W), -1e9, np.float32)
    px, py, dp = pix(hd, f, r); o = np.argsort(dp)
    for i in o:
        x, y = int(px[i]), int(py[i])
        if 0 <= x < W and 0 <= y < H and dp[i] > zb[y, x]: zb[y, x] = dp[i]; img[y, x] = 0.42+0.25*(dp[i]-dp.min())/(dp.max()-dp.min())
    def poly(P, col, wd=2):
        P = np.asarray(P, float); t = np.linspace(0, 1, 12)[None, :, None]; D = (P[:-1, None]+(P[1:, None]-P[:-1, None])*t).reshape(-1, 3)
        x, y, d = pix(D, f, r)
        for xi, yi, di in zip(x.astype(int), y.astype(int), d):
            if wd <= xi < W-wd and wd <= yi < H-wd: img[yi-wd+1:yi+wd, xi-wd+1:xi+wd] = col
    if GHOST:
        for k, g in json.load(open(GHOST)).items():
            if isinstance(g, dict) and g.get('group') in COL and 'ctrl' in g: poly(g['ctrl'], (0.33, 0.33, 0.33), 1)
    for k, g in G.items():
        if isinstance(g, dict) and g.get('group') in COL and 'ctrl' in g:
            poly(g['ctrl'], COL[g['group']], 2); x, y, _ = pix(np.asarray(g['ctrl'][:1], float), f, r); xi, yi = int(x[0]), int(y[0])
            if 4 <= xi < W-4 and 4 <= yi < H-4: img[yi-3:yi+4, xi-3:xi+4] = (1, 1, 1)
    return img
G2 = np.concatenate([np.pad(render(v), ((0, 4), (0, 4), (0, 0))) for v in ('back', 'rear3qR', 'sideR', 'front3qR')], 1)
o = bpy.data.images.new('o', G2.shape[1], G2.shape[0]); rgba = np.ones((G2.shape[0], G2.shape[1], 4), np.float32); rgba[..., :3] = G2
o.pixels.foreach_set(np.ascontiguousarray(rgba[::-1]).ravel()); o.filepath_raw = os.path.abspath(OUT); o.file_format = 'PNG'; o.save(); print('GUIDEVIZ_OK')
