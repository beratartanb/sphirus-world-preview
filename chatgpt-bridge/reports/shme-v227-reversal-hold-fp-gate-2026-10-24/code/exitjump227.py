"""exitjump227.py label [label ...]: the authored-reversal clip's life in a run - for every span where an SHM226_JogRev clip is the selected
asset: entry / exit times, selected clip time at entry / exit vs the clip length (remaining seconds at the exit), the ABP episode
(av_SHM_RedirectActive) span and the FootPlacement-off span (av_SHM_FootPlaceOff) relative to the clip, the play-rate (selected-time advance
per real second), then the JUMPS: max per-frame horizontal displacement of a PLANTED ball (height <= floor + 2 cm) inside the clip and in the
exit window [exit - 0.2, exit + 0.6] s, the max per-frame pelvis displacement beyond the capsule's own travel (|d pelvis_xy| - Speed2D*dt) in the
same windows, and what the Motion Matching selects after the exit (asset, time, database). cm, s. Reads Saved/Codex/SHME_V1_20260925/Evidence."""
import json, sys, math, pathlib
E = pathlib.Path(__file__).resolve().parents[2] / 'Saved/Codex/SHME_V1_20260925/Evidence'
LENS = {}
try: LENS = {k: v['len'] for k, v in json.load(open(pathlib.Path(__file__).resolve().parents[2] / 'Saved/Codex/SHME_V226_20261024/gen226_rev_write.json'))['clips'].items()}
except Exception: pass
def f(x, d=0.0):
    try: return float(x)
    except Exception: return d
def b(x): return str(x) in ('True', 'true', '1', '1.0')
for lab in [a for a in sys.argv[1:] if not a.startswith('--')]:
    p = E / (lab + '.json')
    if not p.exists(): print('EXIT227 %s MISSING' % lab); continue
    R = sorted([r for r in json.load(open(p)) if isinstance(r, dict) and r.get('t') is not None and isinstance(r.get('vb_ball_l'), list)], key=lambda r: f(r['t']))
    n = len(R); sel = ['SHM226' in str(r.get('av_Phase27_SelectedObject')) for r in R]
    floor = {}
    for s in ('l', 'r'):
        zs = sorted(r['vb_ball_' + s][2] for r in R); floor[s] = zs[n // 10] + 2.0
    spans = []; i = 0
    while i < n:
        if sel[i]:
            j = i
            while j + 1 < n and sel[j + 1]: j += 1
            spans.append((i, j)); i = j + 1
        else: i += 1
    def jumps(a, c):
        """max planted-ball per-frame displacement and max pelvis excess displacement over frames a..c (indices)"""
        jb = (0.0, None, None); jp = (0.0, None)
        for k in range(max(a, 1), min(c, n - 1) + 1):
            dt = f(R[k]['t']) - f(R[k - 1]['t'])
            if dt <= 0: continue
            for s in ('l', 'r'):
                q, pq = R[k]['vb_ball_' + s], R[k - 1]['vb_ball_' + s]
                if q[2] < floor[s] and pq[2] < floor[s]:
                    d = math.hypot(q[0] - pq[0], q[1] - pq[1])
                    if d > jb[0]: jb = (d, round(f(R[k]['t']), 3), s)
            pv, ppv = R[k]['vb_pelvis'], R[k - 1]['vb_pelvis']
            ex = math.hypot(pv[0] - ppv[0], pv[1] - ppv[1]) - f(R[k].get('Speed2D')) * dt
            if ex > jp[0]: jp = (ex, round(f(R[k]['t']), 3))
        return jb, jp
    if not spans: print('EXIT227 %-30s no SHM226 clip selected' % lab[-30:]); continue
    for (a, c) in spans:
        ta, tc = f(R[a]['t']), f(R[c]['t']); clip = str(R[c].get('av_Phase27_SelectedObject')); clip0 = str(R[a].get('av_Phase27_SelectedObject'))
        t_in, t_out = f(R[a].get('av_Phase27_SelectedTime')), f(R[c].get('av_Phase27_SelectedTime')); L = LENS.get(clip)
        rate = (t_out - t_in) / (tc - ta) if tc > ta else 0.0
        act = [k for k in range(a, c + 1) if b(R[k].get('av_SHM_RedirectActive'))]
        act_after = [k for k in range(c + 1, min(c + 40, n)) if b(R[k].get('av_SHM_RedirectActive'))]
        fpo = [k for k in range(max(a - 5, 0), min(c + 15, n)) if b(R[k].get('av_SHM_FootPlaceOff'))]
        rev = R[c].get('av_SHM227_Rev', R[c].get('ac_SHM226_Rev'))
        jb_in, jp_in = jumps(a, c)
        ex0 = next((k for k in range(a, n) if f(R[k]['t']) >= tc - 0.2), c); ex1 = next((k for k in range(c, n) if f(R[k]['t']) >= tc + 0.6), n - 1)
        jb_ex, jp_ex = jumps(ex0, ex1)
        nxt = R[c + 1] if c + 1 < n else {}
        sw = [(round(f(R[k]['t']), 2), str(R[k-1].get('av_Phase27_SelectedObject'))[-6:] + '>' + str(R[k].get('av_Phase27_SelectedObject'))[-6:], round(f(R[k-1].get('av_Phase27_SelectedTime')), 2), round(f(R[k].get('av_Phase27_SelectedTime')), 2)) for k in range(a + 1, c + 1) if str(R[k].get('av_Phase27_SelectedObject')) != str(R[k-1].get('av_Phase27_SelectedObject'))]
        print('EXIT227 %-30s clip %s%s in %.2f..%.2f (%.2f s) ct %.2f->%.2f len %s rem %s rate %.2f | episode %s%s | FPoff %s | planted jump in-clip %.1f cm (t %s %s) exit-win %.1f cm (t %s %s) | pelvis excess in %.1f exit %.1f | next %s @%.2f %s'
              % (lab[-30:], clip0.replace('SHM226_JogRev_', ''), ('->' + clip.replace('SHM226_JogRev_', '')) if clip != clip0 else '', ta, tc, tc - ta, t_in, t_out, ('%.2f' % L) if L else '?',
                 ('%.2f' % (L - t_out)) if L else '?', rate,
                 ('%.2f..%.2f' % (f(R[act[0]]['t']) - ta, f(R[act[-1]]['t']) - ta)) if act else 'none', (' +after %d fr' % len(act_after)) if act_after else '',
                 ('%.2f..%.2f' % (f(R[fpo[0]]['t']) - ta, f(R[fpo[-1]]['t']) - ta)) if fpo else 'none',
                 jb_in[0], jb_in[1], jb_in[2], jb_ex[0], jb_ex[1], jb_ex[2], jp_in[0], jp_ex[0],
                 str(nxt.get('av_Phase27_SelectedObject'))[-22:], f(nxt.get('av_Phase27_SelectedTime')), str(nxt.get('av_CurrentSelectedDatabase'))[-20:]) + ((' | SWITCH ' + str(sw)) if sw else ''))
