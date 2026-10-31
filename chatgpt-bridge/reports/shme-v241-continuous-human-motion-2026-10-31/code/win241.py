import sys; sys.path[:0]=['Tools/SHME_V231_20261026']
from ltp231 import load
from contact231 import classify
a,b=float(sys.argv[1]),float(sys.argv[2])
for lab in sys.argv[3:]:
    R=load(lab); eps=[e for e in classify(R,2.5,1e9) if e['cls'] in ('SLIP','DRAG')]
    def w(t0,t1):
        x=[e['drift'] for e in eps if t0<=e['t']<t1]; return max(x) if x else 0.0
    print('%-34s catch[%.2f,%.2f) %.1f  exit[%.2f,%.2f) %.1f  rest %.1f' % (lab,a,b,w(a,b),b,b+0.8,w(b,b+0.8),w(b+0.8,99)))
