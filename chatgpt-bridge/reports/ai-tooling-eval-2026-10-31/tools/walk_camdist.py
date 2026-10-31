"""walk_camdist.py <walk dir A> <walk dir B> [...]: camera-to-pawn distance along the fixed-step trail walks (pass A ticks of
pie_trailwalk.py), to show whether added environment pieces pull the spring arm / GR camera in. Same tick index = same game time.
Per walk: median / p5 / min distance; versus the first walk: ticks with a shortfall > 25 cm and the arc ranges where they occur."""
import json, sys, os, math, statistics as stt

walks = sys.argv[1:]
D = {}
for w in walks:
    t = json.load(open(os.path.join(w, 'trailwalk_log.json')))['passA']['ticks']
    D[w] = [(r['s_cm'], math.dist(r['cam'], [r['pawn'][0], r['pawn'][1], r['pawn'][2]])) for r in t]
base = D[walks[0]]
for w in walks:
    d = sorted(x[1] for x in D[w])
    line = '%-22s ticks %4d  median %.0f  p5 %.0f  min %.0f' % (os.path.basename(w.rstrip('/\\')), len(d), stt.median(d), d[int(0.05 * len(d))], d[0])
    if w != walks[0]:
        n = min(len(base), len(D[w])); bad = [i for i in range(n) if base[i][1] - D[w][i][1] > 25.0]
        ranges, cur = [], None
        for i in bad:
            if cur and i - cur[1] <= 3:
                cur[1] = i
            else:
                cur = [i, i]; ranges.append(cur)
        line += '  shortfall>25cm: %d ticks; arc ranges (cm, worst cm): %s' % (len(bad), ', '.join(
            '%.0f-%.0f (%.0f)' % (D[w][a][0], D[w][b][0], max(base[i][1] - D[w][i][1] for i in range(a, b + 1))) for a, b in ranges))
    print(line)
