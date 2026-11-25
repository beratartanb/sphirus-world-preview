# an_trans.py <label> <plan> [tl]: every key change of a plan as the BODY performs it: capsule speed timeline, clips played, foot plants
# (visible foot horizontal speed < 60 cm/s and height < 6 cm above its recording minimum) between the key change and the settled state,
# trunk lean (pelvis->neck_01 vs vertical, in the travel direction) and its peak. 'tl' prints the 0.1 s timeline.
import json,sys,math
lab=sys.argv[1]; rows=json.load(open('Saved/Codex/Grip_20261106/rec/%s.json'%lab))['rows']; plan=eval(open(sys.argv[2]).read()); TL=len(sys.argv)>3
sp=lambda r: math.hypot(r['vx'],r['vy'])
zmin={f:min(r[f][2] for r in rows) for f in ('v_foot_l','v_foot_r')}
def planted(i,f):
    if i==0: return True
    a,b=rows[i-1],rows[i]; dt=max(b['t']-a['t'],1e-3)
    return math.hypot(b[f][0]-a[f][0],b[f][1]-a[f][1])/dt<60 and b[f][2]-zmin[f]<6
def lean(r):
    p=r['ub']['pelvis']; n=r['ub']['neck_01']; v=sp(r)
    if v<20: return 0.0
    d=((n[0]-p[0])*r['vx']+(n[1]-p[1])*r['vy'])/v
    return math.degrees(math.atan2(d,n[2]-p[2]))
key=lambda x: x.replace(' LeftShift','+Sh').replace(' LeftControl','+Ct') or '-'
segs={}
for i,r in enumerate(rows): segs.setdefault(r['s'],[]).append(i)
for s,ix in sorted(segs.items()):
    if s==0 or s>=len(plan): continue
    i0,i1=ix[0],ix[-1]; v0=sp(rows[i0-1]); t0=rows[i0]['t']; k=plan[s][0]; kp=plan[s-1][0]
    ve=sp(rows[i1])
    if abs(ve-v0)<60: continue
    # settle: first frame after which speed stays within 5 % (or 8 cm/s) of the end speed
    tol=max(8,0.05*max(ve,v0)); j=i1
    for i in range(i1,i0,-1):
        if abs(sp(rows[i])-ve)>tol: j=min(i+1,i1); break
    T=rows[j]['t']-t0; d=sum(math.hypot(rows[i]['x']-rows[i-1]['x'],rows[i]['y']-rows[i-1]['y']) for i in range(i0,j+1))
    plants=[]
    for f in ('v_foot_l','v_foot_r'):
        for i in range(i0+1,j+1):
            if planted(i,f) and not planted(i-1,f): plants.append((rows[i]['t']-t0,f[-1].upper()))
    plants.sort(); clips=[]
    for i in range(i0,j+1):
        c=rows[i]['gasp'][0]
        if not clips or clips[-1][0]!=c: clips.append([c,rows[i]['t']-t0])
    ln=[lean(rows[i]) for i in range(i0,j+1)]; pk=max(ln,key=abs) if ln else 0
    acc=[]
    for i in range(i0,j):
        q=i
        while q<j and rows[q]['t']-rows[i]['t']<0.15: q+=1
        if rows[q]['t']-rows[i]['t']>0.1: acc.append((sp(rows[q])-sp(rows[i]))/(rows[q]['t']-rows[i]['t']))
    pa=max(acc,key=abs) if acc else 0
    print('%s s%-2d [%-9s>%-9s] %3.0f -> %3.0f | settle %.2f s %3.0f cm | peak accel %5.0f | plants %d %s | lean start %4.1f peak %5.1f end %4.1f'%(lab[-22:],s,key(kp),key(k),v0,ve,T,d,pa,len(plants),' '.join('%s%.2f'%(f,t) for t,f in plants[:8]),lean(rows[i0-1]),pk,lean(rows[j])))
    print('      clips: '+'  '.join('%s@%.2f'%(c[-26:],t) for c,t in clips[:7]))
    if TL:
        tn=0
        for i in range(i0,min(j+8,len(rows))):
            if rows[i]['t']-t0>=tn: print('        +%.1f v %3.0f lean %5.1f %s'%(tn,sp(rows[i]),lean(rows[i]),rows[i]['gasp'][0][-24:])); tn+=0.1
