"""balance238.py <label> [--t0 s] [--win 1.6] [--dt 0.0333] [--json]
V2.38 offline balance read of ONE run, from the same LTP frames the game logged (no second simulation):
- intent: the input vector (lix/liy) and the event = first frame the input direction changes by > 30 deg (or --t0);
- capsule: position ax, velocity / heading / acceleration (finite differences, 3-frame mean);
- centre of mass: Dempster/Winter segment fractions on the VISIBLE mesh points (vb_*/vx_*) - an approximation (no arms' mass
  distribution, rigid segments, MetaHuman proportions assumed adult-female-average);
- XCoM (extrapolated centre of mass, Hof 2005) = CoM_xy + v_CoM,xy / w, w = sqrt(g / h_CoM) - the linear-inverted-pendulum
  capture point; level ground assumed;
- support: per foot, planted when the visible ball is within 3 cm of its run floor and moves < 40 cm/s; base of support = the
  planted heel(foot)-ball segments inflated by 5 cm;
- per contact after the event: touchdown time, placement relative to CoM along the OLD travel and toward the NEW direction,
  capsule velocity change during that stance (the impulse the contact delivered), stance length;
- body: pelvis yaw (thigh line), chest yaw (clavicle line), head yaw (calibrated head axis), all relative to the capsule heading
  before the event; pelvis-chest separation; hand speed; clip and database per frame.
The physics here explains a decision; it does not claim measured forces."""
import sys, os, math, json, argparse
H = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [H + '/../SHME_V231_20261026', H]
from ltp231 import load, short
G = 980.0
SEG = [  # (name, mass fraction, proximal key, distal key, COM ratio from proximal) - Winter 2009 Table 4.1 (Dempster)
    ('head', 0.081, 'vb_head', 'vb_head', 0.0), ('trunk', 0.497, 'vb_pelvis', 'vx_neck_01', 0.5),
    ('uarm_l', 0.028, 'vx_upperarm_l', 'vx_lowerarm_l', 0.436), ('uarm_r', 0.028, 'vx_upperarm_r', 'vx_lowerarm_r', 0.436),
    ('farm_l', 0.022, 'vx_lowerarm_l', 'vx_hand_l', 0.682), ('farm_r', 0.022, 'vx_lowerarm_r', 'vx_hand_r', 0.682),
    ('thigh_l', 0.100, 'vx_thigh_l', 'vx_calf_l', 0.433), ('thigh_r', 0.100, 'vx_thigh_r', 'vx_calf_r', 0.433),
    ('leg_l', 0.0465, 'vx_calf_l', 'vx_foot_l', 0.433), ('leg_r', 0.0465, 'vx_calf_r', 'vx_foot_r', 0.433),
    ('foot_l', 0.0145, 'vx_foot_l', 'vb_ball_l', 0.5), ('foot_r', 0.0145, 'vx_foot_r', 'vb_ball_r', 0.5)]
def wrap(a): return (a + 180.0) % 360.0 - 180.0
def hyaw(v): return math.degrees(math.atan2(v[1], v[0]))
def com(r):
    s = [0.0, 0.0, 0.0]; m = 0.0
    for _, f, p, d, k in SEG:
        a, b = r.get(p), r.get(d)
        if not (isinstance(a, tuple) and isinstance(b, tuple)): return None
        for i in range(3): s[i] += f * (a[i] + k * (b[i] - a[i]))
        m += f
    return tuple(x / m for x in s)
def body_yaws(r):
    tl, tr = r['vx_thigh_l'], r['vx_thigh_r']; cl, cr = r['vx_clavicle_l'], r['vx_clavicle_r']
    py = hyaw((tr[1] - tl[1], -(tr[0] - tl[0]))); cy = hyaw((cr[1] - cl[1], -(cr[0] - cl[0])))
    hx = r.get('vaz_head'); hy = hyaw(hx) if isinstance(hx, tuple) and math.hypot(hx[0], hx[1]) > 0.2 else None
    return py, cy, hy
def seg_dist(p, a, b):
    ax, ay = b[0] - a[0], b[1] - a[1]; L = ax * ax + ay * ay
    t = 0.0 if L < 1e-6 else max(0.0, min(1.0, ((p[0] - a[0]) * ax + (p[1] - a[1]) * ay) / L))
    return math.hypot(p[0] - a[0] - t * ax, p[1] - a[1] - t * ay)
