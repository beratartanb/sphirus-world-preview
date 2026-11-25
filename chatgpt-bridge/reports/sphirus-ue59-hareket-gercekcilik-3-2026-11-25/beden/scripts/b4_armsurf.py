# b4_armsurf.py (Blender 5.3 background): REAL-SURFACE hand / forearm clearance against the shorts and the thigh skin.
# Linear blend skinning offline: bind positions (B4 body / B4 shorts = dump + delta), the dumped top-4 skin weights, bind bone transforms
# (bind_bones.json) and the per-frame bone world transforms logged by hk_arm4.py. Every frame of every plan segment (none skipped).
# Signed distance of each (decimated) hand / forearm vertex to the nearest posed shorts vertex along that vertex's posed normal, and to
# the nearest posed thigh-skin vertex (skin only below the shorts hem). Penetration = signed < 0 within 4 cm.
# args: <params json> {'body','body_delta','shorts','shorts_delta','bind','labels':[[label, plan],..],'out', 'dec': 6}
import sys, json, math, os
import numpy as np
from mathutils.kdtree import KDTree
A = json.load(open(sys.argv[sys.argv.index('--') + 1])); OUT = A['out']; os.makedirs(os.path.dirname(OUT), exist_ok=True)
LG = open(OUT, 'w')
def log(*a): LG.write(' '.join(str(x) for x in a) + '\n'); LG.flush()
BIND = json.load(open(A['bind']))
def qmul(q, v):  # rotate vectors v (n,3) by quaternion q (x,y,z,w)
    x, y, z, w = q; u_ = np.array([x, y, z]); t = 2 * np.cross(u_, v); return v + w * t + np.cross(u_, t)
def qconj(q): return [-q[0], -q[1], -q[2], q[3]]
def load(dump, delta):
    d = json.load(open(dump)); L = d['lods']['0']; V = np.array(L['v']); T = np.array(L['t'])
    if delta: V = V + np.array(json.load(open(delta))['lods']['0'])
    return d['bone_index_names'], V, T, L['w']
def vnormals(V, T):
    a = V[T]; fn = np.cross(a[:, 1] - a[:, 0], a[:, 2] - a[:, 0]); N = np.zeros_like(V)
    for k in range(3): np.add.at(N, T[:, k], fn)
    return N / np.maximum(np.linalg.norm(N, axis=1)[:, None], 1e-9)
bnB, VB, TB, WB = load(A['body'], A.get('body_delta')); bnS, VS, TS, WS = load(A['shorts'], A.get('shorts_delta'))
def orient(V, N, tag):
    votes = 0
    for ax in range(3):
        for sg in (1, -1):
            i = int(np.argmax(sg * V[:, ax])); votes += 1 if N[i, ax] * sg > 0 else -1     # extreme points face outwards
    log('normals', tag, 'extreme-point votes %d of 6' % votes); return N if votes > 0 else -N
NB = orient(VB, vnormals(VB, TB), 'body'); NS = orient(VS, vnormals(VS, TS), 'shorts')
arm = ('hand', 'thumb', 'index_', 'middle_', 'ring_', 'pinky', 'lowerarm')
HSEL = [i for i, w in enumerate(WB) if w and any(k in bnB[w[0][0]] for k in arm) and 'toe' not in bnB[w[0][0]]][::A.get('dec', 6)]
SIDE = {i: ('l' if VB[i, 0] > 0 else 'r') for i in HSEL}
PART = {i: ('hand' if 'lowerarm' not in bnB[WB[i][0][0]] else 'forearm') for i in HSEL}
hem = VS[:, 2].min()
TSEL = [i for i, w in enumerate(WB) if w and (bnB[w[0][0]].startswith('thigh') or (bnB[w[0][0]] in ('pelvis', 'spine_01') and VB[i, 2] < 95)) and VB[i, 2] > 40]
# garment layer over each skin vertex (bind pose): distance to the nearest shorts vertex if the shorts cover it (< 5 cm), else 0
kdg = KDTree(len(VS))
for j, p in enumerate(VS): kdg.insert(p.tolist(), j)
kdg.balance()
GOFF = np.array([(lambda r: r[2] if r[2] < 5.0 else 0.0)(kdg.find(VB[i].tolist())) for i in TSEL])
log('hand/forearm verts', len(HSEL), 'shorts verts', len(VS), 'thigh-skin verts below hem', len(TSEL), 'hem z', round(float(hem), 1))
BN = sorted(BIND); BI = {b: k for k, b in enumerate(BN)}
BT = np.array([BIND[b][:3] for b in BN]); BQ = np.array([BIND[b][3:] for b in BN])
def qmulv(q, v):  # q (n,4) x y z w, v (n,3)
    u_ = q[:, :3]; w = q[:, 3:4]; t = 2 * np.cross(u_, v); return v + w * t + np.cross(u_, t)
