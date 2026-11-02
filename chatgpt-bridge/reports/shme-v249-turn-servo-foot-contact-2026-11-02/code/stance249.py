"""stance249.py <label> [...]: the in-game stance at the request frame of a turning start (component space, mesh axes, cm, relative to the
mesh root) vs every cropped turn clip's frame 0 (clipdump.json). Prints per run: ball_l / ball_r / foot_l / foot_r xy, and the per-clip
stance difference |game - clip frame0| per foot."""
import sys, json, math
CD = json.load(open('Saved/Codex/SHME_V249_20261102/data/clipdump.json'))['clips']
def vec(s):
    p = dict(kv.split('=') for kv in s.split()); return float(p['X']), float(p['Y']), float(p['Z'])
def rot(x, y, deg):
    r = math.radians(deg); c, s = math.cos(r), math.sin(r); return x * c - y * s, x * s + y * c
def clip0(name):
    r = CD[name]['rows'][0]; out = {}
    for b, o in (('ball_l', 3), ('ball_r', 6), ('foot_l', 9), ('foot_r', 12)):
        out[b] = rot(r[o] - r[0], r[o + 1] - r[1], -r[2])
    return out
for L in sys.argv[1:]:
    rows = []
    for line in open('Saved/Codex/SHME_V1_20260925/LTP/%s.ltp' % L, encoding='utf8', errors='ignore'):
        d = {}
        for kv in line.rstrip('\n').split('|')[2:]:
            if '=' in kv:
                k, v = kv.split('=', 1); d.setdefault(k, v)
        try: d['t'] = float(d['t']); rows.append(d)
        except Exception: pass
    req = [r for r in rows if r['t'] > 9.0 and float(r.get('acc', 0)) > 1.0]
    if not req: continue
    i = rows.index(req[0]); r = rows[max(0, i - 1)]
    m = vec(r['mh_root']); my = float(r['my']); g = {}
    for b in ('ball_l', 'ball_r', 'foot_l', 'foot_r'):
        w = vec(r['mx_' + b]); g[b] = rot(w[0] - m[0], w[1] - m[1], -my)
    print('%s t=%.2f prev=%s' % (L, r['t'], r.get('av_Phase27_SelectedObject', '')[-34:]))
    print('   game  ' + '  '.join('%s (%6.1f %6.1f)' % (b, g[b][0], g[b][1]) for b in ('ball_l', 'ball_r')))
    for c in sorted(CD):
        if '_crop' not in c: continue
        k = clip0(c); dl = math.hypot(g['ball_l'][0] - k['ball_l'][0], g['ball_l'][1] - k['ball_l'][1]); dr = math.hypot(g['ball_r'][0] - k['ball_r'][0], g['ball_r'][1] - k['ball_r'][1])
        print('   %-32s ball_l (%6.1f %6.1f) ball_r (%6.1f %6.1f)  diff L %5.1f R %5.1f' % (c, k['ball_l'][0], k['ball_l'][1], k['ball_r'][0], k['ball_r'][1], dl, dr))
