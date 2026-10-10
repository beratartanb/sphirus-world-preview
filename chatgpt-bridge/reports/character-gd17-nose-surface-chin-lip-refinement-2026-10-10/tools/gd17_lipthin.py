"""GD17 lateral upper-lip taper: the upper vermilion of the lateral thirds is compressed vertically toward the lip-contact (stomion) line, so
the upper lip narrows gently into the corners like the reference - the contact line and the commissures themselves do NOT move (no
down-turned / sad mouth). Weight = lateral bell (0 at the Cupid's bow centre and at the commissure) x height ramp (0 at the contact line,
1 across the vermilion, fading to 0 on the skin above the border) x front mask.
z' = zst + (z - zst) * (1 - K*w)     zst(x) = Z0 - 0.3*(|x-MX|/2.35)^2 (contact line model, same as gd15_mouthsplit)
usage: blender -b --python gd17_lipthin.py -- <in.npy> <out.npy> [K=0.18] [centre_offset=1.85] [halfwidth=0.62] [Z0=155.6]"""
import sys, numpy as np
a = sys.argv[sys.argv.index('--')+1:]; X = np.load(a[0]); OUT = a[1]; K = float(a[2]) if len(a) > 2 else 0.18; C = float(a[3]) if len(a) > 3 else 1.85
HW = float(a[4]) if len(a) > 4 else 0.62; Z0 = float(a[5]) if len(a) > 5 else 155.6; NS = 24049; MX = -0.23
def ss(t): t = np.clip(t, 0, 1); return t*t*(3-2*t)
S = X[:NS].copy(); ax = np.abs(S[:, 0]-MX); zst = Z0-0.3*np.clip(ax/2.35, 0, 1.3)**2; h = S[:, 2]-zst
lat = np.clip(1-((ax-C)/HW)**2, 0, 1)**2                       # bell around the lateral third
ht = ss(h/0.06)*(1-ss((h-0.42)/0.22))                          # 0 at contact line -> 1 on the vermilion -> 0 on the skin above
front = ss((S[:, 1]-11.2)/0.4)
w = lat*ht*front; Y = X.copy(); Y[:NS, 2] = zst+h*(1-K*w)
np.save(OUT, Y); d = np.abs(Y[:NS, 2]-S[:, 2])*10; print('LIPTHIN verts w>0.05: %d, max dz %.3f mm' % ((w > 0.05).sum(), d.max()))
