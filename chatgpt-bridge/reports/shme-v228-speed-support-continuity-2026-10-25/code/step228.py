"""step228.py label edge_x:top_z[:dir] ...: high-step landing read-out with a proper floor reference. On flat ground the planted ball sits
BELOW z 0 (sole / ball offset, measured per run as the 10th percentile ball height before the first edge, typically -2.7 cm), so a correct
plant on a platform of height H has ball z = H + offset. Per edge and foot (first plant ON the platform): where the ball landed relative to
the edge (cm onto the step), the estimated heel (ball - 16 cm along the travel; negative = heel over the void), the plant height error
(ball z - (top + offset): + = standing on air / hovering, - = inside the surface), the HOVER time (frames the ball is above top + offset +
4 cm while horizontally over the platform, before the plant, with the foot nearly still), the lowest ball height over the platform before
the plant (penetration), the step length of the NEXT plant (other foot, cm) and the pelvis z path (max one-frame change) across the edge.
Also the capsule step-up frames (|dz| > 2 cm). Harness evidence JSON."""
import json, sys, math, pathlib
E = pathlib.Path(__file__).resolve().parents[2] / 'Saved/Codex/SHME_V1_20260925/Evidence'
lab = sys.argv[1]
R = sorted([r for r in json.load(open(E / (lab + '.json'))) if isinstance(r, dict) and r.get('t') is not None and isinstance(r.get('ax'), list) and isinstance(r.get('vb_ball_l'), list)], key=lambda r: float(r['t']))
n = len(R); T = [float(r['t']) for r in R]
def bz(k, s): return R[k]['vb_ball_' + s][2]
def bx(k, s): return R[k]['vb_ball_' + s][0]
def bspeed(k, s):
    if k == 0: return 0.0
    dt = T[k] - T[k - 1]; a, b = R[k]['vb_ball_' + s], R[k - 1]['vb_ball_' + s]
    return math.hypot(a[0] - b[0], a[1] - b[1]) / dt if dt > 0 else 0.0
specs = [(float(p.split(':')[0]), float(p.split(':')[1]), float(p.split(':')[2]) if len(p.split(':')) > 2 else 1.0) for p in sys.argv[2:]]
first_edge = min(s[0] for s in specs) if specs else 1e9
flat = sorted(bz(k, s) for k in range(n) for s in ('l', 'r') if (R[k]['ax'][0] - first_edge) * (specs[0][2] if specs else 1) < -150 and R[k]['ax'][0] > R[0]['ax'][0] + 100)
off = flat[len(flat) // 10] if flat else -2.7
print('STEP228 %s flat planted-ball offset %.1f cm (expected plant z = top %+.1f)' % (lab[-30:], off, off))
for ex, top, d in specs:
    print('  edge x %.0f top %.0f' % (ex, top))
    ks = [k for k in range(1, n) if (R[k]['ax'][0] - ex) * d > -60 and (R[k]['ax'][0] - ex) * d < 250]
    if not ks: print('    capsule never crossed'); continue
    k_cross = next((k for k in ks if (R[k]['ax'][0] - ex) * d >= 0), ks[0])
    cap = [(round(T[k], 2), round(R[k]['ax'][2] - R[k - 1]['ax'][2], 1)) for k in ks if abs(R[k]['ax'][2] - R[k - 1]['ax'][2]) > 2.0]
    pz = [R[k]['vb_pelvis'][2] for k in ks]; pdz = max(abs(R[k]['vb_pelvis'][2] - R[k - 1]['vb_pelvis'][2]) for k in ks)
    print('    capsule step frames %s | pelvis z %.1f..%.1f max|dz| %.1f/frame' % (cap[:6], min(pz), max(pz), pdz))
    plants = {}
    for s in ('l', 'r'):
        kp = None
        for k in ks:
            over = (bx(k, s) - ex) * d > 0.0
            if over and bz(k, s) < top + off + 2.5 and bspeed(k, s) < 60 and all(bspeed(j, s) < 60 and (bx(j, s) - ex) * d > 0 for j in range(k, min(k + 3, n))):
                kp = k; break
        if kp is None: print('    %s: no plant on the platform' % s.upper()); continue
        onto = (bx(kp, s) - ex) * d; heel = onto - 16.0
        err = bz(kp, s) - (top + off)
        pre = [k for k in ks if k < kp and (bx(k, s) - ex) * d > 0]
        hover = [k for k in pre if bz(k, s) > top + off + 4.0 and bspeed(k, s) < 120]
        hover_t = (T[hover[-1]] - T[hover[0]] + (T[1] - T[0])) if hover else 0.0
        lowest = min((bz(k, s) for k in pre), default=float('nan'))
        plants[s] = (kp, onto)
        print('    %s plant t %.2f: %.1f cm onto the step (heel %+.1f%s), z err %+.1f (ball %.1f) | hover %.2f s | lowest over platform before plant %.1f (%+.1f vs expected) | lift %s' % (
            s.upper(), T[kp], onto, heel, ' OVER THE VOID' if heel < 0 else '', err, bz(kp, s), hover_t, lowest, lowest - (top + off) if pre else float('nan'), str(R[kp].get('cv_SwingLift' + s.upper()))[:5]))
    if len(plants) == 2:
        (k1, o1), (k2, o2) = sorted(plants.values(), key=lambda x: x[0])
        print('    first plant -> next plant: %.2f s, %.1f cm apart (next foot lands %.1f cm onto the step)' % (T[k2] - T[k1], o2 - o1, o2))
