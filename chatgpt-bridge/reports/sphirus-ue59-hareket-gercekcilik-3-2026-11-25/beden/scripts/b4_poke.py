# b4_poke.py (Blender 5.3 background): does the BODY show through the SHORTS in motion? Offline linear blend skinning of the body
# (pelvis / glute / thigh skin under the shorts) and of the shorts with the per-frame bone world transforms logged by hk_arm4.py.
# Per frame: signed distance of each covered body vertex to the nearest posed shorts vertex along that shorts vertex's outward normal
# (> 0 = skin outside the garment = visible poke-through). Run for the NEW pair (body+delta, shorts+delta) and the OLD pair (no deltas)
# on the same recordings. Optional: write a per-shorts-vertex outward push (bind space) that clears the new body by 'margin'.
# args: <params json> {'body','body_delta','shorts','shorts_delta','bind','labels':[[label, plan],..],'out','fstep',
#                      'push_out': optional json path, 'margin': 0.35, 'cap': 2.5}
import sys, json, os
import numpy as np
from mathutils.kdtree import KDTree
A = json.load(open(sys.argv[sys.argv.index('--') + 1])); OUT = A['out']; os.makedirs(os.path.dirname(OUT), exist_ok=True)
LG = open(OUT, 'w')
def log(*a): LG.write(' '.join(str(x) for x in a) + '\n'); LG.flush()
BIND = json.load(open(A['bind'])); BN = sorted(BIND); BI = {b: k for k, b in enumerate(BN)}
BT = np.array([BIND[b][:3] for b in BN]); BQ = np.array([BIND[b][3:] for b in BN])
def qmulv(q, v): u_ = q[:, :3]; w = q[:, 3:4]; t = 2 * np.cross(u_, v); return v + w * t + np.cross(u_, t)
def conj(q): return q * np.array([-1, -1, -1, 1.0])
def load(dump, delta):
    d = json.load(open(dump)); L = d['lods']['0']; V = np.array(L['v']); T = np.array(L['t'])
    if delta: V = V + np.array(json.load(open(delta))['lods']['0'])
    return d['bone_index_names'], V, T, L['w']
def vnormals(V, T):
    a = V[T]; fn = np.cross(a[:, 1] - a[:, 0], a[:, 2] - a[:, 0]); N = np.zeros_like(V)
    for k in range(3): np.add.at(N, T[:, k], fn)
    return N / np.maximum(np.linalg.norm(N, axis=1)[:, None], 1e-9)
def orient(V, N):
    votes = 0
    for ax in range(3):
        for sg in (1, -1):
            i = int(np.argmax(sg * V[:, ax])); votes += 1 if N[i, ax] * sg > 0 else -1
    return N if votes > 0 else -N
def prep(idx, V, N, W, bn):
    vi = []; bi = []; ww = []; cov = []
    for k, i in enumerate(idx):
        ws = [(bn[b], w) for b, w in W[i] if w > 0.001]; tot = sum(w for _, w in ws) or 1.0
        ok = [(BI[b], w) for b, w in ws if b in BI]; s_ = sum(w for _, w in ok) or 1.0; cov.append(s_ / tot)
        for b, w in ok: vi.append(k); bi.append(b); ww.append(w / s_)
    vi = np.array(vi); bi = np.array(bi); ww = np.array(ww); idx = np.array(list(idx))
    return (len(idx), vi, bi, ww, qmulv(conj(BQ[bi]), V[idx][vi] - BT[bi]), qmulv(conj(BQ[bi]), N[idx][vi])), np.array(cov)
def pose(P, bt):
    n, vi, bi, ww, loc, nloc = P; MT = np.array([bt[b][:3] for b in BN]); MQ = np.array([bt[b][3:] for b in BN])
    X = np.zeros((n, 3)); Nn = np.zeros((n, 3))
    np.add.at(X, vi, ww[:, None] * (qmulv(MQ[bi], loc) + MT[bi])); np.add.at(Nn, vi, ww[:, None] * qmulv(MQ[bi], nloc))
    return X, Nn / np.maximum(np.linalg.norm(Nn, axis=1)[:, None], 1e-9)
def region(z, x, y):
    side = 'l' if x > 0 else 'r'
    if z > 88: return 'waist/belly' if y > 0 else 'lower back'
    if y < -4 and z > 70: return 'glute ' + side
    if abs(x) > 13 and z > 72: return 'hip side ' + side
    if z < 76: return 'thigh/hem ' + side
    return ('front ' if y > 0 else 'back ') + side
