"""posture226.py: reversal performance read-out at EVENT phases (not frame numbers): per run, the window between the request (speed starts
falling) and the exit (speed back above 90 % of the exit speed) - pelvis height vs capsule (crouch), knee bend (thigh/calf axes), trunk lean
(pelvis->spine_03 from vertical), elbow-hand reach (upperarm->hand distance) and head pitch (spine_03->head from vertical); min/max/mean
inside the window plus the values at the zero crossing and at the exit. Usage: posture226.py label t0 t1 [label t0 t1 ...]"""
import json, sys, math, pathlib
E = pathlib.Path(__file__).resolve().parents[2] / 'Saved/Codex/SHME_V1_20260925/Evidence'
def ang(a, b): return math.degrees(math.acos(max(-1.0, min(1.0, sum(a[i] * b[i] for i in range(3))))))
a = sys.argv[1:]
for i in range(0, len(a), 3):
    lab, t0, t1 = a[i], float(a[i + 1]), float(a[i + 2])
    R = sorted([r for r in json.load(open(E / (lab + '.json'))) if isinstance(r, dict) and r.get('t') is not None and isinstance(r.get('ax'), list) and isinstance(r.get('vb_pelvis'), list)], key=lambda r: float(r['t']))
    W = [r for r in R if t0 <= float(r['t']) <= t1]
    if len(W) < 4: print('POSTURE226 %s: no frames' % lab); continue
    vx = [(W[k]['ax'][0] - W[k - 1]['ax'][0]) / max(float(W[k]['t']) - float(W[k - 1]['t']), 1e-3) for k in range(1, len(W))]
    v0 = vx[0]; z = next((k for k in range(1, len(vx)) if vx[k] * v0 <= 0), None); vend = vx[-1]
    ex = next((k for k in range((z or 0), len(vx)) if abs(vx[k]) >= 0.9 * abs(vend)), len(vx) - 1)
    rows = []
    for r in W:
        pz = r['vb_pelvis'][2] - r['ax'][2]; kl = ang(r['vax_thigh_l'], r['vax_calf_l']); kr = ang(r['vax_thigh_r'], r['vax_calf_r'])
        ch = r['vb_chest']; pe = r['vb_pelvis']; lean = math.degrees(math.atan2(math.hypot(ch[0] - pe[0], ch[1] - pe[1]), ch[2] - pe[2]))
        hd = r.get('vb_head'); hp = math.degrees(math.atan2(math.hypot(hd[0] - ch[0], hd[1] - ch[1]), hd[2] - ch[2])) if hd else 0.0
        reach = []
        for sd in ('l', 'r'):
            h = r.get('vx_hand_' + sd); u_ = r.get('vx_upperarm_' + sd)
            if h and u_: reach.append(math.dist(h, u_))
        rows.append((pz, max(kl, kr), lean, hp, (sum(reach) / len(reach)) if reach else 0.0))
    def col(j): return [x[j] for x in rows]
    def stat(j): c = col(j); return '%5.1f/%5.1f/%5.1f' % (min(c), sum(c) / len(c), max(c))
    print('POSTURE226 %-30s win %.2f..%.2f zero %s exit %s | pelvis-cap min/mean/max %s | knee max %s | lean %s | head %s | reach %s | at zero: pel %.1f knee %.0f lean %.1f | at exit: pel %.1f knee %.0f lean %.1f' % (
        lab[-30:], t0, t1, ('%.2f' % float(W[z]['t'])) if z else '-', '%.2f' % float(W[ex]['t']), stat(0), stat(1), stat(2), stat(3), stat(4),
        rows[z][0] if z else 0, rows[z][1] if z else 0, rows[z][2] if z else 0, rows[ex][0], rows[ex][1], rows[ex][2]))