def analyse(lab, t0=None, win=1.6, pre=0.4):
    R = [r for r in load(lab) if isinstance(r.get('ax'), tuple) and isinstance(r.get('vb_ball_l'), tuple)]
    n = len(R)
    # input event
    if t0 is None:
        prev = None
        for r in R:
            lx, ly = r.get('lix', 0.0) or 0.0, r.get('liy', 0.0) or 0.0
            if math.hypot(lx, ly) < 0.5: continue
            d = hyaw((lx, ly))
            if prev is not None and abs(wrap(d - prev)) > 30.0 and r['t'] > 2.5: t0 = r['t']; break
            prev = d
    if t0 is None: return {'label': lab, 'error': 'no input direction change'}
    # derived per frame
    C = [com(r) for r in R]
    floor = {s: sorted(r['vb_ball_' + s][2] for r in R)[n // 20] for s in 'lr'}
    out = []
    for i, r in enumerate(R):
        a, b = max(i - 1, 0), min(i + 1, n - 1); dt = max(R[b]['t'] - R[a]['t'], 1e-3)
        v = ((R[b]['ax'][0] - R[a]['ax'][0]) / dt, (R[b]['ax'][1] - R[a]['ax'][1]) / dt)
        vc = None if C[a] is None or C[b] is None else ((C[b][0] - C[a][0]) / dt, (C[b][1] - C[a][1]) / dt)
        sup = {}
        for s in 'lr':
            pb, pa = R[b]['vb_ball_' + s], R[a]['vb_ball_' + s]
            sp = math.hypot(pb[0] - pa[0], pb[1] - pa[1]) / dt
            sup[s] = r['vb_ball_' + s][2] < floor[s] + 3.0 and sp < 40.0
        out.append({'t': r['t'], 'v': v, 'vc': vc, 'sup': sup})
    for i, o in enumerate(out):   # acceleration of the capsule (3-frame central difference on the velocity)
        a, b = max(i - 2, 0), min(i + 2, n - 1); dt = max(out[b]['t'] - out[a]['t'], 1e-3)
        o['acc'] = ((out[b]['v'][0] - out[a]['v'][0]) / dt, (out[b]['v'][1] - out[a]['v'][1]) / dt)
    i0 = next(i for i, o in enumerate(out) if o['t'] >= t0)
    # reference heading = capsule velocity heading over the 0.3 s before the event; new heading = the input direction after it
    ref = [o for o in out if t0 - 0.35 <= o['t'] < t0 - 0.05]
    vref = (sum(o['v'][0] for o in ref) / len(ref), sum(o['v'][1] for o in ref) / len(ref)); h0 = hyaw(vref); v0 = math.hypot(*vref)
    r1 = R[min(i0 + 3, n - 1)]; hin = hyaw((r1.get('lix', 0.0), r1.get('liy', 0.0)))
    # the input frame is camera relative: the requested WORLD heading is the capsule heading the run settles on (last 0.3 s of the window)
    late = [o for o in out if t0 + win - 0.3 <= o['t'] <= t0 + win]
    vl = (sum(o['v'][0] for o in late) / max(len(late), 1), sum(o['v'][1] for o in late) / max(len(late), 1))
    h1 = hyaw(vl) if math.hypot(*vl) > 30 else None
    turn = wrap(h1 - h0) if h1 is not None else None
    # yaw offsets: the body lines vs the travel heading in steady motion before the event
    cal = [body_yaws(R[i]) for i, o in enumerate(out) if t0 - 0.9 <= o['t'] < t0 - 0.1]
    def mean_ang(xs): xs = [x for x in xs if x is not None]; return hyaw((sum(math.cos(math.radians(x)) for x in xs), sum(math.sin(math.radians(x)) for x in xs))) if xs else 0.0
    offp = wrap(mean_ang([c[0] for c in cal]) - h0); offc = wrap(mean_ang([c[1] for c in cal]) - h0); offh = wrap(mean_ang([c[2] for c in cal]) - h0)
    ux = (math.cos(math.radians(h0)), math.sin(math.radians(h0))); uy = (-ux[1], ux[0])   # old travel, its left-hand normal (UE: +y right)
    rows = []; contacts = []; prev = {'l': out[i0 - 1]['sup']['l'], 'r': out[i0 - 1]['sup']['r']}
    amax = 0.0; t80 = None; sepmax = 0.0; sep_t = None
    for i in range(max(i0 - int(pre / 0.0333), 0), n):
        o = out[i]; r = R[i]
        if o['t'] > t0 + win: break
        c = C[i]
        if c is None: continue
        h = c[2] - (r['ax'][2] - 88.0); w = math.sqrt(G / max(h, 30.0))
        vc = o['vc'] or o['v']; xc = (c[0] + vc[0] / w, c[1] + vc[1] / w)
        planted = [s for s in 'lr' if o['sup'][s]]
        bos = min((seg_dist(xc, r['vx_foot_' + s], r['vb_ball_' + s]) for s in planted), default=None)
        py, cy, hy = body_yaws(r)
        rel = lambda y, off: None if y is None else wrap(y - off - h0)
        pr, cr, hr = rel(py, offp), rel(cy, offc), rel(hy, offh)
        vh = hyaw(o['v']) if math.hypot(*o['v']) > 20 else None
        acc = math.hypot(*o['acc']); amax = max(amax, acc) if o['t'] >= t0 else amax
        if t80 is None and turn is not None and vh is not None and o['t'] >= t0 and abs(wrap(vh - h0)) >= 0.8 * abs(turn): t80 = o['t'] - t0
        if pr is not None and cr is not None and o['t'] >= t0:
            s = wrap(cr - pr)
            if abs(s) > abs(sepmax): sepmax = s; sep_t = o['t'] - t0
        for s in 'lr':
            if o['t'] >= t0 and o['sup'][s] and not prev[s]:
                d = (r['vb_ball_' + s][0] - c[0], r['vb_ball_' + s][1] - c[1])
                contacts.append({'foot': s.upper(), 't': round(o['t'] - t0, 3), 'i': i, 'along_cm': round(d[0] * ux[0] + d[1] * ux[1], 1),
                                 'side_cm': round(d[0] * uy[0] + d[1] * uy[1], 1), 'clip': short(r.get('av_Phase27_SelectedObject'))[:34]})
            prev[s] = o['sup'][s]
        rows.append({'t': round(o['t'] - t0, 3), 'spd': round(math.hypot(*o['v'])), 'hd': None if vh is None else round(wrap(vh - h0)),
                     'acc': round(acc), 'comz': round(h, 1), 'xcom_bos': None if bos is None else round(bos, 1),
                     'sup': ''.join(s.upper() for s in planted) or '-', 'pel': None if pr is None else round(pr), 'chest': None if cr is None else round(cr),
                     'head': None if hr is None else round(hr), 'sep': None if pr is None or cr is None else round(wrap(cr - pr)),
                     'hands': round(math.hypot(r['vx_hand_l'][0] - r['vx_hand_r'][0], r['vx_hand_l'][1] - r['vx_hand_r'][1])),
                     'clip': short(r.get('av_Phase27_SelectedObject'))[:30], 'ct': round(r.get('av_Phase27_SelectedTime') or 0.0, 2),
                     'cap_err': r.get('cv_CaptureError'), 'rec': r.get('cv_RecoveryDemand'), 'rdem': r.get('cv_RedirectionDemand')})
    # stance impulse: capsule velocity change between touchdown and the next touchdown of any foot
    for k, ct in enumerate(contacts):
        j = contacts[k + 1]['i'] if k + 1 < len(contacts) else min(ct['i'] + 8, n - 1)
        dv = (out[j]['v'][0] - out[ct['i']]['v'][0], out[j]['v'][1] - out[ct['i']]['v'][1])
        ct['dv_cm_s'] = round(math.hypot(*dv)); ct['dv_against_old'] = round(-(dv[0] * ux[0] + dv[1] * ux[1]))
        ct['stance_s'] = round(out[j]['t'] - out[ct['i']]['t'], 3); del ct['i']
    return {'label': lab, 't0': t0, 'v0': round(v0), 'turn_deg': None if turn is None else round(turn), 'input_deg': round(wrap(hin)),
            't80_s': None if t80 is None else round(t80, 3), 'acc_max': round(amax), 'mu_eff': round(amax / G, 2),
            'pelvis_chest_sep_max': round(sepmax), 'sep_t': sep_t and round(sep_t, 2), 'contacts': contacts, 'rows': rows}
if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('label'); ap.add_argument('--t0', type=float); ap.add_argument('--win', type=float, default=1.6)
    ap.add_argument('--json', action='store_true'); ap.add_argument('--every', type=int, default=2)
    a = ap.parse_args(); res = analyse(a.label, a.t0, a.win)
    if a.json: print(json.dumps(res)); sys.exit(0)
    if 'error' in res: print(res); sys.exit(1)
    print('BAL238 %s t0 %.2f v0 %d turn %s t80 %s acc_max %d (mu_eff %.2f) pelvis-chest max %s at %s' % (res['label'], res['t0'], res['v0'], res['turn_deg'], res['t80_s'], res['acc_max'], res['mu_eff'], res['pelvis_chest_sep_max'], res['sep_t']))
    for c in res['contacts']: print('  contact', c)
    print('   t   spd  hd  acc  comz xcom-bos sup pel chest head sep hands clip')
    for x in res['rows'][::a.every]:
        print('%6.2f %4d %4s %5d %5.1f %6s %3s %4s %4s %4s %4s %4d %s@%.2f' % (x['t'], x['spd'], x['hd'], x['acc'], x['comz'], x['xcom_bos'], x['sup'], x['pel'], x['chest'], x['head'], x['sep'], x['hands'], x['clip'], x['ct']))
