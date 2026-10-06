"""pass T: reference vs candidate frame overlay: 50 % blend + candidate silhouette edge (bg-keyed) drawn in magenta on the reference.
usage: blender -b --python blender_g11rt_ovl.py -- <ref.png> <cand.png> <out.png>"""
import bpy, sys, numpy as np
a = sys.argv[sys.argv.index('--')+1:]
def load(p):
    im = bpy.data.images.load(p); w, h = im.size; return np.array(im.pixels[:], np.float32).reshape(h, w, 4)
R = load(a[0]); C = load(a[1]); h = min(R.shape[0], C.shape[0]); w = min(R.shape[1], C.shape[1]); R = R[:h, :w]; C = C[:h, :w]
bg = np.median(np.concatenate([C[:6, :, :3].reshape(-1, 3), C[:, :6, :3].reshape(-1, 3)]), 0); m = np.linalg.norm(C[..., :3]-bg, axis=-1) > 0.06
e = m & ~(np.roll(m, 1, 0) & np.roll(m, -1, 0) & np.roll(m, 1, 1) & np.roll(m, -1, 1)); e = e | np.roll(e, 1, 0) | np.roll(e, 1, 1)
O = R.copy(); O[..., :3] = 0.55*R[..., :3]+0.45*C[..., :3]; O[e, :3] = (1.0, 0.1, 0.9)
P = R.copy(); P[e, :3] = (1.0, 0.1, 0.9)
out = np.concatenate([O, P], 1); im = bpy.data.images.new('o', out.shape[1], out.shape[0]); im.pixels.foreach_set(out.ravel()); im.filepath_raw = a[2]; im.file_format = 'PNG'; im.save(); print('OVL_OK')
