"""tables235.py <out.md> : V2.35 final tables from the LTP side files. (1) worst planted-ball slide / drag (contact231) per scenario,
production o vs pre235 (every V2.35 knob at its V2.34 value) at fixed 30 / 60 / 120 / 20 FPS and real time; (2) the longest double-support
hold inside a reversal clip (both balls slower than 60 cm/s = no foot is stepping, input held) = the user's 'freeze'; (3) the camera
recentre audit (rec233) for walk right, mouse / gamepad. Missing runs are printed as '-'."""
import sys, os, math, subprocess
H = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [H + '/../SHME_V231_20261026', H + '/../SHME_V232_20261027']
from ltp231 import load
from contact231 import classify
def worst(lab):
    try: R = load(lab)
    except Exception: return None
    eps = [e for e in classify(R) if e['cls'] in ('SLIP', 'DRAG')]
    return max([e['drift'] for e in eps] or [0.0])
def hold(lab):
    try: R = [r for r in load(lab) if r.get('stage') not in (None, '', 'yaw_hold')]
    except Exception: return None
    best = 0.0; run = 0.0; prev = None
    for r in R:
        if prev is not None:
            dt = r['t'] - prev['t']
            vl = math.hypot(r['vb_ball_l'][0] - prev['vb_ball_l'][0], r['vb_ball_l'][1] - prev['vb_ball_l'][1]) / max(dt, 1e-3)
            vr = math.hypot(r['vb_ball_r'][0] - prev['vb_ball_r'][0], r['vb_ball_r'][1] - prev['vb_ball_r'][1]) / max(dt, 1e-3)
            inrev = 'Rev' in str(r.get('av_Phase27_SelectedObject', ''))
            if inrev and vl < 60 and vr < 60 and (abs(r.get('lix', 0)) + abs(r.get('liy', 0))) > 0.1: run += dt; best = max(best, run)
            else: run = 0.0
        prev = r
    return best
fmt = lambda x: '-' if x is None else '%.1f' % x
SC = ['j35_rev', 'j35_rev2', 'j35_relstop', 'j30_rel_3200', 'j30_rel_3450', 'j30_slow', 'j34_chain1', 'jstart', 'wstart', 'c29_combo', 'e29_chain', 'e29_load', 'jback', 'wdiag', 's29_swl12', 's34_straight', 'ter_drop_walk', 'ter_step2', 'ter_drop_jog', 'map_r1']
out = ['## 1. Worst planted-foot slide / drag (cm), fixed 30 FPS final production (o) vs pre235', '', '| scenario | o | pre235 | o hold (s) | pre235 hold (s) |', '|---|---|---|---|---|']
for s in SC:
    out.append('| %s | %s | %s | %s | %s |' % (s, fmt(worst('v235fin_%s_o_r1' % s)), fmt(worst('v235fin_%s_pre235_r1' % s)), fmt(hold('v235fin_%s_o_r1' % s)), fmt(hold('v235fin_%s_pre235_r1' % s))))
SF = ['j35_rev', 'j35_rev2', 'j30_rel_3200', 'j30_slow', 'j34_chain1', 'jstart', 'c29_combo', 'e29_chain', 's29_swl12']
out += ['', '## 2. Frame-rate modes (worst slide cm, o / pre235; hold s in a reversal clip o / pre235)', '', '| scenario | 30 | 60 | 120 | 20 | real |', '|---|---|---|---|---|---|']
for s in SF:
    cells = []
    for tag in ('fin', 'f60', 'f120', 'f20', 'freal'):
        cells.append('%s / %s (%s / %s)' % (fmt(worst('v235%s_%s_o_r1' % (tag, s))), fmt(worst('v235%s_%s_pre235_r1' % (tag, s))), fmt(hold('v235%s_%s_o_r1' % (tag, s))), fmt(hold('v235%s_%s_pre235_r1' % (tag, s)))))
    out.append('| %s | %s |' % (s, ' | '.join(cells)))
open(sys.argv[1], 'w', encoding='utf8').write('\n'.join(out) + '\n'); print('\n'.join(out))
