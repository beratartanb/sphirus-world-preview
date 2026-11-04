"""dir255.py <label> [--top N] [--v T0 T1] : V2.55 command truth per frame. Separates MOMENTUM from a WRONG TARGET on the same frames.
For every frame: key direction (stage), control yaw, the direction the keys mean on screen (E = control yaw + key angle), the direction the
engine applied (last input vector, world), velocity, acceleration, actor yaw, the plan target (SHM238_Yaw0 + Delta while SHM238_On), clip, DB.
ERROR e = v_des - v (v_des = commanded direction x max speed). Momentum is not a defect: the velocity may still point the old way, but the
ACCELERATION must point along e. Defect frames (|e| > 60 cm/s):
   WRONG  = a . e_hat < -120 cm/s2   (the body is being accelerated AWAY from what the player commands)
   STALL  = |a . e_hat| < 120 cm/s2  (nothing happens toward the command)
FRAME  = |E - applied| > 20 deg (the keys do not mean what the screen says).
Per held-key segment: reaction times (first a toward e, heading within 30 deg, body within 30 deg), wrong / stall time, wrong-side body turn."""
import sys, math
sys.path.insert(0, 'Tools/SHME_V231_20261026'); import ltp231
L = sys.argv[1]; TOP = int(sys.argv[sys.argv.index('--top') + 1]) if '--top' in sys.argv else 12
V = (float(sys.argv[sys.argv.index('--v') + 1]), float(sys.argv[sys.argv.index('--v') + 2])) if '--v' in sys.argv else None
def ang(a): return (a + 180.0) % 360.0 - 180.0
def num(x, d=0.0):
    try: return float(x)
    except Exception: return d
rows = [r for r in ltp231.load(L) if str(r.get('stage', '')).startswith(('mv_', 'yaw_')) and 'avx' in r]
N = len(rows); T = [r['t'] for r in rows]
def stg(r):
    p = str(r['stage']).split('+')[-1].split('_')
    if p[0] == 'mv' and p[1].startswith('kb') and len(p) >= 5: return (None if p[2] == 'rel' else float(p[2])), p[4], int(p[3]), p[1].endswith('s')
    return None, '0', -1, False
K = [stg(r) for r in rows]
VX = [(r['avx'], r['avy']) for r in rows]
W = 3
A = []
for i in range(N):
    a, b = max(0, i - W), min(N - 1, i + W); dt = max(1e-3, T[b] - T[a]); A.append(((VX[b][0] - VX[a][0]) / dt, (VX[b][1] - VX[a][1]) / dt))
def hd(v): return math.degrees(math.atan2(v[1], v[0]))
out = []; i = 0; tot = {'wrong': 0.0, 'stall': 0.0, 'frame': 0.0, 'held': 0.0}
segs = []
while i < N:
    j = i
    while j + 1 < N and K[j + 1][0] == K[i][0] and K[j + 1][1] == K[i][1]: j += 1
    segs.append((i, j)); i = j + 1
