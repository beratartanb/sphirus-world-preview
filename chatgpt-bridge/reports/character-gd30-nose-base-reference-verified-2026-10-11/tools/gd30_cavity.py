"""GD30 nostril-opening comparison. (1) The nostril CAVITY vertex set is defined once on a base head (default GD28 G28S) and stored as indices:
skin vertices near each nostril axis (segment from the sill to the vestibule dome, per side) whose normal points back toward the axis
(inner walls / roof), within the nose base box. (2) For a candidate head and solved view, a 0.5 px vertex-splat z-buffer gives the visible
surface per cell; cells whose nearest surface is a cavity vertex form the model's visible nostril OPENING (what is dark in a photo).
(3) The reference opening is the darkest connected blob (luminance percentile) inside the ROI. Prints extents of both (front/back column,
top/bottom row per column bins, area) and draws REF opening (orange outline) and model opening (cyan fill) on the reference zoom.
usage: define: -- define <base.npy> <out idx.npy>
       compare: -- cmp <out.jpg> <idx.npy> <cams.json> <view> <ref panel> <x0,x1,y0,y1> <S> <pct> label=head.npy [...]"""
import sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD13_Identity_20261009/tools')); from gd13_common import NS, MX, project, depth, view_dir, skin_normals
a = sys.argv[sys.argv.index('--')+1:]
if a[0] == 'define':
    X = np.load(a[1]); S = X[:NS]; NN = skin_normals(X); x = S[:, 0]-MX; idx = []
    for sg in (1, -1):
        A = np.array([0.72*sg, 13.15, 157.55]); Bp = np.array([0.80*sg, 14.35, 158.55]); d = Bp-A; L = np.linalg.norm(d); d /= L
        P = S-[MX, 0, 0]; t = np.clip((P-A)@d, 0, L); Q = A+t[:, None]*d; r = np.linalg.norm(P-Q, axis=1); toward = ((Q-P)*NN).sum(1)/np.maximum(r, 1e-9)
        m = (r < 0.42) & (toward > 0.15) & (x*sg > 0.18) & (x*sg < 1.35) & (S[:, 1] > 12.9) & (S[:, 1] < 14.9) & (S[:, 2] > 157.35) & (S[:, 2] < 158.95)
        idx += list(np.nonzero(m)[0])
    idx = np.array(sorted(set(idx))); np.save(a[2], idx); print('CAVITY_DEFINED %d vertices' % len(idx)); sys.exit(0)
import gd13_img as gi
OUT, IDX, CAMS, VIEW, REF = a[1:6]; x0, x1, y0, y1 = [int(v) for v in a[6].split(',')]; S = int(a[7]); PCT = float(a[8]); HEADS = a[9:]
cav = np.zeros(NS, bool); cav[np.load(IDX)] = True; C = json.load(open(CAMS))[VIEW]
TP = np.load(os.path.join(os.path.dirname(IDX), 'head_topo.npz')); TRIS = TP['loops'].reshape(-1, 3); TRIS = TRIS[(TRIS < NS).all(1)]; TRICAV = cav[TRIS].sum(1) >= 2
R = gi.load(REF); Lm = R[y0:y1, x0:x1, :3].mean(-1); m = Lm < np.percentile(Lm, PCT)
lab = np.zeros(m.shape, int); n = 0; best = None
for r in range(m.shape[0]):
    for c in range(m.shape[1]):
        if m[r, c] and not lab[r, c]:
            n += 1; st = [(r, c)]; lab[r, c] = n; cnt = 0
            while st:
                rr, cc = st.pop(); cnt += 1
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    q = (rr+dr, cc+dc)
                    if 0 <= q[0] < m.shape[0] and 0 <= q[1] < m.shape[1] and m[q] and not lab[q]: lab[q] = n; st.append(q)
            if best is None or cnt > best[1]: best = (n, cnt)
RB = lab == best[0]
def ext(M, sc):
    rr, cc = np.nonzero(M);
    if not len(rr): return None
    cols = cc/sc+x0; rows = rr/sc+y0; return (cols.min(), cols.max(), rows.min(), rows.max(), len(rr)/sc/sc)
