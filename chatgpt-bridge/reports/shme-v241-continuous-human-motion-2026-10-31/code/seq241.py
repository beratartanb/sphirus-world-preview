import sys, math; sys.path[:0]=['Tools/SHME_V231_20261026']
from ltp231 import load, short
from contact231 import classify
R=load(sys.argv[1]); t0=float(sys.argv[2]) if len(sys.argv)>2 else 5.0
prev=None
for r in R:
    if r['t']<t0: continue
    k=(str(r['av_CurrentSelectedDatabase']), short(r['av_Phase27_SelectedObject']))
    if k!=prev:
        vh=math.degrees(math.atan2(r['avy'],r['avx'])) if r['Speed2D']>5 else float('nan')
        print('%.3f %-22s %-36s t%.2f spd%4.0f ay%5.0f vh%5.0f fam%s Tk%s/%s' % (r['t'],k[0][:22],k[1][:36],r['av_Phase27_SelectedTime'],r['Speed2D'],r['ay'],vh,r['av_SHM_Family'],r.get('av_SHM239_TkPlay'),r.get('av_SHM240_TkDone')))
        prev=k
eps=[e for e in classify(R,2.5,1e9) if e['cls'] in ('SLIP','DRAG') and e['drift']>5]
for e in sorted(eps,key=lambda e:e['t']): print('   %s t=%.2f drift=%.1f %s %s'%(e['cls'],e['t'],e['drift'],e['s'],e['clip']))
