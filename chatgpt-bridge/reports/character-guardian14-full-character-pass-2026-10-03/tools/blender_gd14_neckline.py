"""GUARDIAN-14 Henley neckline correction on the built g17e garment (same topology, so weights and the solved corrective morphs stay
valid): the neck opening is remapped to a higher, narrower henley neckline and the fabric around it follows smoothly, re-seated on
the body at its original stand-off.
Old (g17e builder): front scoop CF z 130.2, V bottom z 120.8, V half-width 2.3, neck half-width at HPS 8.2 (z 145.4), back neck z 142.2.
New (env): NL_ZS (scoop CF) NL_ZO (V bottom) NL_VW (V half-width) NL_XH (HPS half-width) NL_ZB (back neck CB); R = falloff (cm, geodesic).
Boundary mapping (neck edge points only): V edge -> proportional along the V; scoop -> same scoop law with the new CF / HPS;
back neck -> same law with the new half-width. Interior: displacement of the nearest neck-edge vertex * (1-(g/R)^2)^2 over the
mesh (geodesic); detail parts (placket bands, buttons, bindings) and LOD1/2 follow the nearest LOD0 main-panel displacement.
Every moved vertex is re-seated on the body: nearest body point + body normal * original stand-off.
usage: blender -b -P blender_gd14_neckline.py -- <sculpt_package.json.gz> <in outfit_geometry.json.gz> <out outfit_geometry.json.gz>"""
import sys, os, json, gzip, heapq, numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.kdtree import KDTree as KDTree_
a = sys.argv[sys.argv.index('--')+1:]; PKG, GIN, GOUT = a
E = lambda k, d: float(os.environ.get(k, d))
P = json.loads(gzip.open(PKG, 'rb').read()); NB = P['NB']; ALL = np.asarray(P['br_neutral'], float); BX = ALL[:NB]; BT = np.asarray(P['body']['triangles'], np.int64)
HT = np.asarray(P['head']['triangles'], np.int64)[np.asarray(P['head']['material_ids']) == 0]+NB
bvh = BVHTree.FromPolygons([Vector(p) for p in ALL], [list(t) for t in np.r_[BT, HT]])
G = json.loads(gzip.open(GIN, 'rb').read())
ZS0, ZO0, VW0, XH0, ZH, ZB0 = 130.2, 120.8, 2.3, 8.2, 145.4, 142.2
ZS, ZO, VW, XH, ZB, R = E('NL_ZS', 134.0), E('NL_ZO', 126.0), E('NL_VW', 1.9), E('NL_XH', 8.0), E('NL_ZB', 141.4), E('NL_R', 12.0); ZH = E('NL_ZH', 145.2)
def sstep(t): t = np.clip(t, 0, 1); return t*t*(3-2*t)
def nearest(p):
    loc, n, i, d = bvh.find_nearest(Vector(p)); return np.asarray(loc), np.asarray(n)
def standoff(p):
    loc, n = nearest(p); return float(np.dot(p-loc, n))
def seat(p, off):
    loc, n = nearest(p); return loc+n*off
def ray_front(x, z, front):
    o = Vector((x, 40.0 if front else -40.0, z)); d = Vector((0, -1.0 if front else 1.0, 0)); h = bvh.ray_cast(o, d)
    return np.asarray(h[0]) if h[0] is not None else None
h0 = G['henley']; X0 = np.asarray(h0['positions'], float); T0 = np.asarray(h0['triangles'], np.int64); part = np.asarray(h0['part']); main = part == 'SPH_Henley'
# boundary edges of the main panel
Tm = T0[main[T0].all(1)]; E_ = np.r_[Tm[:, [0, 1]], Tm[:, [1, 2]], Tm[:, [2, 0]]]; Es = np.sort(E_, 1); u, cnt = np.unique(Es, axis=0, return_counts=True)
bnd = np.unique(u[cnt == 1].ravel()); xb = X0[bnd]
neck = bnd[(xb[:, 2] > 120.0) & (np.abs(xb[:, 0]) < 12.5) & ((xb[:, 1] > -1.0) | (xb[:, 2] > 139.0))]
log = {'neck_edge_verts': int(len(neck))}
D = np.zeros_like(X0)
# order the neck edge into one chain per side (CF V bottom -> V -> scoop -> HPS -> back neck -> CB) and remap by normalised arc length
nset = set(int(i) for i in neck); NA = {i: [] for i in nset}
for i, j in u[cnt == 1]:
    if int(i) in nset and int(j) in nset: NA[int(i)].append(int(j)); NA[int(j)].append(int(i))
