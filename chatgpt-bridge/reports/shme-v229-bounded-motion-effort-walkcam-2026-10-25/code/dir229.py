"""dir229.py label [label ...]: direction audit (V2.29). Per movement stage, steady window = the last 1.2 s: requested heading (raw input,
world), travel heading (capsule velocity), body facing (actor yaw) and the visible chest facing (shoulder line), all relative to the
CAMERA yaw; travel - request error, speed, the clips Motion Matching played (top 2 by frames), and the stride/foot skate from the stage
report when present. Also 'steps': in the stage's first 1 s, the number of frames where the travel heading moved > 6 deg in one frame
(a stepped / quantised change) and the max travel heading change per frame."""
import json, sys, math, pathlib, re
E = pathlib.Path(__file__).resolve().parents[2] / 'Saved/Codex/SHME_V1_20260925/Evidence'
REP = pathlib.Path(__file__).resolve().parents[2] / 'Saved/Codex/SHME_V212_20261017/Reports'
def f(x, d=0.0):
    try: return float(x)
    except Exception: return d
W = lambda a: (a + 180.0) % 360.0 - 180.0
for lab in [a for a in sys.argv[1:] if not a.startswith('--')]:
    R0 = sorted([r for r in json.load(open(E / (lab + '.json'))) if isinstance(r, dict) and r.get('t') is not None and isinstance(r.get('ax'), list)], key=lambda r: f(r['t']))
    R = []
    for r in R0:
        if R and abs(f(r['t']) - f(R[-1]['t'])) < 0.004: R[-1] = r
        else: R.append(r)
    sk = {}
    rp = REP / (lab + '.txt')
    if rp.exists():
        m = re.search(r'worst stages: (.*)', rp.read_text(encoding='utf8', errors='ignore'))
        if m:
            for it in m.group(1).split(','):
                it = it.strip().rsplit(' ', 1)
                if len(it) == 2: sk[it[0]] = it[1]
    stages = []
    for r in R:
        s = str(r.get('stage', ''))
        if not stages or stages[-1][0] != s: stages.append([s, []])
        stages[-1][1].append(r)
    print('%-22s %6s %6s %6s %6s %6s %5s %5s %5s  %s' % ('stage', 'req', 'trav', 'err', 'actor', 'chest', 'spd', 'stp', 'dmax', 'clips'))
    for s, rs in stages:
        if 'mv_' not in s or 'stop' in s or 'rel' in s or len(rs) < 20: continue
        t_end = f(rs[-1]['t']); win = [r for r in rs if f(r['t']) > t_end - 1.2]
        def m(fn):
            v = [fn(r) for r in win]; v = [x for x in v if x is not None]
            if not v: return None
            sx = sum(math.cos(math.radians(x)) for x in v); sy = sum(math.sin(math.radians(x)) for x in v); return math.degrees(math.atan2(sy, sx))
        cy = lambda r: f(r.get('cy'))
        req = m(lambda r: W(math.degrees(math.atan2(f(r.get('liy')), f(r.get('lix')))) - cy(r)) if math.hypot(f(r.get('lix')), f(r.get('liy'))) > 0.2 else None)
        trv = m(lambda r: W(math.degrees(math.atan2(f(r.get('avy')), f(r.get('avx')))) - cy(r)) if math.hypot(f(r.get('avx')), f(r.get('avy'))) > 20 else None)
        act = m(lambda r: W(f(r.get('ay')) - cy(r)))
        def chest(r):
            sl, sr = r.get('vb_sh_l'), r.get('vb_sh_r')
            if not (isinstance(sl, list) and isinstance(sr, list)): return None
            return W(math.degrees(math.atan2(-(sr[0] - sl[0]), sr[1] - sl[1])) - cy(r))
        ch = m(chest)
        spd = sum(math.hypot(f(r.get('avx')), f(r.get('avy'))) for r in win) / len(win)
        first = [r for r in rs if f(r['t']) < f(rs[0]['t']) + 1.0]; hs = []
        for r in first:
            if math.hypot(f(r.get('avx')), f(r.get('avy'))) > 20: hs.append(math.degrees(math.atan2(f(r.get('avy')), f(r.get('avx')))))
        dd = [abs(W(hs[i] - hs[i - 1])) for i in range(1, len(hs))]
        clips = {}
        for r in win: c = str(r.get('av_Phase27_SelectedObject', ''))[-22:]; clips[c] = clips.get(c, 0) + 1
        top = ' '.join('%s:%d' % kv for kv in sorted(clips.items(), key=lambda kv: -kv[1])[:2])
        fm = lambda x: '-' if x is None else '%.0f' % x
        print('%-22s %6s %6s %6s %6s %6s %5.0f %5d %5.1f  %s %s' % (s[-22:], fm(req), fm(trv), fm(W(trv - req)) if (trv is not None and req is not None) else '-', fm(act), fm(ch), spd, sum(1 for x in dd if x > 6), max(dd) if dd else 0, top, ('skate ' + sk[s]) if s in sk else ''))
