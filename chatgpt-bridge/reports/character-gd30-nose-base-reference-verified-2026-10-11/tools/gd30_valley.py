"""GD30 reference reading aid: an S-times zoom of a panel ROI with a labelled pixel grid (thin line every 1 panel px is too dense - lines every
5 px, labelled every 10 px with a small bitmap font), next to a VALLEY map: Hessian of the Gaussian-smoothed luminance (sigma px), largest
eigenvalue > 0 = a dark line (crease / nostril edge), shown red over the grey image. Optional polylines (panel px) are drawn on both tiles
in given colours so traced reference curves can be checked against the photo.
usage: -- <out.jpg> <image> <scale of image vs panel (1 or 2)> <x0,x1,y0,y1 panel px> <S> <sigma> [name=color=x,y;x,y;...] ..."""
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD13_Identity_20261009/tools')); import gd13_img as gi
a = sys.argv[sys.argv.index('--')+1:]; OUT, IMG = a[0], a[1]; SC = float(a[2]); x0, x1, y0, y1 = [int(v) for v in a[3].split(',')]; S = int(a[4]); SIG = float(a[5]); PL = a[6:]
I = gi.load(IMG); crop = I[int(y0*SC):int(y1*SC), int(x0*SC):int(x1*SC), :3]
L = crop.mean(-1)
def gblur(A, s):
    r = int(3*s+1); k = np.exp(-0.5*(np.arange(-r, r+1)/s)**2); k /= k.sum(); P = np.pad(A, r, mode='edge')
    P = np.apply_along_axis(lambda v: np.convolve(v, k, 'valid'), 0, P); return np.apply_along_axis(lambda v: np.convolve(v, k, 'valid'), 1, P)
G = gblur(L, SIG*SC); gy, gx = np.gradient(G); gyy, gyx = np.gradient(gy); gxy, gxx = np.gradient(gx)
tr = gxx+gyy; det = gxx*gyy-gxy*gyx; lam = tr/2+np.sqrt(np.maximum(tr**2/4-det, 0)); V = np.clip(lam/np.percentile(lam[lam > 0], 98), 0, 1)
W, H = (x1-x0)*S, (y1-y0)*S
A = gi.resize(np.dstack([crop, np.ones(crop.shape[:2])]), W, H).copy(); Vz = gi.resize(np.dstack([V, V, V, np.ones(V.shape)]), W, H)[..., 0]
Bt = A.copy(); g = Bt[..., :3].mean(-1, keepdims=True)*0.55+0.25; Bt[..., :3] = g*(1-Vz[..., None])+np.array([1.0, 0.1, 0.05])*Vz[..., None]
FONT = {'0': ['111', '101', '101', '101', '111'], '1': ['010', '110', '010', '010', '111'], '2': ['111', '001', '111', '100', '111'], '3': ['111', '001', '111', '001', '111'],
        '4': ['101', '101', '111', '001', '001'], '5': ['111', '100', '111', '001', '111'], '6': ['111', '100', '111', '101', '111'], '7': ['111', '001', '010', '010', '010'],
        '8': ['111', '101', '111', '101', '111'], '9': ['111', '101', '111', '001', '111']}
def text(T, s, px, py, col=(1, 1, 0), k=2):
    for ci, ch in enumerate(s):
        for r, row in enumerate(FONT[ch]):
            for c, b in enumerate(row):
                if b == '1':
                    yy, xx = py+r*k, px+(ci*4+c)*k
                    if 0 <= yy < T.shape[0]-k and 0 <= xx < T.shape[1]-k: T[yy:yy+k, xx:xx+k, :3] = col
def grid(T):
    for X in range(x0, x1+1):
        if X % 5 == 0:
            u = (X-x0)*S; T[:, min(u, T.shape[1]-1), :3] = T[:, min(u, T.shape[1]-1), :3]*0.6+(0.4 if X % 10 == 0 else 0.2)
            if X % 10 == 0: text(T, str(X), u+2, 2)
    for Y in range(y0, y1+1):
        if Y % 5 == 0:
            v = (Y-y0)*S; T[min(v, T.shape[0]-1), :, :3] = T[min(v, T.shape[0]-1), :, :3]*0.6+(0.4 if Y % 10 == 0 else 0.2)
            if Y % 10 == 0: text(T, str(Y), 2, v+2)
COL = {'c': (0.1, 0.9, 1.0), 'o': (1.0, 0.6, 0.0), 'g': (0.2, 1.0, 0.2), 'm': (1.0, 0.2, 1.0), 'y': (1.0, 1.0, 0.0), 'w': (1, 1, 1), 'b': (0.2, 0.4, 1.0)}
def poly(T, pts, col):
    for (ax, ay), (bx, by) in zip(pts[:-1], pts[1:]):
        n = int(max(abs(bx-ax), abs(by-ay))*S*2)+1
        for t in np.linspace(0, 1, n):
            u = int(round(((ax+(bx-ax)*t)-x0)*S)); v = int(round(((ay+(by-ay)*t)-y0)*S))
            if 1 <= u < T.shape[1]-1 and 1 <= v < T.shape[0]-1: T[v-1:v+2, u-1:u+2, :3] = col
for T in (A, Bt):
    grid(T)
    for p in PL:
        nm, col, s = p.split('=', 2); pts = [tuple(float(q) for q in xy.split(',')) for xy in s.split(';') if xy]; poly(T, pts, COL[col])
O = np.zeros((H, W*2+8, 4)); O[..., 3] = 1; O[:, :W] = A; O[:, W+8:] = Bt; gi.save(OUT, O); print('VALLEY_OK', OUT)
