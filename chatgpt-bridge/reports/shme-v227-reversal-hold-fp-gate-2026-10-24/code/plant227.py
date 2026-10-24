"""plant227.py label [label ...] [--fam=JogRev] [--vmax=80]: planted-foot slip like plant225 (height-only plant, slip = first->last horizontal
distance of the episode, episodes while the family clip is selected or spanning its exit) PLUS a stricter 'contact' variant: a plant episode
only starts on a frame where the ball is low AND nearly still (horizontal speed < vmax cm/s), so a low skimming swing (the authored clips'
toe-level swings) is not counted as a slide. Prints both worst values and the contact episodes."""
import json, sys, math, pathlib
E = pathlib.Path(__file__).resolve().parents[2] / 'Saved/Codex/SHME_V1_20260925/Evidence'
fam = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--fam=')), 'JogRev'); VMAX = float(next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--vmax=')), '80'))
for lab in [a for a in sys.argv[1:] if not a.startswith('--')]:
    p = E / (lab + '.json')
    if not p.exists(): print('PLANT227 %-28s MISSING' % lab[-28:]); continue
    R = sorted([r for r in json.load(open(p)) if isinstance(r, dict) and r.get('t') is not None and isinstance(r.get('vb_ball_l'), list)], key=lambda r: float(r['t']))
    sel = [fam in str(r.get('av_Phase27_SelectedObject')) for r in R]
    res = {}
    for strict in (False, True):
        out = []
        for s in ('l', 'r'):
            zs = sorted(r['vb_ball_' + s][2] for r in R); z0 = zs[len(zs) // 10] + 2.0; ep = None
            for i in range(1, len(R)):
                p_, q = R[i - 1]['vb_ball_' + s], R[i]['vb_ball_' + s]; dt = max(float(R[i]['t']) - float(R[i - 1]['t']), 1e-3)
                low = q[2] < z0; v = math.hypot(q[0] - p_[0], q[1] - p_[1]) / dt
                if ep is None:
                    if low and (not strict or v < VMAX): ep = [i, i]
                elif low: ep[1] = i
                if (not low or i == len(R) - 1) and ep is not None:
                    a, b = ep; ep = None
                    if any(sel[a:b + 1]):
                        pa, pb = R[a]['vb_ball_' + s], R[b]['vb_ball_' + s]
                        out.append((round(float(R[a]['t']), 2), s, round(float(R[b]['t']) - float(R[a]['t']), 2), round(math.hypot(pb[0] - pa[0], pb[1] - pa[1]), 1)))
        out.sort(); res[strict] = out
    w0 = max((o[3] for o in res[False]), default=0.0); w1 = max((o[3] for o in res[True]), default=0.0)
    print('PLANT227 %-28s worst net %5.1f | contact-start worst %5.1f | contact episodes (t, foot, dur, net): %s' % (lab[-28:], w0, w1, res[True]))
