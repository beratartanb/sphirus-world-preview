"""pelv225.py: height-change evidence per window - the largest one-frame pelvis / capsule z change (the 'pop'), the pelvis z range, the
landing foot's height over the detected ground at touchdown (ball z - ground) and the StepPrepZ range. Usage: pelv225.py label x0 x1 [label x0 x1 ...]
(x = capsule x along the course). Ground at the foot: the floor is z -2 (ball) on flat / platform tops 13 / 28 (ball ~ +11 / +26)."""
import json, sys, math, pathlib
E = pathlib.Path(__file__).resolve().parents[2] / 'Saved/Codex/SHME_V1_20260925/Evidence'
a = sys.argv[1:]
for i in range(0, len(a), 3):
    lab, x0, x1 = a[i], float(a[i + 1]), float(a[i + 2])
    R = sorted([r for r in json.load(open(E / (lab + '.json'))) if isinstance(r, dict) and r.get('t') is not None and isinstance(r.get('ax'), list) and x0 <= r['ax'][0] <= x1], key=lambda r: float(r['t']))
    if len(R) < 3: print('PELV225 %-28s [%5.0f %5.0f] no rows' % (lab[-28:], x0, x1)); continue
    pz = [r['vb_pelvis'][2] for r in R]; cz = [r['ax'][2] for r in R]
    dp = max(abs(pz[k] - pz[k - 1]) for k in range(1, len(pz))); dc = max(abs(cz[k] - cz[k - 1]) for k in range(1, len(cz)))
    sp = [float(r.get('cv_StepPrepZ') or 0) for r in R]
    # landings: contact edges per foot, the ball height at the edge
    land = []
    for s in ('l', 'r'):
        prev = False
        for r in R:
            c = r.get('cv_Contact' + s.upper()) in (True, 'True', 1)
            if c and not prev: land.append((round(float(r['t']), 2), s, round(r['vb_ball_' + s][2], 1), round(r['vb_ball_' + s][0])))
            prev = c
    land.sort()
    print('PELV225 %-28s [%5.0f %5.0f] pelvis z %5.1f..%5.1f max|dz| %4.1f/frame | capsule max|dz| %4.1f | StepPrepZ %5.1f..%5.1f | landings (t, foot, ball z, x): %s' % (lab[-28:], x0, x1, min(pz), max(pz), dp, dc, min(sp), max(sp), land[:6]))