key = lambda x: (x or '-').replace(' LeftShift', '+Sh').replace(' LeftControl', '+Ct')
REC = 'C:/Users/berat/Documents/Unreal Projects/sphirus_UE59/Saved/Codex/Grip_20261106/rec/%s.json'
def run(tag, bdelta, sdelta, push=None):
    bnB, VB, TB, WB = load(A['body'], bdelta); bnS, VS, TS, WS = load(A['shorts'], sdelta)
    NB = orient(VB, vnormals(VB, TB)); NS = orient(VS, vnormals(VS, TS))
    if push is not None: VS = VS + NS * push[:, None]; NS = orient(VS, vnormals(VS, TS))
    kd = KDTree(len(VS))
    for j, p in enumerate(VS): kd.insert(p.tolist(), j)
    kd.balance()
    # covered body vertices: within 4 cm of the shorts in bind pose, inside it (bind signed < 0.2), and in the shorts' height band
    sel = []
    for i in range(len(VB)):
        co, j, d = kd.find(VB[i].tolist())
        if d < 4.0 and float((VB[i] - VS[j]) @ NS[j]) < 0.2: sel.append(i)
    PB, covB = prep(sel, VB, NB, WB, bnB); PS, covS = prep(range(len(VS)), VS, NS, WS, bnS)
    log('== %s: covered body verts %d, shorts verts %d | skin weight on logged bones: body p5 %.2f min %.2f, shorts p5 %.2f min %.2f' % (tag, len(sel), len(VS), np.percentile(covB, 5), covB.min(), np.percentile(covS, 5), covS.min()))
    need = np.zeros(len(VS)); REG = [region(VB[i, 2], VB[i, 0], VB[i, 1]) for i in sel]
    for lab, planf in A['labels']:
        rows = json.load(open(REC % lab))['rows']; plan = eval(open(planf).read()); worst = {}; per = {}
        for fi, r in enumerate(rows):
            h = r['hook'] if isinstance(r['hook'], dict) else {}; bt = h.get('bt')
            if not bt or fi % A.get('fstep', 2): continue
            XB, _ = pose(PB, bt); XS, NSp = pose(PS, bt); kdS = KDTree(len(XS))
            for j, p in enumerate(XS): kdS.insert(p.tolist(), j)
            kdS.balance(); s = r['s']
            for k in range(len(sel)):
                co, j, d = kdS.find(XB[k].tolist())
                if d > 4.0: continue
                sg = float((XB[k] - XS[j]) @ NSp[j])
                if sg > 0:
                    rg = REG[k]; worst[rg] = max(worst.get(rg, (0, 0, 0, '')), (sg, r['t'], s, r['gasp'][0]))
                    per.setdefault((s, rg), set()).add(fi); need[j] = max(need[j], sg)
        log('#### %s %s' % (tag, lab))
        for rg, (sg, t, s, clip) in sorted(worst.items(), key=lambda x: -x[1][0]):
            log('  %-14s worst %4.1f cm at t %.2f seg s%d [%s] clip %s' % (rg, sg, t, s, key(plan[s][0] if s < len(plan) else ''), clip[-34:]))
        nfr = {}
        for (s, rg), fs in per.items(): nfr[s] = max(nfr.get(s, 0), len(fs))
        log('  frames with any poke (>0 cm) per segment (every %d-th frame):' % A.get('fstep', 2), dict(sorted(nfr.items())))
    return need, VS, TS, NS
run('OLD body + OLD shorts', None, None)
need, VS, TS, NS = run('NEW body + B4 shorts', A['body_delta'], A['shorts_delta'])
if A.get('push_out'):
    # spread the need to neighbours (12 graph-smoothing passes of max-then-average), add the margin where any need, cap
    nb = [set() for _ in range(len(VS))]
    for a, b, c in TS: nb[a] |= {b, c}; nb[b] |= {a, c}; nb[c] |= {a, b}
    p = need.copy()
    for _ in range(4): p = np.array([max([p[i]] + [p[j] for j in nb[i]]) for i in range(len(p))])
    for _ in range(8): p = np.array([0.5 * p[i] + 0.5 * np.mean([p[j] for j in nb[i]]) if nb[i] else p[i] for i in range(len(p))])
    push = np.where(p > 0.02, np.minimum(p + A.get('margin', 0.35), A.get('cap', 2.5)), 0.0)
    json.dump({'push': push.tolist()}, open(A['push_out'], 'w'))
    log('push: verts moved %d, max %.2f cm, p95 of moved %.2f' % (int((push > 0).sum()), push.max(), np.percentile(push[push > 0], 95) if (push > 0).any() else 0))
    run('NEW body + B4 shorts + push (check)', A['body_delta'], A['shorts_delta'], push)
log('POKE_DONE'); LG.close(); open(OUT + '.done', 'w').write('ok')
