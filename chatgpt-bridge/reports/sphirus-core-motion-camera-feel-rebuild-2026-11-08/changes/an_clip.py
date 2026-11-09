# an_clip.py <rec.json>...: identifies the clip and clip time the hidden driver is playing in each recorded frame by nearest
# neighbour against Saved/Codex/Day_20261107/cliplib.json (root-relative positions of six bones), then per plan segment:
# clip histogram, estimated play rate (clip-time advance per frame x 30), mean match distance, and clip switches per second.
import json,sys,math,collections
lib=json.load(open('Saved/Codex/Day_20261107/cliplib.json')); FPS=lib['fps']
flat=[]; names=[]; times=[]
for n,frs in lib['clips'].items():
    for i,row in enumerate(frs): flat.append(row); names.append(n); times.append(i/FPS)
def nearest(v,ncol=None):
    best=1e18; bi=-1
    for i,row in enumerate(flat):
        d=0.0
        for a,b in zip(v,row[:ncol] if ncol else row):
            d+=(a-b)*(a-b)
            if d>=best: break
        else:
            best=d; bi=i
    return bi,math.sqrt(best)
for fn in sys.argv[1:]:
    d=json.load(open(fn)); R=d['rows']; plan=d['plan']
    print('==',fn.split('/')[-1])
    ids=[]
    for r in R:
        if 'drv' in r: i,dist=nearest(r['drv'])
        elif 's_foot_l' in r:
            # older recordings: driver feet in the actor frame (root at capsule bottom, actor yaw)
            yaw=math.radians(r['yaw']-90.0); c,sn=math.cos(-yaw),math.sin(-yaw); v=[]
            for b in ('s_foot_l','s_foot_r'):
                dx,dy,dz=r[b][0]-r['x'],r[b][1]-r['y'],r[b][2]-(r['z']-86)
                v+=[dx*c-dy*sn,dx*sn+dy*c,dz]
            i,dist=nearest(v,6)
        else: ids.append((None,None,None)); continue
        ids.append((names[i],times[i],dist))
    for s,seg in enumerate(plan):
        idx=[k for k,r in enumerate(R) if r['s']==s and ids[k][0]]
        if len(idx)<3: continue
        hist=collections.Counter(ids[k][0] for k in idx); dist=sum(ids[k][2] for k in idx)/len(idx)
        rates=[]; sw=0
        for a,b in zip(idx,idx[1:]):
            if ids[a][0]==ids[b][0]:
                dt=ids[b][1]-ids[a][1]
                if 0<dt<0.2: rates.append(dt*FPS)
            else: sw+=1
        spd=[math.hypot(R[k]['vx'],R[k]['vy']) for k in idx]
        rt=sorted(rates); med=rt[len(rt)//2] if rt else None
        print(' SEG',s,repr(seg[0]),'spd',round(sum(spd)/len(spd)),'| clips',dict(hist.most_common(3)),'| rate med',round(med,2) if med else None,'| switches/s',round(sw/(len(idx)/FPS),1),'| matchdist',round(dist,1))
