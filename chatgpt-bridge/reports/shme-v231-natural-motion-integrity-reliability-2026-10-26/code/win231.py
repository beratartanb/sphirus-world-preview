"""win231.py <label> [t0 t1] : frame table around an event (speed along facing, selected clip/time, ball z/speed, clip-bound speed)."""
import sys, math, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ltp231 import load, short
lab = sys.argv[1]; t0 = float(sys.argv[2]) if len(sys.argv) > 2 else 6.0; t1 = float(sys.argv[3]) if len(sys.argv) > 3 else 7.6
R = load(lab); prev = None
print('t      v_fwd  v_lat | sel                              ct    | bzL   bvL  bzR   bvR | DesV  Clip On | RA Fam Hold Brk IdleE')
for r in R:
    if not (t0 <= r['t'] <= t1): continue
    yaw = math.radians(r.get('ay', 0.0)); f = (math.cos(yaw), math.sin(yaw))
    if prev:
        dt = r['t'] - prev['t'] or 1e-3
        pr, pc = prev['mh_root'], r['mh_root']; vx, vy = (pc[0] - pr[0]) / dt, (pc[1] - pr[1]) / dt
        vf = vx * f[0] + vy * f[1]; vl = -vx * f[1] + vy * f[0]
        bv = {}
        for s in 'lr':
            a, b = prev['vb_ball_' + s], r['vb_ball_' + s]; bv[s] = math.hypot(b[0] - a[0], b[1] - a[1]) / dt
        print('%5.3f %6.0f %6.0f | %-32s %5.2f | %5.1f %4.0f %5.1f %4.0f | %5.0f %5.0f %s | %s %s %s %s %s' % (r['t'], vf, vl, short(r.get('av_Phase27_SelectedObject'))[:32], r.get('av_Phase27_SelectedTime', 0) or 0,
              r['vb_ball_l'][2], bv['l'], r['vb_ball_r'][2], bv['r'], r.get('av_SHM228_DesV', 0) or 0, r.get('cv_ClipSpeed', 0) or 0, str(r.get('cv_ClipSpeedOn'))[:1],
              str(r.get('av_SHM_RedirectActive'))[:1], str(r.get('cv_Family'))[-8:], str(r.get('av_SHM227_Hold'))[:4], str(r.get('av_SHM228_Brake'))[:4], str(r.get('av_SHM_IdleEntry'))[:1]))
    prev = r
