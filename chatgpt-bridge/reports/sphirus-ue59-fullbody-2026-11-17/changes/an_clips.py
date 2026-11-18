# an_clips.py <vc55 labels>: clip sequence (Motion Matching selection) with start time and duration, per plan segment.
import sys, json
for lb in sys.argv[1:]:
    d = json.load(open('Saved/Codex/Grip_20261106/rec/%s.json' % lb)); R = d['rows']; print('=====', lb)
    cur = None; t0 = 0; seg = None
    for r in R + [dict(t=R[-1]['t'], s=-1, gasp=['END'])]:
        c = str((r.get('gasp') or [''])[0])
        if c != cur:
            if cur is not None: print('  s%-2s %6.2f +%5.2f  %s' % (seg, t0, r['t'] - t0, cur))
            cur, t0, seg = c, r['t'], r['s']
