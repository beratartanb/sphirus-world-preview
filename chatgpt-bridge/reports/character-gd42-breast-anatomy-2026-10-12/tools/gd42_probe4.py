import sys, numpy as np
sys.path.insert(0, sys.argv[sys.argv.index('--')+1]); from gd42_lib import Body, MX
a = sys.argv[sys.argv.index('--')+2:]; B = Body(a[0], a[1], extra=a[2]); XR = B.XR; x, y, z = XR.T
print('CHESTROWS  z | y(x=0) y(x=4) y(x=8) y(x=12) | x_max(front half) | y_back | yc')
for zz in range(108, 138, 2):
    p = B.section(float(zz), B.uarm < 0.4, XR)
    if len(p) < 8: print('CHESTROWS', zz, 'few'); continue
    px, py = p[:, 0], p[:, 1]; fr = py > (py.max()+py.min())/2
    def yat(xx):
        s = fr & (np.abs(px-xx) < 0.6); return round(float(py[s].max()), 2) if s.any() else None
    print('CHESTROWS %3d | %s %s %s %s | %5.1f | %6.2f | %5.2f' % (zz, yat(0), yat(4), yat(8), yat(12), px.max(), py.min(), 0.5*(py.max()+py.min())))
