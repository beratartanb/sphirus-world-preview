"""xr2_geopath.py <walkmap prefix> <hubA> <hubB> [...pairs]: draw the shortest walkable paths on the walk map crop -> <prefix>_geo_crop.png"""
import sys, os, heapq, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import xr2_layout as LY, xr2_geodesic as G, pngtool as PT
pre = sys.argv[1]; pairs = list(zip(sys.argv[2::2], sys.argv[3::2]))
free = np.load(pre + '_free.npy'); z = np.load(pre + '_z.npy')


def path(src, dst):
    H, W = free.shape; dist = {src: 0.0}; prev = {}; pq = [(0.0, src)]
    NB = [(-1, 0, 1), (1, 0, 1), (0, -1, 1), (0, 1, 1), (-1, -1, 1.414), (-1, 1, 1.414), (1, -1, 1.414), (1, 1, 1.414)]
    while pq:
        d, (j, i) = heapq.heappop(pq)
        if (j, i) == dst: break
        if d > dist.get((j, i), 1e18): continue
        for dj, di, w in NB:
            jj, ii = j + dj, i + di
            if 0 <= jj < H and 0 <= ii < W and free[jj, ii] and abs(z[jj, ii] - z[j, i]) < 45:
                nd = d + w
                if nd < dist.get((jj, ii), 1e18): dist[(jj, ii)] = nd; prev[(jj, ii)] = (j, i); heapq.heappush(pq, (nd, (jj, ii)))
    p = [dst]
    while p[-1] != src and p[-1] in prev: p.append(prev[p[-1]])
    return p


img = PT.rpng(pre + '_walk.png')
cols = [(255, 0, 255), (0, 255, 255), (255, 255, 255), (255, 128, 0)]
for k, (a, b) in enumerate(pairs):
    for j, i in path(G.cell(free, LY.HUBS[a]), G.cell(free, LY.HUBS[b])): img[j - 1:j + 1, i - 1:i + 1] = cols[k % 4]
c = img[int((-8500 + 16000) / 50):int((10500 + 16000) / 50), int((-6000 + 12000) / 50):int((5500 + 12000) / 50)]
PT.wpng(pre + '_geo_crop.png', np.repeat(np.repeat(c, 2, 0), 2, 1)); print('GEO', pre + '_geo_crop.png')
