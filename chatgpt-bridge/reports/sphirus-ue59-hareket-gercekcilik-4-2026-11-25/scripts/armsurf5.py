# armsurf5.py (Blender 5.3 background): hand / forearm vs shorts + thigh, pass 4 method (replaces b4_armsurf.py readings).
# Every frame: body (thigh / pelvis skin) and shorts are skinned offline (dumped top-4 weights, bind bones, per-frame bone world
# transforms logged by hk_arm4.py). The covering volume at a height z is the 2-D convex outline of the POSED shorts and thigh-skin
# points within +-1.5 cm of z: one outline above the crotch, one per leg below it (split at the pelvis mid-plane). A hand / forearm
# point inside the outline penetrates; depth = distance to the outline edge. No neutral-pose garment offset is subtracted and no
# inside/outside sign is taken from the thin garment's normals. Contact runs are counted only over CONSECUTIVE frames (a missing
# sample ends a run). Output lists the worst frames (time + frame index) so they can be checked on the synchronous video frame.
# args: <params json> {'body','body_delta','shorts','shorts_delta','bind','labels':[[label, plan],..],'out','dec':4,'fstep':1}
import sys, json, math, os
import numpy as np
A = json.load(open(sys.argv[sys.argv.index('--') + 1])); OUT = A['out']; os.makedirs(os.path.dirname(OUT), exist_ok=True)
LG = open(OUT, 'w')
def log(*a): LG.write(' '.join(str(x) for x in a) + '\n'); LG.flush()
BIND = json.load(open(A['bind'])); BN = sorted(BIND); BI = {b: k for k, b in enumerate(BN)}
BT = np.array([BIND[b][:3] for b in BN]); BQ = np.array([BIND[b][3:] for b in BN])
def qmulv(q, v): u_ = q[:, :3]; w = q[:, 3:4]; t = 2 * np.cross(u_, v); return v + w * t + np.cross(u_, t)
def conj(q): return q * np.array([-1, -1, -1, 1.0])
def load(dump, delta):
    d = json.load(open(dump)); L = d['lods']['0']; V = np.array(L['v'])
    if delta: V = V + np.array(json.load(open(delta))['lods']['0'])
    return d['bone_index_names'], V, L['w']
bnB, VB, WB = load(A['body'], A.get('body_delta')); bnS, VS, WS = load(A['shorts'], A.get('shorts_delta'))
arm = ('hand', 'thumb', 'index_', 'middle_', 'ring_', 'pinky', 'lowerarm')
HSEL = [i for i, w in enumerate(WB) if w and any(k in bnB[w[0][0]] for k in arm) and 'toe' not in bnB[w[0][0]]][::A.get('dec', 4)]
SIDE = np.array(['l' if VB[i, 0] > 0 else 'r' for i in HSEL]); PART = np.array(['hand' if 'lowerarm' not in bnB[WB[i][0][0]] else 'forearm' for i in HSEL])
TSEL = [i for i, w in enumerate(WB) if w and (bnB[w[0][0]].startswith('thigh') or bnB[w[0][0]] in ('pelvis', 'spine_01')) and 40 < VB[i, 2] < 100]
def prep(idx, V, W, bn):
    vi = []; bi = []; ww = []
    for k, i in enumerate(idx):
        ws = [(BI[bn[b]], w) for b, w in W[i] if w > 0.001 and bn[b] in BI]; s_ = sum(w for _, w in ws) or 1.0
        for b, w in ws: vi.append(k); bi.append(b); ww.append(w / s_)
    vi = np.array(vi); bi = np.array(bi); ww = np.array(ww); idx = np.array(list(idx))
    return (len(idx), vi, bi, ww, qmulv(conj(BQ[bi]), V[idx][vi] - BT[bi]))
def pose(P, bt):
    n, vi, bi, ww, loc = P; MT = np.array([bt[b][:3] for b in BN]); MQ = np.array([bt[b][3:] for b in BN])
    X = np.zeros((n, 3)); np.add.at(X, vi, ww[:, None] * (qmulv(MQ[bi], loc) + MT[bi])); return X
PH = prep(HSEL, VB, WB, bnB); PS = prep(range(len(VS)), VS, WS, bnS); PT = prep(TSEL, VB, WB, bnB)
log('method: convex outline of posed shorts + thigh skin per 3 cm slice (one above crotch, one per leg below) | hand/forearm pts %d, shorts %d, thigh skin %d' % (len(HSEL), len(VS), len(TSEL)))
def hull(P):
    P = sorted(set(map(tuple, np.round(P, 2))))
    if len(P) < 3: return None
    def cr(o, a, b): return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo = []; up = []
    for p in P:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    for p in reversed(P):
        while len(up) >= 2 and cr(up[-2], up[-1], p) <= 0: up.pop()
        up.append(p)
    return np.array(lo[:-1] + up[:-1])
