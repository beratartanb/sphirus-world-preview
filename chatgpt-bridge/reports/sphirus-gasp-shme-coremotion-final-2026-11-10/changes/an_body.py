# an_body.py <rec.json> [...]: per-segment locomotion + visible-body metrics from vid.py telemetry (rows with 'ub').
#  speed (mean/max), stop time & distance after release, selected-anim runs (GASP 'gasp' field, else 'cc' clip id),
#  re-selections per second, and upper-body numbers on the visible MetaHuman:
#   shoulderDrop = neck_01.z - mean(upperarm_l.z, upperarm_r.z)   (cm; larger = shoulders sit lower under the neck)
#   clavSwing    = p95-p5 of left-minus-right shoulder elevation over the clavicle root ((upperarm-clavicle).z) (cm)
#   twist        = p95-p5 of horizontal angle between shoulder line (upperarm_l->r) and hip line (thigh_l->r) (deg)
#   armSwing     = p95-p5 of forward offset of the hands from the pelvis in the capsule frame (cm)
#   headBob      = p95-p5 of head.z - capsule z (cm)
#   headX        = screen X of the head (min/mean/max)
import json, sys, math
def wrap(a):
    while a > 180: a -= 360
    while a < -180: a += 360
    return a
def pct(v, p):
    v = sorted(v); return v[min(len(v) - 1, max(0, int(round(p * (len(v) - 1)))))] if v else float('nan')
def rng(v): return pct(v, .95) - pct(v, .05) if v else float('nan')
for fn in sys.argv[1:]:
    d = json.load(open(fn)); R = d['rows']; plan = d['plan']; print('==', fn.replace('\\', '/').split('/')[-1], len(R), 'rows')
    for s in sorted(set(r['s'] for r in R)):
        rows = [r for r in R if r['s'] == s]; key = plan[s][0] or 'release'
        sp = [math.hypot(r['vx'], r['vy']) for r in rows]; t = 0.0; stop_t = None; dist = 0.0
        for r, v in zip(rows, sp):
            if stop_t is None and v < 5: stop_t = t
            if stop_t is None: dist += v * r['gdt']
            t += r['gdt']
        sel = []; nsw = 0
        for r in rows:
            g = r.get('gasp'); a = g[0] if g else (('clip%s' % r['cc'][0]) if r.get('cc') else None)
            if not sel or sel[-1][0] != a: sel.append([a, 0.0]); nsw += 1 if len(sel) > 1 else 0
            sel[-1][1] += r['gdt']
        ub = [r['ub'] for r in rows if isinstance(r.get('ub'), dict)]
        txt = '  seg %2d %-14s %4.1fs spd %3.0f/%3.0f' % (s, key, t, sum(sp) / len(sp), max(sp))
        if key == 'release' and sp[0] > 30: txt += ' | stop %s s %.0f cm' % ('%.2f' % stop_t if stop_t is not None else '>seg', dist)
        if ub:
            sd = [b['neck_01'][2] - 0.5 * (b['upperarm_l'][2] + b['upperarm_r'][2]) for b in ub]
            cs = [(b['upperarm_l'][2] - b['clavicle_l'][2]) - (b['upperarm_r'][2] - b['clavicle_r'][2]) for b in ub]
            tw = [wrap(math.degrees(math.atan2(b['upperarm_r'][1] - b['upperarm_l'][1], b['upperarm_r'][0] - b['upperarm_l'][0]) - math.atan2(b['thigh_r'][1] - b['thigh_l'][1], b['thigh_r'][0] - b['thigh_l'][0]))) for b in ub if 'thigh_r' in b]
            hb = [b['head'][2] - r['z'] for r, b in zip([r for r in rows if isinstance(r.get('ub'), dict)], ub)]
            arm = []
            for r, b in zip([r for r in rows if isinstance(r.get('ub'), dict)], ub):
                yw = math.radians(r['yaw']); fx, fy = math.cos(yw), math.sin(yw)
                vl = r.get('v_hand_l'); vr = r.get('v_hand_r'); pv = b['pelvis']
                if vl and vr: arm.append(((vl[0] - pv[0]) * fx + (vl[1] - pv[1]) * fy) - ((vr[0] - pv[0]) * fx + (vr[1] - pv[1]) * fy))
            txt += ' | shoulderDrop %.1f clavSwing %.1f twist %.1f armSwing %.0f headBob %.1f' % (sum(sd) / len(sd), rng(cs), rng(tw), rng(arm), rng(hb))
        ud = [r['ud'] for r in rows if isinstance(r.get('ud'), dict)]
        if ud:
            dsd = [b['neck_01'][2] - 0.5 * (b['upperarm_l'][2] + b['upperarm_r'][2]) for b in ud]
            dcs = [(b['upperarm_l'][2] - b['clavicle_l'][2]) - (b['upperarm_r'][2] - b['clavicle_r'][2]) for b in ud]
            dtw = [wrap(math.degrees(math.atan2(b['upperarm_r'][1] - b['upperarm_l'][1], b['upperarm_r'][0] - b['upperarm_l'][0]) - math.atan2(b['thigh_r'][1] - b['thigh_l'][1], b['thigh_r'][0] - b['thigh_l'][0]))) for b in ud]
            txt += ' | DRV drop %.1f clav %.1f twist %.1f' % (sum(dsd) / len(dsd), rng(dcs), rng(dtw))
        hx = [r['scr']['head'][0] for r in rows if isinstance(r.get('scr'), dict)]
        if hx: txt += ' | headX %.2f/%.2f/%.2f' % (min(hx), sum(hx) / len(hx), max(hx))
        print(txt)
        print('      sel %d sw (%.1f/s): %s' % (nsw, nsw / max(t, .1), ' > '.join('%s %.2f' % (str(a).replace('M_Neutral_', '').replace('M_Relaxed_', 'Rx_')[:34], dd) for a, dd in sel[:14])))
