# an_time.py <label...>: time-base table per recording (patch #8 rows): rows, sim time, frame label, wall clock, game step stats,
#   dilation range, and per-plan-segment sim duration vs requested; plus 5 sample rows (f, t, tf, tw, gdt, dil, x, speed).
import json, sys, math, statistics as st
RD = 'Saved/Codex/Grip_20261106/rec/'
for L in sys.argv[1:]:
    d = json.load(open(RD + L + '.json')); R = d['rows']; P = d['plan']
    g = [r['gdt'] for r in R[1:]]
    print('== %s fps %.0f rows %d | sim t %.3f s | sum gdt %.3f | frame label %.3f | wall %.2f s | gdt med %.4f min %.4f max %.4f sd %.4f | dil %.2f..%.2f' % (
        L, d['fps'], len(R), R[-1]['t'], sum(g), R[-1].get('tf', 0), R[-1].get('tw', 0), st.median(g), min(g), max(g), st.pstdev(g), min(r.get('dil', 0) for r in R), max(r.get('dil', 0) for r in R)))
    segs = []
    for s in sorted(set(r['s'] for r in R)):
        S = [r for r in R if r['s'] == s]
        segs.append('%s %.2f/%.2f' % (P[s][0] or '-', S[-1]['t'] - S[0]['t'] + S[-1]['gdt'] if len(S) > 1 else 0, P[s][1]))
    print('   seg sim/requested: ' + ' | '.join(segs))
    for i in (0, 1, len(R) // 3, len(R) // 2, len(R) - 1):
        r = R[i]; print('   f %4d t %.4f tf %.3f tw %.3f gdt %.4f dil %.3f x %.1f v %.0f' % (r['f'], r['t'], r.get('tf', 0), r.get('tw', 0), r['gdt'], r.get('dil', 0), r['x'], math.hypot(r['vx'], r['vy'])))
