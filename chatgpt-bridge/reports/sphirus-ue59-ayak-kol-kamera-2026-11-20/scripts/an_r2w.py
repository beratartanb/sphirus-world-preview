# an_r2w.py <label...>: arm carriage around gait changes on SIM time, visible MetaHuman body (actor frame, cm/deg).
# For every plan segment boundary where LeftShift is released while W stays held (jog -> walk with forward input) and for plain
# walk segments, windows after the boundary: 0-0.5, 0.5-1.0, 1.0-1.5, 1.5-2.5, 3-6 s:
#   hand_up = max over both hands of hand height above the spine_05 joint (chest level ~ 0; walk loop ~ -30)
#   hand_fwd= max forward hand offset from spine_05;  elbow = mean elbow angle (180 = straight);  abd = upper-arm abduction
#   RelA / MoveA = body-ABP relax weights (recorder patch 6 extension)
import sys, json, math, statistics as st
sys.argv, _a = [sys.argv[0]], sys.argv[1:]
exec(open('Tools/UE59_20261119/an_shoulder.py', encoding='utf8').read().split('\nfor ')[0].split('\nif __name__')[0])
def ang(a, b, c):
    u_ = [a[i] - b[i] for i in range(3)]; v_ = [c[i] - b[i] for i in range(3)]
    d = sum(u_[i] * v_[i] for i in range(3)) / max(1e-6, math.sqrt(sum(x * x for x in u_)) * math.sqrt(sum(x * x for x in v_)))
    return math.degrees(math.acos(max(-1, min(1, d))))
def arm(r):
    s5 = vis(r, 'spine_05'); up = []; fw = []; el = []
    for sd in ('l', 'r'):
        h = vis(r, 'hand_' + sd); ua = vis(r, 'upperarm_' + sd); la = vis(r, 'lowerarm_' + sd)
        up.append(h[2] - s5[2]); fw.append(h[0] - s5[0]); el.append(ang(ua, la, h))
    return max(up), max(fw), st.mean(el), met(r, vis)[3]
for L in _a:
    d = json.load(open(RD + L + '.json')); R = d['rows']; P = d['plan']; print('==', L)
    for s in range(1, len(P)):
        k0, k1 = P[s - 1][0].split(), P[s][0].split()
        tag = 'jog->walk' if ('LeftShift' in k0 and 'LeftShift' not in k1 and 'W' in k1) else ('walk' if k1 == ['W'] and not k0 else None)
        if not tag: continue
        S = [r for r in R if r['s'] == s and isinstance(r.get('sh'), dict)]
        if not S: continue
        t0 = S[0]['t']; out = []
        for a, b in ((0, .5), (.5, 1), (1, 1.5), (1.5, 2.5), (3, 6)):
            W = [r for r in S if a <= r['t'] - t0 < b]
            if not W: continue
            A = [arm(r) for r in W]
            out.append('%.1f-%.1f up %5.1f fwd %4.1f elb %3.0f abd %4.1f Rel %.2f Mv %.2f v %3.0f' % (a, b, max(x[0] for x in A), max(x[1] for x in A), st.mean(x[2] for x in A), st.mean(x[3] for x in A),
                       st.mean(r['sh']['a'].get('RelA', -1) for r in W), st.mean(r['sh']['a'].get('MoveA', -1) for r in W), st.mean(math.hypot(r['vx'], r['vy']) for r in W)))
        print('  seg %d %s (prev %.1fs)' % (s, tag, P[s - 1][1])); [print('     ' + o) for o in out]
