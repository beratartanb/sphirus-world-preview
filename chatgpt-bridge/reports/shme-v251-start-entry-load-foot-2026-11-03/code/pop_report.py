"""pop_report.py <label> [--thr 25] [--json] : whole-run animation-transition pop detector on the RENDERED body.
Root-relative (driver root `mh_root`, mesh yaw `my` + 90) positions of vb_head / vb_chest / vb_pelvis / vb_sh_l / vb_sh_r per
harness tick; per frame: root-relative acceleration (m/s^2, from uneven-dt second differences) and the excess displacement
(cm) = |second difference| minus what a smooth motion with the neighbours' acceleration would give (FPS-robust).
Natural gait accelerations of the upper body stay < ~15-20 m/s^2; a crossfade / pose-replacement / evaluator handover shows
as a spike. Events = runs of frames above --thr on any of head/chest/pelvis/shoulders, merged within 0.12 s.
Each event is attributed: input stage (harness segment) and time since its start, the Motion Matching database/clip switch
nearest the event (ABP telemetry), CP owner flags (sto start / so stop), idle takeover, redirect hold, SHME family, montage.
Transition windows: per stage boundary and per gait event (mid-run gait button), the max pop in [0, 1.2 s].
Output: text table (and with --json a machine-readable dump to Saved/Codex/SHME_V21_20261014/Pops/<label>.json)."""
import json, sys, math, pathlib, bisect, re
ROOT = pathlib.Path(__file__).resolve().parents[2]
E = ROOT / 'Saved/Codex/SHME_V1_20260925/Evidence'
OUT = ROOT / 'Saved/Codex/SHME_V21_20261014/Pops'
args = sys.argv[1:]; lab = args[0]
THR = float(args[args.index('--thr') + 1]) if '--thr' in args else 25.0
rows = json.load(open(E / (lab + '.json')))
try: A = json.load(open(E / (lab + '_abp.json')))
except Exception: A = []
try: S = json.load(open(E / (lab + '_shm.json')))
except Exception: S = []
# protocol runs log protocol time; harness (no_ltp) runs log game time. Offset from the last rows (validation.md).
off = 0.0
if S and rows:
    o = float(S[-1].get('gt', 0)) - float(rows[-1].get('t', 0))
    off = o if abs(o) > 0.05 else 0.0
BONES = ('vb_head', 'vb_chest', 'vb_pelvis', 'vb_sh_l', 'vb_sh_r')
def vec(x):
    if isinstance(x, list) and len(x) == 3: return [float(q) for q in x]
    return None
def rel(r, k):
    p = vec(r.get(k)); o = vec(r.get('mh_root'))
    if not p or not o: return None
    yaw = math.radians(float(r.get('my', 0.0)) + 90.0); f = (math.cos(yaw), math.sin(yaw)); l = (-f[1], f[0])
    d = (p[0] - o[0], p[1] - o[1], p[2] - o[2])
    return (d[0] * f[0] + d[1] * f[1], d[0] * l[0] + d[1] * l[1], d[2])
def dedup(rs):
    """harness rows with the same game time (several slate ticks in one game frame, e.g. around a hitch) -> keep the last"""
    out = []
    for r in rs:
        if out and abs(float(r['t']) - float(out[-1]['t'])) < 0.004: out[-1] = r
        else: out.append(r)
    return out
