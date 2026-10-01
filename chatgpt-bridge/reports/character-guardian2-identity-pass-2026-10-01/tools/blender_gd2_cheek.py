"""GUARDIAN-2 pass skin c15: (1) pull the baked rosy / mauve cheek patch of the head base colour toward the surrounding skin ring colour
(low-frequency, per-channel gain in [0.8, 1.25], detail kept), (2) optional light natural freckle density on nose bridge / upper cheeks
(small soft warm-brown specks, low contrast, seeded). No wrinkle / bag / hollow is introduced.
usage: blender -b --factory-startup --python blender_gd2_cheek.py -- <in BC png> <out BC png> [AMT=0.6] [FRECKLE=0.0]"""
import bpy, sys, os, json, numpy as np
a = sys.argv[sys.argv.index('--')+1:]; IN, OUT = a[0], a[1]; AMT = float(a[2]) if len(a) > 2 else 0.6; FR = float(a[3]) if len(a) > 3 else 0.0
im = bpy.data.images.load(os.path.abspath(IN)); w, h = im.size; X = np.asarray(im.pixels[:], np.float32).reshape(h, w, im.channels)[::-1][..., :3].copy(); bpy.data.images.remove(im)
def s2l(x): return np.where(x <= 0.04045, x/12.92, ((x+0.055)/1.055)**2.4)
def l2s(x): x = np.clip(x, 0, 1); return np.where(x <= 0.0031308, x*12.92, 1.055*x**(1/2.4)-0.055)
def sstep(x): x = np.clip(x, 0, 1); return x*x*(3-2*x)
def blur(m, r):
    c = np.cumsum(np.pad(m, ((r+1, r), (0, 0), (0, 0)), mode='edge'), 0); m = (c[2*r+1:]-c[:-2*r-1])/(2*r+1)
    c = np.cumsum(np.pad(m, ((0, 0), (r+1, r), (0, 0)), mode='edge'), 1); return (c[:, 2*r+1:]-c[:, :-2*r-1])/(2*r+1)
L = s2l(X); f = 8; Ls = L.reshape(h//f, f, w//f, f, 3).mean((1, 3)); hs, ws = Ls.shape[:2]; Lb = blur(blur(Ls, 5), 5)
yy, xx = np.mgrid[0:hs, 0:ws].astype(np.float32); U = (xx+0.5)/ws; V = (yy+0.5)/hs
gain = np.ones((hs, ws, 3), np.float32); rep = {}
for cu, cv, ru, rv in ((0.29, 0.455, 0.115, 0.085), (0.71, 0.455, 0.115, 0.085)):
    d = np.sqrt(((U-cu)/ru)**2+((V-cv)/rv)**2); m = 1-sstep((d-0.7)/0.4); ring = (d > 1.2) & (d < 1.7) & (V > 0.33)
    ref = np.median(Lb[ring], 0); g = np.clip(1+AMT*(ref[None, None, :]/np.maximum(Lb, 1e-4)-1), 0.8, 1.25)
    gain = gain*(1-m[..., None])+g*m[..., None]; rep[f'{cu}'] = {'ring': np.round(ref, 4).tolist(), 'centre': np.round(Lb[d < 0.5].mean(0), 4).tolist()}
gain = blur(gain, 3); gu = np.repeat(np.repeat(gain, f, 0), f, 1)[:h, :w]; L = L*gu
if FR > 0:   # freckles: soft specks, density mask on nose bridge + upper cheeks (UV), warm brown, darken only
    rng = np.random.default_rng(7); uu = (np.arange(w)+0.5)/w; vv = (np.arange(h)+0.5)/h
    def dens(u, v):
        nose = np.exp(-(((u-0.5)/0.06)**2+((v-0.43)/0.07)**2)); ch = sum(np.exp(-(((u-cu)/0.10)**2+((v-0.44)/0.06)**2)) for cu in (0.33, 0.67)); return np.clip(nose+0.8*ch, 0, 1)
    N = int(2600*FR); P = rng.random((N*4, 2)); keep = rng.random(N*4) < dens(P[:, 0], P[:, 1]); P = P[keep][:N]
    col = np.array([0.36, 0.20, 0.11]); spot = np.zeros((h, w), np.float32)
    for (u, v) in P:
        r = rng.uniform(1.6, 3.6); cx, cy = u*w, v*h; x0, x1, y0, y1 = int(cx-3*r), int(cx+3*r)+1, int(cy-3*r), int(cy+3*r)+1
        if x0 < 0 or y0 < 0 or x1 >= w or y1 >= h: continue
        gx, gy = np.meshgrid(np.arange(x0, x1)-cx, np.arange(y0, y1)-cy); k = np.exp(-(gx**2+gy**2)/(2*r*r))*rng.uniform(0.25, 0.6)
        spot[y0:y1, x0:x1] = np.maximum(spot[y0:y1, x0:x1], k)
    sp = spot[..., None]*FR; L = L*(1-sp)+L*np.clip(col/np.maximum(L.mean((0, 1)), 1e-3), 0.3, 1.0)*sp; rep['freckles'] = int(len(P))
out = l2s(L); o = bpy.data.images.new('o', w, h, alpha=True); rgba = np.ones((h, w, 4), np.float32); rgba[..., :3] = out[::-1]
o.pixels.foreach_set(rgba.ravel()); o.filepath_raw = os.path.abspath(OUT); o.file_format = 'PNG'; o.save()
print('CHEEK_OK', OUT, json.dumps(rep))
