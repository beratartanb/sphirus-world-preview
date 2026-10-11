"""GD31 nostril-interior darkening of the baked base-colour texture (lookdev, new texture name only): the cavity triangles (vertex set
data/cavity_idx.npy; >= 2 cavity corners) are rasterised in UV space with a per-vertex weight (1 inside the cavity, EDGE on the aperture loop,
0 outside), the weight map is blurred by BLUR px and the colour is multiplied by (1 - STRENGTH * w). The outer skin is untouched (weight 0 at the
first non-cavity ring). Writes the new PNG plus a before/after crop for review.
usage: blender -b --python gd31_texnostril.py -- <in.png> <out.png> <topo.npz> <cavity idx.npy> <preview.jpg> [STRENGTH=0.75] [EDGE=0.35] [BLUR=3]"""
import bpy, sys, os, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD13_Identity_20261009/tools')); import gd13_img as gi; from gd13_common import NS
sys.path.insert(0, os.path.join(os.getcwd(), 'Tools/CharacterLookdev_20260930')); from id_common import pkg
a = sys.argv[sys.argv.index('--')+1:]; INP, OUTP, TOPO, CAVP, PREV = a[:5]; ST = float(a[5]) if len(a) > 5 else 0.75; EDGE = float(a[6]) if len(a) > 6 else 0.35; BL = int(a[7]) if len(a) > 7 else 3
P = pkg()['head']; T = np.asarray(P['triangles'], int); UVc = np.asarray(P['uv'], float)
cav = np.zeros(int(T.max())+1, bool); cav[np.load(CAVP)] = True
TP = np.load(TOPO); TT = TP['loops'].reshape(-1, 3); TT = TT[(TT < NS).all(1)]; E = np.unique(np.sort(np.r_[TT[:, [0, 1]], TT[:, [1, 2]], TT[:, [2, 0]]], 1), axis=0)
loop = np.zeros(len(cav), bool); m1 = cav[E[:, 0]] & ~cav[E[:, 1]]; m2 = cav[E[:, 1]] & ~cav[E[:, 0]]; loop[E[m1, 0]] = True; loop[E[m2, 1]] = True
# geodesic depth from the aperture loop into the cavity (Dijkstra over cavity vertices, edge lengths of the base head), smooth weight:
# 0 at the rim, 1 deeper than D0+D1 mm (EDGE re-used as D0 mm, BLUR scales the UV blur)
import heapq
HB = np.load(os.path.join(os.path.dirname(TOPO), 'head_G30S.npy'))[:NS]
adj = [[] for _ in range(len(cav))]
for i, j in E:
    if cav[i] and cav[j]: L = float(np.linalg.norm(HB[i]-HB[j]))*10; adj[i].append((j, L)); adj[j].append((i, L))
dist = np.full(len(cav), np.inf); pq = []
for i in np.nonzero(loop)[0]: dist[i] = 0.0; heapq.heappush(pq, (0.0, i))
while pq:
    d0, i = heapq.heappop(pq)
    if d0 > dist[i]: continue
    for j, L in adj[i]:
        if d0+L < dist[j]: dist[j] = d0+L; heapq.heappush(pq, (d0+L, j))
D0, D1 = EDGE, float(os.environ.get("GD31_D1", "2.0"))
def ssv(t): t = np.clip(t, 0, 1); return t*t*(3-2*t)
wv = np.where(cav & np.isfinite(dist), ssv((dist-D0)/D1), 0.0); print('TEXNOSTRIL geodesic depth max %.2f mm, verts w>0.5: %d' % (np.nanmax(np.where(np.isfinite(dist), dist, 0)), (wv > 0.5).sum()))
I = gi.load(INP); H, W = I.shape[:2]; Wm = np.zeros((H, W), np.float32)
sel = np.nonzero(cav[T].sum(1) >= 2)[0]; print('TEXNOSTRIL cavity triangles', len(sel))
for ti in sel:
    uv = UVc[ti]; xs = uv[:, 0]*W; ys = (1-uv[:, 1])*H; ww = wv[T[ti]]
    u0, u1 = max(int(np.floor(xs.min())), 0), min(int(np.ceil(xs.max())), W-1); v0, v1 = max(int(np.floor(ys.min())), 0), min(int(np.ceil(ys.max())), H-1)
    if u0 > u1 or v0 > v1: continue
    den = (ys[1]-ys[2])*(xs[0]-xs[2])+(xs[2]-xs[1])*(ys[0]-ys[2])
    if abs(den) < 1e-12: continue
    gu, gv = np.meshgrid(np.arange(u0, u1+1)+0.5, np.arange(v0, v1+1)+0.5)
    l0 = ((ys[1]-ys[2])*(gu-xs[2])+(xs[2]-xs[1])*(gv-ys[2]))/den; l1 = ((ys[2]-ys[0])*(gu-xs[2])+(xs[0]-xs[2])*(gv-ys[2]))/den; l2 = 1-l0-l1
    ins = (l0 >= -0.02) & (l1 >= -0.02) & (l2 >= -0.02)
    val = l0*ww[0]+l1*ww[1]+l2*ww[2]; sub = Wm[v0:v1+1, u0:u1+1]; sub[ins] = np.maximum(sub[ins], val[ins])
rr, cc = np.nonzero(Wm > 0)
if len(rr):
    r0, r1, c0, c1 = max(rr.min()-20, 0), min(rr.max()+20, H), max(cc.min()-20, 0), min(cc.max()+20, W)
    box = Wm[r0:r1, c0:c1]; k = np.exp(-0.5*(np.arange(-3*BL, 3*BL+1)/max(BL, 1e-6))**2); k /= k.sum()
    box = np.apply_along_axis(lambda v: np.convolve(v, k, 'same'), 0, box); box = np.apply_along_axis(lambda v: np.convolve(v, k, 'same'), 1, box); Wm[r0:r1, c0:c1] = box
    before = I[r0:r1, c0:c1].copy(); I[r0:r1, c0:c1, :3] *= (1-ST*np.clip(box, 0, 1))[..., None]; after = I[r0:r1, c0:c1]
    pv = np.concatenate([before, np.ones((before.shape[0], 6, 4), np.float32), after], 1); gi.save(PREV, gi.resize(pv, pv.shape[1]*2, pv.shape[0]*2))
    print('TEXNOSTRIL box rows %d-%d cols %d-%d, weighted px %d' % (r0, r1, c0, c1, (box > 0.05).sum()))
gi.save(OUTP, I); print('TEXNOSTRIL_OK', OUTP)
