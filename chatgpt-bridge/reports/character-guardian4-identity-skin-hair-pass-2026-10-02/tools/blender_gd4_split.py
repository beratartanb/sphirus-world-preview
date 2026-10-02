"""GUARDIAN-4: mirrored split-face diagnostic in the Tier A FRONT frame. For each item (reference or candidate clay rendered at the Tier A
front camera) writes one row: [image | LEFT-LEFT (character left half = image right, mirrored) | RIGHT-RIGHT (character right half mirrored)]
about a vertical axis through the eye midpoint (reference: tracker eyelid curves; candidate: projected eyeball centres). If the two mirrored
faces differ strongly the face is asymmetric; compare the reference's difference with each candidate's.
usage: blender -b -P blender_gd4_split.py -- <out.png> <x0,x1,y0,y1 crop> <row height> ref=<img> | <img>@<head.npy> ..."""
import bpy, sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930'))
from gd_common import topix
a = sys.argv[sys.argv.index('--')+1:]; OUT = a[0]; x0, x1, y0, y1 = map(int, a[1].split(',')); RH = int(a[2])
def load(p):
    im = bpy.data.images.load(os.path.abspath(p)); w, h = im.size; x = np.asarray(im.pixels[:], np.float32).reshape(h, w, im.channels)[::-1].copy(); bpy.data.images.remove(im)
    return x[..., :3]
R = json.load(open('Saved/Codex/CharacterGuardian_20261001/track/ref_front.json')); c = lambda k: np.mean(np.asarray(R[k]), 0)
rows = []
for it in a[3:]:
    if it.startswith('ref='): img = load(it[4:]); mx = ((c('crv_eyelid_upper_l')+c('crv_eyelid_lower_l'))/2+(c('crv_eyelid_upper_r')+c('crv_eyelid_lower_r'))/2)[0]/2
    else:
        ip, hp = it.split('@'); img = load(ip); X = np.load(hp); mx = topix('front', np.stack([X[28955:29725].mean(0), X[29725:30495].mean(0)])).mean(0)[0]
    m = int(round(mx)); H, W = img.shape[:2]; hw = min(m, W-m)
    Lh = img[:, m:m+hw]; Rh = img[:, m-hw:m]          # image right half = character LEFT
    LL = np.concatenate([Lh[:, ::-1], Lh], 1); RR = np.concatenate([Rh, Rh[:, ::-1]], 1)
    def cr(z, off): return z[y0:y1, max(x0-off, 0):x1-off]
    off = m-hw; seg = [img[y0:y1, x0:x1], cr(LL, off), cr(RR, off)]
    hmin = min(s.shape[0] for s in seg); seg = [s[:hmin] for s in seg]
    gap = np.full((hmin, 6, 3), 0.08, np.float32); rows.append(np.concatenate([seg[0], gap, seg[1], gap, seg[2]], 1))
wmin = min(r.shape[1] for r in rows); rows = [r[:, :wmin] for r in rows]
sep = np.full((6, wmin, 3), 0.08, np.float32); out = np.concatenate(sum([[r, sep] for r in rows], [])[:-1], 0)
h, w = out.shape[:2]; rgba = np.ones((h, w, 4), np.float32); rgba[..., :3] = np.clip(out, 0, 1); im = bpy.data.images.new('o', w, h, alpha=True)
im.pixels.foreach_set(np.ascontiguousarray(rgba[::-1]).ravel()); im.filepath_raw = os.path.abspath(OUT); im.file_format = 'PNG'; im.save()
im2 = bpy.data.images.load(os.path.abspath(OUT)); s = RH*len(rows)/h; im2.scale(int(w*s), int(h*s)); im2.save(); print('SPLIT_OK', OUT, w, h)
