"""ltpcols248.py <label> <t0> <t1> [fields,...]: print selected LTP fields per row in [t0,t1] (default fields = the start-route decision set)."""
import sys, re
L = sys.argv[1]; t0 = float(sys.argv[2]); t1 = float(sys.argv[3])
F = sys.argv[4].split(',') if len(sys.argv) > 4 else ['t','cy','ay','camrot','accyaw','acc','cv_HasIntent','cv_DesiredVelocity','av_CurrentSelectedDatabase','av_Phase27_SelectedObject','av_Phase27_SelectedTime','av_SHM_IdleHold','av_CP_StartOwned']
p = 'Saved/Codex/SHME_V1_20260925/LTP/%s.ltp' % L
last = None
for line in open(p, encoding='utf8', errors='ignore'):
    d = {}
    for kv in line.rstrip('\n').split('|')[2:]:
        if '=' in kv:
            k, v = kv.split('=', 1); d.setdefault(k, v)
    try: t = float(d.get('t', 'nan'))
    except ValueError: continue
    if t0 <= t <= t1:
        row = [d.get(f, '?') for f in F]
        if row[1:] != last: print(' '.join('%s=%s' % (f, v) for f, v in zip(F, row)))
        last = row[1:]
