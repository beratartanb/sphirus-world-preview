"""diag235.py <label> [t0 t1] [--every N] : V2.35 first-broken-frame inspector for one run (LTP side file).
Per frame, together: raw input (lix/liy), capsule speed + travel heading, body (mesh) yaw, family / redirect state, MM database + selected
clip + clip time and its advance rate (clip s per world s), contacts + support side, visible-body pelvis speed and offset from the capsule,
pose speed (mean speed of hands / feet / head RELATIVE to the visible pelvis, cm/s) and the visible ball speeds.
Flags: FRZ = pose speed < 30 cm/s while an input is held and the capsule moves or the request opposes the travel; CLK = clip time advance
< 0.3x (clock held / slowed) or a jump (> 2.5x / backwards = re-selection); SEL = clip changed.
Summary (--sum): freeze episodes (>= 0.2 s) with their clip, family and the cause class (A clock / B same-pose / C family / D body)."""
import sys, os, math
H = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [H + '/../SHME_V231_20261026']
from ltp231 import load
def v3(r, k):
    v = r.get(k); return v if isinstance(v, tuple) else None
def sub(a, b): return (a[0] - b[0], a[1] - b[1], a[2] - b[2])
def n2(a): return math.hypot(a[0], a[1])
J = ['vx_hand_l', 'vx_hand_r', 'vx_foot_l', 'vx_foot_r', 'vb_head']
def frames(label, stage_filter=True):
    R = load(label)
    R = [r for r in R if r.get('stage') not in (None, '', 'yaw_hold') or not stage_filter]
    R.sort(key=lambda r: r['t'])
    out = []; prev = None
    for r in R:
        f = {'t': r['t'], 'lix': r.get('lix', 0.0), 'liy': r.get('liy', 0.0), 'stage': r.get('stage')}
        f['fam'] = r.get('cv_Family'); f['red'] = r.get('cv_RedirectActive'); f['rcls'] = r.get('cv_RedirectClass')
        f['db'] = str(r.get('av_CurrentSelectedDatabase', '')).replace('PSD_', '')[:26]; f['clip'] = str(r.get('av_Phase27_SelectedObject', ''))[:34]
        f['ct'] = r.get('av_Phase27_SelectedTime'); f['cl'] = r.get('cv_ContactL'); f['cr'] = r.get('cv_ContactR'); f['sup'] = r.get('cv_SupportSide')
        f['yaw'] = r.get('my'); a = v3(r, 'ax'); f['a'] = a; f['pel'] = v3(r, 'vb_pelvis'); f['j'] = [v3(r, k) for k in J]
        f['bl'] = v3(r, 'vb_ball_l'); f['br'] = v3(r, 'vb_ball_r'); f['speed'] = r.get('Speed2D', 0.0)
        if prev and f['t'] > prev['t']:
            dt = f['t'] - prev['t']; f['dt'] = dt
            va = sub(a, prev['a']) if a and prev['a'] else (0, 0, 0)
            f['head'] = math.degrees(math.atan2(va[1], va[0])) if n2(va) / dt > 5 else None
            f['vpel'] = n2(sub(f['pel'], prev['pel'])) / dt if f['pel'] and prev['pel'] else 0.0
            ps = []
            for j0, j1 in zip(prev['j'], f['j']):
                if j0 and j1 and f['pel'] and prev['pel']: ps.append(n2(sub(sub(j1, f['pel']), sub(j0, prev['pel']))) / dt + 0 * abs(((j1[2] - f['pel'][2]) - (j0[2] - prev['pel'][2])) / dt))
            f['pose'] = sum(ps) / len(ps) if ps else 0.0
            f['vbl'] = n2(sub(f['bl'], prev['bl'])) / dt if f['bl'] and prev['bl'] else 0.0
            f['vbr'] = n2(sub(f['br'], prev['br'])) / dt if f['br'] and prev['br'] else 0.0
            f['sel'] = f['clip'] != prev['clip']
            f['rate'] = ((f['ct'] - prev['ct']) / dt) if (not f['sel'] and isinstance(f['ct'], float) and isinstance(prev['ct'], float)) else None
            f['off'] = n2(sub(f['pel'], a)) if f['pel'] and a else 0.0
        else:
            f.update(dt=0, head=None, vpel=0, pose=0, vbl=0, vbr=0, sel=False, rate=None, off=0)
        held = abs(f['lix']) + abs(f['liy']) > 0.1
        f['frz'] = held and f['pose'] < 30.0 and f['dt'] > 0
        f['clk'] = f['rate'] is not None and (f['rate'] < 0.3 or f['rate'] > 2.5)
        out.append(f); prev = f
    return out
