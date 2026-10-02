"""GUARDIAN-7: flat silhouette of the MAIN hair mass only (no loose / fine strands, no shading) over the head silhouette, side (y-z) and front (x-z).
usage: blender -b -P blender_gd7_silmask.py -- <head.npy> <out.png> <strands.npz> [...]   (one row per npz)"""
import bpy, sys, os, numpy as np
a = sys.argv[sys.argv.index('--')+1:]; X = np.load(a[0]); OUT = a[1]; S = X[:24049]; R = 6; W = 300; H = 300
def raster(P, u, v, img, col):
    iu = ((P[:, u]-u0[u])*R).astype(int); iv = (H-1-((P[:, 2]-140.0)*R)).astype(int); m = (iu >= 0) & (iu < W) & (iv >= 0) & (iv < H)
    for du in (-1, 0, 1):
        for dv in (-1, 0, 1): img[np.clip(iv[m]+dv, 0, H-1), np.clip(iu[m]+du, 0, W-1)] = col
u0 = {0: -25.0, 1: -25.0}; rows = []
for npz in a[2:]:
    D = np.load(npz); M = D['main'].reshape(-1, 3); row = []
    for u in (1, 0):
        img = np.full((H, W, 3), 0.92, np.float32); raster(M, u, 2, img, (0.45, 0.25, 0.12)); raster(S[S[:, 1] > -20], u, 2, img, (0.6, 0.6, 0.6))
        if u == 1: img = img[:, ::-1]
        row.append(img); row.append(np.full((H, 6, 3), 0.2, np.float32))
    rows.append(np.concatenate(row[:-1], 1)); rows.append(np.full((6, rows[-1].shape[1], 3), 0.2, np.float32))
out = np.concatenate(rows[:-1], 0); h, w = out.shape[:2]; rgba = np.ones((h, w, 4), np.float32); rgba[..., :3] = out
im = bpy.data.images.new('o', w, h); im.pixels.foreach_set(np.ascontiguousarray(rgba[::-1]).ravel()); im.filepath_raw = os.path.abspath(OUT); im.file_format = 'PNG'; im.save(); print('SILMASK_OK')
