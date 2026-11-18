import sys, math, os
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'an_hip.py')).read().split('for lb in sys.argv[1:]')[0]; exec(src)
for lb in sys.argv[1:]:
    j, R, bone, S = load(lb); print(lb, j['bones'])
    for a, b in ((6, 12), (13.4, 15.7), (16.6, 18.9)):
        W = [r for r in R if a <= r[0] <= b]; out = []
        for sk in (1,):
            tp = []; pz = []; fl = []; sep = []; hz = []
            for r in W:
                ay = math.radians(r[4]); f = (math.cos(ay), math.sin(ay))
                p = bone(r, sk, 'pelvis'); s5 = bone(r, sk, 'spine_05'); h = bone(r, sk, 'head'); l = bone(r, sk, 'foot_l'); rr = bone(r, sk, 'foot_r')
                tp.append(math.degrees(math.atan2((s5[0]-p[0])*f[0] + (s5[1]-p[1])*f[1], s5[2]-p[2]))); pz.append(p[2]); hz.append(h[2])
                sep.append((l[0]-rr[0])*f[0] + (l[1]-rr[1])*f[1])
            sp = sum(math.hypot(r[6], r[7]) for r in W)/len(W)
            # cadence from zero crossings of fore-aft foot separation
            zc = sum(1 for k in range(1, len(sep)) if sep[k-1]*sep[k] < 0)
            print('  %5.1f-%5.1f speed %3.0f trunk pitch %+5.1f (range %4.1f) pelvis z %5.1f (bob %4.1f) head z %5.1f stride sep max %5.1f steps/min %4.0f' % (a, b, sp, sum(tp)/len(tp), max(tp)-min(tp), sum(pz)/len(pz), max(pz)-min(pz), sum(hz)/len(hz), max(abs(x) for x in sep), zc/(b-a)*60))