for si, (i, j) in enumerate(segs):
    if K[i][0] is None or T[j] - T[i] < 0.08: continue
    keys = K[i][1]; a0 = K[i][0]; prev = K[segs[si - 1][0]][1] if si else '?'
    v0 = VX[i]; s0 = math.hypot(*v0)
    wrong = stall = fr = 0.0; t_a = t_h = t_b = None; mins = 1e9; wr_run = 0.0; wr_max = 0.0; st_run = 0.0; st_max = 0.0; fmax = 0.0; clips = []; bp = 0.0
    prevD = None; osc = 0; Dfirst = None; tgt_err = 0.0; yaw0 = rows[i].get('ay', 0.0); ysum = 0.0; ylast = yaw0
    for k in range(i, j + 1):
        r = rows[k]; dt = T[k] - T[k - 1] if k else 0.0
        li = (r.get('lix', 0.0), r.get('liy', 0.0)); hasli = math.hypot(*li) > 0.01
        E = r['cy'] + a0; D = hd(li) if hasli else E
        if Dfirst is None: Dfirst = D
        fe = abs(ang(E - D)) if 0.05 < T[k] - T[i] < 0.35 else 0.0; fmax = max(fmax, fe)   # the frame must agree with the screen right after a key change; a held key keeps its world direction by design
        if fe > 20: fr += dt
        if k > i and hasli and prevD is not None and abs(ang(D - prevD)) > 15: osc += 1
        prevD = D if hasli else prevD
        vm = num(r.get('pv_cm.MaxWalkSpeed'), 300.0); dx, dy = math.cos(math.radians(D)), math.sin(math.radians(D))
        ex, ey = dx * vm - VX[k][0], dy * vm - VX[k][1]; em = math.hypot(ex, ey); s = math.hypot(*VX[k]); mins = min(mins, s)
        pr = (A[k][0] * ex + A[k][1] * ey) / max(em, 1e-3)
        if em > 60 and T[k] - T[i] > 0.12:
            if pr < -120: wrong += dt; wr_run += dt; wr_max = max(wr_max, wr_run)
            else: wr_run = 0.0
            if abs(pr) < 120: stall += dt; st_run += dt; st_max = max(st_max, st_run)
            else: st_run = 0.0
        else: wr_run = st_run = 0.0
        if t_a is None and pr > 150: t_a = T[k] - T[i]
        if t_h is None and s > 50 and abs(ang(hd(VX[k]) - D)) < 30: t_h = T[k] - T[i]
        if t_b is None and abs(ang(r.get('ay', 0.0) - D)) < 30: t_b = T[k] - T[i]
        d_ = ang(r.get('ay', 0.0) - ylast); ysum += d_; ylast = r.get('ay', 0.0)
        if str(r.get('pv_CR_Backpedal')) == 'True': bp += dt
        c = ltp231.short(r.get('av_Phase27_SelectedObject', ''))[-24:]
        if not clips or clips[-1] != c: clips.append(c)
        if str(r.get('av_SHM238_On')) == 'True': tgt_err = max(tgt_err, abs(ang(num(r.get('av_SHM238_Yaw0')) + num(r.get('av_SHM238_Delta')) - D)))
    dur = T[j] - T[i]; tot['held'] += dur; tot['wrong'] += wrong; tot['stall'] += stall; tot['frame'] += fr
    chg = ang(Dfirst - hd(v0)) if s0 > 30 else 0.0
    side = ''
    if s0 > 80 and 20 < abs(chg) < 150 and dur > 0.5 and abs(ysum) > 25 and ysum * chg < 0: side = 'WRONGSIDE'
    tot['osc'] = tot.get('osc', 0) + osc; out.append(dict(t=T[i], dur=dur, osc=osc, prev=prev, keys=keys, s0=s0, chg=chg, ta=t_a, th=t_h, tb=t_b, mins=mins, wrong=wrong, wr=wr_max, stall=stall, st=st_max, fmax=fmax, fr=fr, tgt=tgt_err, ysum=ysum, side=side, bp=bp, clips=clips))
f2 = lambda x: '  -  ' if x is None else '%5.2f' % x
print('DIR255 %s held %.1f s | WRONG %.2f s | STALL %.2f s | FRAME %.2f s | OSC %d | events %d | wrongside %d | runs>0.15s wrong %d stall>0.3s %d' % (L, tot['held'], tot['wrong'], tot['stall'], tot['frame'], tot.get('osc', 0), len(out), sum(1 for e in out if e['side']), sum(1 for e in out if e['wr'] > 0.15), sum(1 for e in out if e['st'] > 0.3)))
print(' t      dur  keys      v0  chg  | tA    tHead tBody minV | wrong(max) stall(max) | frame tgtErr yaw  bp   clips')
ranked = sorted(out, key=lambda e: -(2 * e['wr'] + e['st'] + (1 if e['side'] else 0)))
for e in ranked[:TOP]:
    print('%6.2f %4.2f %3s>%-3s %4.0f %+5.0f | %s %s %s %4.0f | %.2f(%.2f) %.2f(%.2f) | %3.0f %4.0f %+5.0f %.1f %s %s' % (e['t'], e['dur'], e['prev'], e['keys'], e['s0'], e['chg'], f2(e['ta']), f2(e['th']), f2(e['tb']), e['mins'], e['wrong'], e['wr'], e['stall'], e['st'], e['fmax'], e['tgt'], e['ysum'], e['bp'], e['side'], ' > '.join(e['clips'][:4])))
if V:
    print('--- timeline')
    for k in range(N):
        if V[0] <= T[k] <= V[1] and k % 3 == 0:
            r = rows[k]; li = (r.get('lix', 0.0), r.get('liy', 0.0)); D = hd(li) if math.hypot(*li) > .01 else float('nan')
            print('%6.2f %-3s cy %+6.0f E %s D %+6.0f v %4.0f vh %+6.0f ay %+6.0f IFY %+6.0f Loco %+6.0f st %s Off %+5.0f bp %s on238 %s tgt %+6.0f 228 %s | %s %.2f %s' % (T[k], K[k][1], r['cy'], ('%+6.0f' % ang(r['cy'] + K[k][0])) if K[k][0] is not None else '   -  ', D, math.hypot(*VX[k]), hd(VX[k]), r.get('ay', 0.0), num(r.get('cv_LocoIFY')), num(r.get('cv_LocoYaw')), str(r.get('cv_LocoState'))[:3], num(r.get('cv_InFrameOff')), str(r.get('pv_CR_Backpedal'))[:1], str(r.get('av_SHM238_On'))[:1], ang(num(r.get('av_SHM238_Yaw0')) + num(r.get('av_SHM238_Delta'))), str(r.get('av_SHM228_On'))[:1], ltp231.short(r.get('av_Phase27_SelectedObject', ''))[-26:], num(r.get('av_Phase27_SelectedTime')), ltp231.short(r.get('av_CurrentSelectedDatabase', ''))[-22:]))
