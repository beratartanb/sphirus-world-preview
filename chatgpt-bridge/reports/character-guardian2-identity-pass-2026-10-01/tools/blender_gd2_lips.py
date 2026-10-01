"""GUARDIAN-2 skin c16: mute the lip colour of the head base colour (less saturated pink, slightly browner / darker, as in the reference);
soft UV window around the lips, detail kept. usage: blender -b --factory-startup --python blender_gd2_lips.py -- <in BC> <out BC> [desat=0.3] [dark=0.06]; c17+: warm brown-rose shift (1, 0.95, 0.88) instead of a blue cut"""
import bpy, sys, os, numpy as np
a = sys.argv[sys.argv.index('--')+1:]; IN, OUT = a[0], a[1]; DS = float(a[2]) if len(a) > 2 else 0.3; DK = float(a[3]) if len(a) > 3 else 0.06
im = bpy.data.images.load(os.path.abspath(IN)); w, h = im.size; X = np.asarray(im.pixels[:], np.float32).reshape(h, w, im.channels)[::-1][..., :3].copy(); bpy.data.images.remove(im)
def sstep(x): x = np.clip(x, 0, 1); return x*x*(3-2*x)
V, U = np.mgrid[0:h, 0:w].astype(np.float32); U = (U+0.5)/w; V = (V+0.5)/h
d = np.sqrt(((U-0.5)/0.10)**2+((V-0.587)/0.045)**2); m = (1-sstep((d-0.8)/0.4))
red = np.clip((X[..., 0]-0.5*(X[..., 1]+X[..., 2])-0.12)/0.12, 0, 1)   # only the reddish vermilion pixels inside the window
m = m*red; g = X.mean(-1, keepdims=True); Y = X+(g-X)*DS*m[..., None]; Y = Y*(1-DK*m[..., None]); WT = np.array([1.0, 0.95, 0.88]); Y = Y*(1+(WT-1)*m[..., None])
o = bpy.data.images.new('o', w, h, alpha=True); rgba = np.ones((h, w, 4), np.float32); rgba[..., :3] = np.clip(Y, 0, 1)[::-1]
o.pixels.foreach_set(rgba.ravel()); o.filepath_raw = os.path.abspath(OUT); o.file_format = 'PNG'; o.save(); print('LIPS_OK', OUT, float(m.max()), int((m > 0.2).sum()))
