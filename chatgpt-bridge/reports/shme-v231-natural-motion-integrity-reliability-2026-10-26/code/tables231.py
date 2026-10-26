"""tables231.py <out.txt> <label>... : V2.31 evidence table. Per run: worst planted SLIP/DRAG (contact231) whole run and per event window when the
scenario has one (swl12 W at 6.2, e29 second reversal 6.8, j30_rel re-press, e31_s2 second S), entry clip of the first authored reversal,
worst head acceleration (m/s2), FPS check, idle entries inside a held reversal. Writes and prints TABLE231 rows."""
import sys, os, re, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ltp231 import load, short
from contact231 import classify
def window(lab):
    if 's29_swl' in lab: m = re.search(r'swl(\d\d)', lab); t = 5.0 + int(m.group(1)) / 10.0; return (t - 0.1, t + 1.4)
    m = re.search(r'e31_s2_(\d+)', lab)
    if m: t = int(m.group(1)) / 1000.0 + 2.0; return (t - 0.1, t + 1.4)
    if 'e29_load' in lab or 'e29_recov' in lab: return (6.7, 8.2)
    if 'e29_chain' in lab: return (6.1, 7.9)
    m = re.search(r'j30_rel_(\d+)', lab)
    if m: t = int(m.group(1)) / 1000.0 + 2.15; return (t - 0.1, t + 1.0)
    return None
rows = []
for lab in sys.argv[2:]:
    try: R = load(lab)
    except Exception as e: rows.append('%-36s MISSING' % lab); continue
    eps = classify(R); bad = [e for e in eps if e['cls'] in ('SLIP', 'DRAG')]
    w = max(bad, key=lambda e: e['drift']) if bad else None
    win = window(lab); ww = None
    if win:
        wb = [e for e in bad if win[0] <= e['tw'] <= win[1]]; ww = max(wb, key=lambda e: e['drift']) if wb else None
    hs = [(r['t'], r['vb_head']) for r in R if isinstance(r.get('vb_head'), tuple) and r['t'] > 2.0]; ha = 0.0   # move stage only (the 2 s yaw hold has the observer setup)
    for i in range(2, len(hs)):
        (t0, a), (t1, b), (t2, c) = hs[i - 2], hs[i - 1], hs[i]; d = (t2 - t0) / 2 or 1e-3
        ha = max(ha, math.sqrt(sum(((c[k] - 2 * b[k] + a[k]) / (d * d) / 100) ** 2 for k in range(3))))
    ent = next((short(r.get('av_Phase27_SelectedObject')) for r in R if short(r.get('av_Phase27_SelectedObject')).startswith(('SHM226_JogRev', 'SHM231')) and (not win or r['t'] >= win[0])), '')
    wd = [r.get('wdt') for r in R if isinstance(r.get('wdt'), float) and r['t'] > 0.5]
    fx = sorted(wd)[len(wd) // 2] if wd else 0
    idle = sum(1 for r in R if str(r.get('av_SHM_IdleEntry')) == 'True' and str(r.get('av_SHM227_Hold')) == 'True')
    rows.append('%-36s | worst %5.1f %-24s | window %5s %-24s | head %4.0f | entry %-26s | dt %.4f | idleInHold %d' % (
        lab[-36:], w['drift'] if w else 0.0, (w['clip'][:24] if w else ''), ('%.1f' % ww['drift']) if ww else ('0.0' if win else '-'),
        (ww['clip'][:24] if ww else ''), ha, ent[:26], fx, idle))
open(sys.argv[1], 'w', encoding='utf8').write('\n'.join(rows) + '\n')
for r in rows: print('TABLE231 ' + r)
