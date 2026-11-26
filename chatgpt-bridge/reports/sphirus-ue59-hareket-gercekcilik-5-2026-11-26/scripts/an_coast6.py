# an_coast6.py <label> <scene json> [release segment, default 2]: brake assist on 'sph-tele/5.1' data (fields by NAME; a missing
# field is an error). Geometric capsule-to-box distance as an_coast5; coast frames = CS_Clear true.
import json, sys, math
sys.path.insert(0, 'Tools/UE59_20261126'); import tele5
lab = sys.argv[1]; S = json.loads(sys.argv[2]) if len(sys.argv) > 2 else []; seg = int(sys.argv[3]) if len(sys.argv) > 3 else 2
R = tele5.load(lab, need=('CS_Clear', 'CS_Budget', 'CS_Avail', 'CS_Floor'))
rel = [(r, t) for r, t in R if r['s'] == seg]
if not rel: raise SystemExit('%s: no release segment' % lab)
def boxdist(px, py, b):
    x, y, zc, sx, sy, sz = b[:6]; yaw = math.radians(b[6] if len(b) > 6 else 0); dx, dy = px - x, py - y
    lx = dx * math.cos(-yaw) - dy * math.sin(-yaw); ly = dx * math.sin(-yaw) + dy * math.cos(-yaw)
    return math.hypot(max(abs(lx) - sx / 2, 0), max(abs(ly) - sy / 2, 0))
t0 = rel[0][1]['gt']; coast = [t['gt'] - t0 for r, t in rel if t['f']['CS_Clear'] is True]
ts = next((t['gt'] - t0 for i, (r, t) in enumerate(rel) if t['speed'] < 5 and all(q[1]['speed'] < 5 for q in rel[i:i + 9])), None)
d = sum(math.hypot(rel[i][0]['x'] - rel[i - 1][0]['x'], rel[i][0]['y'] - rel[i - 1][0]['y']) for i in range(1, len(rel)))
gaps = ['box%d closest %.0f cm' % (k, min(boxdist(r['x'], r['y'], b) - 35.0 for r, t in rel)) for k, b in enumerate(S)]
print('%s [%s] release v %.0f | coast %.2f s (%d frames) | %s | travel %.0f cm | %s | min budget while coasting %s' % (lab, rel[0][1]['schema'], rel[0][1]['speed'], (coast[-1] if coast else 0), len(coast),
      ('rest after %.2f s' % ts) if ts is not None else 'NOT AT REST (end %.0f cm/s)' % rel[-1][1]['speed'], d, '; '.join(gaps) or 'open lane',
      min([t['f']['CS_Budget'] for r, t in rel if t['f']['CS_Clear'] is True] or ['-'])))
