"""GD30 which-vertices map: visible nose-base skin vertices (y > YMIN, z < ZMAX) projected with a solved camera over a render (2x frame), coloured
by |x-MX| band: < 0.3 red (columella), 0.3-0.65 yellow (columella-lobule junction / infratip), 0.65-1.0 green (soft triangle / medial rim),
1.0-1.4 cyan (rim / lobule), > 1.4 blue (lateral lobule). Also y bands as dot size? no - second tile coloured by y: < 13.5 blue, 13.5-14.2 cyan,
14.2-14.8 green, 14.8-15.3 yellow, > 15.3 red. usage: -- <out.jpg> <head.npy> <cams.json> <view> <render2x.png> <x0,x1,y0,y1 (1x)> <S> [YMIN=12.3] [ZMAX=159.3]"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD13_Identity_20261009/tools')); import gd13_img as gi; from gd13_common import NS, MX, project, depth, view_dir, skin_normals
a = sys.argv[sys.argv.index('--')+1:]; OUT, HEAD, CAMS, VIEW, IMG = a[:5]; x0, x1, y0, y1 = [int(v) for v in a[5].split(',')]; S = int(a[6])
YMIN = float(a[7]) if len(a) > 7 else 12.3; ZMAX = float(a[8]) if len(a) > 8 else 159.3
X = np.load(HEAD); P = X[:NS]; NN = skin_normals(X); c = json.load(open(CAMS))[VIEW]; uv = project(c, P); dp = depth(c, P); vd = view_dir(c)
gx = np.floor((uv[:, 0]-x0)*2).astype(int); gy = np.floor((uv[:, 1]-y0)*2).astype(int); W2, H2 = (x1-x0)*2, (y1-y0)*2
ins = (gx >= 0) & (gx < W2) & (gy >= 0) & (gy < H2); zb = np.full((H2, W2), np.inf); np.minimum.at(zb, (gy[ins], gx[ins]), dp[ins])
vis = np.zeros(NS, bool); vis[ins] = dp[ins] <= zb[gy[ins], gx[ins]]+0.12; vis &= (NN@vd) > 0.0
m = vis & (P[:, 1] > YMIN) & (P[:, 2] < ZMAX); ax = np.abs(P[:, 0]-MX)
I = gi.load(IMG); crop = I[y0*2:y1*2, x0*2:x1*2]; base = gi.resize(crop, (x1-x0)*S, (y1-y0)*S); base[..., :3] = base[..., :3]*0.6+0.2
def tile(colfn):
    T = base.copy()
    for i in np.nonzero(m)[0]:
        u = int(round((uv[i, 0]-x0)*S)); v = int(round((uv[i, 1]-y0)*S))
        if 1 <= u < T.shape[1]-1 and 1 <= v < T.shape[0]-1: T[v-1:v+2, u-1:u+2, :3] = colfn(i)
    for Y in range(y0, y1+1):
        if Y % 5 == 0: T[min((Y-y0)*S, T.shape[0]-1), :(14 if Y % 10 == 0 else 7), :3] = (1, 1, 0)
    for Xc in range(x0, x1+1):
        if Xc % 5 == 0: T[:(14 if Xc % 10 == 0 else 7), min((Xc-x0)*S, T.shape[1]-1), :3] = (1, 1, 0)
    return T
XC = lambda i: (1, .2, .2) if ax[i] < 0.3 else (1, 1, .2) if ax[i] < 0.65 else (.2, 1, .2) if ax[i] < 1.0 else (.2, .9, 1) if ax[i] < 1.4 else (.3, .4, 1)
YC = lambda i: (.3, .4, 1) if P[i, 1] < 13.5 else (.2, .9, 1) if P[i, 1] < 14.2 else (.2, 1, .2) if P[i, 1] < 14.8 else (1, 1, .2) if P[i, 1] < 15.3 else (1, .2, .2)
A, Bt = tile(XC), tile(YC); O = np.zeros((A.shape[0], A.shape[1]*2+6, 4)); O[..., 3] = 1; O[:, :A.shape[1]] = A; O[:, A.shape[1]+6:] = Bt
gi.save(OUT, O); print('XBANDS_OK', OUT)
