# an_coast5.py <label> <scene json> [segment of the release, default 2]: brake-assist run against a test scene.
# Distance to obstacles is GEOMETRIC: the smallest 2-D distance from the capsule circle (radius 35) to each scene box footprint
# (oriented rectangle, yaw), over the whole release segment - not an X-coordinate difference. Boxes lower than 40 cm above the feet
# (steps / low obstacles) are reported separately. Rest = speed < 5 cm/s held 0.15 s; a run that never rests is reported as such.
import json, sys, math
rows = json.load(open('Saved/Codex/Grip_20261106/rec/%s.json' % sys.argv[1]))['rows']; S = json.loads(sys.argv[2]) if len(sys.argv) > 2 else []
seg = int(sys.argv[3]) if len(sys.argv) > 3 else 2
H = lambda r: r['hook'] if isinstance(r['hook'], dict) else {}
sp = lambda r: math.hypot(r['vx'], r['vy'])
rel = [r for r in rows if r['s'] == seg]
if not rel: print(sys.argv[1], 'no release'); sys.exit()
def boxdist(px, py, b):
    x, y, zc, sx, sy, sz = b[:6]; yaw = math.radians(b[6] if len(b) > 6 else 0)
    dx, dy = px - x, py - y; lx = dx * math.cos(-yaw) - dy * math.sin(-yaw); ly = dx * math.sin(-yaw) + dy * math.cos(-yaw)
    ex, ey = max(abs(lx) - sx / 2, 0), max(abs(ly) - sy / 2, 0); return math.hypot(ex, ey)
r0 = rel[0]; ts = None
for i, r in enumerate(rel):
    if sp(r) < 5 and all(sp(q) < 5 for q in rel[i:i + 9]): ts = r; break
ex = [H(r).get('ex') or [0, 0, 0, 0, 0] for r in rel]; ex = [e if isinstance(e, list) else [0, 0, 0, 0, 0] for e in ex]
coast = [r['t'] - r0['t'] for r in rel if isinstance(H(r).get('exs'), list) and H(r)['exs'][0] == 'True']
d = sum(math.hypot(rel[i]['x'] - rel[i - 1]['x'], rel[i]['y'] - rel[i - 1]['y']) for i in range(1, len(rel) if ts is None else rel.index(ts) + 1))
feet = r0['z'] - 88.2
gap = []
for k, b in enumerate(S):
    top = b[2] + b[5] / 2 - feet
    m = min(boxdist(r['x'], r['y'], b) - 35.0 for r in rel)
    gap.append('box%d(top %+.0f cm) closest %.0f cm' % (k, top, m))
clips = []
for r in rel:
    c = (r['gasp'][0] or 'None')[-26:]
    if not clips or clips[-1] != c: clips.append(c)
print('%s release v %.0f | coast %.2f s (frames %d) | %s | travel %.0f cm | %s | z %.0f..%.0f | clips %s' % (
    sys.argv[1], sp(r0), (coast[-1] if coast else 0.0), len(coast), ('rest after %.2f s' % (ts['t'] - r0['t'])) if ts else 'NOT AT REST (end %.0f cm/s)' % sp(rel[-1]),
    d, '; '.join(gap) or 'open lane', min(r['z'] for r in rel), max(r['z'] for r in rel), ' > '.join(clips[:6])))
print('   telemetry max: avail %.0f floor %.0f budget %.0f | min budget while coasting %.0f' % (max(e[1] for e in ex), max(e[2] for e in ex), max(e[3] for e in ex), min([e[3] for e, r in zip(ex, rel) if isinstance(H(r).get('exs'), list) and H(r)['exs'][0] == 'True'] or [0])))
