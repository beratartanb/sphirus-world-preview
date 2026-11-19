# an_r2wslide.py <label...>: planted-foot drift (an_stop3 contact definition, sim time) in the 0-2.5 s after a jog->walk change
# with forward input held, + clips played. Worst single contact per foot.
import sys, json, math
sys.argv, _a = [sys.argv[0]], sys.argv[1:]
exec(open('Tools/UE59_20261119/an_stop3.py', encoding='utf8').read().split('\no = []')[0])
for L in _a:
    d = json.load(open(RD + L + '.json')); R = d['rows']; P = d['plan']; TT, srcn = simtime(R)
    for s in range(1, len(P)):
        k0, k1 = P[s - 1][0].split(), P[s][0].split()
        if not ('LeftShift' in k0 and 'LeftShift' not in k1 and 'W' in k1): continue
        idx = [i for i, r in enumerate(R) if r['s'] == s]; S = [R[i] for i in idx]; T = [TT[i] - TT[idx[0]] for i in idx]
        dr = [0.0, 0.0]; nc = [0, 0]
        for k, b in ((0, 'ball_l'), (1, 'ball_r')):
            for (i0, i1) in contacts(S, T, k, b, 2.5):
                nc[k] += 1; a0 = S[i0]['ub'][b][:2]
                dr[k] = max([dr[k]] + [math.hypot(S[j]['ub'][b][0] - a0[0], S[j]['ub'][b][1] - a0[1]) for j in range(i0, i1 + 1)])
        cl = []
        for j, r in enumerate(S):
            c = (r.get('gasp') or [None])[0]
            if c and (not cl or cl[-1][0] != c): cl.append((c, round(T[j], 2)))
        print('%s seg %d jog->walk | drift L %.1f R %.1f (contacts %d/%d) | %s' % (L, s, dr[0], dr[1], nc[0], nc[1], ' > '.join('%s@%s' % (c[2:40], t) for c, t in cl[:4])))
