# b11_match.py (Blender -b --python, numpy): template SKM_Body (complete) <- B10 body shape.
# 1) match every B10 vertex to a template vertex by per-vertex UV0 (exact), check edges agree;
# 2) displacement d = B10 - template on matched vertices; unmatched template vertices (the hidden-face holes) get a biharmonic
#    (minimum ||L d||^2, uniform Laplacian) displacement with all matched vertices fixed -> smooth continuation of the B10 shape;
# 3) writes new template positions + report. args after --: dir
import sys, json, os, numpy as np
from mathutils import kdtree
A_ = sys.argv[sys.argv.index('--') + 1:]; D = A_[0]; BN = A_[1] if len(A_) > 1 else 'b10'; ON = A_[2] if len(A_) > 2 else 'b11'
T = json.load(open(D + 'tmpl.json'))
if BN.endswith('.npy'):
    S0 = json.load(open(D + 'sph8.json')); S0['v'] = (np.array(S0['v']) + np.load(BN)).round(4).tolist(); B = S0
else: B = json.load(open(D + BN + '.json'))
S = json.load(open(D + 'sph8.json'))
tv = np.array(T['v']); tuv = np.array(T['uv']); bv = np.array(B['v']); buv = np.array(B['uv']); sv = np.array(S['v'])
rep = {'nt': len(tv), 'nb': len(bv)}
kd = kdtree.KDTree(len(tuv))
for j, q in enumerate(tuv): kd.insert((q[0], q[1], 0.0), j)
kd.balance()
m = -np.ones(len(bv), int); dd = np.zeros(len(bv))
amb = 0
for i, q in enumerate(buv):
    hits = kd.find_range((q[0], q[1], 0.0), 2e-5)
    if not hits: hits = [kd.find((q[0], q[1], 0.0))]
    if len(hits) > 1:
        amb += 1; hits.sort(key=lambda h: np.linalg.norm(tv[h[1]] - sv[i]))
    m[i] = hits[0][1]; dd[i] = hits[0][2]
rep['uv_dist_max'] = float(dd.max()); rep['uv_far'] = int((dd > 2e-5).sum()); rep['ambiguous'] = amb
# UV seams: per-vertex UV picks one of several UV elements, so seam vertices miss or collide. Keep only exact, unique matches,
# then resolve the rest by position: predicted template position = Sph8 position + mean (template - Sph8) offset of matched mesh
# neighbours, nearest free template vertex within 0.35 cm; repeated until nothing changes.
from collections import Counter
cnt = Counter(m[dd <= 2e-5].tolist())
ok = (dd <= 2e-5) & np.array([cnt[int(x)] == 1 for x in m])
m[~ok] = -1
nbB = [set() for _ in range(len(bv))]
for a, b, c in B['t']:
    for x, y in ((a, b), (b, c), (c, a)): nbB[x].add(y); nbB[y].add(x)
used = set(m[m >= 0].tolist()); passes = 0
while True:
    passes += 1; changed = 0
    free = [j for j in range(len(tv)) if j not in used]; kf = kdtree.KDTree(len(free))
    for k, j in enumerate(free): kf.insert(tuple(tv[j]), k)
    kf.balance()
    for i in np.where(m < 0)[0]:
        nn = [n for n in nbB[i] if m[n] >= 0]
        if not nn: continue
        o = np.mean([tv[m[n]] - sv[n] for n in nn], axis=0); p = sv[i] + o
        co, k, dist = kf.find(tuple(p))
        if dist < 0.35 and free[k] not in used: m[i] = free[k]; used.add(free[k]); changed += 1
    if not changed or passes > 20: break
rep['pos_resolved_passes'] = passes; rep['still_unmatched_b10'] = int((m < 0).sum())
assert (m >= 0).all(), rep
rep['dup_targets'] = int(len(m) - len(set(m.tolist())))
# position sanity: Sph8 vs template distance for matched pairs (identity difference, should be smooth, a few cm)
pd = np.linalg.norm(sv - tv[m], axis=1); rep['sph8_tmpl_dist'] = [float(np.percentile(pd, p)) for p in (50, 90, 99, 100)]
# edge agreement
def edges(t):
    E = set()
    for a, b, c in t: E |= {tuple(sorted(x)) for x in ((a, b), (b, c), (c, a))}
    return E
Et = edges(T['t']); Eb = edges(B['t'])
mapped = {tuple(sorted((int(m[a]), int(m[b])))) for a, b in Eb}
rep['b10_edges'] = len(Eb); rep['edges_missing_in_tmpl'] = len(mapped - Et)
# index monotonic?
rep['monotone'] = bool(np.all(np.diff(m) > 0))
known = np.zeros(len(tv), bool); known[m] = True; U = np.where(~known)[0]; rep['unmatched'] = int(len(U))
zs = tv[U, 2]; rep['unmatched_z'] = [float(zs.min()), float(zs.max())] if len(U) else []
rep['unmatched_hist_z'] = np.histogram(zs, bins=[0, 60, 80, 86, 92, 98, 104, 110, 130, 150, 200])[0].tolist()
# displacement
d = np.zeros_like(tv); d[m] = bv - tv[m]
nb = [set() for _ in range(len(tv))]
for a, b in Et: nb[a].add(b); nb[b].add(a)
ui = {int(u): k for k, u in enumerate(U)}
R = sorted(set(U.tolist()) | {x for u in U for x in nb[u]})
# L row r: d_r - mean(d_nb)
nu = len(U); A = np.zeros((len(R), nu)); rhs = np.zeros((len(R), 3))
for r_i, r in enumerate(R):
    w = 1.0 / len(nb[r])
    for x, c in [(r, 1.0)] + [(x, -w) for x in nb[r]]:
        if x in ui: A[r_i, ui[x]] += c
        else: rhs[r_i] -= c * d[x]
sol = np.linalg.lstsq(A, rhs, rcond=None)[0]
d[U] = sol
new = tv + d
rep['hole_disp_cm'] = [float(np.percentile(np.linalg.norm(sol, axis=1), p)) for p in (0, 50, 100)] if nu else []
# unmatched cluster centres (by connected components)
seen = set(); comps = []
for u in U:
    u = int(u)
    if u in seen: continue
    st = [u]; seen.add(u); cc = []
    while st:
        x = st.pop(); cc.append(x)
        for y in nb[x]:
            if y in ui and y not in seen: seen.add(y); st.append(y)
    comps.append({'n': len(cc), 'c': [round(float(v), 1) for v in tv[cc].mean(0)], 'cnew': [round(float(v), 1) for v in new[cc].mean(0)]})
rep['components'] = sorted(comps, key=lambda c: -c['n'])
json.dump({'pos': np.round(new, 4).tolist(), 'map': m.tolist(), 'U': U.tolist()}, open(D + ON + '_pos.json', 'w'))
json.dump(rep, open(D + ON + '_match_rep.json', 'w'), indent=1)
