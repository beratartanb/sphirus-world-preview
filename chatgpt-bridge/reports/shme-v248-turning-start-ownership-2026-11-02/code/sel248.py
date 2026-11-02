"""sel248.py <label> [t_req=9.6]: start-selection summary of a j45_sl-type run: control yaw / body yaw at the request, the sequence of
(database, clip) selections from the request for 2.5 s with their start times, and the body yaw 1.5 s later (did the body turn?)."""
import sys
L = sys.argv[1]; treq = float(sys.argv[2]) if len(sys.argv) > 2 else 9.6
rows = []
for line in open('Saved/Codex/SHME_V1_20260925/LTP/%s.ltp' % L, encoding='utf8', errors='ignore'):
    d = {}
    for kv in line.rstrip('\n').split('|')[2:]:
        if '=' in kv:
            k, v = kv.split('=', 1); d.setdefault(k, v)
    try: d['t'] = float(d['t'])
    except Exception: continue
    rows.append(d)
req = [r for r in rows if r['t'] >= treq and float(r.get('acc', 0)) > 1.0]
if not req: print(L, 'no request after', treq); sys.exit()
r0 = req[0]; t0 = r0['t']
def ang(a, b): return ((float(a) - float(b) + 180) % 360) - 180
print('%s req t=%.2f cy=%s ay=%s accyaw=%s  req-body=%.0f req-look=%.0f' % (L, t0, r0['cy'], r0['ay'], r0['accyaw'], ang(r0['accyaw'], r0['ay']), ang(r0['accyaw'], r0['cy'])))
seq = []; last = None
for r in rows:
    if t0 - 0.05 <= r['t'] <= t0 + 2.5:
        k = (r.get('av_CurrentSelectedDatabase', '?'), r.get('av_Phase27_SelectedObject', '?'))
        if k != last: seq.append((r['t'], k)); last = k
for t, (db, c) in seq: print('  %.2f  %s / %s' % (t, db.replace('PSD_', ''), c))
after = [r for r in rows if r['t'] >= t0 + 1.5]
if after: print('  body yaw +1.5 s: %s (turned %.0f deg); speed %s' % (after[0]['ay'], ang(after[0]['ay'], r0['ay']), after[0].get('Speed2D')))
