"""GUARDIAN face pass: lift the baked grey-purple periorbital patch of the head base colour (reads as eyeshadow / fatigue; the clay
render shows no matching form). Low-frequency, per-channel, self-limiting gain: inside a soft periorbital window, pixels whose blurred
colour is darker than the surrounding skin ring are pulled AMT of the way toward the ring colour; detail (pores, freckles) kept.
usage: blender -b --factory-startup --python blender_gd_periorbital.py -- <in BC png> <out BC png> [AMT=0.75]"""
import bpy, sys, os, numpy as np
a = sys.argv[sys.argv.index('--')+1:]; IN, OUT = a[0], a[1]; AMT = float(a[2]) if len(a) > 2 else 0.75
im = bpy.data.images.load(os.path.abspath(IN)); w, h = im.size; X = np.asarray(im.pixels[:], np.float32).reshape(h, w, im.channels)[::-1][..., :3].copy(); bpy.data.images.remove(im)
def s2l(x): return np.where(x <= 0.04045, x/12.92, ((x+0.055)/1.055)**2.4)
def l2s(x): x = np.clip(x, 0, 1); return np.where(x <= 0.0031308, x*12.92, 1.055*x**(1/2.4)-0.055)
L = s2l(X); f = 8; Ls = L.reshape(h//f, f, w//f, f, 3).mean((1, 3)); hs, ws = Ls.shape[:2]
def blur(m, r):
    c = np.cumsum(np.pad(m, ((r+1, r), (0, 0), (0, 0)), mode='edge'), 0); m = (c[2*r+1:]-c[:-2*r-1])/(2*r+1)
    c = np.cumsum(np.pad(m, ((0, 0), (r+1, r), (0, 0)), mode='edge'), 1); return (c[:, 2*r+1:]-c[:, :-2*r-1])/(2*r+1)
Lb = blur(blur(Ls, 4), 4)
yy, xx = np.mgrid[0:hs, 0:ws].astype(np.float32); U = (xx+0.5)/ws; V = (yy+0.5)/hs
def sstep(x): x = np.clip(x, 0, 1); return x*x*(3-2*x)
win = np.zeros((hs, ws), np.float32); gain = np.ones((hs, ws, 3), np.float32); rep = {}
for cu, cv, ru, rv in ((0.38, 0.35, 0.10, 0.055), (0.62, 0.35, 0.10, 0.055), (0.383, 0.291, 0.11, 0.032), (0.617, 0.291, 0.11, 0.032)):
    d = np.sqrt(((U-cu)/ru)**2+((V-cv)/rv)**2); m = 1-sstep((d-0.75)/0.35)
    ring = (d > 1.15) & (d < 1.6)
    ref = np.median(Lb[ring], 0); rep[f'{cu},{cv}'] = (np.round(ref, 4).tolist(), np.round(Lb[d < 0.6].mean(0), 4).tolist())
    g = np.clip(1+AMT*(ref[None, None, :]/np.maximum(Lb, 1e-4)-1), 1.0, 1.8)   # only lighten
    gain = np.maximum(gain, gain*(1-m[..., None])+g*m[..., None]); win = np.maximum(win, m)
gain = blur(gain, 3); gu = np.repeat(np.repeat(gain, f, 0), f, 1)[:h, :w]
out = l2s(L*gu); o = bpy.data.images.new('o', w, h, alpha=True); rgba = np.ones((h, w, 4), np.float32); rgba[..., :3] = out[::-1]
o.pixels.foreach_set(rgba.ravel()); o.filepath_raw = os.path.abspath(OUT); o.file_format = 'PNG'; o.save()
print('PERIORBITAL_OK', OUT, 'ring vs centre (lin rgb)', rep, 'gain max', np.round(gain.max((0, 1)), 3).tolist())
