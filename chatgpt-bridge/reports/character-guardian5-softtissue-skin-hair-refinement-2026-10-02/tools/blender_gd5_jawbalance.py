"""GUARDIAN-5: frontal jaw/chin balance in photo space (same method as the user's corrected guide): candidate projected with the Tier A
front camera; facial midline = line fitted (x = a + b*y) through projected midline landmarks (nasion, dorsum, pronasale, subnasale,
philtrum, stomion, chin); left/right visible-contour distances from that axis at equal heights (fractions of eye-line -> menton:
0.54 upper lower-face / mouth, 0.76 mid jaw, 0.91 lower jaw / chin). Px in the Tier A front frame. Read-only diagnostic.
usage: blender -b -P blender_gd5_jawbalance.py -- <head.npy> [...]"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930'))
from gd_common import topix
for hp in sys.argv[sys.argv.index('--')+1:]:
    X = np.load(hp); S = X[:24049]; eL = X[28955:29725].mean(0); eR = X[29725:30495].mean(0); mx = (eL[0]+eR[0])/2; ez = (eL[2]+eR[2])/2
    pts = []
    for z in np.arange(ez+1.0, ez-12.5, -0.5):
        m = (np.abs(S[:, 2]-z) < 0.2) & (np.abs(S[:, 0]-mx) < 1.2) & (S[:, 1] > 6)
        if m.sum(): i = np.nonzero(m)[0]; pts.append(S[i[np.argmax(S[i, 1])]])
    P = topix('front', np.asarray(pts)); b, a = np.polyfit(P[:, 1], P[:, 0], 1)
    keep = S[:, 1] > 3.0; Q = topix('front', S[keep]); pe = topix('front', np.stack([eL, eR])).mean(0)
    j = np.nonzero((S[keep][:, 1] > 8) & (S[keep][:, 2] > 148.5) & (S[keep][:, 2] < 153.5))[0]; men = Q[j[np.argmax(Q[j, 1])]]
    r = {'axis_tilt_px_per_100px': round(float(b*100), 2), 'menton_off_px': round(float(men[0]-(a+b*men[1])), 1)}
    for nm, f in (('upper_lower_face', 0.54), ('mid_jaw', 0.76), ('lower_jaw_chin', 0.91)):
        y = pe[1]+f*(men[1]-pe[1]); band = np.abs(Q[:, 1]-y) < 3.0; ax = a+b*y
        L = float(Q[band, 0].max()-ax); R = float(ax-Q[band, 0].min()); r[nm] = {'L_imgR': round(L, 1), 'R_imgL': round(R, 1), 'delta': round(L-R, 1)}
    print('JAWBAL', os.path.basename(hp), json.dumps(r))
# optional overlay: env OVL="<head.npy>|<clay img in the Tier A front frame>|<out png>" -> red fitted axis, cyan checkpoints, yellow crossings
if os.environ.get('OVL'):
    import bpy
    hp, ip, op = os.environ['OVL'].split('|'); X = np.load(hp); S = X[:24049]; eL = X[28955:29725].mean(0); eR = X[29725:30495].mean(0); mx = (eL[0]+eR[0])/2; ez = (eL[2]+eR[2])/2
    pts = []
    for z in np.arange(ez+1.0, ez-12.5, -0.5):
        m = (np.abs(S[:, 2]-z) < 0.2) & (np.abs(S[:, 0]-mx) < 1.2) & (S[:, 1] > 6)
        if m.sum(): i = np.nonzero(m)[0]; pts.append(S[i[np.argmax(S[i, 1])]])
    P = topix('front', np.asarray(pts)); b, a = np.polyfit(P[:, 1], P[:, 0], 1)
    keep = S[:, 1] > 3.0; Q = topix('front', S[keep]); pe = topix('front', np.stack([eL, eR])).mean(0)
    j = np.nonzero((S[keep][:, 1] > 8) & (S[keep][:, 2] > 148.5) & (S[keep][:, 2] < 153.5))[0]; men = Q[j[np.argmax(Q[j, 1])]]
    im = bpy.data.images.load(os.path.abspath(ip)); w, h = im.size; I = np.asarray(im.pixels[:], np.float32).reshape(h, w, im.channels)[::-1].copy()
    def dot(x, y, c, r=2):
        x, y = int(round(x)), int(round(y)); I[max(y-r, 0):y+r+1, max(x-r, 0):x+r+1, :3] = c
    for yy in np.arange(pe[1]-40, men[1]+15, 1.0): dot(a+b*yy, yy, (1.0, 0.25, 0.25), 1)
    for f in (0.54, 0.76, 0.91):
        y = pe[1]+f*(men[1]-pe[1]); band = np.abs(Q[:, 1]-y) < 3.0; xl, xr = Q[band, 0].min(), Q[band, 0].max()
        for xx in np.arange(xl, xr, 1.0): dot(xx, y, (0.35, 0.8, 1.0), 1)
        dot(xl, y, (0.35, 0.8, 1.0), 5); dot(xr, y, (0.35, 0.8, 1.0), 5); dot(a+b*y, y, (1.0, 0.9, 0.2), 4)
    o = bpy.data.images.new('o', w, h, alpha=True); rgba = np.ones((h, w, 4), np.float32); rgba[..., :3] = I[..., :3]
    o.pixels.foreach_set(np.ascontiguousarray(rgba[::-1]).ravel()); o.filepath_raw = os.path.abspath(op); o.file_format = 'PNG'; o.save(); print('OVL_OK', op)