def walk(start, side):
    ch = [start]; prev = None
    while True:
        nx = [j for j in NA[ch[-1]] if j != prev and j not in ch and (X0[j, 0] >= -0.05 if side > 0 else X0[j, 0] <= 0.05)]
        if not nx: break
        prev = ch[-1]; ch.append(nx[0])
    return ch
def arclen(Q):
    s_ = np.r_[0, np.cumsum(np.linalg.norm(np.diff(Q, axis=0), axis=1))]; return s_/max(s_[-1], 1e-6)
def poly_at(C, t):
    s_ = arclen(C); return np.stack([np.interp(t, s_, C[:, k]) for k in range(C.shape[1])], 1)
for side in (1, -1):
    cand = [i for i in nset if X0[i, 1] > 0 and X0[i, 0]*side >= -0.05]
    start = min(cand, key=lambda i: X0[i, 2])
    ch = np.array(walk(start, side)); Q = X0[ch]
    k_h = int(np.argmax(np.abs(Q[:, 0])))                         # HPS: most lateral point of the neck chain
    fr = ch[:k_h+1]
    # back neck: the back panel is a separate component; start at the back-panel vertex coincident with the front HPS and walk to CB
    hps = X0[ch[k_h]]; cb = [i for i in nset if i not in set(int(v) for v in fr) and X0[i, 1] < 2.0 and np.linalg.norm(X0[i]-hps) < 0.6]
    if cb:
        b0 = min(cb, key=lambda i: np.linalg.norm(X0[i]-hps)); used = set(int(v) for v in fr); bkl = [b0]; prev = None
        while True:
            nx = [j for j in NA[bkl[-1]] if j != prev and j not in bkl and j not in used and X0[j, 1] < 2.0 and (X0[j, 0]*side >= -0.05)]
            if not nx: break
            prev = bkl[-1]; bkl.append(nx[0])
        bk = np.array(bkl)
    else: bk = ch[k_h:]
    xs = np.linspace(0, 1, 200)
    vee = np.stack([np.linspace(0.25, VW, 40), np.linspace(ZO, ZS, 40)], 1)
    xsc = np.linspace(VW, XH, 80); sc = np.stack([xsc, ZS+(ZH-ZS)*((xsc-VW)/(XH-VW))**2.1], 1)
    sc = np.stack([xsc, ZS+(ZH-ZS)*((xsc-VW)/(XH-VW))**2.0], 1); CFr = np.r_[vee, sc[1:]]; xb_ = np.linspace(XH, 0.0, 80); CBk = np.stack([xb_, ZB+(ZH-ZB)*(xb_/XH)**2.2], 1)
    for seg, Cn, front in ((fr, CFr, True), (bk, CBk, False)):
        if len(seg) < 2: continue
        t = arclen(X0[seg][:, [0, 2]]); tg = poly_at(Cn, t)
        for i, (xn, zn) in zip(seg, tg):
            hit = nearest(np.array([side*xn, X0[i, 1], zn]))[0]   # project the target (x, z) at the vertex's own depth onto the body (works on the shoulder top too)
            off = standoff(X0[i]); D[i] = hit+nearest(hit)[1]*off-X0[i]
            if os.environ.get('NL_DEBUG'): print('NLDBG', [round(v, 2) for v in X0[i]], '->', [round(v, 2) for v in X0[i]+D[i]], 'front' if front else 'back')
    log['chain_%d' % side] = [len(fr), len(bk)]
# geodesic propagation over the main panel from the neck edge
NV = len(X0); ADJ = [[] for _ in range(NV)]
for i, j in u: ADJ[i].append(j); ADJ[j].append(i)
# sewn seams: panels are separate components whose seam vertices coincide in 3D -> connect coincident boundary vertices so the
# displacement crosses front / back / sleeve seams and the panels move together (no seam opening)
from mathutils.kdtree import KDTree as _KD
_kb = _KD(len(bnd))
for k_, i in enumerate(bnd): _kb.insert(Vector(X0[i]), k_)
_kb.balance(); nweld = 0
for i in bnd:
    for (co, k_, dd) in _kb.find_range(Vector(X0[i]), E('NL_WELD', 0.12)):
        j = int(bnd[k_])
        if j != i and j not in ADJ[i]: ADJ[i].append(j); ADJ[j].append(int(i)); nweld += 1
