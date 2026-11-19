# an_camocc.py <label...>: view obstruction by the character's own head/hair, from recorded camera pose (cam x,y,z,pitch,yaw),
# horizontal FOV and the head bone. Head+hair modelled as a sphere (radius 13 cm) centred 6 cm above the head joint; projected into
# the 1509x920 PIE view (aspect 1.64). Per frame on a 24x15 screen grid:
#   cov    = fraction of the whole frame covered by the head sphere
#   lowmid = fraction of the lower-middle region (middle third horizontally, lower 60 %) covered (the reported hair complaint)
#   ctr    = 1 if the screen centre (aim / travel direction) is covered
# Camera motion is reported RELATIVE to the character (camera minus pelvis, actor frame) and as rotation steps, not world steps:
#   relstep = frame-to-frame change of the camera offset from the character (cm), rotstep = change of camera yaw/pitch (deg).
import json, sys, math, statistics as st
RD = 'Saved/Codex/Grip_20261106/rec/'; RAD = 13.0; UP = 6.0; ASP = 1509 / 920
GX = [(-1 + (i + 0.5) * 2 / 24) for i in range(24)]; GY = [(-1 + (j + 0.5) * 2 / 15) for j in range(15)]
def occ(r):
    cx, cy, cz, p, y = r['cam']; h = r['ub']['head']; c = (h[0], h[1], h[2] + UP)
    pr, yr = math.radians(p), math.radians(y)
    f = (math.cos(pr) * math.cos(yr), math.cos(pr) * math.sin(yr), math.sin(pr)); rt = (-math.sin(yr), math.cos(yr), 0.0)
    upv = (f[1] * rt[2] - f[2] * rt[1], f[2] * rt[0] - f[0] * rt[2], f[0] * rt[1] - f[1] * rt[0]); upv = tuple(-x for x in upv) if upv[2] < 0 else upv
    d = (c[0] - cx, c[1] - cy, c[2] - cz); dep = sum(d[i] * f[i] for i in range(3))
    if dep <= 1: return 1.0, 1.0, 1, dep
    th = math.tan(math.radians(r['fov']) / 2); tv = th / ASP
    sx = sum(d[i] * rt[i] for i in range(3)) / dep / th; sy = sum(d[i] * upv[i] for i in range(3)) / dep / tv
    rx = RAD / dep / th; ry = RAD / dep / tv
    ins = lambda gx, gy: ((gx - sx) / rx) ** 2 + ((gy - sy) / ry) ** 2 <= 1
    cov = sum(ins(gx, gy) for gx in GX for gy in GY) / (24 * 15)
    lm = [(gx, gy) for gx in GX for gy in GY if abs(gx) <= 1 / 3 and gy <= 0.2]
    return cov, sum(ins(a, b) for a, b in lm) / len(lm), int(ins(0, 0)), dep
for L in sys.argv[1:]:
    R = json.load(open(RD + L + '.json'))['rows']; O = []
    prev = None
    for r in R:
        cov, lm, ctr, dep = occ(r)
        yw = math.radians(r['yaw']); dx = r['cam'][0] - r['x']; dy = r['cam'][1] - r['y']
        rel = (dx * math.cos(yw) + dy * math.sin(yw), -dx * math.sin(yw) + dy * math.cos(yw), r['cam'][2] - r['z'])
        rs = math.dist(rel, prev[0]) if prev else 0.0; ro = max(abs((r['cam'][4] - prev[1] + 180) % 360 - 180), abs(r['cam'][3] - prev[2])) if prev else 0.0
        prev = (rel, r['cam'][4], r['cam'][3]); O.append((r['t'], cov, lm, ctr, dep, rs, ro, math.hypot(r['vx'], r['vy'])))
    n = len(O); bad = [o for o in O if o[2] > 0.25]
    print('== %s frames %d | lowmid>25%%: %d frames (%.1f%%), max lowmid %.0f%% | centre covered %d frames | mean cov %.1f%% max %.0f%% | min head depth %.0f cm | relstep p99 %.1f cm max %.1f | rotstep max %.1f deg' % (
        L, n, len(bad), 100 * len(bad) / max(1, n), 100 * max(o[2] for o in O), sum(o[3] for o in O), 100 * st.mean(o[1] for o in O), 100 * max(o[1] for o in O), min(o[4] for o in O),
        sorted(o[5] for o in O)[int(0.99 * (n - 1))], max(o[5] for o in O), max(o[6] for o in O)))
    if '-v' in sys.argv[1:] or len(sys.argv) == 2:
        t0 = O[0][0]
        for k in range(0, n, max(1, n // 40)):
            o = O[k]; print('   %5.1f s lowmid %3.0f%% cov %3.0f%% ctr %d depth %5.1f relstep %4.1f v %3.0f' % (o[0] - t0, 100 * o[2], 100 * o[1], o[3], o[4], o[5], o[7]))