def conj(q): return q * np.array([-1, -1, -1, 1.0])
def prep(idx, V, N, W, bn):
    vi = []; bi = []; ww = []
    for k, i in enumerate(idx):
        ws = [(BI[bn[b]], w) for b, w in W[i] if w > 0.001 and bn[b] in BI]; s_ = sum(w for _, w in ws) or 1.0
        for b, w in ws: vi.append(k); bi.append(b); ww.append(w / s_)
    vi = np.array(vi); bi = np.array(bi); ww = np.array(ww); idx = np.array(list(idx))
    loc = qmulv(conj(BQ[bi]), V[idx][vi] - BT[bi]); nloc = qmulv(conj(BQ[bi]), N[idx][vi])
    return (len(idx), vi, bi, ww, loc, nloc)
PH = prep(HSEL, VB, NB, WB, bnB); PS = prep(range(len(VS)), VS, NS, WS, bnS); PT = prep(TSEL, VB, NB, WB, bnB)
def pose(P, bt):
    n, vi, bi, ww, loc, nloc = P; MT = np.array([bt[b][:3] for b in BN]); MQ = np.array([bt[b][3:] for b in BN])
    X = np.zeros((n, 3)); Nn = np.zeros((n, 3))
    np.add.at(X, vi, ww[:, None] * (qmulv(MQ[bi], loc) + MT[bi])); np.add.at(Nn, vi, ww[:, None] * qmulv(MQ[bi], nloc))
    Nn /= np.maximum(np.linalg.norm(Nn, axis=1)[:, None], 1e-9); return X, Nn
key = lambda x: (x or '-').replace(' LeftShift', '+Sh').replace(' LeftControl', '+Ct')
for lab, planf in A['labels']:
    rows = json.load(open('C:/Users/berat/Documents/Unreal Projects/sphirus_UE59/Saved/Codex/Grip_20261106/rec/%s.json' % lab))['rows']; plan = eval(open(planf).read())
    worst = {}; per_seg = {}; ep = []
    for fi, r in enumerate(rows):
        h = r['hook'] if isinstance(r['hook'], dict) else {}; bt = h.get('bt')
        if not bt or fi % A.get('fstep', 2): continue
        XH, NH = pose(PH, bt); XS, NSn = pose(PS, bt); XT, NT = pose(PT, bt)
        kdS = KDTree(len(XS))
        for j, p in enumerate(XS): kdS.insert(p.tolist(), j)
        kdS.balance(); kdT = KDTree(len(XT))
        for j, p in enumerate(XT): kdT.insert(p.tolist(), j)
        kdT.balance()
        best = {}
        for k, i in enumerate(HSEL):
            p = XH[k]; co, j, d = kdT.find(p.tolist())
            if d > 6.0: continue
            sgn = float((p - XT[j]) @ NT[j]); g = GOFF[j]
            kk = (SIDE[i], PART[i], 'skin'); best[kk] = min(best.get(kk, (9e9, i)), (sgn, i))
            if g > 0:
                kk2 = (SIDE[i], PART[i], 'shorts'); best[kk2] = min(best.get(kk2, (9e9, i)), (sgn - g, i))
        s = r['s']; clip = r['gasp'][0]
        for kk, (sgn, i) in best.items():
            per_seg.setdefault((s, kk), []).append((sgn, r['t'], clip))
            if kk not in worst or sgn < worst[kk][0]: worst[kk] = (sgn, r['t'], s, clip, i)
    log('#### %s (%d frames, every %d-th)' % (lab, len(rows), A.get('fstep', 2)))
    for kk, (sgn, t, s, clip, i) in sorted(worst.items()):
        log('  WORST %-3s %-8s vs %-6s signed %5.1f cm at t %.2f seg s%d [%s] clip %s' % (kk[0], kk[1], kk[2], sgn, t, s, key(plan[s][0] if s < len(plan) else ''), clip))
    for (s, kk), L in sorted(per_seg.items()):
        pen = [x for x in L if x[0] < 0]
        if not pen: continue
        # longest run of consecutive penetrating samples
        ts = [x[1] for x in L]; run = best_run = 0; start = None; bstart = None
        for x in L:
            if x[0] < 0:
                run += 1
                if run == 1: start = x[1]
                if run > best_run: best_run = run; bstart = start
            else: run = 0
        dt = (ts[-1] - ts[0]) / max(1, len(ts) - 1)
        m = min(pen); log('  s%-2d [%-10s] %-3s %-8s vs %-6s penetrating %3d of %3d samples | deepest %5.1f cm at t %.2f (%s) | longest %.2f s from t %.2f' % (s, key(plan[s][0] if s < len(plan) else ''), kk[0], kk[1], kk[2], len(pen), len(L), m[0], m[1], m[2][-30:], best_run * dt, bstart or 0))
log('ARMSURF_DONE'); LG.close(); open(OUT + '.done', 'w').write('ok')
