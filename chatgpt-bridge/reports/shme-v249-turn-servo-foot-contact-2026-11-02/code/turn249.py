"""turn249.py <label> [--every N]: frame-by-frame decomposition of a turning-start clip in game (V2.49).
Ground truth = data/clipdump.json (clip-space root x/y/yaw and balls per key, root included; the in-game root is locked to ref pose, so the
mesh component frame IS the clip root frame). For every LTP row while Phase27_SelectedObject is a turn clip:
  ideal mesh frame(t) = M(entry) o inv(Root(ct_entry)) o Root(ct)       (capsule following the clip root exactly)
  CAP  pos err = |mesh root world - ideal pos| (cm), yaw err = mesh yaw - ideal yaw (deg)  -> capsule authority error
  POSE err     = |in-game component-space ball - clip ball relative to its root at ct| (cm)  -> warping / foot placement / blend
  BALL world   = drift of each ball since entry; contact = ball z < 8 cm
Also prints the clip-time step per frame (dct / dt: 1.0 = clip plays at real speed) and the contract flags."""
import sys, json, math
L = sys.argv[1]; EVERY = int(sys.argv[sys.argv.index('--every') + 1]) if '--every' in sys.argv else 1
CD = json.load(open('Saved/Codex/SHME_V249_20261102/data/clipdump.json'))['clips']
def vec(s):
    try:
        p = dict(kv.split('=') for kv in s.split()); return float(p['X']), float(p['Y']), float(p['Z'])
    except Exception: return None
rows = []
for line in open('Saved/Codex/SHME_V1_20260925/LTP/%s.ltp' % L, encoding='utf8', errors='ignore'):
    d = {}
    for kv in line.rstrip('\n').split('|')[2:]:
        if '=' in kv:
            k, v = kv.split('=', 1); d.setdefault(k, v)
    try: d['t'] = float(d['t'])
    except Exception: continue
    rows.append(d)
def wrap(a): return (a + 180.0) % 360.0 - 180.0
def rot(x, y, deg):
    r = math.radians(deg); c, s = math.cos(r), math.sin(r); return x * c - y * s, x * s + y * c
def sample(clip, ct):
    R = CD[clip]['rows']; n = len(R); f = max(0.0, min(n - 1.0, ct * 30.0)); i = int(f); j = min(n - 1, i + 1); a = f - i
    out = []
    for k in range(len(R[0])):
        v0, v1 = R[i][k], R[j][k]
        if k == 2: v1 = v0 + wrap(v1 - v0)
        out.append(v0 + (v1 - v0) * a)
    return out
turn = [r for r in rows if '_crop' in r.get('av_Phase27_SelectedObject', '') or 'Start_Turn' in r.get('av_Phase27_SelectedObject', '')]
if not turn: print(L, 'no turn clip'); sys.exit()
e = turn[0]; key = e['av_Phase27_SelectedObject']
clip = [k for k in CD if k.startswith(key[:30])][0]
ct0 = float(e['av_Phase27_SelectedTime']); r0 = sample(clip, ct0)
m0 = vec(e['mh_root']); my0 = float(e['my'])
print('%s clip %s entry t=%.3f ct=%.3f mesh yaw %.1f  (yaw err + = mesh turned less than the clip toward + yaw)' % (L, clip, e['t'], ct0, my0))
print('   t     ct   dct/dt  CAPpos CAPyaw  POSEr POSEl  ballR_w ballL_w  zR   zL   spd  CSon CYon TS  sel')
bw0 = {s: vec(e['mx_ball_' + s]) for s in ('l', 'r')}; prev = None; last_clip = clip; n = 0
for r in rows:
    if r['t'] < e['t'] - 1e-6 or r['t'] > e['t'] + 1.3: continue
    sel = r.get('av_Phase27_SelectedObject', '')
    ct = float(r.get('av_Phase27_SelectedTime', 0))
    in_clip = sel == key
    m = vec(r['mh_root']); my = float(r['my'])
    if in_clip:
        c = sample(clip, ct)
        dx, dy = rot(c[0] - r0[0], c[1] - r0[1], my0 - r0[2]); ip = (m0[0] + dx, m0[1] + dy); iy = my0 + wrap(c[2] - r0[2])
        cpe = math.hypot(m[0] - ip[0], m[1] - ip[1]); cye = wrap(my - iy)
        pe = {}
        for s, off in (('l', 3), ('r', 6)):
            bw = vec(r['mx_ball_' + s]); bx, by = rot(bw[0] - m[0], bw[1] - m[1], -my)
            cx, cy = rot(c[off] - c[0], c[off + 1] - c[1], -c[2])
            pe[s] = math.hypot(bx - cx, by - cy)
    else: cpe = cye = float('nan'); pe = {'l': float('nan'), 'r': float('nan')}
    bd = {s: math.hypot(vec(r['mx_ball_' + s])[0] - bw0[s][0], vec(r['mx_ball_' + s])[1] - bw0[s][1]) for s in ('l', 'r')}
    z = {s: vec(r['mx_ball_' + s])[2] for s in ('l', 'r')}
    dct = (ct - prev[0]) / max(1e-4, r['t'] - prev[1]) if prev and in_clip and prev[2] else float('nan')
    prev = (ct, r['t'], in_clip)
    n += 1
    if n % EVERY: continue
    print('%6.3f %5.3f %6.2f %6.1f %6.1f %6.1f %5.1f %7.1f %7.1f %5.1f %5.1f %5.0f %4s %4s %3s %s' % (r['t'], ct, dct, cpe, cye, pe['r'], pe['l'], bd['r'], bd['l'], z['r'], z['l'],
          float(r.get('Speed2D', 0)), r.get('cv_ClipSpeedOn', '?')[:1], r.get('cv_ClipYawOn', '?')[:1], r.get('av_SHM248_TurnStart', '?')[:1], sel[-28:]))
