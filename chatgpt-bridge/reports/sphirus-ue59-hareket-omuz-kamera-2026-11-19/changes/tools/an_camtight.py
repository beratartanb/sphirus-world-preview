# an_camtight.py <label>...: player camera vs head in the indoor passage, per 0.5 s: camera-head distance, camera height above the
# head, head angular size (25 cm head / distance, deg), boom safety fraction proxy (distance), speed.
import json, sys, math, statistics as st
for L in sys.argv[1:]:
    R = json.load(open('Saved/Codex/Grip_20261106/rec/%s.json' % L))['rows']; t0 = R[0]['t']; print('==', L)
    ds = []; dzs = []; jumps = 0; prev = None
    for r in R:
        c = r['cam']; h = r['v_head']; d = math.dist(c[:3], h[:3]); dz = c[2] - h[2]; ds.append(d); dzs.append(dz)
        if prev is not None and math.dist(prev, c[:3]) > 12: jumps += 1
        prev = c[:3]
    for i in range(0, len(R), 15):
        w = R[i:i + 15]; dd = st.mean(math.dist(r['cam'][:3], r['v_head'][:3]) for r in w); dz = st.mean(r['cam'][2] - r['v_head'][2] for r in w)
        print('  %5.1f s  dist %5.1f  cam above head %5.1f  head size %4.1f deg  speed %4.0f' % (w[0]['t'] - t0, dd, dz, math.degrees(2 * math.atan(12.5 / max(dd, 1))), st.mean(math.hypot(r['vx'], r['vy']) for r in w)))
    print('  SUMMARY min dist %.1f  p10 dist %.1f  mean cam-above-head %.1f  frames with camera step > 12 cm: %d' % (min(ds), sorted(ds)[len(ds) // 10], st.mean(dzs), jumps))
