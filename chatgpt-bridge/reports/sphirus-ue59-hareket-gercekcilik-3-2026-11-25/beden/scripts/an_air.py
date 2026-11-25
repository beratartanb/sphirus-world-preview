# an_air.py <label> <plan> [thr cm]: flight phases (both visible feet above their ground contact height + thr) per key segment:
# longest flight, total flight share, yaw turned by the pelvis during the longest flight, clip; plus the same for steady loops.
import json,sys,math
lab=sys.argv[1]; rows=json.load(open('Saved/Codex/Grip_20261106/rec/%s.json'%lab))['rows']; plan=eval(open(sys.argv[2]).read()); thr=float(sys.argv[3]) if len(sys.argv)>3 else 5.0
g=lambda r: r['z']-88.2
fz=lambda r,s: min(r['v_foot_'+s][2], r['ub']['ball_'+s][2])-g(r)
lo=min(min(fz(r,'l'),fz(r,'r')) for r in rows)
def air(r): return (fz(r,'l')-lo>thr) and (fz(r,'r')-lo>thr)
key=lambda x: x.replace(' LeftShift','+Sh').replace(' LeftControl','+Ct') or '-'
def hy(r):
    u=r['ub']; return math.degrees(math.atan2(u['thigh_r'][1]-u['thigh_l'][1],u['thigh_r'][0]-u['thigh_l'][0]))
segs={}
for i,r in enumerate(rows): segs.setdefault(r['s'],[]).append(i)
for s,ix in sorted(segs.items()):
    if s==0 or s>=len(plan): continue
    runs=[]; cur=[]
    for i in ix:
        if air(rows[i]): cur.append(i)
        elif cur: runs.append(cur); cur=[]
    if cur: runs.append(cur)
    if not runs: continue
    lr=max(runs,key=len); dur=rows[lr[-1]]['t']-rows[lr[0]]['t']+1/60; tot=sum(rows[r[-1]]['t']-rows[r[0]]['t']+1/60 for r in runs)
    yaw=abs(((hy(rows[lr[-1]])-hy(rows[lr[0]]))+180)%360-180)
    print('%s s%-2d [%-9s>%-9s] longest flight %.3f s (pelvis turns %3.0f deg in it) | flight share %3.0f %% of %.2f s | %s'%(lab[-18:],s,key(plan[s-1][0]),key(plan[s][0]),dur,yaw,100*tot/(rows[ix[-1]]['t']-rows[ix[0]]['t']+1e-6),rows[ix[-1]]['t']-rows[ix[0]]['t'],rows[lr[0]]['gasp'][0][-28:]))
