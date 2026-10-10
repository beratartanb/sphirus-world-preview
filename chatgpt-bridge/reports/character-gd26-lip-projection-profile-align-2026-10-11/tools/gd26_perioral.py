"""GD26 perioral block advancement with a shape-preserving nose base. One forward (+y) displacement field:
  below the junction ZJ (subnasale level): dy = f(z) (monotone cubic through control points [z, mm]; flat over the lips, fading over sulcus/chin);
  above ZJ (nose base / columella): dy = A * ss((YT - y)/(YT - YS)) * ss((ZB - z)/(ZB - ZA)) - full at and behind the subnasale (y <= YS), 0 at the
  nose tip (y >= YT), so the tip->subnasale outline is compressed horizontally about the tip (shape kept, chord steeper) instead of bulging;
  vertical fade from ZA to ZB keeps the dorsum / upper alae. A = f(ZJ) keeps the field continuous at the junction.
Both parts x lateral plateau ss((X1-|x-MX|)/(X1-X0)) x depth ramp ss((y-Y1)/(Y0-Y1)); skin + teeth (incl. tongue/gums) + saliva move together.
usage: -- <in.npy> <out.npy> <ctrl json [[z,mm],...]> <ZJ> <YS> <YT> <ZA> <ZB> <X0> <X1> <Y0> <Y1>"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD13_Identity_20261009/tools')); from gd13_common import SEG, NS, MX
a = sys.argv[sys.argv.index('--')+1:]; X = np.load(a[0]).astype(float); OUT = a[1]; CP = np.array(json.loads(a[2]), float)
ZJ, YS, YT, ZA, ZB, X0, X1, Y0, Y1 = [float(v) for v in a[3:12]]
def ss(t): t = np.clip(t, 0, 1); return t*t*(3-2*t)
CP = CP[np.argsort(CP[:, 0])]; zc, fc = CP[:, 0], CP[:, 1]/10.0
def pchip(z):
    h = np.diff(zc); m = np.diff(fc)/h; d = np.zeros_like(fc)
    for i in range(1, len(fc)-1):
        if m[i-1]*m[i] > 0: w1, w2 = 2*h[i]+h[i-1], h[i]+2*h[i-1]; d[i] = (w1+w2)/(w1/m[i-1]+w2/m[i])
    d[0] = m[0]; d[-1] = m[-1]; out = np.zeros_like(z); k = np.clip(np.searchsorted(zc, z)-1, 0, len(zc)-2); t = (z-zc[k])/h[k]
    v = (2*t**3-3*t**2+1)*fc[k]+(t**3-2*t**2+t)*h[k]*d[k]+(-2*t**3+3*t**2)*fc[k+1]+(t**3-t**2)*h[k]*d[k+1]
    out = np.where(z < zc[0], fc[0], np.where(z > zc[-1], fc[-1], v)); return out
A = float(pchip(np.array([ZJ]))[0])
idx = list(range(NS))
for part in ('teeth', 'saliva'): idx += list(range(SEG[part][0], SEG[part][1]))
idx = np.array(idx); P = X[idx]; x, y, z = P[:, 0]-MX, P[:, 1], P[:, 2]
low = pchip(np.minimum(z, ZJ)); low = np.where(z <= ZJ, low, 0.0)
high = A*ss((YT-y)/(YT-YS))*ss((ZB-z)/(ZB-ZA)); high = np.where(z > ZJ, high, 0.0)
D = (low+high)*ss((X1-np.abs(x))/(X1-X0))*ss((y-Y1)/(Y0-Y1))
Y = X.copy(); Y[idx, 1] += D; np.save(OUT, Y)
print('PERIORAL A %.2f mm | moved >0.05mm: %d, max %.2f mm, teeth max %.2f mm' % (A*10, (np.abs(D) > 0.005).sum(), np.abs(D).max()*10, np.abs(D[idx >= NS]).max()*10))
