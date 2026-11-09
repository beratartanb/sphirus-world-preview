# an_turn.py <rec.json> <segment> [<segment>...]: per 0.05 s of game time inside a segment: capsule speed, facing yaw,
# velocity direction, heading error (velocity vs facing), visible-body clip + clip time (pose library NN), database.
import json,sys,math
lib=json.load(open('Saved/Codex/Day_20261107/cliplib.json')); flat=[];names=[];times=[]
for n,frs in lib['clips'].items():
    for i,row in enumerate(frs): flat.append(row); names.append(n); times.append(i/30.0)
def nearest(v):
    best=1e18;bi=0
    for i,row in enumerate(flat):
        d=0.0
        for a,b in zip(v,row):
            d+=(a-b)*(a-b)
            if d>=best: break
        else: best=d;bi=i
    return bi
d=json.load(open(sys.argv[1])); R=d['rows']
for s in [int(x) for x in sys.argv[2:]]:
    rows=[r for r in R if r['s']==s]; t=0.0; nxt=0.0
    print('== seg',s,d['plan'][s] if 'plan' in d else '')
    for r in rows:
        if t>=nxt-1e-6:
            sp=math.hypot(r['vx'],r['vy']); vd=math.degrees(math.atan2(r['vy'],r['vx'])) if sp>5 else float('nan')
            err=abs((vd-r['yaw']+180)%360-180) if sp>5 else 0
            i=nearest(r['drv']); db=str(r.get('db',''))[:14].replace('PSD_Sph_','')
            arm=r.get('arm') or [0]
            print('t=%5.2f v=%5.0f yaw=%6.1f vdir=%6.1f err=%5.1f  %-28s %5.2f  db=%-10s arm=%.0f hx=%s'%(t,sp,r['yaw'],vd,err,names[i].replace('af_Loco_','').replace('af_Stand_',''),times[i],db,arm[0],(r.get('scr') or {}).get('head',[None])[0]))
            nxt+=0.05
        t+=r.get('gdt',1/30)
