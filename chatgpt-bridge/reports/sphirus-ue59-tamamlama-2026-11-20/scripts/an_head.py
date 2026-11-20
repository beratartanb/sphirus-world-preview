# an_head.py <label> <planfile> [t0 t1 step]: head/chest pitch relative to the standing idle of the same recording.
# Bone world rotators -> matrices; R_rel = R_now * R_idle^-1 applied to the idle facing (actor forward): pitch = elevation of that
# vector (deg, negative = looking/tilting DOWN), yaw = deviation from the actor/velocity heading. Bones: head, neck_01, spine_05, pelvis.
import json, sys, math, ast, statistics as S
RD='Saved/Codex/Grip_20261106/rec/'
lab=sys.argv[1]; plan=ast.literal_eval(open(sys.argv[2]).read())
R=json.load(open(RD+lab+'.json')); R=R['rows'] if isinstance(R,dict) else R
def M(yaw,pitch,roll):
    y,p,r=map(math.radians,(yaw,pitch,roll)); cy,sy,cp,sp,cr,sr=math.cos(y),math.sin(y),math.cos(p),math.sin(p),math.cos(r),math.sin(r)
    # UE FRotationMatrix axes (rows = X,Y,Z axis vectors)
    X=(cp*cy,cp*sy,sp); Y=(sr*sp*cy-cr*sy,sr*sp*sy+cr*cy,-sr*cp); Z=(-(cr*sp*cy+sr*sy),cy*sr-cr*sp*sy,cr*cp)
    return (X,Y,Z)
def tolocal(m,v): return tuple(sum(m[i][k]*v[k] for k in range(3)) for i in range(3))
def toworld(m,l): return tuple(sum(m[i][k]*l[i] for i in range(3)) for k in range(3))
idle=[r for r in R if r['s']==0 and r['t']>0.8]; B=('head','neck_01','spine_05','pelvis')
loc={}
r0=idle[len(idle)//2]; a0=math.radians(r0['yaw']); f0=(math.cos(a0),math.sin(a0),0.0)
for b in B: loc[b]=tolocal(M(*r0['ub'][b][3:6]),f0)
def pit(r,b):
    g=toworld(M(*r['ub'][b][3:6]),loc[b]); sp=math.hypot(r['vx'],r['vy'])
    return math.degrees(math.asin(max(-1,min(1,g[2]))))
if len(sys.argv)>4:
    t0,t1=float(sys.argv[3]),float(sys.argv[4]); st=float(sys.argv[5]) if len(sys.argv)>5 else 0.1; nx=t0
    for r in R:
        if t0<=r['t']<=t1 and r['t']>=nx-1e-6:
            nx+=st; print('t %.2f sp %4.0f head %6.1f neck %6.1f chest %6.1f pelvis %6.1f  HeadA %s %s'%(r['t'],math.hypot(r['vx'],r['vy']),pit(r,'head'),pit(r,'neck_01'),pit(r,'spine_05'),pit(r,'pelvis'),(r.get('bsig') or [None]*5)[4],str((r.get('gasp') or ['?'])[0])[-28:]))
    sys.exit()
segs={}
for r in R: segs.setdefault(r['s'],[]).append(r)
print('seg keys                 speed | head pitch mean [min] | neck | chest | pelvis   (deg vs idle, - = down/forward)')
for s in sorted(segs):
    rows=segs[s]; dur=rows[-1]['t']-rows[0]['t']
    if dur<1.9 or s>=len(plan): continue
    rows=[r for r in rows if r['t']>=rows[0]['t']+0.45*dur]
    h=[pit(r,'head') for r in rows]
    print('%-3d %-20s %5.0f | %6.1f [%6.1f] | %6.1f | %6.1f | %6.1f'%(s,plan[s][0][:20],S.mean(math.hypot(r['vx'],r['vy']) for r in rows),S.mean(h),min(h),S.mean(pit(r,'neck_01') for r in rows),S.mean(pit(r,'spine_05') for r in rows),S.mean(pit(r,'pelvis') for r in rows)))
