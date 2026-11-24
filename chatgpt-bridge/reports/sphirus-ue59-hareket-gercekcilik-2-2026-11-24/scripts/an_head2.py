# an_head2.py <label> [plan]: head stability per steady segment: head yaw (eye line, world, relative to travel direction), head roll (eye line),
# head lateral / vertical position (visible body, component space), p2p per gait cycle (mean / worst).
import json,sys,math
lab=sys.argv[1]; rows=json.load(open('Saved/Codex/Grip_20261106/rec/%s.json'%lab))['rows']
plan=eval(open(sys.argv[2]).read()) if len(sys.argv)>2 else None
segs={}
for r in rows: segs.setdefault(r['s'],[]).append(r)
def cyc(seg):
    e=[i for i in range(1,len(seg)) if seg[i]['hook']['cv'][0]>50 and seg[i-1]['hook']['cv'][0]<=50]; return [(e[i],e[i+1]) for i in range(len(e)-1)]
def p2p(v,cs):
    o=[]
    for a,b in cs:
        w=v[a:b]; n=len(w)
        if n<6: continue
        k=(w[-1]-w[0])/(n-1); d=[w[i]-w[0]-k*i for i in range(n)]; o.append(max(d)-min(d))
    return (sum(o)/len(o),max(o)) if o else (float('nan'),float('nan'))
def unwrap(v):
    o=[v[0]]
    for x in v[1:]: o.append(o[-1]+((x-o[-1]+180)%360-180))
    return o
print('####',lab)
for s,seg in sorted(segs.items()):
    seg=[r for r in seg if r.get('eyes') and r['hook'].get('pv')]
    sp=[math.hypot(r['vx'],r['vy']) for r in seg]
    if len(seg)<120 or min(sp[len(sp)//3:])<120: continue
    seg=seg[len(seg)//3:]; cs=cyc(seg)
    if len(cs)<3: continue
    yaw=[];roll=[];lat=[];ver=[]
    for r in seg:
        (ax,ay,az),(bx,by,bz)=r['eyes']; dx,dy,dz=bx-ax,by-ay,bz-az
        tr=math.degrees(math.atan2(r['vy'],r['vx']))
        yaw.append(math.degrees(math.atan2(dy,dx))-tr); roll.append(math.degrees(math.atan2(dz,math.hypot(dx,dy))))
        h=r['hook']['pv']['head']; lat.append(h[0]); ver.append(h[2])
    yaw=unwrap(yaw)
    k=plan[s][0] if plan and s<len(plan) else '?'
    f=lambda v:'%4.1f/%4.1f'%p2p(v,cs)
    print('s%-2d [%-24s] v %3.0f cycles %2d | head yaw %s deg | head roll %s deg | head lateral %s cm | head vertical %s cm   (mean/worst per cycle)'%(s,k,sum(sp)/len(sp),len(cs),f(yaw),f(roll),f(lat),f(ver)))
