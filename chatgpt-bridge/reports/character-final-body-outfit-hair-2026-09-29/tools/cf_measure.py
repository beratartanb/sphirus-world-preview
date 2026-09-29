import sys,json,math;sys.path.insert(0,'.')
from shc_combo import *
VER=sys.argv[1]
m=json.load(open(C.parent/'CharacterFinal_20260929'/f'br_morph_{VER}.json'))
after=list(cpos)
for v,d in m['Body']['BR_Neutral'].items(): v=int(v); after[v]=[cpos[v][i]+d[i] for i in range(3)]
for v,d in m['Head']['BR_Neutral'].items():
  ci=cid('Head',int(v)); after[ci]=[cpos[ci][i]+d[i] for i in range(3)]
def hull(pts):
  pts=sorted(set((round(p[0],4),round(p[1],4)) for p in pts))
  if len(pts)<3: return 0
  def cr(o,a,b): return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
  lo=[];up=[]
  for p in pts:
    while len(lo)>=2 and cr(lo[-2],lo[-1],p)<=0: lo.pop()
    lo.append(p)
  for p in reversed(pts):
    while len(up)>=2 and cr(up[-2],up[-1],p)<=0: up.pop()
    up.append(p)
  h=lo[:-1]+up[:-1]; return sum(math.dist(h[i],h[(i+1)%len(h)]) for i in range(len(h)))
ARM=('upperarm','lowerarm','hand')
def torso(v): return sum(x for b,x in cweights(v).items() if b.startswith(ARM))<0.3
meas={'neck z146':(146,lambda v,p:abs(p[0])<8),'chest z128':(128,lambda v,p:torso(v)),'underbust z119':(119,lambda v,p:torso(v)),'waist z109':(109,lambda v,p:torso(v)),
 'high hip z97':(97,lambda v,p:torso(v) and abs(p[0])<20),'hip z86':(86,lambda v,p:abs(p[0])<22 and torso(v)),'L thigh z70':(70,lambda v,p:p[0]>0.5),'L calf z35':(35,lambda v,p:p[0]>0),'L upper arm':(None,None)}
res={}
for k,(z,f) in meas.items():
  if z is None: continue
  ids=[v for v in range(CN) if abs(cpos[v][2]-z)<0.4 and f(v,cpos[v]) and not (v>=NB and (v-NB) in WELD)]
  a=hull([cpos[v] for v in ids]); b=hull([after[v] for v in ids]); res[k]=(round(a,2),round(b,2),round((b-a)*10,2))
  print(f'{k:14s} before {a:7.2f} cm  after {b:7.2f} cm  delta {(b-a)*10:+.2f} mm')
H=lambda P:max(p[2] for p in P)-min(p[2] for p in P); print('height before %.3f after %.3f'%(H(cpos),H(after)))
sw=lambda P:max(p[0] for p in P if abs(p[2]-141)<3)-min(p[0] for p in P if abs(p[2]-141)<3); print('shoulder width (z141 max-min x) before %.2f after %.2f'%(sw(cpos),sw(after)))
json.dump(res,open(C.parent/'CharacterFinal_20260929'/f'proportions_{VER}.json','w'),indent=1)
