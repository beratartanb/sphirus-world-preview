"""plant225.py: planted-foot slip per plant episode WHILE a given clip family is selected (default 'JogRev'), plus the episode that spans
the clip exit. A plant = consecutive frames with the ball within 1.5 cm of that foot's own floor height (10th-percentile ball z + 2 cm; height only,
so a sliding foot is not excluded); slip = horizontal distance first -> last frame of the episode (the distance a viewer sees the planted foot travel).
Usage: plant225.py label [label ...] [--fam=JogRev]"""
import json, sys, math, pathlib
E = pathlib.Path(__file__).resolve().parents[2] / 'Saved/Codex/SHME_V1_20260925/Evidence'
fam = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fam=')), 'JogRev')
for lab in [a for a in sys.argv[1:] if not a.startswith('--')]:
    R = sorted([r for r in json.load(open(E / (lab + '.json'))) if isinstance(r, dict) and r.get('t') is not None and isinstance(r.get('vb_ball_l'), list)], key=lambda r: float(r['t']))
    sel = [fam in str(r.get('av_Phase27_SelectedObject')) for r in R]
    out = []
    for s in ('l', 'r'):
        zs = sorted(r['vb_ball_' + s][2] for r in R); z0 = zs[len(zs) // 10] + 2.0   # floor = 10th percentile (spawn frames excluded)
        ep = None
        for i in range(1, len(R)):
            p, q = R[i - 1]['vb_ball_' + s], R[i]['vb_ball_' + s]; dt = float(R[i]['t']) - float(R[i - 1]['t'])
            planted = q[2] < z0   # height only: a fast slide must not be classified away
            if planted and ep is None: ep = [i, i]
            elif planted: ep[1] = i
            if (not planted or i == len(R) - 1) and ep is not None:
                a, b = ep; ep = None
                if any(sel[a:b + 1]):
                    pa, pb = R[a]['vb_ball_' + s], R[b]['vb_ball_' + s]
                    path = sum(math.hypot(R[k]['vb_ball_' + s][0] - R[k - 1]['vb_ball_' + s][0], R[k]['vb_ball_' + s][1] - R[k - 1]['vb_ball_' + s][1]) for k in range(a + 1, b + 1))
                    out.append((round(float(R[a]['t']), 2), s, round(float(R[b]['t']) - float(R[a]['t']), 2), round(math.hypot(pb[0] - pa[0], pb[1] - pa[1]), 1), round(path, 1)))
    out.sort()
    worst = max((o[3] for o in out), default=0.0)
    print('PLANT225 %-28s worst net %5.1f | episodes (t, foot, dur, net, path): %s' % (lab[-28:], worst, out))
