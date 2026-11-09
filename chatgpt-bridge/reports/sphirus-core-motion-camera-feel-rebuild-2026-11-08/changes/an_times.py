# an_times.py <rec.json>...: per segment, (a) which clip and clip time the visible body matches (pose library nearest
# neighbour, time in the clip), (b) the probe's fresh-search picks, (c) mean gdt and capsule speed, (d) the db/gait fields.
import json,sys,collections,math
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
for fn in sys.argv[1:]:
    d=json.load(open(fn)); R=d['rows']; print('==',fn.split('/')[-1],'frames',len(R),'mean gdt',round(sum(r.get('gdt',1/30) for r in R)/len(R),4))
    for s in sorted(set(r['s'] for r in R)):
        rows=[r for r in R if r['s']==s]
        if len(rows)<4: continue
        sp=round(sum(math.hypot(r['vx'],r['vy']) for r in rows)/len(rows))
        body=collections.Counter(); clips=collections.Counter()
        for r in rows:
            bi=nearest(r['drv']); nm=names[bi].replace('af_Loco_','').replace('af_Stand_',''); body[(nm,round(times[bi],1))]+=1; clips[nm]+=1
        probe=collections.Counter((r['mm'][0].split('.')[-1].strip("'>").replace('af_Loco_','').replace('af_Stand_',''),round(r['mm'][1],1)) for r in rows if 'mm' in r)
        dbs=collections.Counter(str(r.get('db')) for r in rows)
        print(' SEG',s,repr(d['plan'][s][0]),'spd',sp,'| body clips',dict(clips.most_common(3)))
        print('     body times',sorted(body.items(),key=lambda x:-x[1])[:8])
        print('     probe',sorted(probe.items(),key=lambda x:-x[1])[:6],'| db',dict(dbs.most_common(2)))
