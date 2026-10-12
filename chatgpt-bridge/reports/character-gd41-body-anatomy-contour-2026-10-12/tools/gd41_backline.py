import sys, os, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from gd41_lib import Body
a = sys.argv[sys.argv.index('--')+1:]; B0 = Body(a[0], a[1]); B1 = Body(a[0], a[1], extra=a[2])
print('BACKLINE  z | back_lk back_D5 d_back | front_lk front_D5 d_front | w_lk w_D5')
for zz in range(86, 124, 2):
    m0 = B0.arm < 0.3; f0, b0, xm0, xn0 = B0.extents(zz, m0); f1, b1, xm1, xn1 = B1.extents(zz, m0)
    print('BACKLINE %3d | %6.2f %6.2f %+5.2f | %6.2f %6.2f %+5.2f | %5.1f %5.1f' % (zz, b0, b1, b1-b0, f0, f1, f1-f0, xm0-xn0, xm1-xn1))
