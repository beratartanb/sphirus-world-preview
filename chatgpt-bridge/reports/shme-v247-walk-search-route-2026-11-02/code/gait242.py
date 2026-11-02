"""gait242.py <label> [<label> ...] [--json out.json] : V2.42 locomotion-identity metrics from the harness LTP (visible MetaHuman body).
Per walking stage (stage name mv_walk_* with capsule speed > 40 cm/s for >= 1.2 s): cadence (steps/s), ground step length (cm, between
consecutive plant points of alternating feet), stride time, double-support fraction, stance/swing split, swing apex clearance (ball z above
the floor), pelvis lateral / vertical excursion (peak-to-peak, cm), pelvis-vs-chest yaw counter-rotation (deg p2p, thigh line vs clavicle
line), arm swing amplitude (hand forward excursion relative to the pelvis along the travel direction, cm p2p), head vertical bob (cm p2p),
capsule speed mean and the MM play rate (SelectedTime advance / wall time) + databases played.
Per stop (release -> next press): time to both feet still, pelvis settle time (|dz| < 0.3 cm/s^2 proxy: pelvis z velocity < 2 cm/s),
last-step length, capsule stop distance; per start: time to first ball lift, first-step length, time to 90 % of walk speed.
Definitions: low = ball z < 10th-percentile ball z + 3.5 cm; planted = low and ball speed < 30 cm/s (contact231 uses +2 cm / 25 cm/s; the
walk's heel-off phase keeps the ball low while the ankle rises, so the looser low band is needed to see double support)."""
import sys, os, math, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'SHME_V231_20261026'))
from ltp231 import load, short

def yaw_of(a, b): return math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
def wrap(d): return (d + 180.0) % 360.0 - 180.0
def p2p(xs): return (max(xs) - min(xs)) if xs else 0.0

