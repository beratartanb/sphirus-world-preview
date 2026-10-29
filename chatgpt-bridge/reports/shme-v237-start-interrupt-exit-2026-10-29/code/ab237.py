"""ab237.py <label>... : V2.37 A/B summary per run on the visible body: worst planted SLIP / DRAG (contact231) with time / foot / owner clip,
the SHM236 / SHM237 start / re-push clip episodes (first..last clip time, mean clip rate, what came next), frames with no database
(av_CurrentSelectedDatabase None after 2.5 s = DB not ready; such a run is not a content result) and the SLIP/DRAG list (--v)."""
import sys, os
H = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [os.path.join(H, '..', 'SHME_V231_20261026')]
from ltp231 import load, short
from contact231 import classify
V = '--v' in sys.argv
for lab in [a for a in sys.argv[1:] if not a.startswith('--')]:
    try: R = load(lab)
    except Exception as e: print('%-40s MISSING' % lab); continue
    eps = [e for e in classify(R) if e['cls'] in ('SLIP', 'DRAG')]
    w = max(eps, key=lambda e: e['drift']) if eps else None
    def at(i): return R[min(i, len(R) - 1)]
    wtxt = '%.1f cm %s %.2f %s@%.2f' % (w['drift'], w['s'], at(w['i0'])['t'], short(at(w.get('iw', w['i0']))['av_Phase27_SelectedObject']), at(w.get('iw', w['i0']))['av_Phase27_SelectedTime']) if w else '0'
    nodb = sum(1 for r in R if r['t'] > 2.5 and str(r.get('av_CurrentSelectedDatabase')) == 'None')
    epis = []; cur = None
    for i, r in enumerate(R):
        c = short(r['av_Phase27_SelectedObject'])
        if c.startswith(('SHM237_', 'SHM236_JogStart')):
            if cur and cur['clip'] == c and i == cur['i1'] + 1: cur['i1'] = i
            else:
                if cur: epis.append(cur)
                cur = {'clip': c, 'i0': i, 'i1': i}
        elif cur and i == cur['i1'] + 1: cur['next'] = '%s@%.2f' % (c, r['av_Phase27_SelectedTime']); epis.append(cur); cur = None
    if cur: epis.append(cur)
    et = []
    for e in epis:
        a, b = R[e['i0']], R[e['i1']]; dt = b['t'] - a['t']
        rate = (b['av_Phase27_SelectedTime'] - a['av_Phase27_SelectedTime']) / dt if dt > 0 else 0
        et.append('%s %.2f-%.2f s ct %.2f-%.2f rate %.2f -> %s' % (e['clip'].replace('SHM237_', '7:').replace('SHM236_', '6:'), a['t'], b['t'], a['av_Phase27_SelectedTime'], b['av_Phase27_SelectedTime'], rate, e.get('next', '-')))
    print('%-40s worst %-48s noDB %d | %s' % (lab, wtxt, nodb, ' ; '.join(et) or 'no SHM236/237 start'))
    if V:
        for e in eps: print('     %5.2f %s %-5s %5.1f %s@%.2f' % (at(e['i0'])['t'], e['s'], e['cls'], e['drift'], short(at(e.get('iw', e['i0']))['av_Phase27_SelectedObject']), at(e.get('iw', e['i0']))['av_Phase27_SelectedTime']))
