# an_lab.py <rec.json>...: lab analysis per segment -
#  motion: capsule speed, body clip (pose library NN) and its clip time, clip switches/s and time resets/s of the body
#          (NN time jumping backwards by > 0.25 s while the clip stays the same = a restart), database field, steady/idle flags;
#  idle:   head world speed p50/p95 (cm/s) and the body clip-time trace sampled every 2 s (repeat period of the idle);
#  camera: normalized head/pelvis screen X (min/mean/max), spring arm length / collision-fix frames, camera-head distance.
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
def q(xs,p):
    xs=sorted(xs); return xs[min(len(xs)-1,int(p*len(xs)))] if xs else 0
for fn in sys.argv[1:]:
    d=json.load(open(fn)); R=d['rows']; T=sum(r.get('gdt',1/30) for r in R)
    print('==',fn.split('/')[-1],'frames',len(R),'game s',round(T,1),'mean gdt',round(T/len(R),4))
    for s in sorted(set(r['s'] for r in R)):
        rows=[r for r in R if r['s']==s]
        if len(rows)<4: continue
        Ts=sum(r.get('gdt',1/30) for r in rows); sp=[math.hypot(r['vx'],r['vy']) for r in rows]
        nn=[nearest(r['drv']) for r in rows]; cl=[names[i].replace('af_Loco_','').replace('af_Stand_','') for i in nn]; tt=[times[i] for i in nn]
        sw=sum(1 for i in range(1,len(cl)) if cl[i]!=cl[i-1]); rs=sum(1 for i in range(1,len(cl)) if cl[i]==cl[i-1] and tt[i]<tt[i-1]-0.25)
        # continuity of the dominant clip: share of consecutive frames (same clip) whose clip time advances 0.3-2.5 x dt
        dom=collections.Counter(cl).most_common(1)[0][0]
        # resample to ~30 fps bins before judging continuity (the pose library is 30 fps; finer frames quantize to 0 / 1 frame)
        acc=0.0; sel=[0]
        for i in range(1,len(rows)):
            acc+=rows[i].get('gdt',1/30)
            if acc>=1/30-1e-4: sel.append(i); acc=0.0
        pairs=[(tt[sel[k-1]],tt[sel[k]],sum(rows[j].get('gdt',1/30) for j in range(sel[k-1]+1,sel[k]+1))) for k in range(1,len(sel)) if cl[sel[k]]==dom and cl[sel[k-1]]==dom]
        cont=sum(1 for a,b,g in pairs if 0.3*g<=(b-a)<=2.5*g or (b<a and b<0.3))/max(1,len(pairs))
        hv=[math.dist(rows[i]['v_head'],rows[i-1]['v_head'])/max(rows[i].get('gdt',1/30),1e-3) for i in range(1,len(rows))]
        hx=[r['scr']['head'][0] for r in rows if isinstance(r.get('scr'),dict) and r['scr'].get('head')]; px=[r['scr']['pelvis'][0] for r in rows if isinstance(r.get('scr'),dict) and r['scr'].get('pelvis')]
        hy=[r['scr']['head'][1] for r in rows if isinstance(r.get('scr'),dict) and r['scr'].get('head')]
        arm=[r['arm'] for r in rows if isinstance(r.get('arm'),(list,tuple))]; col=sum(1 for a in arm if a[-1])
        cam=[math.dist(r['cam'][:3],(r['x'],r['y'],r['z']+66)) for r in rows]
        dbs=collections.Counter(str(r.get('db'))[2:18] if isinstance(r.get('db'),list) else str(r.get('db'))[:16] for r in rows)
        fl=collections.Counter(str(r.get('flags'))[:14] for r in rows)
        print(' SEG',s,repr(d['plan'][s][0]),'yr',d['plan'][s][2],'| %.1fs'%Ts,'spd mean %d p95 %d'%(sum(sp)/len(sp),q(sp,0.95)),'| body',dict(collections.Counter(cl).most_common(3)),'| sw/s %.1f restarts/s %.1f cont(%s) %.2f n=%d'%(sw/max(Ts,1e-3),rs/max(Ts,1e-3),dom,cont,len(pairs)),'| yaw %d->%d'%(rows[0]['yaw'],rows[-1]['yaw']))
        print('      head v p50 %d p95 %d'%(q(hv,0.5),q(hv,0.95)),'| headX min/mean/max %s'%(('%.2f/%.2f/%.2f'%(min(hx),sum(hx)/len(hx),max(hx))) if hx else '-'),'headY mean %s'%(('%.2f'%(sum(hy)/len(hy))) if hy else '-'),'pelvisX mean %s'%(('%.2f'%(sum(px)/len(px))) if px else '-'),'| arm %s coll %d/%d'%(('%.0f'%(sum(a[0] for a in arm)/len(arm))) if arm else '-',col,len(arm)),'cam-head %d'%(sum(cam)/len(cam)),'| db',dict(dbs.most_common(2)),'| flags',dict(fl.most_common(2)))
        if s==0 and Ts>20:
            trace=[(round(sum(r.get('gdt',1/30) for r in rows[:i]),1),cl[i],round(tt[i],1)) for i in range(0,len(rows),60)]
            print('      idle trace (t, clip, cliptime):',trace[:40])
