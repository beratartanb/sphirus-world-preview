"""step226.py: high-step landing read-out. For each step edge (x position, top height) of a course: the first plant of each foot ON the
platform - ball x minus the edge (how far onto the step), the estimated heel (ball - 16 cm along the travel), the lowest ball height over
the platform BEFORE that plant (negative = inside the step), the lift / shift at that moment, the pelvis z path across the step (max one-frame
change) and the capsule step-up frames. Usage: step226.py label edge_x:top_z[:dir] ... (dir +1 / -1 travel along x, default +1)"""
import json, sys, math, pathlib
E = pathlib.Path(__file__).resolve().parents[2] / 'Saved/Codex/SHME_V1_20260925/Evidence'
lab = sys.argv[1]
R = sorted([r for r in json.load(open(E / (lab + '.json'))) if isinstance(r, dict) and r.get('t') is not None and isinstance(r.get('ax'), list) and isinstance(r.get('vb_ball_l'), list)], key=lambda r: float(r['t']))
def C(r, s): return r.get('cv_Contact' + s.upper()) in (True, 'True', 1)
for spec in sys.argv[2:]:
    parts = spec.split(':'); ex = float(parts[0]); top = float(parts[1]); d = float(parts[2]) if len(parts) > 2 else 1.0
    print('STEP226 %s edge x %.0f top %.0f' % (lab[-30:], ex, top))
    # capsule crossing window: capsule within +-120 cm of the edge
    W = [r for r in R if abs(r['ax'][0] - ex) <= 150]
    if not W: print('   no frames near the edge'); continue
    capz = [r['ax'][2] for r in W]; pz = [r['vb_pelvis'][2] for r in W]
    rise = [(round(float(W[i]['t']), 2), round(capz[i] - capz[i - 1], 1)) for i in range(1, len(W)) if abs(capz[i] - capz[i - 1]) > 2.0]
    dpmax = max(abs(pz[i] - pz[i - 1]) for i in range(1, len(pz)))
    print('   capsule step frames %s | pelvis z %.1f..%.1f max|dz| %.1f/frame' % (rise[:8], min(pz), max(pz), dpmax))
    for s in ('l', 'r'):
        prev = False; plant = None; minz = None
        for r in W:
            b = r['vb_ball_' + s]; on_top = (b[0] - ex) * d > 0
            if on_top and not C(r, s) and (minz is None or b[2] < minz[0]): minz = (b[2], round(float(r['t']), 2))
            if C(r, s) and not prev and on_top: plant = r; break
            prev = C(r, s)
        if plant is None: print('   %s: no plant on the platform in the window' % s.upper()); continue
        b = plant['vb_ball_' + s]; onto = (b[0] - ex) * d; heel = onto - 16.0
        print('   %s plant t %.2f: ball %.1f cm onto the step (heel est. %.1f), ball z %.1f (top %.0f) | lowest swing ball over the platform before the plant %s | lift %.1f shift %.1f' % (
            s.upper(), float(plant['t']), onto, heel, b[2], top, ('%.1f at %.2f' % minz) if minz else '-', float(plant.get('cv_SwingLift' + s.upper()) or 0), float(plant.get('cv_SwingShiftT' + s.upper()) or 0)))
