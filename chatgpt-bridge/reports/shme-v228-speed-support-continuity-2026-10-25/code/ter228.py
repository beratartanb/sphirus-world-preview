"""ter228.py label edge_x [dir] [span_before] [span_after]: per-frame terrain trace around a step edge: capsule x (rel. edge) and z, both balls
(x rel. edge, z), the swing lift / ground / path-max component signals per foot, contacts, speed. Shows whether the lift saw the platform
in time, how far the foot sank before the plant, and the pelvis path. Harness evidence JSON."""
import json, sys, pathlib
E = pathlib.Path(__file__).resolve().parents[2] / 'Saved/Codex/SHME_V1_20260925/Evidence'
lab = sys.argv[1]; ex = float(sys.argv[2]); d = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
before = float(sys.argv[4]) if len(sys.argv) > 4 else 120.0; after = float(sys.argv[5]) if len(sys.argv) > 5 else 160.0
R = sorted([r for r in json.load(open(E / (lab + '.json'))) if isinstance(r, dict) and r.get('t') is not None and isinstance(r.get('ax'), list) and isinstance(r.get('vb_ball_l'), list)], key=lambda r: float(r['t']))
def f(x):
    try: return float(x)
    except Exception: return float('nan')
def b(x): return '1' if str(x) in ('True', 'true', '1', '1.0') else '.'
print('TER228 %s edge x %.0f' % (lab[-30:], ex))
print('%-6s %6s %5s | %6s %5s %5s %5s %5s %s | %6s %5s %5s %5s %5s %s | %5s %5s' % ('t', 'cap_x', 'cap_z', 'bL_x', 'bL_z', 'liftL', 'grdL', 'pathL', 'cL', 'bR_x', 'bR_z', 'liftR', 'grdR', 'pathR', 'cR', 'pelv_z', 'speed'))
for r in R:
    cx = (r['ax'][0] - ex) * d
    if cx < -before or cx > after: continue
    print('%-6.2f %6.0f %5.1f | %6.0f %5.1f %5.1f %5.1f %5.1f %s | %6.0f %5.1f %5.1f %5.1f %5.1f %s | %5.1f %5.0f' % (
        f(r['t']), cx, r['ax'][2], (r['vb_ball_l'][0] - ex) * d, r['vb_ball_l'][2], f(r.get('cv_SwingLiftL')), f(r.get('cv_SwingGroundL')), f(r.get('cv_SwingPathMaxL')), b(r.get('cv_ContactL')),
        (r['vb_ball_r'][0] - ex) * d, r['vb_ball_r'][2], f(r.get('cv_SwingLiftR')), f(r.get('cv_SwingGroundR')), f(r.get('cv_SwingPathMaxR')), b(r.get('cv_ContactR')), r['vb_pelvis'][2], f(r.get('Speed2D'))))
