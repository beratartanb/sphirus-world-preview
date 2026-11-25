# an_trav4.py <label> : traversal attempt on the test lane: check telemetry at the jump key, montage / movement mode timeline,
# height reached, where the capsule ends, and whether it ended on top / beyond / in front of the obstacle.
import json, sys, math
lab = sys.argv[1]; rows = json.load(open('Saved/Codex/Grip_20261106/rec/%s.json' % lab))['rows']
H = lambda r: r['hook'] if isinstance(r['hook'], dict) else {}
x0 = rows[0]['x']; z0 = rows[0]['z']; last = None; out = []
for r in rows:
    e = H(r).get('ex'); s_ = H(r).get('exs')
    k = (str(r['mont'])[-40:], )
    if k != last: out.append('  t %5.2f s%d x %+5.0f z %5.1f v %3.0f | montage %s | clip %s' % (r['t'], r['s'], r['x'] - x0, r['z'], math.hypot(r['vx'], r['vy']), k[0], (r['gasp'][0] or '')[-28:])); last = k
j = [r for r in rows if r['s'] == 2]
e = H(j[2]).get('ex') if len(j) > 2 else None; s_ = H(j[2]).get('exs') if len(j) > 2 else None
print('%s | at jump: TR_Kind/GT_H/GT_D/GT_Dist %s | Ok/Room/Done/FlOk %s | max z %.0f (start %.0f) | end x %+.0f z %.0f' % (lab, e[10:14] if isinstance(e, list) and len(e) > 13 else e, s_[1:] if isinstance(s_, list) else s_, max(r['z'] for r in rows), z0, rows[-1]['x'] - x0, rows[-1]['z']))
print('\n'.join(out[:10]))
