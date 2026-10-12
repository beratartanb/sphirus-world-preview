import sys, numpy as np
sys.path.insert(0, sys.argv[sys.argv.index('--')+1]); from gd42_lib import Body, MX
a = sys.argv[sys.argv.index('--')+2:]; B = Body(a[0], a[1]); XR = B.XR; x, y, z = XR.T; W8 = B.P['weights']
def chain(pre): return np.asarray([sum(w for b, w in W8[v].items() if b.startswith(pre)) for v in range(B.NB)])
clav = chain(('clavicle',)); ua = B.uarm; la = chain(('lowerarm', 'hand', 'index', 'middle', 'ring', 'pinky', 'thumb'))
for nm, sel in (('breast box x4-14 z121-135 y>4', (x > 4) & (x < 14) & (z > 121) & (z < 135) & (y > 4)), ('lateral chest x12-17 z118-132', (x > 12) & (x < 17) & (z > 118) & (z < 132)), ('axilla x14-20 z130-140', (x > 14) & (x < 20) & (z > 130) & (z < 140)), ('upper back x0-14 z118-134 y<-2', (x > 0) & (x < 14) & (z > 118) & (z < 134) & (y < -2)), ('sternum x0-3 z122-134 y>8', (x >= 0) & (x < 3) & (z > 122) & (z < 134) & (y > 8))):
    print('%-34s n=%4d clav p50/p95 %.2f/%.2f  uarm p50/p95 %.2f/%.2f  lowerarm+hand max %.2f' % (nm, sel.sum(), np.percentile(clav[sel], 50), np.percentile(clav[sel], 95), np.percentile(ua[sel], 50), np.percentile(ua[sel], 95), la[sel].max()))
