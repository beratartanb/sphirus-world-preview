# an_final.py <rec.json>...: acceptance table per segment using the recorded game delta (gdt) instead of an assumed step:
# mean capsule speed, mean game step, planted-foot speed (20th percentile of the slower foot's horizontal world speed),
# actor yaw change, camera distance to the head pivot and its frame-to-frame jitter, FOV, and the driver clip family mix
# from the pose library (walk/jog/run/idle/turn) when drv data exists.
import json,sys,math,collections,os
lib=None
if os.path.exists('Saved/Codex/Day_20261107/cliplib.json'):
    lib=json.load(open('Saved/Codex/Day_20261107/cliplib.json')); flat=[]; names=[]
    for n,frs in lib['clips'].items():
        for row in frs: flat.append(row); names.append(n)
def nearest(v):
    best=1e18; bi=-1
    for i,row in enumerate(flat):
        d=0.0
        for a,b in zip(v,row):
            d+=(a-b)*(a-b)
            if d>=best: break
        else: best=d; bi=i
    return names[bi]
def fam(n):
    if 'Idle_Turn' in n: return 'idleturn'
    if 'Idle' in n: return 'idle'
    for k in ('Run','Jog','Walk'):
        if k in n: return k.lower()+('_start' if 'Start' in n else '_stop' if 'Stop' in n else '_pivot' if 'Pivot' in n else '')
    return 'other'
def ang(a): return (a+180)%360-180
for fn in sys.argv[1:]:
    d=json.load(open(fn)); R=d['rows']; plan=d['plan']
    print('==',fn.split('/')[-1],'frames',len(R),'mean gdt',round(sum(r.get('gdt',1/30) for r in R)/len(R),4))
    for s,seg in enumerate(plan):
        rows=[r for r in R if r['s']==s]
        if len(rows)<4: continue
        sp=[math.hypot(r['vx'],r['vy']) for r in rows]; gd=[r.get('gdt',1/30) for r in rows]
        p20=[]
        for ft in ('v_foot_l','v_foot_r'):
            v=sorted(math.hypot(rows[i][ft][0]-rows[i-1][ft][0],rows[i][ft][1]-rows[i-1][ft][1])/max(gd[i],1e-3) for i in range(1,len(rows)))
            p20.append(v[len(v)//5])
        cam=[math.dist(r['cam'][:3],(r['x'],r['y'],r['z']+66)) for r in rows]; cj=[abs(cam[i+1]-2*cam[i]+cam[i-1]) for i in range(1,len(cam)-1)]
        fams=collections.Counter(fam(nearest(r['drv'])) for r in rows if 'drv' in r) if lib else {}
        print(' SEG',s,repr(seg[0]),'yr',seg[2],'| spd',round(sum(sp)/len(sp)),'| gdt',round(sum(gd)/len(gd),3),'| plant p20',round(min(p20)),'| yaw',round(ang(rows[-1]['yaw']-rows[0]['yaw'])),'| cam',round(sum(cam)/len(cam)),'jit',round(sum(cj)/max(1,len(cj)),2),'| fov',round(sum(r['fov'] for r in rows)/len(rows),1),'|',dict(fams.most_common(4)))
