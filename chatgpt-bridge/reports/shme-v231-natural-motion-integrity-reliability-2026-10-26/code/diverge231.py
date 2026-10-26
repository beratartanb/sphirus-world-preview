"""diverge231.py <labelA> <labelB> [eps] : first frames where two same-input runs differ (per field), aligned by frame index within the move stage."""
import sys, os, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ltp231 import load
A, B = load(sys.argv[1]), load(sys.argv[2]); eps = float(sys.argv[3]) if len(sys.argv) > 3 else 0.05
print('frames', len(A), len(B))
first = {}
for i, (a, b) in enumerate(zip(A, B)):
    if abs(a['t'] - b['t']) > 1e-4: print('time misalign at', i, a['t'], b['t']); break
    for k, va in a.items():
        if k in first or k in ('fc', 'stage'): continue
        vb = b.get(k)
        if isinstance(va, tuple) and isinstance(vb, tuple): d = max(abs(x - y) for x, y in zip(va, vb))
        elif isinstance(va, float) and isinstance(vb, float): d = abs(va - vb)
        else: d = 0 if str(va) == str(vb) else 1e9
        if d > eps: first[k] = (a['t'], va, vb)
for k, (t, va, vb) in sorted(first.items(), key=lambda x: x[1][0])[:40]: print('%.3f %-34s %s | %s' % (t, k, str(va)[:60], str(vb)[:60]))
