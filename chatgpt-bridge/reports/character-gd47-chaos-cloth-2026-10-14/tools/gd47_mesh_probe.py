"""GD47: probe the Henley f5 LOD0 (DynamicMesh order, data/henley_f5_mesh.json.gz): sections, main-fabric boundary loops, main/trim contact.
usage: blender -b --python gd47_mesh_probe.py -- <mesh.json.gz>"""
import sys, json, gzip, collections, numpy as np
a = sys.argv[sys.argv.index('--') + 1:]; d = json.load(gzip.open(a[0], 'rt'))
P = np.array(d['P']); T = np.array(d['T']); M = np.array(d['M'])
print('bbox', P.min(0).round(1), P.max(0).round(1))
for m in (0, 1, 2):
    vs = np.unique(T[M == m]); print('mat', m, 'verts', len(vs), 'min', P[vs].min(0).round(1), 'max', P[vs].max(0).round(1))
def loops_of(Ts):
    ec = collections.Counter()
    for t in Ts:
        for x, y in ((t[0], t[1]), (t[1], t[2]), (t[2], t[0])): ec[(min(x, y), max(x, y))] += 1
    be = [e for e, c in ec.items() if c == 1]; adj = collections.defaultdict(list)
    for x, y in be: adj[x].append(y); adj[y].append(x)
    seen = set(); out = []
    for s in adj:
        if s in seen: continue
        comp = []; st = [s]
        while st:
            v = st.pop()
            if v in seen: continue
            seen.add(v); comp.append(v); st += adj[v]
        out.append(comp)
    return out, sum(1 for c in ec.values() if c > 2)
for m in (0, 1):
    L, nm = loops_of(T[M == m]); print('--- mat', m, 'loops', len(L), 'nonmanifold edges', nm)
    for l in sorted(L, key=len, reverse=True)[:14]:
        q = P[l]; print(' ', len(l), 'c', q.mean(0).round(1), 'min', q.min(0).round(1), 'max', q.max(0).round(1))
v0 = set(np.unique(T[M == 0]).tolist()); v1 = set(np.unique(T[M == 1]).tolist()); sh = sorted(v0 & v1); print('shared main-trim verts', len(sh))
# trim components
L1 = collections.defaultdict(set); par = {}
def f(x):
    while par.setdefault(x, x) != x: x = par[x]
    return x
for t in T[M == 1]:
    for v in t[1:]: par[f(v)] = f(t[0])
comp = collections.defaultdict(list)
for v in v1: comp[f(v)].append(v)
print('trim components', len(comp))
for c in sorted(comp.values(), key=len, reverse=True)[:10]:
    q = P[c]; print(' ', len(c), 'c', q.mean(0).round(1), 'min', q.min(0).round(1), 'max', q.max(0).round(1))
# main-fabric z / x histogram for region design
v0a = np.array(sorted(v0)); Q = P[v0a]
for z0 in range(80, 160, 5):
    s = Q[(Q[:, 2] >= z0) & (Q[:, 2] < z0 + 5)]
    if len(s): print('z', z0, 'n', len(s), 'x', s[:, 0].min().round(1), s[:, 0].max().round(1), 'y', s[:, 1].min().round(1), s[:, 1].max().round(1))
