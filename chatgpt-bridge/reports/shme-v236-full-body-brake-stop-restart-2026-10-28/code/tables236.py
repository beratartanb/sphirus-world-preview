"""tables236.py <out.md> : V2.36 final tables from the LTP side files (one build: the promoted production o vs pre236 = every V2.36 group at
its V2.35 value). (1) worst planted-ball slide / drag (contact231) + the reversal 'hold' (both balls < 60 cm/s inside a reversal clip with
input held) at fixed 30; (2) whole-body stop audit (stop236: arm swing kept during the brake, pull-back, stagger, trunk at +0.6 s, pelvis
dip, last landing) for the stop scenarios; (3) frame-rate modes 60 / 120 / 20 / real; (4) cold first use in the clean editor.
Missing runs print '-' (never counted as a pass)."""
import sys, os, math, json
H = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [H + '/../SHME_V231_20261026', H + '/../SHME_V232_20261027', H]
from ltp231 import load
from contact231 import classify
import stop236
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
            if 'Rev' in str(r.get('av_Phase27_SelectedObject', '')) and vl < 60 and vr < 60 and (abs(r.get('lix', 0)) + abs(r.get('liy', 0))) > 0.1: run += dt; best = max(best, run)
            else: run = 0.0
        prev = r
    return best
fmt = lambda x: '-' if x is None else '%.1f' % x
fm2 = lambda x: '-' if x is None else '%.2f' % x
out = ['## 1. Worst planted-foot slide / drag (cm) and reversal hold (s), fixed 30 FPS: V2.36 production (o) vs pre236 (V2.35 values)', '',
       '| scenario | o | pre236 | o hold | pre236 hold |', '|---|---|---|---|---|']
S30 = ['j36_stop', 'j36_stopb', 'j36_stopr', 'j36_rse', 'j36_rsm', 'j36_rsl', 'j36_rsx', 'j36_wjs', 'j36_wjsb', 'j36_sside', 'j35_rev', 'j35_rev2', 'j35_relstop',
       'j30_rel_3200', 'j30_rel_3450', 'j30_slow', 'j34_chain1', 'jstart', 'wstart', 'c29_combo', 'e29_chain', 'e29_load', 'jback', 'wdiag', 's29_swl12',
       's34_straight', 'ter_drop_jog', 'map_r1']
for s in S30:
    a, b = 'v236fin_%s_o_r1' % s, 'v236fin_%s_pre236_r1' % s
    out.append('| %s | %s | %s | %s | %s |' % (s, fmt(worst(a)), fmt(worst(b)), fm2(hold(a)), fm2(hold(b))))
out += ['', '## 2. Whole-body stop audit (stop236, visible mesh), fixed 30', '',
        '| run | release s | arm swing kept (after/before) | pull-back cm | stagger cm @+0.6 s | trunk deg @0 / @+0.6 | pelvis dip cm | last landing s |',
        '|---|---|---|---|---|---|---|---|']
for s in ['j36_stop', 'j36_stopb', 'j36_stopr', 'j36_wjs', 'j36_wjsb']:
    for v in ('o', 'pre236'):
        try:
            for o in stop236.audit('v236fin_%s_%s_r1' % (s, v)):
                out.append('| %s %s | %s | %s | %s | %s | %s / %s | %s | %s |' % (s, v, o['t_release'], o['arm_pp'][2], o['back_cm'], o['stagger_cm'], o['trunk_deg'][0], o['trunk_deg'][1], o['pelvis_dip'], o['last_land']))
        except Exception as e: out.append('| %s %s | - | %s |||||| ' % (s, v, str(e)[:40]))
SF = ['j36_stop', 'j36_stopb', 'j36_stopr', 'j36_wjs', 'j35_rev', 'j35_rev2', 'j30_rel_3200', 'j30_slow', 'j34_chain1', 'jstart', 'c29_combo', 'e29_chain', 'e29_load']
out += ['', '## 3. Frame-rate modes: worst slide cm o / pre236 (reversal hold s o / pre236)', '', '| scenario | 30 | 60 | 120 | 20 | real |', '|---|---|---|---|---|---|']
for s in SF:
    cells = []
    for tag in ('fin', 'f60', 'f120', 'f20', 'freal'):
        a, b = 'v236%s_%s_o_r1' % (tag, s), 'v236%s_%s_pre236_r1' % (tag, s)
        cells.append('%s / %s (%s / %s)' % (fmt(worst(a)), fmt(worst(b)), fm2(hold(a)), fm2(hold(b))))
    out.append('| %s | %s |' % (s, ' | '.join(cells)))
out += ['', '## 4. Cold first use in the clean editor (no warm run): frames with no database + worst slide', '', '| run | no-DB frames | worst cm |', '|---|---|---|']
for s in ('j36_stop', 'j35_rev', 'e29_load', 'j34_chain1'):
    lab = 'v236cold_%s_o_r1' % s
    try: R = load(lab); n = sum(1 for r in R if r['t'] > 2.5 and str(r.get('av_CurrentSelectedDatabase')) == 'None')
    except Exception: n = None
    out.append('| %s | %s | %s |' % (lab, n, fmt(worst(lab))))
open(sys.argv[1], 'w', encoding='utf8').write('\n'.join(out) + '\n'); print('\n'.join(out))
