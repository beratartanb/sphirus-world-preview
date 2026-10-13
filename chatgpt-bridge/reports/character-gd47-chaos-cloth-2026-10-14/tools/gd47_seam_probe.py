"""GD47: are the main-fabric panel boundaries coincident (unwelded seams)? nearest other-piece vertex distance per boundary vertex."""
import sys, json, gzip, collections, numpy as np
from mathutils.kdtree import KDTree
d = json.load(gzip.open(sys.argv[sys.argv.index('--') + 1], 'rt')); P = np.array(d['P']); T = np.array(d['T']); M = np.array(d['M'])
T0 = T[M == 0]; par = {}
def f(x):
    while par.setdefault(x, x) != x: par[x] = par[par[x]]; x = par[x]
    return x
for t in T0:
    for v in t[1:]: par[f(v)] = f(t[0])
v0 = np.unique(T0); piece = {v: f(v) for v in v0.tolist()}; ids = sorted(set(piece.values())); pid = {r: i for i, r in enumerate(ids)}
print('pieces', len(ids), [sum(1 for v in piece if piece[v] == r) for r in ids])
ec = collections.Counter()
for t in T0:
    for x, y in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0])): ec[(min(x, y), max(x, y))] += 1
bv = sorted({v for e, c in ec.items() if c == 1 for v in e})
kd = KDTree(len(v0)); [kd.insert(P[v].tolist(), v) for v in v0.tolist()]; kd.balance()
res = collections.Counter(); dists = []
for v in bv:
    best = None
    for co, idx, dist in kd.find_n(P[v].tolist(), 8):
        if piece[idx] != piece[v]: best = dist; break
    dists.append(best if best is not None else 99)
dists = np.array(dists); print('boundary verts', len(bv), 'coincident(<0.01)', int((dists < 0.01).sum()), '<0.3', int((dists < 0.3).sum()), 'none', int((dists >= 99).sum()))
for p in ids:
    sel = [i for i, v in enumerate(bv) if piece[v] == p]; q = P[[bv[i] for i in sel]]
    print('piece', pid[p], 'bverts', len(sel), 'coinc', int((dists[sel] < 0.01).sum()), 'c', P[[v for v in piece if piece[v] == p]].mean(0).round(1))
# also coincident with same-piece other verts (UV seam inside a piece)?
dup = 0
for v in v0.tolist():
    for co, idx, dist in kd.find_n(P[v].tolist(), 2):
        if idx != v and dist < 0.001: dup += 1; break
print('verts with an exact duplicate', dup)
