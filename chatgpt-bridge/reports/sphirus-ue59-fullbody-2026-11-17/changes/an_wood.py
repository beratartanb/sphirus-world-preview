# an_wood.py <vc55 labels>: timeline of state/flag/montage changes in an interaction recording (read-only)
import json, sys, os
R = os.path.join(os.path.dirname(__file__), '..', '..', 'Saved', 'Codex', 'Grip_20261106', 'rec')
for lab in sys.argv[1:]:
    d = json.load(open(os.path.join(R, lab + '.json')))
    rows = d['rows'] if isinstance(d, dict) else d
    print('=====', lab, 'rows', len(rows), 'top', [k for k in d.keys() if k != 'rows'] if isinstance(d, dict) else '')
    if isinstance(d, dict):
        for k in d:
            if k != 'rows': print('  ', k, str(d[k])[:300])
    last = {}
    for r in rows:
        for k in ('st', 'flags', 'mont', 'hub', 'arm', 'reach'):
            v = r.get(k)
            s = json.dumps(v)[:160]
            if last.get(k) != s:
                if k in ('st', 'flags', 'mont', 'hub'): print('  t %6.2f %-5s %s' % (r.get('t', 0), k, s))
                last[k] = s