R = dedup([r for r in rows if r.get('t') is not None])
T = [float(r['t']) for r in R]
P = {b: [rel(r, b) for r in R] for b in BONES}
acc = {b: [0.0] * len(R) for b in BONES}; exc = {b: [0.0] * len(R) for b in BONES}
for b in BONES:
    for i in range(1, len(R) - 1):
        x0, x1, x2 = P[b][i - 1], P[b][i], P[b][i + 1]
        if not (x0 and x1 and x2): continue
        d0 = max(T[i] - T[i - 1], 1e-3); d1 = max(T[i + 1] - T[i], 1e-3)
        if d0 > 0.1 or d1 > 0.1: continue          # hitch (> 0.1 s frame): not a pose pop (V2.1: was 0.25)
        a = [((x2[j] - x1[j]) / d1 - (x1[j] - x0[j]) / d0) / ((d0 + d1) / 2.0) / 100.0 for j in range(3)]
        acc[b][i] = math.sqrt(sum(q * q for q in a))
    for i in range(2, len(R) - 2):
        if acc[b][i] <= 0: continue
        nb = [acc[b][k] for k in (i - 2, i - 1, i + 1, i + 2) if acc[b][k] > 0]
        base = sorted(nb)[len(nb) // 2] if nb else 0.0
        dt = max(T[i + 1] - T[i - 1], 1e-3) / 2.0
        exc[b][i] = max(acc[b][i] - base, 0.0) * dt * dt * 100.0     # cm of displacement not explained by the neighbours
AT = [float(a.get('gt', 0)) - off for a in A]
def abp_at(t):
    if not A: return {}
    i = bisect.bisect_left(AT, t); i = min(max(i, 0), len(A) - 1)
    if i > 0 and abs(AT[i - 1] - t) < abs(AT[i] - t): i -= 1
    return A[i]
def switch_near(t, win=0.07):
    """the Motion Matching clip / db change closest to t inside +-win"""
    if not A: return None
    i0 = bisect.bisect_left(AT, t - win - 0.05); best = None
    for i in range(max(i0, 1), len(A)):
        if AT[i] > t + win: break
        if str(A[i].get('mmanim')) != str(A[i - 1].get('mmanim')) or str(A[i].get('mmdb')) != str(A[i - 1].get('mmdb')):
            d = abs(AT[i] - t)
            if best is None or d < best[0]:
                best = (d, '%s:%s -> %s:%s' % (str(A[i - 1].get('mmdb')).replace('PSD_', '')[:22], str(A[i - 1].get('mmanim'))[-26:], str(A[i].get('mmdb')).replace('PSD_', '')[:22], str(A[i].get('mmanim'))[-26:]))
    return best[1] if best else None
def flags_change(t, win=0.07):
    """ABP owner flags that flip within +-win of t"""
    out = []
    if not A: return out
    i0 = bisect.bisect_left(AT, t - win - 0.05)
    for i in range(max(i0, 1), len(A)):
        if AT[i] > t + win: break
        for k, nm in (('sto', 'CPstart'), ('so', 'CPstop'), ('idle', 'idle'), ('hold', 'stanceHold'), ('rdh', 'rdHold'), ('tip', 'turnInPlace'), ('wait', 'idleWait'), ('fam', 'family')):
            if str(A[i].get(k)) != str(A[i - 1].get(k)): out.append('%s %s->%s' % (nm, A[i - 1].get(k), A[i].get(k)))
    return sorted(set(out))
stage_start = {}; stages = [str(r.get('stage', '')) for r in R]
for i, s in enumerate(stages):
    if i == 0 or s != stages[i - 1]: stage_start.setdefault(s, T[i])
# events
ev = []
for i in range(len(R)):
    m = max(acc[b][i] for b in BONES)
    if m < THR: continue
    if ev and T[i] - ev[-1]['t1'] <= 0.12:
        e = ev[-1]; e['t1'] = T[i]
        if m > e['peak']: e.update(peak=m, ti=T[i], bone=max(BONES, key=lambda b: acc[b][i]), exc=max(exc[b][i] for b in BONES))
    else:
        ev.append(dict(t0=T[i], t1=T[i], ti=T[i], peak=m, bone=max(BONES, key=lambda b: acc[b][i]), exc=max(exc[b][i] for b in BONES)))
for e in ev:
    i = bisect.bisect_left(T, e['ti']); i = min(i, len(R) - 1); r = R[i]; a = abp_at(e['ti'])
    st = stages[i]; e['stage'] = st; e['since'] = round(e['ti'] - stage_start.get(st, e['ti']), 2)
    e['speed'] = round(float(r.get('Speed2D', 0)), 0); e['switch'] = switch_near(e['ti']); e['flags'] = flags_change(e['ti'])
    e['db'] = str(a.get('mmdb', '')).replace('PSD_', ''); e['clip'] = str(a.get('mmanim', ''))[-30:]; e['mont'] = str(r.get('mona', r.get('mont', '')))[-30:]
    e['fam'] = a.get('fam'); e['dt'] = round(T[min(i + 1, len(T) - 1)] - T[max(i - 1, 0)], 3)
    owner = 'MM switch' if e['switch'] else ('CP/flag ' + ','.join(e['flags']) if e['flags'] else ('montage' if e['mont'] not in ('none', '', 'None') else 'in-clip / layer'))
    e['owner'] = owner
# transition windows: stage boundaries + gait events
win = []
for i in range(1, len(R)):
    if stages[i] != stages[i - 1]:
        t0 = T[i]; mx = 0.0; who = None
        for e in ev:
            if t0 - 0.05 <= e['ti'] <= t0 + 1.2 and e['peak'] > mx: mx = e['peak']; who = e['owner'] + (' ' + e['switch'] if e['switch'] else '')
        # also the plain max acceleration in the window (sub-threshold)
        mxa = 0.0
        for k in range(i, len(R)):
            if T[k] > t0 + 1.2: break
            mxa = max(mxa, max(acc[b][k] for b in BONES))
        win.append(dict(t=round(t0, 2), frm=stages[i - 1], to=stages[i], max_acc=round(mxa, 1), event_peak=round(mx, 1), owner=who))
rate = round(len(R) / max(T[-1] - T[0], 0.1), 1) if len(T) > 2 else 0
summary = dict(label=lab, rows=len(R), rate=rate, thr=THR, events=len(ev), worst=round(max([e['peak'] for e in ev] or [0]), 1),
               by_owner={})
for e in ev:
    k = e['owner'].split(' ')[0] + (' ' + e['owner'].split(' ')[1] if e['owner'].startswith(('MM', 'CP')) else '')
    summary['by_owner'][k] = summary['by_owner'].get(k, 0) + 1
try: _pie = json.load(open(E.parent / (lab + '_pie.json'))); _st = _pie.get('status', '?') + ('' if _pie.get('state_mode') is None else ' ' + _pie['state_mode'])   # V2.26: run status + state mode
except Exception: _st = '?'
print('%s | rows %d rate %.1f/s | pops >%g m/s2: %d (worst %.0f) | by owner %s | %s' % (lab, len(R), rate, THR, len(ev), summary['worst'], summary['by_owner'], _st))
print('%7s %5s %-26s %5s %4s %-9s %6s %5s | %s' % ('t', 'peak', 'stage', '+s', 'v', 'bone', 'exc_cm', 'dt', 'owner / switch / flags'))
for e in sorted(ev, key=lambda e: -e['peak'])[:25]:
    print('%7.2f %5.0f %-26s %5.2f %4.0f %-9s %6.2f %5.3f | %s%s%s' % (e['ti'], e['peak'], e['stage'][:26], e['since'], e['speed'], e['bone'][3:], e['exc'], e['dt'], e['owner'][:40], (' | ' + e['switch']) if e['switch'] else '', (' | ' + ','.join(e['flags'])) if e['flags'] and not e['owner'].startswith('CP') else ''))
print('transition windows (max upper-body acc in [0, 1.2 s] after each input change):')
for w in win:
    print('  %6.2f %-24s -> %-24s max %5.1f | event %5.1f %s' % (w['t'], w['frm'][:24], w['to'][:24], w['max_acc'], w['event_peak'], w['owner'] or ''))
if '--json' in args:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / (lab + '.json')).write_text(json.dumps(dict(summary=summary, events=ev, windows=win), indent=1), encoding='utf8')
