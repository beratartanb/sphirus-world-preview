"""Fast offline groom preview (hair v14 iteration): strands.npz from blender_lk_hair_locks.py -> orthographic density renders
front / side (+x) / back / top with the head silhouette. Colour: main groom lock path (brown), main groom bun section
(last ~40% of points, red), loose groom (green). Diagnostic only - the UE captures remain the visual authority.
usage: blender -b --factory-startup --python blender_hair_preview.py -- <strands.npz> <sculpt_package.json.gz> <out.png>"""
import bpy, sys, json, gzip
import numpy as np
a = sys.argv[sys.argv.index('--')+1:]; D = np.load(a[0]); P = json.loads(gzip.open(a[1], 'rb').read()); OUT = a[2]
HEAD = np.asarray(P['br_neutral'], np.float32)[P['NB']:] if not __import__('os').environ.get('SPH_HEAD_NPY') else np.load(__import__('os').environ['SPH_HEAD_NPY']).astype(np.float32); BODY = np.asarray(P['br_neutral'], np.float32)[:P['NB']]
S = 480; C = np.array([0.0, 2.0, 156.0]); SPAN = 44.0
VIEWS = {'front': (0, 2, 1, 1), 'side': (1, 2, 0, 1), 'back': (0, 2, 1, -1), 'top': (0, 1, 2, 1)}
def proj(p, v):
    i, j, k, sg = v; x = (p[:, i]-C[i])*(sg if v != VIEWS['side'] else -1); y = p[:, j]-C[j]
    if v == VIEWS['top']: x = p[:, 0]-C[0]; y = p[:, 1]-C[1]
    return ((x/SPAN+0.5)*S).astype(int), ((0.5-y/SPAN)*S).astype(int)
def splat(img, p, col, v, w=1.0):
    u, vv = proj(p, v); m = (u >= 0) & (u < S) & (vv >= 0) & (vv < S); np.add.at(img, (vv[m], u[m]), np.asarray(col, np.float32)*w)
tiles = []
for name, v in VIEWS.items():
    img = np.zeros((S, S, 3), np.float32)
    sil = np.zeros((S, S, 3), np.float32); splat(sil, HEAD, (1, 1, 1), v); splat(sil, BODY[BODY[:, 2] > 125], (1, 1, 1), v)
    sil = (sil.sum(-1) > 0).astype(np.float32)
    def dense(st):   # upsample polylines so lines are continuous
        t = np.linspace(0, 1, 4)[None, None, :, None]; seg = st[:, :-1, None, :]*(1-t)+st[:, 1:, None, :]*t; return seg.reshape(st.shape[0], -1, 3)
    M = D['main']; L = D['loose']; n = M.shape[1]; cut = int(n*0.6)
    splat(img, dense(M[:, :cut+1]).reshape(-1, 3), (0.55, 0.35, 0.18), v, 0.012)
    splat(img, dense(M[:, cut:]).reshape(-1, 3), (0.8, 0.12, 0.08), v, 0.012)
    if len(L): splat(img, dense(L).reshape(-1, 3), (0.1, 0.9, 0.2), v, 0.08)
    img = 1-np.exp(-img*3.0); img = np.maximum(img, sil[..., None]*0.18)
    tiles.append(img)
out = np.concatenate([np.concatenate(tiles[:2], 1), np.concatenate(tiles[2:], 1)], 0)[::-1]
im = bpy.data.images.new('pv', out.shape[1], out.shape[0], alpha=False); rgba = np.ones(out.shape[:2]+(4,), np.float32); rgba[..., :3] = np.clip(out, 0, 1)
im.pixels.foreach_set(rgba.ravel()); im.filepath_raw = __import__('os').path.abspath(OUT); im.file_format = 'PNG'; im.save(); print('PREVIEW_OK', OUT)
