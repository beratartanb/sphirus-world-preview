# an_turn.py <label> <plan>: body coordination through direction changes (visible body, world frame).
#  per key change with a direction change, window 0 .. 1.2 s: hip line yaw (thigh_l -> thigh_r), shoulder line yaw (upperarm_l -> upperarm_r),
#  twist = shoulder yaw - hip yaw (wrapped): range in the window; hip yaw rate peak (deg/s, 0.05 s window); hip line tilt range (roll);
#  trunk side bend = angle of pelvis -> neck_01 from vertical in the hip-line plane (range); lean into the turn = same angle, signed
#  toward the centre of the turn (mean while the travel direction changes); capsule: direction change, time until the velocity
#  direction is within 10 deg of the final one, lateral acceleration peak.
import json,sys,math
lab=sys.argv[1]; rows=json.load(open('Saved/Codex/Grip_20261106/rec/%s.json'%lab))['rows']; plan=eval(open(sys.argv[2]).read())
W=lambda a:(a+180)%360-180
def yaw(a,b): return math.degrees(math.atan2(b[1]-a[1],b[0]-a[0]))
def feats(r):
    u=r['ub']; hy=yaw(u['thigh_l'],u['thigh_r']); sy=yaw(u['upperarm_l'],u['upperarm_r'])
    hl=u['thigh_l']; hr=u['thigh_r']; tilt=math.degrees(math.atan2(hr[2]-hl[2],math.hypot(hr[0]-hl[0],hr[1]-hl[1])))
    ax=[hr[0]-hl[0],hr[1]-hl[1]]; n=math.hypot(*ax) or 1; ax=[ax[0]/n,ax[1]/n]; p=u['pelvis']; k=u['neck_01']
    bend=math.degrees(math.atan2((k[0]-p[0])*ax[0]+(k[1]-p[1])*ax[1],k[2]-p[2]))
    return hy,sy,tilt,bend,ax
key=lambda x: x.replace(' LeftShift','+Sh').replace(' LeftControl','+Ct') or '-'
dirk=lambda k: tuple(sorted(x for x in k.split() if x in 'WASD'))
segs={}
for i,r in enumerate(rows): segs.setdefault(r['s'],[]).append(i)
tot=[]
for s,ix in sorted(segs.items()):
    if s==0 or s>=len(plan): continue
    k=plan[s][0]; kp=plan[s-1][0]
    if not dirk(k) or not dirk(kp) or dirk(k)==dirk(kp): continue
    i0=ix[0]; t0=rows[i0]['t']; w=[i for i in range(i0,len(rows)) if rows[i]['t']-t0<=1.2]
    if len(w)<10: continue
    F=[feats(rows[i]) for i in w]; tw=[W(f[1]-f[0]) for f in F]
    hy=[F[0][0]]
    for f in F[1:]: hy.append(hy[-1]+W(f[0]-hy[-1]))
    rate=0
    for a in range(len(w)):
        b=a
        while b<len(w)-1 and rows[w[b]]['t']-rows[w[a]]['t']<0.05: b+=1
        dt=rows[w[b]]['t']-rows[w[a]]['t']
        if dt>0.03: rate=max(rate,abs(hy[b]-hy[a])/dt)
    v0=rows[i0-1]; d0=math.degrees(math.atan2(v0['vy'],v0['vx'])); ve=rows[w[-1]]; d1=math.degrees(math.atan2(ve['vy'],ve['vx'])); dd=W(d1-d0)
    tset=next((rows[i]['t']-t0 for i in w if math.hypot(rows[i]['vx'],rows[i]['vy'])>60 and abs(W(math.degrees(math.atan2(rows[i]['vy'],rows[i]['vx']))-d1))<10),-1)
    la=0; lean=[]
    for a in range(1,len(w)):
        r1=rows[w[a-1]]; r2=rows[w[a]]; dt=max(r2['t']-r1['t'],1e-3); sp=math.hypot(r2['vx'],r2['vy'])
        if sp>50:
            nx,ny=-r2['vy']/sp,r2['vx']/sp; al=((r2['vx']-r1['vx'])*nx+(r2['vy']-r1['vy'])*ny)/dt; la=max(la,abs(al))
            if abs(al)>150:
                ax=F[a][4]; sgn=1 if (ax[0]*nx+ax[1]*ny)*al>0 else -1; lean.append(F[a][3]*sgn)
    rng=lambda x: max(x)-min(x)
    o=(abs(dd),rng(tw),max(abs(x) for x in tw),rate,rng([f[2] for f in F]),rng([f[3] for f in F]),(sum(lean)/len(lean)) if lean else 0,tset,la)
    tot.append(o)
    print('%s s%-2d [%-9s>%-9s] v %3.0f turn %3.0f deg in %.2f s | twist range %4.1f max %4.1f | hip yaw rate peak %4.0f deg/s | hip tilt range %4.1f | side bend range %4.1f | lean into turn %5.1f | lat accel peak %4.0f'%(lab[-20:],s,key(kp),key(k),math.hypot(v0['vx'],v0['vy']),o[0],o[7],o[1],o[2],o[3],o[4],o[5],o[6],o[8]))
if tot: print('%s MEAN n %d | twist range %4.1f max %4.1f | hip yaw rate %4.0f | hip tilt %4.1f | side bend %4.1f | lean into turn %5.1f'%(lab[-20:],len(tot),sum(o[1] for o in tot)/len(tot),sum(o[2] for o in tot)/len(tot),sum(o[3] for o in tot)/len(tot),sum(o[4] for o in tot)/len(tot),sum(o[5] for o in tot)/len(tot),sum(o[6] for o in tot)/len(tot)))
