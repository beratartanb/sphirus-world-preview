"""Black silhouette of a figure against a flat studio background (Blender numpy): background = median of the top rows; mask =
colour distance > thr or saturation above the background's. Optional second image drawn as a red outline over the first mask.
Jobs: img|out|thr[|outline_img]   usage: blender -b -P id_silhouette.py -- job ..."""
import bpy, sys
import numpy as np
def load(p):
    im = bpy.data.images.load(p); w, h = im.size; a = np.asarray(im.pixels[:], np.float32).reshape(h, w, im.channels)[..., :3]; bpy.data.images.remove(im); return a
def mask(a, thr):
    h, w = a.shape[:2]; k = max(2, int(w*0.035)); edge = np.concatenate([a[:, :k], a[:, -k:]], 1); bg = np.median(edge, 1)   # per-row background from the side columns
    rowv = np.abs(np.diff(bg, axis=0, prepend=bg[:1])).sum(-1); bgs = bg.max(-1)-bg.min(-1)
    sat = a.max(-1)-a.min(-1); d = np.linalg.norm(a-bg[:, None, :], axis=-1); m = (d > thr) | (sat > bgs[:, None]+0.08)
    for _ in range(2): m = m & (np.roll(m, 1, 0) | np.roll(m, -1, 0)) & (np.roll(m, 1, 1) | np.roll(m, -1, 1))   # remove specks
    return m
for job in sys.argv[sys.argv.index('--')+1:]:
    f = job.split('|'); a = load(f[0]); m = mask(a, float(f[2])); o = np.ones_like(a)*0.92; o[m] = 0.0
    if len(f) > 3:
        b = load(f[3]); mb = mask(b, float(f[2])); e = mb ^ (np.roll(mb, 1, 0) & np.roll(mb, -1, 0) & np.roll(mb, 1, 1) & np.roll(mb, -1, 1)); e = e | np.roll(e, 1, 0) | np.roll(e, 1, 1)
        o[mb & ~m] = [0.95, 0.6, 0.6]; o[e] = [0.9, 0.05, 0.05]
    h, w = m.shape; im = bpy.data.images.new('s', w, h); rgba = np.ones((h, w, 4), np.float32); rgba[..., :3] = o; im.pixels.foreach_set(rgba.ravel()); im.filepath_raw = f[1]; im.file_format = 'PNG'; im.save(); print('SIL', f[1], round(float(m.mean()), 3))
