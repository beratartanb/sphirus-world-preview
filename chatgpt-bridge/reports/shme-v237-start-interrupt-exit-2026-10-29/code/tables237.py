"""tables237.py <out.md> : V2.37 final tables from the LTP side files of ONE build (promoted production o vs pre237 = every V2.37 group at
its V2.36 value). (1) worst planted-ball SLIP / DRAG (contact231) with its owner clip + the reversal hold, fixed 30; (2) whole-body stop audit
(stop236) + the BRAKE-WINDOW pelvis (release +0.15 .. +0.8 s; minimum of the visible pelvis above the root and the knee angle there - the
release frame itself carries the jog loop's own pelvis bob and is not the brake); (3) start / re-push clip episodes (clip rate, played span);
(4) frame-rate modes 60 / 120 / 20 / real; (5) cold first use in the clean editor. Missing runs print '-' (never counted as a pass); runs with
database-not-ready frames are marked '*'.
Build 2 (stop DB continuing bias -25): every run whose production run searched the stop DB was repeated under tag fin2 / g60 / g120 / g20 /
greal / cold2; L() takes that label when it exists, otherwise the first-build label (such runs never search the stop DB) marked +."""
import sys, os, math
H = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [H + '/../SHME_V231_20261026', H + '/../SHME_V236_20261028', H]
from ltp231 import load, short
from contact231 import classify
import stop236
def runs(lab):
    try: return load(lab)
    except Exception: return None
def worst(lab):
    R = runs(lab)
    if R is None: return None, ''
    eps = [e for e in classify(R) if e['cls'] in ('SLIP', 'DRAG')]
    if not eps: return 0.0, ''
    w = max(eps, key=lambda e: e['drift']); r = R[min(w.get('iw', w['i0']), len(R) - 1)]
    return w['drift'], short(r['av_Phase27_SelectedObject']).replace('SHM_JogQ_', '')[:30]
def nodb(lab):
    R = runs(lab); return sum(1 for r in R if r['t'] > 2.5 and str(r.get('av_CurrentSelectedDatabase')) == 'None') if R else 0
def hold(lab):
    R = runs(lab)
    if R is None: return None
    R = [r for r in R if r.get('stage') not in (None, '', 'yaw_hold')]; best = run = 0.0; prev = None
    for r in R:
        if prev is not None:
            dt = r['t'] - prev['t']
            vl = math.hypot(r['vb_ball_l'][0] - prev['vb_ball_l'][0], r['vb_ball_l'][1] - prev['vb_ball_l'][1]) / max(dt, 1e-3)
            vr = math.hypot(r['vb_ball_r'][0] - prev['vb_ball_r'][0], r['vb_ball_r'][1] - prev['vb_ball_r'][1]) / max(dt, 1e-3)
            if 'Rev' in str(r.get('av_Phase27_SelectedObject', '')) and vl < 60 and vr < 60 and (abs(r.get('lix', 0)) + abs(r.get('liy', 0))) > 0.1: run += dt; best = max(best, run)
            else: run = 0.0
        prev = r
    return best
def ang(a, b, c):
    u = [a[i] - b[i] for i in range(3)]; v = [c[i] - b[i] for i in range(3)]
    return math.degrees(math.acos(max(-1, min(1, sum(u[i] * v[i] for i in range(3)) / max(math.sqrt(sum(x * x for x in u)) * math.sqrt(sum(x * x for x in v)), 1e-6)))))
def brake_pelvis(lab, t_rel):
    R = runs(lab)
    if R is None: return None
    W = [r for r in R if t_rel + 0.15 <= r['t'] <= t_rel + 0.8]
    if not W: return None
    r = min(W, key=lambda r: r['vb_pelvis'][2] - r['mx_root'][2])
    kl, kr = ang(r['vx_thigh_l'], r['vx_calf_l'], r['vx_foot_l']), ang(r['vx_thigh_r'], r['vx_calf_r'], r['vx_foot_r'])
    knee = kl if r['vb_ball_l'][2] <= r['vb_ball_r'][2] else kr  # support leg (lower ball); the swing knee bends ~90 by design
    fpo = (r.get('ac_SHM_HCo_pelvis_TZ') or 0) - (r.get('ac_SHM_HCi_pelvis_TZ') or 0)
    return r['vb_pelvis'][2] - r['mx_root'][2], knee, fpo
def episodes(lab):
    R = runs(lab)
    if R is None: return '-'
    out = []; cur = None
    for i, r in enumerate(R):
        c = short(r['av_Phase27_SelectedObject'])
        if c.startswith(('SHM237_JogStart', 'SHM237_RePush', 'SHM236_JogStart')):
            if cur and cur[0] == c and i == cur[2] + 1: cur[2] = i
            else:
                if cur: out.append(cur)
                cur = [c, i, i]
    if cur: out.append(cur)
    t = []
    for c, a, b in out:
        dt = R[b]['t'] - R[a]['t']
        if dt <= 0.05: continue
        t.append('%s %.2f-%.2f r%.2f' % (c.replace('SHM237_', '').replace('SHM236_', '6:'), R[a]['av_Phase27_SelectedTime'], R[b]['av_Phase27_SelectedTime'], (R[b]['av_Phase27_SelectedTime'] - R[a]['av_Phase27_SelectedTime']) / dt))
    return '; '.join(t) or 'none'
