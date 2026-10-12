import sys, os, json, numpy as np
sys.path.insert(0, sys.argv[sys.argv.index('--')+1]); from gd42_lib import Body, ss, nrm, MX
a = sys.argv[sys.argv.index('--')+2:]; B = Body(a[0], a[1], extra=a[2]); XR = B.XR; x, y, z = XR.T
AP = {k: np.asarray(v)-np.array([MX, 0, 0]) for k, v in B.P['breast_apex'].items()}; A = AP['l']; print('apex pkg', np.round(A, 2))
reg = (x > 1.5) & (x < 20) & (z > 112) & (z < 142) & (y > 0) & (B.arm < 0.3); print('breast-region verts (x 1.5..20, z 112..142, front)', reg.sum(), 'density/cm2 ~', round(reg.sum()/(18.5*30*0.7), 2))
# sagittal profile at x = apex: max y per z band (0.5 cm) within |x-Ax|<0.6
for xs in (A[0], 4.0, 13.0):
    sel = (np.abs(x-xs) < 0.7) & (y > 0) & (B.arm < 0.3); prof = []
    for zz in np.arange(112, 142, 1.0):
        b = sel & (np.abs(z-zz) < 0.6)
        if b.any(): prof.append((zz, round(float(y[b].max()), 2)))
    print('SAG x=%.1f' % xs, prof)
# transverse at apex z
sel = (np.abs(z-A[2]) < 0.7) & (y > 0) & (B.arm < 0.3); prof = []
for xx in np.arange(0, 20, 1.0):
    b = sel & (np.abs(x-xx) < 0.6)
    if b.any(): prof.append((xx, round(float(y[b].max()), 2)))
print('TRANS z=apex', prof)
# the current apex: max y in the chest band
band = (z > 118) & (z < 136) & (x > 2) & (B.arm < 0.3); i = np.argmax(y*band); print('max-y vert', np.round(XR[i], 2), 'normal', np.round(B.normals()[i], 2))
