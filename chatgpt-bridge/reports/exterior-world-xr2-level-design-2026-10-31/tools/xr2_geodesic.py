"""xr2_geodesic.py <walkmap prefix> [...]: shortest walkable distance (8-connected, 45 cm step rule) between hub pairs of the shortcut probes
vs the straight line, per walkmap. Detour ratio ~1 = the forest between the two places is freely crossable."""
import sys, os, json, math, heapq
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import xr2_layout as LY
X0, X1, Y0, Y1, C = -12000.0, 12000.0, -16000.0, 14000.0, 50.0
PAIRS = [('eastbank', 'narrows'), ('backyard', 'climb'), ('west', 'saddle'), ('SE', 'gate'), ('saddle', 'backyard'), ('J2', 'saddle'), ('glade', 'west'),
         ('landing', 'glade'), ('glade', 'saddle'), ('eastbank', 'hollow'), ('west', 'climb')]


def dijkstra(free, z, src, dst):
    H, W = free.shape; dist = {src: 0.0}; pq = [(0.0, src)]
    NB = [(-1, 0, 1), (1, 0, 1), (0, -1, 1), (0, 1, 1), (-1, -1, 1.414), (-1, 1, 1.414), (1, -1, 1.414), (1, 1, 1.414)]
    while pq:
        d, (j, i) = heapq.heappop(pq)
        if (j, i) == dst: return d * C / 100
        if d > dist.get((j, i), 1e18): continue
        for dj, di, w in NB:
            jj, ii = j + dj, i + di
            if 0 <= jj < H and 0 <= ii < W and free[jj, ii] and abs(z[jj, ii] - z[j, i]) < 45:
                nd = d + w
                if nd < dist.get((jj, ii), 1e18):
                    dist[(jj, ii)] = nd; heapq.heappush(pq, (nd, (jj, ii)))
    return None


def cell(free, xy):
    i, j = int((xy[0] - X0) / C), int((xy[1] - Y0) / C)
    if free[j, i]: return (j, i)
    c = np.argwhere(free[j - 8:j + 9, i - 8:i + 9]); k = np.argmin(np.hypot(c[:, 0] - 8, c[:, 1] - 8)); return (j - 8 + c[k][0], i - 8 + c[k][1])


def main():
  for pre in sys.argv[1:]:
    free = np.load(pre + '_free.npy'); z = np.load(pre + '_z.npy'); out = {}
    for a, b in PAIRS:
        A, B = LY.HUBS[a], LY.HUBS[b]; st = math.hypot(B[0] - A[0], B[1] - A[1]) / 100
        g = dijkstra(free, z, cell(free, A), cell(free, B))
        out['%s->%s' % (a, b)] = {'straight_m': round(st, 1), 'walk_m': None if g is None else round(g, 1), 'ratio': None if g is None else round(g / st, 2)}
    json.dump(out, open(pre + '_geodesic.json', 'w'), indent=1)
    print('==', os.path.basename(pre)); [print('  %-20s straight %6.1f  walk %6s  ratio %s' % (k, v['straight_m'], v['walk_m'], v['ratio'])) for k, v in out.items()]


if __name__ == '__main__':
    main()
