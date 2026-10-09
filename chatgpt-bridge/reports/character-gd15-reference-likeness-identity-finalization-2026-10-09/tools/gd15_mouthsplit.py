"""GD15 mouth preset blend with separate upper / lower lip weights (region blends are exactly linear in the weight: verified 0.00 mm).
New head = head - w_old*(preset_old - probe) + [wu*w_up + wl*(1-w_up)]*(preset_new - probe), w_up = smooth step across the stomion line
(z_st = 155.6 at the midline, 155.3 at the corners, 1.6 mm blend band) so the commissures and the mouth interior / teeth blend continuously.
usage: blender -b --python gd15_mouthsplit.py -- <head.npy> <probe.f32> <old preset.f32> <w_old> <new preset.f32> <w_upper> <w_lower> <out.npy>"""
import sys, numpy as np
a = sys.argv[sys.argv.index('--')+1:]
L = lambda f: np.fromfile(f, np.float32).reshape(-1, 3).astype(float)
X = np.load(a[0]); P = L(a[1]); O = L(a[2]); wo = float(a[3]); Nw = L(a[4]); wu = float(a[5]); wl = float(a[6]); MX = -0.23
ax = np.abs(P[:, 0]-MX); zst = 155.6-0.3*np.clip(ax/2.35, 0, 1.5)**2
t = np.clip((P[:, 2]-zst+0.08)/0.16, 0, 1); wup = t*t*(3-2*t)
Y = X-wo*(O-P)+((wu*wup+wl*(1-wup))[:, None])*(Nw-P); np.save(a[7], Y)
print('MOUTHSPLIT max change %.2f mm' % (np.linalg.norm(Y-X, axis=1).max()*10))