e = ext(RB, 1); print('%-8s opening cols %.1f-%.1f rows %.1f-%.1f area %.1f px^2' % ('REF', *e))
W, H = (x1-x0)*S, (y1-y0)*S; base = gi.resize(R[y0:y1, x0:x1].copy(), W, H); base[..., :3] = base[..., :3]*0.7+0.15
RBz = gi.resize(np.dstack([RB.astype(float)]*3+[np.ones(RB.shape)]), W, H)[..., 0] > 0.5
edge = RBz ^ (np.roll(RBz, 1, 0) & np.roll(RBz, -1, 0) & np.roll(RBz, 1, 1) & np.roll(RBz, -1, 1))
tiles = []
for h in HEADS:
    lb, p = h.split('=', 1); X = np.load(p); P = X[:NS]; NN = skin_normals(X); uv = project(C, P); dp = depth(C, P); vd = view_dir(C)
    cen = P[TRIS].mean(1); TRI_NOSE = np.nonzero((cen[:, 1] > 11.0) & (cen[:, 2] > 155.5) & (cen[:, 2] < 162.0) & (np.abs(cen[:, 0]-MX) < 3.5))[0]
    K = 4; W2, H2 = (x1-x0)*K, (y1-y0)*K; zb = np.full((H2, W2), np.inf); own = np.full((H2, W2), -1)
    U = (uv[:, 0]-x0)*K; Vv = (uv[:, 1]-y0)*K
    for ti in TRI_NOSE:
        a_, b_, c_ = TRIS[ti]; xs = np.array([U[a_], U[b_], U[c_]]); ys = np.array([Vv[a_], Vv[b_], Vv[c_]]); zs = np.array([dp[a_], dp[b_], dp[c_]])
        u0, u1 = max(int(np.floor(xs.min())), 0), min(int(np.ceil(xs.max())), W2-1); v0, v1 = max(int(np.floor(ys.min())), 0), min(int(np.ceil(ys.max())), H2-1)
        if u0 > u1 or v0 > v1: continue
        den = (ys[1]-ys[2])*(xs[0]-xs[2])+(xs[2]-xs[1])*(ys[0]-ys[2])
        if abs(den) < 1e-12: continue
        gu, gv = np.meshgrid(np.arange(u0, u1+1)+0.5, np.arange(v0, v1+1)+0.5)
        l0 = ((ys[1]-ys[2])*(gu-xs[2])+(xs[2]-xs[1])*(gv-ys[2]))/den; l1 = ((ys[2]-ys[0])*(gu-xs[2])+(xs[0]-xs[2])*(gv-ys[2]))/den; l2 = 1-l0-l1
        ins = (l0 >= 0) & (l1 >= 0) & (l2 >= 0)
        if not ins.any(): continue
        zz = l0*zs[0]+l1*zs[1]+l2*zs[2]; vv, uu = np.nonzero(ins); vv += v0; uu += u0; zv = zz[ins]
        better = zv < zb[vv, uu]; zb[vv[better], uu[better]] = zv[better]; own[vv[better], uu[better]] = ti
    CM = (own >= 0) & TRICAV[np.maximum(own, 0)]
    e = ext(CM, K); RBk = np.kron(RB, np.ones((K, K), bool)); inter = (RBk & CM).sum(); uni = (RBk | CM).sum(); iou = inter/max(uni, 1)
    rc = np.nonzero(RBk); mc = np.nonzero(CM); dr = (mc[0].mean()-rc[0].mean())/K if len(mc[0]) else np.nan; dcol = (mc[1].mean()-rc[1].mean())/K if len(mc[0]) else np.nan
    print('%-8s opening cols %.1f-%.1f rows %.1f-%.1f area %.1f px^2 | IoU %.3f  centre d(col,row) %+.1f %+.1f px' % ((lb,)+e+(iou, dcol, dr)) if e else '%-8s no visible opening' % lb)
    T = base.copy(); CMz = gi.resize(np.dstack([CM.astype(float)]*3+[np.ones(CM.shape)]), W, H)[..., 0] > 0.5
    T[CMz, :3] = T[CMz, :3]*0.3+np.array([0.1, 0.85, 1.0])*0.7; T[edge, :3] = (1.0, 0.55, 0.0)
    for Y in range(y0, y1+1):
        if Y % 5 == 0: T[min((Y-y0)*S, H-1), :(14 if Y % 10 == 0 else 7), :3] = (1, 1, 0)
    for Xc in range(x0, x1+1):
        if Xc % 5 == 0: T[:(14 if Xc % 10 == 0 else 7), min((Xc-x0)*S, W-1), :3] = (1, 1, 0)
    tiles.append(T)
O = np.zeros((H, len(tiles)*(W+6)-6, 4)); O[..., 3] = 1
for i, T in enumerate(tiles): O[:, i*(W+6):i*(W+6)+W] = T
gi.save(OUT, O); print('CAVITY_OK', OUT)
