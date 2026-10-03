"""GUARDIAN-14 skin k12 = k11 BC with the lip colour muted (Tier A: muted rose-brown, low saturation; k11 lips render too red / dark).
Lip region = soft ellipse in the MetaHuman head UV (same as blender_gd4_skin.py 'lips': centre (0.5, 0.595), radii (0.105, 0.042)), feathered.
lip' = mix(lip, luminance*LIPLIFT*tint, LIPMIX).  usage: blender -b -P blender_gd14_skin_lips.py -- <in BC> <out BC> [mix] [lift]"""
import bpy, sys, os, numpy as np
a = sys.argv[sys.argv.index('--')+1:]; src, dst = a[0], a[1]; MIX = float(a[2]) if len(a) > 2 else 0.35; LIFT = float(a[3]) if len(a) > 3 else 1.06
im = bpy.data.images.load(os.path.abspath(src)); w, h = im.size; x = np.asarray(im.pixels[:], np.float32).reshape(h, w, im.channels)[::-1].copy()
v, u = np.mgrid[0:h, 0:w]; u = (u+0.5)/w; v = (v+0.5)/h
def sstep(t): t = np.clip(t, 0, 1); return t*t*(3-2*t)
r = np.sqrt(((u-0.5)/0.105)**2+((v-0.595)/0.042)**2); m = (1-sstep((r-0.75)/0.4))[..., None]
rgb = x[..., :3]; lum = (rgb*np.array([0.30, 0.59, 0.11], np.float32)).sum(2, keepdims=True)
tgt = np.clip(lum*LIFT*np.array([1.10, 0.95, 0.90], np.float32), 0, 1)
x[..., :3] = rgb*(1-MIX*m)+tgt*MIX*m
o = bpy.data.images.new('o', w, h, alpha=True); o.pixels.foreach_set(np.ascontiguousarray(x[::-1]).ravel()); o.filepath_raw = os.path.abspath(dst); o.file_format = 'PNG'; o.save(); print('LIPS_OK', MIX, LIFT)
