import sys; sys.path[:0]=['Tools/SHME_V231_20261026','Tools/SHME_V238_20261030']
from ltp231 import load
from contact231 import classify
for lab in sys.argv[1:]:
    R=load(lab); eps=[e for e in classify(R,2.5,1e9) if e['cls'] in ('SLIP','DRAG') and e['drift']>4]
    print(lab, len(R))
    for e in sorted(eps,key=lambda e:-e['drift'])[:4]: print('  %s t=%.2f dur=%.2f drift=%.1f %s %s'%(e['cls'],e['t'],e['dur'],e['drift'],e['s'],e['clip']))
