# an_cmp.py <seg> <rec.json>...: compact comparison of one protocol segment across recordings - stop time/distance,
# capsule speed at 0.25/0.5/0.75/1.0 s, facing at those times, body clip sequence (run-length, NN) in the first 1.3 s,
# clip switches in that window, database sequence.
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
seg=int(sys.argv[1])
for fn in sys.argv[2:]:
    d=json.load(open(fn)); rows=[r for r in d['rows'] if r['s']==seg]; t=0.0; T=[]; 
    for r in rows: T.append(t); t+=r.get('gdt',1/30)
    sp=[math.hypot(r['vx'],r['vy']) for r in rows]; x0=(rows[0]['x'],rows[0]['y'])
    def at(tt):
        i=min(range(len(T)),key=lambda k:abs(T[k]-tt)); return i
    stop=[T[i] for i in range(len(rows)) if sp[i]<3 and sp[0]>50]; stop=stop[0] if stop else None
    dist=math.hypot(rows[at(stop)]['x']-x0[0],rows[at(stop)]['y']-x0[1]) if stop else None
    seq=[]; sw=0; last=None
    for i in range(len(rows)):
        if T[i]>1.3: break
        j=nearest(rows[i]['drv']); n=names[j].replace('af_Loco_','').replace('af_Stand_','')
        if n!=last:
            seq.append('%s@%.2f'%(n,times[j])); sw+=1 if last else 0; last=n
    dbs=[]; 
    for r in rows:
        v=str(r.get('db',''))[2:16].replace('PSD_Sph_','').split('.')[0].split("'")[0]
        if not dbs or dbs[-1]!=v: dbs.append(v)
    print('==',fn.split('/')[-1].replace('.json',''),'seg',seg,d['plan'][seg][0] or 'release')
    print('  stop %s s, %s cm | v@0.25/0.5/0.75/1.0: %s | yaw: %s'%(('%.2f'%stop) if stop else '-',('%.0f'%dist) if dist else '-',[round(sp[at(x)]) for x in (0.25,0.5,0.75,1.0)],[round(rows[at(x)]['yaw']) for x in (0.25,0.5,0.75,1.0)]))
    print('  switches(1.3s)',sw,'| db',dbs,'\n  ',' > '.join(seq))