def analyse(label):
    R = [r for r in load(label) if isinstance(r.get('vb_ball_l'), tuple) and isinstance(r.get('vb_pelvis'), tuple) and isinstance(r.get('ax'), tuple)]
    if len(R) < 10: return {'label': label, 'err': 'no rows'}
    out = {'label': label, 'rows': len(R), 'stages': {}, 'stops': [], 'starts': []}
    floor = {}
    for s in 'lr':
        zs = sorted(r['vb_ball_' + s][2] for r in R); floor[s] = zs[len(zs) // 10] + 3.5   # V2.42: 'low' = within 3.5 cm of the standing ball height (heel-off keeps the ball low)
    # per-frame foot state
    for i, r in enumerate(R):
        r['_t'] = r['t']; r['_v'] = r['Speed2D']
        for s in 'lr':
            b = r['vb_ball_' + s]; a = R[i - 1]['vb_ball_' + s] if i else b; dt = max(r['t'] - R[i - 1]['t'], 1e-3) if i else 1.0
            sp = math.hypot(b[0] - a[0], b[1] - a[1]) / dt
            r['_low' + s] = b[2] < floor[s]; r['_sp' + s] = sp; r['_pl' + s] = r['_low' + s] and sp < 30.0
    # plant episodes (planted runs)
    plants = {s: [] for s in 'lr'}
    for s in 'lr':
        i = 0
        while i < len(R):
            if R[i]['_pl' + s]:
                j = i
                while j + 1 < len(R) and R[j + 1]['_low' + s]: j += 1
                xy = [R[k]['vb_ball_' + s] for k in range(i, j + 1) if R[k]['_pl' + s]]
                cx = sum(p[0] for p in xy) / len(xy); cy = sum(p[1] for p in xy) / len(xy)
                plants[s].append({'t0': R[i]['t'], 't1': R[j]['t'], 'x': cx, 'y': cy, 'i0': i, 'i1': j}); i = j + 1
            else: i += 1
    # stages
    stages = []
    cur = None
    for i, r in enumerate(R):
        st = r.get('stage', '')
        if cur is None or st != cur['name']:
            cur = {'name': st, 'i0': i, 'i1': i}; stages.append(cur)
        cur['i1'] = i
    for sg in stages:
        rows = R[sg['i0']:sg['i1'] + 1]; T = rows[-1]['t'] - rows[0]['t']
        name = sg['name']
        if not name.startswith('mv_') or 'rel' in name or 'stop' in name: continue
        moving = [r for r in rows if r['_v'] > 40]
        if len(moving) < 36: continue
        t0, t1 = moving[0]['t'], moving[-1]['t']
        # alternating plant points inside the stage (skip the first/last partial)
        P = sorted([dict(p, s=s) for s in 'lr' for p in plants[s] if t0 + 0.3 <= p['t0'] <= t1 - 0.2], key=lambda p: p['t0'])
        steps = []
        for a, b in zip(P, P[1:]):
            if a['s'] != b['s']: steps.append({'len': math.hypot(b['x'] - a['x'], b['y'] - a['y']), 'dt': b['t0'] - a['t0'], 'ds': max(0.0, a['t1'] - b['t0'])})
        trav = (moving[-1]['ax'][0] - moving[0]['ax'][0], moving[-1]['ax'][1] - moving[0]['ax'][1]); tl = math.hypot(*trav) or 1.0; fwd = (trav[0] / tl, trav[1] / tl)
        pel = [r['vb_pelvis'] for r in moving]; lat = [(-fwd[1]) * p[0] + fwd[0] * p[1] for p in pel]; vert = [p[2] for p in pel]
        head = [r['vb_head'][2] for r in moving if isinstance(r.get('vb_head'), tuple)]
        # yaws: pelvis from thigh line, chest from clavicle line (vx_*)
        pyaw, cyaw = [], []
        for r in moving:
            if isinstance(r.get('vx_thigh_l'), tuple) and isinstance(r.get('vx_thigh_r'), tuple): pyaw.append(yaw_of(r['vx_thigh_r'], r['vx_thigh_l']))
            if isinstance(r.get('vx_clavicle_l'), tuple) and isinstance(r.get('vx_clavicle_r'), tuple): cyaw.append(yaw_of(r['vx_clavicle_r'], r['vx_clavicle_l']))
        counter = [wrap(c - p) for p, c in zip(pyaw, cyaw)] if pyaw and cyaw else []
        arms = {}
        for s in 'lr':
            hs = [r for r in moving if isinstance(r.get('vx_hand_' + s), tuple)]
            arms[s] = p2p([fwd[0] * (r['vx_hand_' + s][0] - r['vb_pelvis'][0]) + fwd[1] * (r['vx_hand_' + s][1] - r['vb_pelvis'][1]) for r in hs])
        apex = {s: p2p([r['vb_ball_' + s][2] for r in moving]) for s in 'lr'}
        # MM play rate + databases
        dbs = {}
        rate = []
        for a, b in zip(moving, moving[1:]):
            db = short(b.get('av_CurrentSelectedDatabase')); dbs[db] = dbs.get(db, 0) + 1
            try:
                if short(a.get('av_Phase27_SelectedObject')) == short(b.get('av_Phase27_SelectedObject')):
                    d = float(b['av_Phase27_SelectedTime']) - float(a['av_Phase27_SelectedTime']); w = b['t'] - a['t']
                    if 0 < d < 0.2 and w > 0: rate.append(d / w)
            except Exception: pass
        st = {'t': [round(t0, 2), round(t1, 2)], 'speed_mean': round(sum(r['_v'] for r in moving) / len(moving), 1), 'n_steps': len(steps)}
        if steps:
            st.update({'step_len_mean': round(sum(x['len'] for x in steps) / len(steps), 1), 'step_len_sd': round((sum((x['len'] - sum(y['len'] for y in steps) / len(steps)) ** 2 for x in steps) / len(steps)) ** 0.5, 1),
                       'cadence_steps_s': round(len(steps) / max(1e-3, P[-1]['t0'] - P[0]['t0']), 2) if len(P) > 1 else None,
                       'step_time_mean': round(sum(x['dt'] for x in steps) / len(steps), 3), 'double_support_frac': round(sum(x['ds'] for x in steps) / max(1e-3, sum(x['dt'] for x in steps)), 3)})
            st['step_from_speed'] = round(st['speed_mean'] * st['step_time_mean'], 1)
        st.update({'pelvis_lat_p2p': round(p2p(lat), 1), 'pelvis_vert_p2p': round(p2p(vert), 1), 'head_vert_p2p': round(p2p(head), 1), 'counter_rot_p2p_deg': round(p2p(counter), 1),
                   'pelvis_yaw_p2p_deg': round(p2p([wrap(y - pyaw[0]) for y in pyaw]), 1) if pyaw else None, 'arm_swing_p2p': {s: round(v, 1) for s, v in arms.items()},
                   'ball_lift_p2p': {s: round(v, 1) for s, v in apex.items()}, 'mm_rate_mean': round(sum(rate) / len(rate), 3) if rate else None, 'dbs': dbs})
        out['stages'][name] = st
    # stops: stage containing 'rel' (released) -> time to both feet still + pelvis settle; starts: stage after a rel
    for k, sg in enumerate(stages):
        name = sg['name']; rows = R[sg['i0']:sg['i1'] + 1]
        if 'rel' in name or name == 'mv_stop':
            tr = rows[0]['t']; v0 = rows[0]['_v']
            still = next((r['t'] for r in rows if r['_pll'] and r['_plr'] and r['_v'] < 5), None)
            vstop = next((r['t'] for r in rows if r['_v'] < 5), None)
            pz = [(r['t'], r['vb_pelvis'][2]) for r in rows]
            settle = None
            for (ta, za), (tb, zb) in zip(pz, pz[1:]):
                if tb - tr > 0.3 and abs(zb - za) / max(tb - ta, 1e-3) < 2.0 and (vstop is not None and tb >= vstop): settle = tb; break
            d = math.hypot(rows[-1]['ax'][0] - rows[0]['ax'][0], rows[-1]['ax'][1] - rows[0]['ax'][1])
            lastp = sorted([dict(p, s=s) for s in 'lr' for p in plants[s] if p['t0'] >= tr - 0.05 and p['t0'] <= rows[-1]['t']], key=lambda p: p['t0'])
            dbs = {}
            for r in rows: db = short(r.get('av_CurrentSelectedDatabase')); dbs[db] = dbs.get(db, 0) + 1
            out['stops'].append({'stage': name, 't_release': round(tr, 2), 'v_release': round(v0, 1), 'capsule_stop_s': round(vstop - tr, 2) if vstop else None, 'feet_still_s': round(still - tr, 2) if still else None,
                                 'pelvis_settle_s': round(settle - tr, 2) if settle else None, 'stop_dist_cm': round(d, 1), 'n_plants_after_release': len(lastp), 'dbs': dbs})
        elif k > 0 and ('rel' in stages[k - 1]['name']) and name.startswith('mv_'):
            tp = rows[0]['t']
            lift = next((r['t'] for r in rows if (not r['_lowl']) or (not r['_lowr'])), None)
            v90 = next((r['t'] for r in rows if r['_v'] >= 0.9 * 132.0), None)
            P = sorted([dict(p, s=s) for s in 'lr' for p in plants[s] if p['t0'] > tp], key=lambda p: p['t0'])
            first = math.hypot(P[1]['x'] - P[0]['x'], P[1]['y'] - P[0]['y']) if len(P) > 1 else None
            dbs = {}
            for r in rows[:45]: db = short(r.get('av_CurrentSelectedDatabase')); dbs[db] = dbs.get(db, 0) + 1
            out['starts'].append({'stage': name, 't_press': round(tp, 2), 'first_lift_s': round(lift - tp, 2) if lift else None, 't90_s': round(v90 - tp, 2) if v90 else None, 'first_step_cm': round(first, 1) if first else None, 'dbs': dbs})
    return out

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]; js = None
    if '--json' in sys.argv: js = sys.argv[sys.argv.index('--json') + 1]; args = [a for a in args if a != js]
    res = [analyse(a) for a in args]
    for r in res:
        print('== ' + r['label'])
        for k, v in r.get('stages', {}).items(): print('  ' + k, json.dumps(v))
        for v in r.get('stops', []): print('  STOP', json.dumps(v))
        for v in r.get('starts', []): print('  START', json.dumps(v))
    if js: json.dump(res, open(js, 'w'), indent=1)