def inside_depth(h, p):
    # >0 = inside by that distance to the nearest edge, <0 = outside clearance (approx: distance to nearest edge)
    a = h; b = np.roll(h, -1, axis=0); e = b - a; w = p - a
    t = np.clip((w * e).sum(1) / np.maximum((e * e).sum(1), 1e-9), 0, 1); d = np.linalg.norm(w - e * t[:, None], axis=1).min()
    crs = e[:, 0] * w[:, 1] - e[:, 1] * w[:, 0]
    return d if (crs >= 0).all() else -d
key = lambda x: (x or '-').replace(' LeftShift', '+Sh').replace(' LeftControl', '+Ct')
for lab, planf in A['labels']:
    rows = json.load(open('C:/Users/berat/Documents/Unreal Projects/sphirus_UE59/Saved/Codex/Grip_20261106/rec/%s.json' % lab))['rows']; plan = eval(open(planf).read())
    worst = {}; runs = {}; cur = {}; prevf = {}; evs = []
    for fi, r in enumerate(rows):
        h = r['hook'] if isinstance(r['hook'], dict) else {}; bt = h.get('bt')
        if not bt or fi % A.get('fstep', 1): continue
        pel = np.array(bt['pelvis'][:3]); XH = pose(PH, bt)
        near = np.where(np.linalg.norm(XH[:, :2] - pel[:2], axis=1) < 45)[0]
        best = {}
        if len(near):
            XS = pose(PS, bt); XT = pose(PT, bt); C = np.vstack([XS, XT])
            lat = np.array(bt['thigh_out_l'][:3]) - np.array(bt['thigh_out_r'][:3]); lat[2] = 0.0  # character's left, from the hip joints
            # crotch height: lowest posed shorts point near the mid-plane
            mid = np.abs((C[:, :3] - pel) @ (lat / np.linalg.norm(lat))) < 3
            crz = C[mid, 2].min() + 4 if mid.any() else pel[2] - 15
            ln = lat / np.linalg.norm(lat); HC = {}
            for k in near:
                p = XH[k]; zb = int(math.floor(p[2] / 3.0)); ps = (p - pel) @ ln
                hk = (zb, 0 if p[2] >= crz else (1 if ps > 0 else -1))
                if hk not in HC:
                    band = C[np.abs(C[:, 2] - (zb + 0.5) * 3.0) < 1.5]
                    if hk[1] != 0 and len(band):
                        sd = (band - pel) @ ln; band = band[sd > 0] if hk[1] > 0 else band[sd <= 0]
                    HC[hk] = hull(band[:, :2]) if len(band) >= 6 else None
                hl = HC[hk]
                if hl is None: continue
                d = inside_depth(hl, p[:2]); kk = (SIDE[k], PART[k])
                if kk not in best or d > best[kk][0]: best[kk] = (d, k)
        s = r['s']; clip = r['gasp'][0] or 'None'
        for kk in set(list(best) + list(cur)):
            d = best.get(kk, (-99, 0))[0]
            consecutive = prevf.get(kk) == fi - A.get('fstep', 1)
            if d > 0:
                if kk not in worst or d > worst[kk][0]: worst[kk] = (d, r['t'], fi, s, clip)
                evs.append((d, r['t'], fi, s, kk, clip))
                if kk in cur and consecutive: cur[kk][1] = r['t']; cur[kk][2] = max(cur[kk][2], d); cur[kk][3] += 1
                else:
                    if kk in cur: runs.setdefault(kk, []).append(cur[kk])
                    cur[kk] = [r['t'], r['t'], d, 1, s, clip]
                prevf[kk] = fi
            elif kk in cur:
                runs.setdefault(kk, []).append(cur.pop(kk))
    for kk, v in cur.items(): runs.setdefault(kk, []).append(v)
    dt = rows[2]['t'] - rows[1]['t']
    log('#### %s (%d frames, every %d-th, frame step %.4f s)' % (lab, len(rows), A.get('fstep', 1), dt))
    for kk, (d, t, fi, s, clip) in sorted(worst.items()):
        log('  WORST %s %-7s inside the shorts/thigh outline by %4.1f cm at t %.3f (frame %d) seg s%d [%s] clip %s' % (kk[0], kk[1], d, t, fi, s, key(plan[s][0] if s < len(plan) else ''), clip))
    for kk, L in sorted(runs.items()):
        L = sorted(L, key=lambda x: -(x[1] - x[0]))
        for t0, t1, dm, n, s, clip in L[:4]:
            log('  RUN %s %-7s %.3f-%.3f s = %.3f s (%d consecutive frames) max depth %.1f cm seg s%d [%s] %s' % (kk[0], kk[1], t0, t1, t1 - t0 + dt, n, dm, s, key(plan[s][0] if s < len(plan) else ''), clip[-30:]))
    evs.sort(key=lambda x: -x[0])
    log('  TOP FRAMES (for synchronous video check): ' + ', '.join('t %.3f f%d %s %s %.1f' % (t, fi, kk[0], kk[1], d) for d, t, fi, s, kk, clip in evs[:8]))
log('ARMSURF5_DONE'); LG.close(); open(OUT + '.done', 'w').write('ok')