def row(f):
    fl = ('FRZ ' if f['frz'] else '') + ('CLK ' if f['clk'] else '') + ('SEL' if f['sel'] else '')
    hd = '%5.0f' % f['head'] if f['head'] is not None else '    -'
    rt = '%4.2f' % f['rate'] if f['rate'] is not None else '   -'
    return ('%6.3f in(%+.0f,%+.0f) v%4.0f hd%s yaw%5.0f fam%s red%s %-22s %-30s ct%5.2f r%s L%d R%d sup%+.0f pel%4.0f off%4.1f pose%4.0f bl%4.0f br%4.0f %s'
            % (f['t'], f['lix'], f['liy'], f['speed'], hd, f['yaw'] or 0, str(f['fam'])[:3], str(f['red'])[:1], f['db'], f['clip'],
               f['ct'] if isinstance(f['ct'], float) else -1, rt, bool(f['cl']), bool(f['cr']), f['sup'] or 0, f['vpel'], f['off'], f['pose'], f['vbl'], f['vbr'], fl))
def episodes(F, min_len=0.2):
    eps = []; cur = None
    for f in F:
        if f['frz']:
            if cur is None: cur = {'t0': f['t'], 'rows': []}
            cur['rows'].append(f); cur['t1'] = f['t']
        else:
            if cur and cur['t1'] - cur['t0'] >= min_len: eps.append(cur)
            cur = None
    if cur and cur['t1'] - cur['t0'] >= min_len: eps.append(cur)
    for e in eps:
        rs = e['rows']; clips = sorted(set(r['clip'] for r in rs)); rates = [r['rate'] for r in rs if r['rate'] is not None]
        sel = sum(r['sel'] for r in rs); fams = sorted(set(str(r['fam']) for r in rs))
        mr = sum(rates) / len(rates) if rates else None
        if mr is not None and mr < 0.3: c = 'A clock held'
        elif sel >= 2: c = 'A/B re-selection'
        elif mr is not None and mr > 0.6: c = 'B/D clip advances, pose static'
        else: c = '?'
        e.update(clips=clips, mrate=mr, sel=sel, fams=fams, cls=c, vmin=min(r['speed'] for r in rs), vmax=max(r['speed'] for r in rs))
    return eps
if __name__ == '__main__':
    a = sys.argv[1:]; lab = a[0]; F = frames(lab)
    if '--sum' in a:
        for e in episodes(F):
            print('FRZ %.2f-%.2f (%.2f s) v %.0f..%.0f fam %s clip-rate %s sel %d cls %s clips %s' % (e['t0'], e['t1'], e['t1'] - e['t0'], e['vmin'], e['vmax'], e['fams'],
                  '%.2f' % e['mrate'] if e['mrate'] is not None else '-', e['sel'], e['cls'], e['clips']))
        sys.exit()
    t0 = float(a[1]) if len(a) > 1 else -1e9; t1 = float(a[2]) if len(a) > 2 else 1e9
    ev = int(a[a.index('--every') + 1]) if '--every' in a else 1
    for i, f in enumerate(F):
        if t0 <= f['t'] <= t1 and (i % ev == 0 or f['frz'] or f['sel']): print(row(f))
