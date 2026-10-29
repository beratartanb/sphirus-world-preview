"""pelvis237.py <label> <t0> <t1> : pelvis height chain on the SAME frames (cm above the root / floor):
  src  = the played clip's own pelvis at the played clip time (stick JSON of a generated clip: V236 / V237 stick folders; '-' for vendor clips)
  mm   = MM-stage mesh pelvis (mx_pelvis - mx_root)       -> src vs mm = blending / inertialization of the selected poses
  vis  = visible pelvis (vb_pelvis - mx_root)              -> mm vs vis = FootPlacement / PBI pelvis / retarget
plus the knee angle of each visible leg (thigh-calf-foot, 180 = straight) and the support (planted ball) so a crouch reads as
'legs bent while both feet are planted' vs 'a stride'. Prints PELV237 summary: min of each stage after t0 and the stage where the drop grows."""
import sys, os, math, json, glob
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, '..', 'SHME_V231_20261026'))
from ltp231 import load, short
ROOT = os.path.abspath(os.path.join(H, '..', '..'))
STK = {}
for p in glob.glob(os.path.join(ROOT, 'Saved', 'Codex', 'SHME_V23[67]_*', 'stick', '*.json')): STK[os.path.basename(p)[:-5]] = p
_cache = {}
def src_pelvis(clip, t):
    if clip not in STK: return None
    if clip not in _cache:
        d = json.load(open(STK[clip])); i = d['bones'].index('pelvis'); rt = d.get('root')
        _cache[clip] = (d['dt'], [fr[i][2] - (rt[k][2] if rt else 0.0) for k, fr in enumerate(d['frames'])])
    dt, zs = _cache[clip]; f = min(len(zs) - 1, max(0, int(round(t / dt)))); return zs[f]
def ang(a, b, c):
    u = [a[i] - b[i] for i in range(3)]; v = [c[i] - b[i] for i in range(3)]
    nu = math.sqrt(sum(x * x for x in u)); nv = math.sqrt(sum(x * x for x in v))
    return math.degrees(math.acos(max(-1, min(1, sum(u[i] * v[i] for i in range(3)) / max(nu * nv, 1e-6)))))
if __name__ == '__main__':
    lab, t0, t1 = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]); R = load(lab); mins = {'src': 1e9, 'mm': 1e9, 'vis': 1e9}; rows = []
    for r in R:
        if not (t0 <= r['t'] <= t1): continue
        rt = r['mx_root']; clip = short(r['av_Phase27_SelectedObject']); ct = r['av_Phase27_SelectedTime']
        sp = src_pelvis(clip, ct); mm = r['mx_pelvis'][2] - rt[2]; vis = r['vb_pelvis'][2] - rt[2]
        kl = ang(r['vx_thigh_l'], r['vx_calf_l'], r['vx_foot_l']); kr = ang(r['vx_thigh_r'], r['vx_calf_r'], r['vx_foot_r'])
        bl, br = r['vb_ball_l'][2] - rt[2], r['vb_ball_r'][2] - rt[2]
        rows.append((r['t'], r['Speed2D'], clip, ct, sp, mm, vis, kl, kr, bl, br))
        if sp is not None: mins['src'] = min(mins['src'], sp)
        mins['mm'] = min(mins['mm'], mm); mins['vis'] = min(mins['vis'], vis)
    for x in rows:
        print('%.2f v%4.0f %-28s %5.2f src %5s mm %5.1f vis %5.1f | knee L %3.0f R %3.0f | ball z L %5.1f R %5.1f' % (x[0], x[1], x[2][:28], x[3], '-' if x[4] is None else '%.1f' % x[4], x[5], x[6], x[7], x[8], x[9], x[10]))
    fin = rows[-1] if rows else None
    if fin: print('PELV237 %s min src %.1f mm %.1f vis %.1f | final src %s mm %.1f vis %.1f | drop vs final: src %s mm %.1f vis %.1f' % (lab, mins['src'], mins['mm'], mins['vis'],
        '-' if fin[4] is None else '%.1f' % fin[4], fin[5], fin[6], '-' if fin[4] is None else '%.1f' % (mins['src'] - fin[4]), mins['mm'] - fin[5], mins['vis'] - fin[6]))
