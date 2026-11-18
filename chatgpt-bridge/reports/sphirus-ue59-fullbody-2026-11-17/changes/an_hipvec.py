# an_hipvec.py <labels>: pelvis offset from the capsule as a vector, expressed in the HIP-LINE frame (not the capsule frame, which snaps
# with control yaw). If |offset| stays near its straight-line value the "lateral excursion" of an_hip.py is frame geometry, not a throw.
import sys, math, os
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'an_hip.py')).read().split('for lb in sys.argv[1:]')[0]; exec(src)
for lb in sys.argv[1:]:
    j, R, bone, S = load(lb); T = [r[0] for r in R]; cy = unwrap([r[5] for r in R])
    ev = []; i = 1
    while i < len(R):
        dt = T[i] - T[i-1]
        if dt > 0 and abs((cy[i] - cy[i-1]) / dt) > 100:
            k = i
            while k < len(R) - 1 and abs(cy[k+1] - cy[k]) > 0.5: k += 1
            ev.append((i - 1, cy[k] - cy[i-1])); i = k + 30
        else: i += 1
    print('=====', lb)
    for sk, nm in ((0, 'drv'), (1, 'vis')):
        s = series(R, bone, sk)
        def vec(k):
            r = R[k]; p = bone(r, sk, 'pelvis'); dx, dy = p[0] - r[1], p[1] - r[2]
            h = math.radians(s[k]['hip']); return dx*math.cos(h) + dy*math.sin(h), -dx*math.sin(h) + dy*math.cos(h), math.hypot(dx, dy)
        for i0, dl in ev:
            pre = [vec(k) for k in range(max(0, i0 - 45), i0)]
            w = [k for k in range(i0, len(R)) if T[k] - T[i0] <= 1.5]
            V = [vec(k) for k in w]
            mpre = max(v[2] for v in pre); fpre = sum(v[0] for v in pre)/len(pre)
            pk = max(V, key=lambda v: v[2]); tpk = T[w[V.index(pk)]] - T[i0]
            lh = max(abs(v[1]) for v in V); lpre = max(abs(v[1]) for v in pre)
            print('%s %+5.0f | straight: fwd mean %+5.1f |off| max %4.1f hipframe-lat max %4.1f | turn: |off| max %4.1f at +%.2fs (fwd %+5.1f lat %+5.1f) hipframe-lat max %4.1f' % (nm, dl, fpre, mpre, lpre, pk[2], tpk, pk[0], pk[1], lh))
