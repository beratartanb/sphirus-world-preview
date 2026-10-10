"""GD20 smooth perioral profile field: ONE low-frequency displacement along +y (forward) whose magnitude is a smooth function of z (monotone cubic through
control points [z, mm]), a lateral plateau in |x - MX| (full to X0, smooth fade to X1) and full tissue thickness in y (1 for y >= Y0, fading to 0 at Y1),
applied to the skin AND to the teeth / saliva parts by the same field (no inner-sheet shear, no stacked-bump ripples).
usage: -- <in.npy> <out.npy> <ctrl json [[z, mm], ...]> <X0> <X1> <Y0> <Y1>"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD13_Identity_20261009/tools')); from gd13_common import SEG, NS, MX
a = sys.argv[sys.argv.index('--')+1:]; X = np.load(a[0]).astype(float); OUT = a[1]; CP = np.array(json.loads(a[2]), float); X0, X1, Y0, Y1 = [float(v) for v in a[3:7]]
CP = CP[np.argsort(CP[:, 0])]; zc, fc = CP[:, 0], CP[:, 1]/10.0
def ss(t): t = np.clip(t, 0, 1); return t*t*(3-2*t)
def pchip(z):   # monotone cubic (Fritsch-Carlson) through the control points, 0 outside
    h = np.diff(zc); m = np.diff(fc)/h; d = np.zeros_like(fc)
    for i in range(1, len(fc)-1):
        if m[i-1]*m[i] > 0: w1, w2 = 2*h[i]+h[i-1], h[i]+2*h[i-1]; d[i] = (w1+w2)/(w1/m[i-1]+w2/m[i])
    d[0] = m[0]; d[-1] = m[-1]; out = np.zeros_like(z); k = np.clip(np.searchsorted(zc, z)-1, 0, len(zc)-2); t = (z-zc[k])/h[k]; inside = (z >= zc[0]) & (z <= zc[-1])
    h00 = 2*t**3-3*t**2+1; h10 = t**3-2*t**2+t; h01 = -2*t**3+3*t**2; h11 = t**3-t**2
    out[inside] = (h00*fc[k]+h10*h[k]*d[k]+h01*fc[k+1]+h11*h[k]*d[k+1])[inside]; return out
def field(P):
    f = pchip(P[:, 2]); gx = ss((X1-np.abs(P[:, 0]-MX))/(X1-X0)); hy = ss((P[:, 1]-Y1)/(Y0-Y1)); return f*gx*hy
Y = X.copy(); idx = list(range(NS))
for part in ('teeth', 'saliva'):
    if part in SEG: idx += list(range(SEG[part][0], SEG[part][1]))
idx = np.array(idx); D = field(X[idx]); Y[idx, 1] += D
print('PROFIELD verts moved >0.05mm: %d, max %.2f mm, teeth max %.2f mm' % ((np.abs(D) > 0.005).sum(), np.abs(D).max()*10, (np.abs(field(X[SEG['teeth'][0]:SEG['teeth'][1]])).max()*10 if 'teeth' in SEG else 0)))
np.save(OUT, Y)
