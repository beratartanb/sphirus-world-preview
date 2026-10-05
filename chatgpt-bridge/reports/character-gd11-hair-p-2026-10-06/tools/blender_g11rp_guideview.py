"""GD11 hair pass P: draw the primary lock centrelines (prim:* of a guides.json) over the build head, coloured by the pass-P family
(or by the builder group when the file has no family), thick depth-tested polylines with a dot at the root.
usage: blender -b --factory-startup --python blender_g11rp_guideview.py -- <out.png> <guides.json> <head.npy> [views csv] [family json for colours]"""
import bpy, sys, os, json, math, numpy as np
a = sys.argv[sys.argv.index('--')+1:]; OUT, GJ, HEAD = a[0], a[1], a[2]; VIEWS = (a[3] if len(a) > 3 and a[3] else 'front,q3L,q3R,profL,profR,rear3qR,back').split(',')
G = json.load(open(GJ)); FAMJ = json.load(open(a[4])) if len(a) > 4 else G; hd = np.load(HEAD)[:24049]; S = 30; W, H = 764, 824; CZ = 160.0
COL = {'A_front_edge': (1.0, 0.25, 0.25), 'B_front_top': (1.0, 0.75, 0.1), 'C_temple_edge': (0.3, 0.95, 0.35), 'D_above_ear': (0.2, 0.85, 1.0), 'E_upper_side': (0.45, 0.5, 1.0), 'F_top_mid': (1.0, 0.45, 0.9),
       'F_crown_side': (0.8, 0.5, 1.0), 'G_behind_ear': (1.0, 1.0, 0.3), 'H_back': (0.85, 0.85, 0.85)}
def basis(v):
    yaw = {'rear3qR': 45.0, 'rear3qL': 135.0, 'profR': 0.0, 'profL': 180.0, 'back': 90.0, 'front': -90.0, 'q3R': -45.0, 'q3L': -135.0}[v]; f = np.array([math.cos(math.radians(yaw)), math.sin(math.radians(yaw)), 0.0]); r = np.array([-f[1], f[0], 0.0]); return f, r
def render(v):
    f, r = basis(v); img = np.full((H, W, 3), 0.2, np.float32); zb = np.full((H, W), -1e9, np.float32)
    def pix(P): return (W/2+(P@r)*S).astype(int), (H/2-(P[:, 2]-CZ)*S).astype(int), -(P@f)
    px, py, dp = pix(hd); ok = (px >= 1) & (px < W-1) & (py >= 1) & (py < H-1); px, py, dp = px[ok], py[ok], dp[ok]
    for i in np.argsort(dp): zb[py[i], px[i]] = dp[i]; img[py[i], px[i]] = 0.45
    for k_, v_ in G.items():
        if not (k_.startswith('prim:') and isinstance(v_, dict) and 'ctrl' in v_): continue
        fam = FAMJ.get(k_, {}).get('family_p'); c = COL.get(fam, (0.6, 0.6, 0.6)); st = np.asarray(v_['ctrl'], float); x, y, dep = pix(st)
        for k in range(len(x)-1):
            n = int(max(abs(x[k+1]-x[k]), abs(y[k+1]-y[k])))+1
            for t in np.linspace(0, 1, n):
                xi, yi = int(x[k]+(x[k+1]-x[k])*t), int(y[k]+(y[k+1]-y[k])*t); de = dep[k]+(dep[k+1]-dep[k])*t
                for ox in (-1, 0, 1):
                    for oy in (-1, 0, 1):
                        if 0 <= xi+ox < W and 0 <= yi+oy < H and de > zb[yi+oy, xi+ox]-0.6: img[yi+oy, xi+ox] = c
        if 2 <= x[0] < W-3 and 2 <= y[0] < H-3 and dep[0] > zb[y[0], x[0]]-0.6: img[y[0]-3:y[0]+4, x[0]-3:x[0]+4] = (1, 1, 1)
    return img
Gm = np.concatenate([np.pad(render(v), ((0, 4), (0, 4), (0, 0))) for v in VIEWS], 1)
o = bpy.data.images.new('o', Gm.shape[1], Gm.shape[0]); rgba = np.ones((Gm.shape[0], Gm.shape[1], 4), np.float32); rgba[..., :3] = Gm
o.pixels.foreach_set(np.ascontiguousarray(rgba[::-1]).ravel()); o.filepath_raw = os.path.abspath(OUT); o.file_format = 'PNG'; o.save(); print('GUIDEVIEW_OK', OUT)