NEW = {'fin': 'fin2', 'f60': 'g60', 'f120': 'g120', 'f20': 'g20', 'freal': 'greal', 'cold': 'cold2'}
def L(tag, s, v):
    a = 'v237%s_%s_%s_r1' % (NEW.get(tag, tag), s, v)
    return (a, '') if runs(a) is not None else ('v237%s_%s_%s_r1' % (tag, s, v), '+')
fmt = lambda x: '-' if x is None else '%.1f' % x
def cell(lab, mark=''):
    w, o = worst(lab); n = nodb(lab) if w is not None else 0
    return ('-' if w is None else '%.1f%s%s' % (w, '*' if n else '', mark)), o
out = ['## 1. Worst planted-ball slide / drag (cm, owner clip) and reversal hold (s), fixed 30 FPS: V2.37 production (o) vs pre237 (V2.36 values); + = first-build run (never searches the stop DB)', '',
       '| scenario | o | o owner | pre237 | pre237 owner | o hold | pre237 hold |', '|---|---|---|---|---|---|---|']
S30 = ['j36_stop', 'j36_stopb', 'j36_stopr', 'j36_rse', 'j36_rsm', 'j36_rsl', 'j36_rsx', 'j36_wjs', 'j36_wjsb', 'j36_sside', 'j35_rev', 'j35_rev2', 'j35_relstop',
       'j30_rel_3200', 'j30_rel_3450', 'j30_slow', 'j34_chain1', 'jstart', 'wstart', 'c29_combo', 'e29_chain', 'e29_load', 'jback', 'wdiag', 's29_swl12', 's34_straight', 'ter_drop_jog', 'map_r1']
for s in S30:
    (a, ma), (b, mb) = L('fin', s, 'o'), L('fin', s, 'pre237'); ca, oa = cell(a, ma); cb, ob = cell(b, mb); ha, hb = hold(a), hold(b)
    out.append('| %s | %s | %s | %s | %s | %s | %s |' % (s, ca, oa, cb, ob, '-' if ha is None else '%.2f' % ha, '-' if hb is None else '%.2f' % hb))
out += ['', '## 2. Whole-body stop audit (stop236, visible mesh) + brake-window pelvis, fixed 30', '',
        '| run | release s | arm swing kept | pull-back cm | trunk deg @0 / @+0.6 | pelvis dip vs final (incl. loop bob) | BRAKE pelvis min cm | support knee deg there | FootPlacement pelvis there cm | last landing s |',
        '|---|---|---|---|---|---|---|---|---|---|']
for s in ['j36_stop', 'j36_stopb', 'j36_stopr', 'j36_wjs', 'j36_wjsb']:
    for v in ('o', 'pre237'):
        lab = L('fin', s, v)[0]
        try:
            for o in stop236.audit(lab):
                bp = brake_pelvis(lab, o['t_release'])
                out.append('| %s %s | %s | %s | %s | %s / %s | %s | %s | %s | %s | %s |' % (s, v, o['t_release'], o['arm_pp'][2], o['back_cm'], o['trunk_deg'][0], o['trunk_deg'][1], o['pelvis_dip'],
                           fmt(bp[0]) if bp else '-', '%.0f' % bp[1] if bp else '-', fmt(bp[2]) if bp else '-', o['last_land']))
        except Exception as e: out.append('| %s %s | - | %s |||||||| ' % (s, v, str(e)[:40]))
out += ['', '## 3. Start / re-push clip episodes (clip time span, clip rate), fixed 30', '', '| run | episodes |', '|---|---|']
for s in ['j36_wjs', 'j34_chain1', 'j36_rsm', 'j36_rse', 'j36_rsl', 'j36_stopr', 'jstart']:
    for v in ('o', 'pre237'): out.append('| %s %s | %s |' % (s, v, episodes(L('fin', s, v)[0])))
SF = ['j36_stop', 'j36_stopr', 'j36_rsm', 'j36_wjs', 'j34_chain1', 'j35_rev', 'j30_rel_3450', 'jstart', 'c29_combo', 'e29_chain', 'e29_load', 'j36_sside']
out += ['', '## 4. Frame-rate modes: worst slide cm o / pre237 (reversal hold s o / pre237); * = database-not-ready frames in the run', '', '| scenario | 30 | 60 | 120 | 20 | real |', '|---|---|---|---|---|---|']
for s in SF:
    cells = []
    for tag in ('fin', 'f60', 'f120', 'f20', 'freal'):
        (a, ma), (b, mb) = L(tag, s, 'o'), L(tag, s, 'pre237'); ha, hb = hold(a), hold(b)
        cells.append('%s / %s (%s / %s)' % (cell(a, ma)[0], cell(b, mb)[0], '-' if ha is None else '%.2f' % ha, '-' if hb is None else '%.2f' % hb))
    out.append('| %s | %s |' % (s, ' | '.join(cells)))
out += ['', '## 5. Cold first use in the clean editor (no warm run): frames with no database + worst slide', '', '| run | no-DB frames | worst cm |', '|---|---|---|']
for s in ('j36_stop', 'j36_rsm', 'j36_wjs', 'j34_chain1', 'j35_rev'):
    lab = L('cold', s, 'o')[0]; R = runs(lab)
    out.append('| %s | %s | %s |' % (lab, '-' if R is None else nodb(lab), cell(lab)[0]))
open(sys.argv[1], 'w', encoding='utf8').write('\n'.join(out) + '\n'); print('\n'.join(out))