log['weld_links'] = nweld
dist = np.full(NV, np.inf); src = np.full(NV, -1); pq = []
for i in neck: dist[i] = 0.0; src[i] = i; heapq.heappush(pq, (0.0, int(i)))
while pq:
    g, i = heapq.heappop(pq)
    if g > dist[i] or g > R: continue
    for j in ADJ[i]:
        ng = g+float(np.linalg.norm(X0[i]-X0[j]))
        if ng < dist[j] and ng <= R: dist[j] = ng; src[j] = src[i]; heapq.heappush(pq, (ng, j))
w = np.where(np.isfinite(dist), (1-np.clip(dist/R, 0, 1)**2)**2, 0.0)
# pin every other panel boundary (armhole / shoulder / side seams, hem, placket edge): displacement fades to 0 within NL_PIN cm of it,
# so the body panel never separates from the sleeves at the seams (g18n v1 opened the front shoulder seam)
pins = np.array([i for i in bnd if int(i) not in set(int(j) for j in neck)]); dpin = np.full(NV, np.inf); pq = []
for i in pins: dpin[i] = 0.0; heapq.heappush(pq, (0.0, int(i)))
PIN = E('NL_PIN', 0.0)
while pq:
    g, i = heapq.heappop(pq)
    if g > dpin[i] or g > PIN: continue
    for j in ADJ[i]:
        ng = g+float(np.linalg.norm(X0[i]-X0[j]))
        if ng < dpin[j] and ng <= PIN: dpin[j] = ng; heapq.heappush(pq, (ng, j))
pinw = np.where(np.isfinite(dpin), sstep(dpin/PIN), 1.0) if PIN > 0 else np.ones(NV); w = w*pinw
log['pinned_boundary_verts'] = int(len(pins))
# SPATIAL displacement field (method change: topological propagation opened the sewn seams between separately meshed panels).
# Shepard interpolation of the neck-edge displacements over 3D space with a radial falloff: coincident seam vertices of different
# panels get identical displacement by construction, so seams cannot open.
_nl = np.array(sorted(nset)); _kn = KDTree_(len(_nl))
for k_, i in enumerate(_nl): _kn.insert(Vector(X0[i]), k_)
_kn.balance()
for i in _nl:
    grp = [int(_nl[k_]) for (co, k_, dd) in _kn.find_range(Vector(X0[i]), 0.12)]
    if len(grp) > 1: m_ = D[grp].mean(0); D[grp] = m_
srcs = np.array([i for i in neck if np.linalg.norm(D[i]) > 1e-4 or True]); SP = X0[srcs]; SD = D[srcs]
RS = E('NL_RS', 7.0); Dm = np.zeros_like(X0)
for i in range(NV):
    r = np.linalg.norm(SP-X0[i], axis=1); k = np.argsort(r)[:8]; rk = np.maximum(r[k], 1e-3)
    if rk[0] > RS: continue
    wk = 1.0/rk**2; Dm[i] = (wk[:, None]*SD[k]).sum(0)/wk.sum()*(1-np.clip(rk[0]/RS, 0, 1)**2)**2
Dm[neck] = D[neck]; M = np.ones(NV, bool)
mov = np.linalg.norm(Dm, axis=1) > 1e-3
X1 = X0.copy()
for i in np.nonzero(mov)[0]: X1[i] = seat(X0[i]+Dm[i], standoff(X0[i]))
Dmain = X1-X0
from mathutils.kdtree import KDTree
kd = KDTree(int(main.sum())); idm = np.nonzero(main)[0]
for k, i in enumerate(idm): kd.insert(Vector(X0[i]), k)
kd.balance()
def follow(Xa):
    out = Xa.copy()
    for n, p in enumerate(Xa):
        hits = kd.find_n(Vector(p), 4); ws = np.array([1.0/max(h[2], 1e-3) for h in hits]); dd = np.array([Dmain[idm[h[1]]] for h in hits])
        out[n] = p+(ws[:, None]*dd).sum(0)/ws.sum()
    return out
det = ~main & ~mov; X1[det] = follow(X0[det])
G['henley']['positions'] = X1.tolist()
for L in ('henley_lod1', 'henley_lod2'):
    XL = np.asarray(G[L]['positions'], float); G[L]['positions'] = follow(XL).tolist()
gzip.open(GOUT, 'wt', encoding='utf-8').write(json.dumps(G, separators=(',', ':')))
d = np.linalg.norm(X1-X0, axis=1); log.update({'moved>1mm': int((d > 0.1).sum()), 'max_cm': round(float(d.max()), 2), 'cf_scoop_new_z': round(float(X1[neck][np.argmin(np.abs(X1[neck][:, 0])+10*(X1[neck][:, 1] < 0))][2]), 2)})
print('NECKLINE_OK', json.dumps(log))
